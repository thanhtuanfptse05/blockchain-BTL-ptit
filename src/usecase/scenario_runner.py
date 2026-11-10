"""Scenario simulation runner coordinating SC01, SC02, and SC03 block loops.

# Implements FR-001, FR-002, FR-003, FR-004, FR-005, FR-006, FR-007, FR-008, FR-009, FR-010, FR-011, FR-012, FR-013, FR-014, FR-015, FR-016, FR-017, FR-018, FR-019, FR-020
# Implements BR-07, BR-08, BR-10, BR-11, SRS §9, §10, §15.1
"""

import copy
from typing import Dict, List, Set
from src.domain.config import SimulationConfig
from src.domain.agent import BorrowerAgent, AssetType
from src.domain.amm_pool import AMMPool
from src.domain.block_result import BlockResult
from src.domain.liquidation_event import LiquidationEvent
from src.domain.simulation_result import KPISummary, SimulationResult
from src.usecase.agent_generator import generate_borrower_agents
from src.usecase.amm_engine import (
    initialize_pools,
    swap_exact_input,
    apply_exogenous_shock,
    get_market_prices,
)
from src.usecase.health_factor import is_liquidatable, EPSILON
from src.usecase.liquidation_engine import (
    liquidate_borrower_position,
    compute_total_bad_debt,
)


def run_scenario(
    scenario_id: str,
    config: SimulationConfig,
    agents: List[BorrowerAgent],
    pool_a: AMMPool,
    pool_b: AMMPool,
) -> SimulationResult:
    """Run a discrete block-by-block simulation for a single scenario.

    # Implements SRS §10, BR-07, BR-08, BR-11

    Args:
        scenario_id: "SC01" (Baseline), "SC02" (Direct Shock), or "SC03" (Contagion).
        config: SimulationConfig instance.
        agents: Independent copy of initial borrower agent positions.
        pool_a: Independent copy of initial Pool A (ETH/USDC).
        pool_b: Independent copy of initial Pool B (stETH/ETH).

    Returns:
        SimulationResult containing exactly max_blocks + 1 BlockResult records.
    """
    block_results: List[BlockResult] = []
    all_events: List[LiquidationEvent] = []
    cumulative_debt_repaid: float = 0.0
    liquidated_agent_ids: Set[int] = set()

    for block in range(config.max_blocks + 1):
        if block == 0:
            # Block 0: Snapshot initial undisturbed market state (SRS §10.1)
            prices = get_market_prices(pool_a, pool_b)
            b0 = BlockResult(
                scenario=scenario_id,
                block=0,
                eth_price_usd=prices["eth_price_usd"],
                steth_price_usd=prices["steth_price_usd"],
                steth_discount_pct=prices["steth_discount_pct"],
                liquidations_eth=0,
                liquidations_steth=0,
                liquidations_total=0,
                liquidated_agents_unique_cumulative=0,
                liquidation_debt_repaid_usd=0.0,
                liquidation_debt_repaid_cumulative_usd=0.0,
                bad_debt_usd=0.0,
            )
            block_results.append(b0)
            continue

        # Block >= 1:
        # Step a: Apply exogenous shock at block 1 once (SC02, SC03 only)
        if block == 1 and scenario_id in ("SC02", "SC03"):
            apply_exogenous_shock(pool_a, config.shock_pct)

        # Step b: Determine candidates at start of block sorted by agent_id
        cur_prices = get_market_prices(pool_a, pool_b)
        candidates = [
            a
            for a in agents
            if is_liquidatable(
                a,
                cur_prices["eth_price_usd"],
                cur_prices["steth_price_usd"],
                config.liquidation_threshold,
            )
        ]
        candidates.sort(key=lambda a: a.agent_id)

        # Step c: Process each candidate position
        block_debt_repaid: float = 0.0
        block_liq_eth: int = 0
        block_liq_steth: int = 0

        for agent in candidates:
            # Re-check eligibility with pre-trade spot prices (FR-008, BR-11)
            spot_prices = get_market_prices(pool_a, pool_b)
            if not is_liquidatable(
                agent,
                spot_prices["eth_price_usd"],
                spot_prices["steth_price_usd"],
                config.liquidation_threshold,
            ):
                continue

            agent_price = (
                spot_prices["eth_price_usd"]
                if agent.collateral_type == AssetType.ETH
                else spot_prices["steth_price_usd"]
            )

            event = liquidate_borrower_position(
                agent=agent,
                scenario=scenario_id,
                block=block,
                spot_price_usd=agent_price,
                close_factor=config.close_factor,
                liquidation_penalty=config.liquidation_penalty,
            )

            if event is not None:
                all_events.append(event)
                block_debt_repaid += event.debt_repaid_usd
                liquidated_agent_ids.add(agent.agent_id)

                if event.asset == AssetType.ETH.value:
                    block_liq_eth += 1
                else:
                    block_liq_steth += 1

                # Step c (Selling Route for SC03): Feedback collateral into AMMs (BR-08)
                if scenario_id == "SC03" and event.collateral_seized > EPSILON:
                    if event.asset == AssetType.ETH.value:
                        # Dump ETH into Pool A
                        swap_exact_input(pool_a, event.collateral_seized)
                    elif event.asset == AssetType.STETH.value:
                        # Dump stETH into Pool B to get ETH, then dump all received ETH into Pool A
                        eth_received = swap_exact_input(pool_b, event.collateral_seized)
                        if eth_received > EPSILON:
                            swap_exact_input(pool_a, eth_received)

        # Step d: Record end-of-block market results
        cumulative_debt_repaid += block_debt_repaid
        end_prices = get_market_prices(pool_a, pool_b)
        current_bad_debt = compute_total_bad_debt(agents)

        br = BlockResult(
            scenario=scenario_id,
            block=block,
            eth_price_usd=end_prices["eth_price_usd"],
            steth_price_usd=end_prices["steth_price_usd"],
            steth_discount_pct=end_prices["steth_discount_pct"],
            liquidations_eth=block_liq_eth,
            liquidations_steth=block_liq_steth,
            liquidations_total=block_liq_eth + block_liq_steth,
            liquidated_agents_unique_cumulative=len(liquidated_agent_ids),
            liquidation_debt_repaid_usd=block_debt_repaid,
            liquidation_debt_repaid_cumulative_usd=cumulative_debt_repaid,
            bad_debt_usd=current_bad_debt,
        )
        block_results.append(br)

    # Compile overall KPI summary (FR-018)
    final_br = block_results[-1]
    summary = KPISummary(
        scenario_id=scenario_id,
        final_eth_price_usd=final_br.eth_price_usd,
        final_steth_price_usd=final_br.steth_price_usd,
        final_steth_discount_pct=final_br.steth_discount_pct,
        liquidated_agents_unique=len(liquidated_agent_ids),
        total_agents=len(agents),
        liquidated_agents_ratio_pct=(len(liquidated_agent_ids) / len(agents)) * 100.0,
        liquidation_events_total=len(all_events),
        total_debt_repaid_usd=cumulative_debt_repaid,
        bad_debt_usd=final_br.bad_debt_usd,
    )

    return SimulationResult(
        scenario_id=scenario_id,
        parameters=config,
        block_results=block_results,
        liquidation_events=all_events,
        summary=summary,
    )


