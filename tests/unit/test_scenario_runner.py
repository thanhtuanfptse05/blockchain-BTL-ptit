"""Unit tests for Scenario Runner (SC01, SC02, SC03 coordination).

# Implements FR-001, FR-003, FR-004, FR-005, FR-006, FR-007, FR-008, FR-009, FR-010, FR-011, FR-012, FR-013, FR-014, FR-016, FR-017, FR-018, FR-019
# Implements UT-10, UT-11, UT-14, ST-01, ST-02, ST-03, ST-07
"""

import pytest
from src.domain.config import SimulationConfig
from src.domain.simulation_result import SimulationResult
from src.usecase.scenario_runner import run_all_scenarios, run_scenario


def test_run_all_scenarios_returns_3_scenarios_with_exact_blocks(default_config: SimulationConfig):
    """Verify run_all_scenarios contract: 3 keys (SC01, SC02, SC03), each having max_blocks + 1 records (UT-14, SC-001)."""
    results = run_all_scenarios(default_config)
    assert set(results.keys()) == {"SC01", "SC02", "SC03"}

    for sc_id, sim in results.items():
        assert isinstance(sim, SimulationResult)
        assert sim.scenario_id == sc_id
        # Must have exactly max_blocks + 1 blocks (31 for default 30)
        assert len(sim.block_results) == default_config.max_blocks + 1

        # Check block numbering from 0 to 30 in sequence
        blocks = [br.block for br in sim.block_results]
        assert blocks == list(range(default_config.max_blocks + 1))

        # Block 0 invariant
        b0 = sim.block_results[0]
        assert b0.block == 0
        assert b0.liquidations_total == 0
        assert b0.liquidated_agents_unique_cumulative == 0
        assert b0.bad_debt_usd == 0.0
        assert b0.liquidation_debt_repaid_usd == 0.0


def test_sc01_baseline_is_flat_and_zero_liquidations(default_config: SimulationConfig):
    """Verify SC01: flat 3000 USD, flat 1.0% discount, zero liquidations across all blocks (UT-11, ST-01)."""
    results = run_all_scenarios(default_config)
    sc01 = results["SC01"]

    assert len(sc01.liquidation_events) == 0
    assert sc01.summary.liquidated_agents_unique == 0
    assert sc01.summary.liquidation_events_total == 0
    assert sc01.summary.bad_debt_usd == 0.0

    for br in sc01.block_results:
        assert br.eth_price_usd == pytest.approx(3000.0, rel=1e-6)
        assert br.steth_price_usd == pytest.approx(2970.0, rel=1e-6)
        assert br.steth_discount_pct == pytest.approx(1.0, rel=1e-6)
        assert br.liquidations_total == 0
        assert br.bad_debt_usd == 0.0


def test_sc02_direct_shock_without_amm_feedback(default_config: SimulationConfig):
    """Verify SC02: shock at block 1 to 2550, liquidations occur, but prices do not change after shock (UT-10, ST-02)."""
    results = run_all_scenarios(default_config)
    sc02 = results["SC02"]

    # Block 0 is pre-shock
    assert sc02.block_results[0].eth_price_usd == pytest.approx(3000.0, rel=1e-6)

    # Liquidations occurred in SC02
    assert len(sc02.liquidation_events) > 0
    assert sc02.summary.liquidated_agents_unique > 0

    # From block 1 to 30, prices must remain strictly 2550 USD (no AMM selling feedback)
    for br in sc02.block_results[1:]:
        assert br.eth_price_usd == pytest.approx(2550.0, rel=1e-6)
        assert br.steth_price_usd == pytest.approx(2524.5, rel=1e-6)
        assert br.steth_discount_pct == pytest.approx(1.0, rel=1e-6)


def test_sc03_cascade_contagion_causes_price_depression_and_depeg(default_config: SimulationConfig):
    """Verify SC03: collateral sold into AMM causes secondary price drop and stETH depeg (ST-03, ST-04)."""
    results = run_all_scenarios(default_config)
    sc02 = results["SC02"]
    sc03 = results["SC03"]

    # In SC03, because collateral is sold on AMMs, final prices must be lower than SC02
    assert sc03.summary.final_eth_price_usd < sc02.summary.final_eth_price_usd
    assert sc03.summary.final_steth_price_usd < sc02.summary.final_steth_price_usd
    assert sc03.summary.final_steth_discount_pct > sc02.summary.final_steth_discount_pct

    # Total liquidated unique agents in SC03 must be >= SC02
    assert sc03.summary.liquidated_agents_unique >= sc02.summary.liquidated_agents_unique


def test_deterministic_simulation_reproducibility(default_config: SimulationConfig):
    """Verify running the simulation twice with identical config yields 100% identical outputs (ST-07)."""
    res1 = run_all_scenarios(default_config)
    res2 = run_all_scenarios(default_config)

    for sc_id in ("SC01", "SC02", "SC03"):
        sim1 = res1[sc_id]
        sim2 = res2[sc_id]

        assert sim1.summary == sim2.summary
        assert len(sim1.block_results) == len(sim2.block_results)
        assert len(sim1.liquidation_events) == len(sim2.liquidation_events)

        for br1, br2 in zip(sim1.block_results, sim2.block_results):
            assert br1 == br2

        for ev1, ev2 in zip(sim1.liquidation_events, sim2.liquidation_events):
            assert ev1 == ev2

