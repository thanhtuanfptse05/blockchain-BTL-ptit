"""Unit tests for Analytics & KPI Summary component.

# Implements FR-07, FR-11, SRS §7.5, §11, §12.2
"""

import pytest
from src.domain.config import SimulationConfig
from src.domain.block_result import BlockResult
from src.domain.liquidation_event import LiquidationEvent
from src.domain.simulation_result import KPISummary, SimulationResult
from src.interface.components.metrics import (
    calculate_kpi_summary,
    generate_comparison_table,
    format_usd,
    format_pct,
)


@pytest.fixture
def dummy_config() -> SimulationConfig:
    return SimulationConfig()


def make_dummy_block_result(
    block: int,
    eth_price: float,
    steth_price: float,
    discount: float,
    bad_debt: float = 0.0,
    scenario: str = "SC03",
) -> BlockResult:
    return BlockResult(
        scenario=scenario,
        block=block,
        eth_price_usd=eth_price,
        steth_price_usd=steth_price,
        steth_discount_pct=discount,
        liquidations_eth=0,
        liquidations_steth=0,
        liquidations_total=0,
        liquidated_agents_unique_cumulative=0,
        liquidation_debt_repaid_usd=0.0,
        liquidation_debt_repaid_cumulative_usd=0.0,
        bad_debt_usd=bad_debt,
    )


def make_dummy_event(
    block: int,
    agent_id: int,
    repaid_usd: float = 10000.0,
    scenario: str = "SC03",
    asset: str = "ETH",
) -> LiquidationEvent:
    return LiquidationEvent(
        scenario=scenario,
        block=block,
        agent_id=agent_id,
        asset=asset,
        hf_before=0.95,
        debt_repaid_usd=repaid_usd,
        collateral_seized=5.0,
        collateral_value_at_oracle_usd=10500.0,
        remaining_debt_usd=10000.0,
        remaining_collateral=5.0,
    )


def test_calculate_kpi_summary_basic(dummy_config):
    # UT: Extract 6 core KPIs for SC03 matching final block & unique events
    blocks = [
        make_dummy_block_result(0, 2500.0, 2500.0, 0.0, 0.0),
        make_dummy_block_result(1, 2000.0, 1960.0, 2.0, 500.0),
    ]
    events = [
        make_dummy_event(1, 10, 10000.0, 0.0),
        make_dummy_event(1, 20, 15000.0, 500.0),
        make_dummy_event(1, 10, 5000.0, 0.0),  # Agent 10 liquidated twice
    ]
    summary_dummy = KPISummary(
        scenario_id="SC03",
        final_eth_price_usd=2000.0,
        final_steth_price_usd=1960.0,
        final_steth_discount_pct=2.0,
        liquidated_agents_unique=2,
        total_agents=100,
        liquidated_agents_ratio_pct=2.0,
        liquidation_events_total=3,
        total_debt_repaid_usd=30000.0,
        bad_debt_usd=500.0,
    )
    sim_res = SimulationResult(
        scenario_id="SC03",
        parameters=dummy_config,
        block_results=blocks,
        liquidation_events=events,
        summary=summary_dummy,
    )

    kpi = calculate_kpi_summary(sim_res, total_agents=100)
    assert kpi.scenario_id == "SC03"
    assert kpi.final_eth_price_usd == 2000.0
    assert kpi.final_steth_price_usd == 1960.0
    assert kpi.final_steth_discount_pct == 2.0
    assert kpi.liquidated_agents_unique == 2
    assert kpi.total_agents == 100
    assert kpi.liquidated_agents_ratio_pct == 2.0
    assert kpi.liquidation_events_total == 3
    assert kpi.total_debt_repaid_usd == 30000.0
    assert kpi.bad_debt_usd == 500.0


def test_calculate_kpi_summary_with_sc02_delta(dummy_config):
    # UT: Calculate deltas between SC03 and SC02
    blocks_sc02 = [
        make_dummy_block_result(0, 2500.0, 2500.0, 0.0, 0.0),
        make_dummy_block_result(1, 2000.0, 2000.0, 0.0, 0.0),
    ]
    events_sc02 = [make_dummy_event(1, 10, 10000.0, 0.0)]
    sc02_res = SimulationResult(
        scenario_id="SC02",
        parameters=dummy_config,
        block_results=blocks_sc02,
        liquidation_events=events_sc02,
        summary=None,
    )

    blocks_sc03 = [
        make_dummy_block_result(0, 2500.0, 2500.0, 0.0, 0.0),
        make_dummy_block_result(1, 1900.0, 1843.0, 3.0, 1500.0),
    ]
    events_sc03 = [
        make_dummy_event(1, 10, 10000.0, 0.0),
        make_dummy_event(1, 20, 15000.0, 1500.0),
        make_dummy_event(1, 30, 20000.0, 0.0),
    ]
    sc03_res = SimulationResult(
        scenario_id="SC03",
        parameters=dummy_config,
        block_results=blocks_sc03,
        liquidation_events=events_sc03,
        summary=None,
    )

    kpi = calculate_kpi_summary(sc03_res, total_agents=100, ref_sc02=sc02_res)
    assert kpi.delta_eth_price_usd == -100.0
    assert kpi.delta_steth_price_usd == -157.0
    assert kpi.delta_steth_discount_pct == 3.0
    assert kpi.delta_liquidated_agents == 2  # 3 unique in SC03 - 1 in SC02
    assert kpi.delta_liquidation_events == 2  # 3 in SC03 - 1 in SC02
    assert kpi.delta_bad_debt_usd == 1500.0