def run_all_scenarios(config: SimulationConfig) -> Dict[str, SimulationResult]:
    """Integration API contract: Run SC01, SC02, and SC03 from identical initial state.

    # Implements SRS §15.1, FR-001, FR-003, FR-004

    Args:
        config: Validated SimulationConfig instance.

    Returns:
        Dict mapping scenario_id ("SC01", "SC02", "SC03") to SimulationResult.
    """
    # 1. Generate base population and initial AMM pools once
    base_agents = generate_borrower_agents(config)
    base_pool_a, base_pool_b = initialize_pools(config)

    # 2. Execute each scenario with deepcopied independent state
    sc01 = run_scenario(
        "SC01",
        config,
        copy.deepcopy(base_agents),
        copy.deepcopy(base_pool_a),
        copy.deepcopy(base_pool_b),
    )

    sc02 = run_scenario(
        "SC02",
        config,
        copy.deepcopy(base_agents),
        copy.deepcopy(base_pool_a),
        copy.deepcopy(base_pool_b),
    )

    sc03_raw = run_scenario(
        "SC03",
        config,
        copy.deepcopy(base_agents),
        copy.deepcopy(base_pool_a),
        copy.deepcopy(base_pool_b),
    )

    # 3. Calculate deltas for SC03 vs SC02 (FR-11, FR-07)
    delta_eth = sc03_raw.summary.final_eth_price_usd - sc02.summary.final_eth_price_usd
    delta_steth = sc03_raw.summary.final_steth_price_usd - sc02.summary.final_steth_price_usd
    delta_discount = sc03_raw.summary.final_steth_discount_pct - sc02.summary.final_steth_discount_pct
    delta_unique = sc03_raw.summary.liquidated_agents_unique - sc02.summary.liquidated_agents_unique
    delta_events = sc03_raw.summary.liquidation_events_total - sc02.summary.liquidation_events_total
    delta_bad_debt = sc03_raw.summary.bad_debt_usd - sc02.summary.bad_debt_usd

    sc03_summary = KPISummary(
        scenario_id=sc03_raw.summary.scenario_id,
        final_eth_price_usd=sc03_raw.summary.final_eth_price_usd,
        final_steth_price_usd=sc03_raw.summary.final_steth_price_usd,
        final_steth_discount_pct=sc03_raw.summary.final_steth_discount_pct,
        liquidated_agents_unique=sc03_raw.summary.liquidated_agents_unique,
        total_agents=sc03_raw.summary.total_agents,
        liquidated_agents_ratio_pct=sc03_raw.summary.liquidated_agents_ratio_pct,
        liquidation_events_total=sc03_raw.summary.liquidation_events_total,
        total_debt_repaid_usd=sc03_raw.summary.total_debt_repaid_usd,
        bad_debt_usd=sc03_raw.summary.bad_debt_usd,
        delta_eth_price_usd=delta_eth,
        delta_steth_price_usd=delta_steth,
        delta_steth_discount_pct=delta_discount,
        delta_liquidated_agents=delta_unique,
        delta_liquidation_events=delta_events,
        delta_bad_debt_usd=delta_bad_debt,
    )

    sc03 = SimulationResult(
        scenario_id=sc03_raw.scenario_id,
        parameters=sc03_raw.parameters,
        block_results=sc03_raw.block_results,
        liquidation_events=sc03_raw.liquidation_events,
        summary=sc03_summary,
    )

    return {"SC01": sc01, "SC02": sc02, "SC03": sc03}