def test_zero_division_guard_in_comparison_table(dummy_config):
    # UT: When SC02 has 0 liquidations and SC03 > 0, relative change is "N/A"
    blocks_sc01 = [make_dummy_block_result(0, 2500.0, 2500.0, 0.0, 0.0)]
    sc01_res = SimulationResult("SC01", dummy_config, blocks_sc01, [], None)

    blocks_sc02 = [make_dummy_block_result(0, 2000.0, 2000.0, 0.0, 0.0)]
    sc02_res = SimulationResult("SC02", dummy_config, blocks_sc02, [], None)

    blocks_sc03 = [make_dummy_block_result(0, 1900.0, 1850.0, 2.63, 100.0)]
    events_sc03 = [make_dummy_event(1, 15, 5000.0, 100.0)]
    sc03_res = SimulationResult("SC03", dummy_config, blocks_sc03, events_sc03, None)

    comparison = generate_comparison_table(sc01_res, sc02_res, sc03_res)
    rows = {r["metric"]: r for r in comparison}

    assert "Liquidated Agents (unique)" in rows
    liq_agent_row = rows["Liquidated Agents (unique)"]
    assert liq_agent_row["sc02_value"] == "0"
    assert liq_agent_row["sc03_value"] == "1"
    assert liq_agent_row["relative_change"] == "N/A"

    # Both SC02 and SC03 = 0 (e.g. if shock = 0)
    sc03_zero_events = SimulationResult("SC03", dummy_config, blocks_sc03, [], None)
    comp_both_zero = generate_comparison_table(sc01_res, sc02_res, sc03_zero_events)
    rows_both_zero = {r["metric"]: r for r in comp_both_zero}
    assert rows_both_zero["Liquidated Agents (unique)"]["relative_change"] == "0.0%"


def test_formatting_helpers():
    assert format_usd(2412.35) == "$2,412.35"
    assert format_usd(0.0) == "$0.00"
    assert format_usd(1234567.891) == "$1,234,567.89"
    assert format_pct(2.153) == "2.15%"
    assert format_pct(0.0) == "0.00%"


def test_calculate_kpi_summary_zero_liquidations(dummy_config):
    # UT: Acceptance Scenario 2 - Zero liquidations
    blocks = [
        make_dummy_block_result(0, 3000.0, 2970.0, 1.0, 0.0),
        make_dummy_block_result(1, 3000.0, 2970.0, 1.0, 0.0),
    ]
    sim_res = SimulationResult(
        scenario_id="SC03",
        parameters=dummy_config,
        block_results=blocks,
        liquidation_events=[],
        summary=None,
    )
    kpi = calculate_kpi_summary(sim_res, total_agents=100)
    assert kpi.liquidated_agents_unique == 0
    assert kpi.liquidation_events_total == 0
    assert kpi.liquidated_agents_ratio_pct == 0.0
    assert kpi.total_debt_repaid_usd == 0.0
    assert kpi.bad_debt_usd == 0.0


def test_kpi_summary_with_live_scenario_runner():
    # UT: End-to-end integration with live scenario runner
    from src.usecase.scenario_runner import run_all_scenarios

    config = SimulationConfig(num_borrowers=50, max_blocks=5, seed=123)
    results = run_all_scenarios(config)

    sc03_res = results["SC03"]
    sc02_res = results["SC02"]

    kpi = calculate_kpi_summary(sc03_res, total_agents=config.num_borrowers, ref_sc02=sc02_res)
    final_b = sc03_res.block_results[-1]

    assert kpi.final_eth_price_usd == final_b.eth_price_usd
    assert kpi.final_steth_price_usd == final_b.steth_price_usd
    assert kpi.final_steth_discount_pct == final_b.steth_discount_pct
    assert kpi.bad_debt_usd == final_b.bad_debt_usd
    assert kpi.total_agents == 50
    assert kpi.delta_eth_price_usd is not None
    assert kpi.delta_steth_price_usd is not None

