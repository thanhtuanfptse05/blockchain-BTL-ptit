"""System tests verifying empirical invariants ST-01 through ST-07.

# Implements ST-01, ST-02, ST-03, ST-04, ST-05, ST-06, ST-07
# Implements BR-11 (Mathematical invariants)
"""

import pytest
from src.domain.config import SimulationConfig
from src.usecase.scenario_runner import run_all_scenarios


def test_st01_sc01_baseline_stability():
    """ST-01: Baseline stability invariant - zero liquidations, price flat at $3000."""
    config = SimulationConfig()
    results = run_all_scenarios(config)
    sc01 = results["SC01"]

    assert len(sc01.liquidation_events) == 0
    assert sc01.summary.liquidated_agents_unique == 0
    assert sc01.summary.liquidation_events_total == 0

    for br in sc01.block_results:
        assert br.eth_price_usd == pytest.approx(3000.0, rel=1e-6)
        assert br.steth_price_usd == pytest.approx(2970.0, rel=1e-6)
        assert br.steth_discount_pct == pytest.approx(1.0, rel=1e-6)
        assert br.liquidations_total == 0


def test_st02_sc02_fixed_price_post_shock():
    """ST-02: Direct shock invariant - price drops at block 1 to 2550 and stays strictly fixed."""
    config = SimulationConfig(shock_pct=15.0)
    results = run_all_scenarios(config)
    sc02 = results["SC02"]

    assert sc02.block_results[0].eth_price_usd == pytest.approx(3000.0, rel=1e-6)
    assert len(sc02.liquidation_events) > 0

    for br in sc02.block_results[1:]:
        assert br.eth_price_usd == pytest.approx(2550.0, rel=1e-6)
        assert br.steth_price_usd == pytest.approx(2524.5, rel=1e-6)
        assert br.steth_discount_pct == pytest.approx(1.0, rel=1e-6)


def test_st03_sc03_cascade_price_depression_and_depeg():
    """ST-03: Contagion cascade invariant - collateral dumping depresses prices and deepens depeg."""
    config = SimulationConfig(shock_pct=15.0)
    results = run_all_scenarios(config)
    sc02 = results["SC02"]
    sc03 = results["SC03"]

    # Final price in SC03 must be lower than fixed price in SC02
    assert sc03.summary.final_eth_price_usd < sc02.summary.final_eth_price_usd
    assert sc03.summary.final_steth_price_usd < sc02.summary.final_steth_price_usd
    assert sc03.summary.final_steth_discount_pct > sc02.summary.final_steth_discount_pct


def test_st04_initial_population_equity():
    """ST-04: Comparative initial population equity between SC02 and SC03."""
    config = SimulationConfig(seed=42)
    results = run_all_scenarios(config)
    sc02 = results["SC02"]
    sc03 = results["SC03"]

    assert sc02.summary.total_agents == sc03.summary.total_agents
    assert sc02.block_results[0].eth_price_usd == sc03.block_results[0].eth_price_usd
    assert sc02.block_results[0].steth_price_usd == sc03.block_results[0].steth_price_usd


def test_st05_shock_magnitude_sensitivity():
    """ST-05: Larger shock percentage triggers more liquidated agents."""
    cfg_mild = SimulationConfig(shock_pct=10.0, seed=42)
    cfg_severe = SimulationConfig(shock_pct=25.0, seed=42)

    res_mild = run_all_scenarios(cfg_mild)
    res_severe = run_all_scenarios(cfg_severe)

    assert (
        res_severe["SC03"].summary.liquidated_agents_unique
        >= res_mild["SC03"].summary.liquidated_agents_unique
    )


def test_st06_pool_liquidity_depth_sensitivity():
    """ST-06: Lower Pool A TVL results in greater price impact per liquidated ETH."""
    cfg_deep = SimulationConfig(pool_a_tvl_usd=300_000_000.0, shock_pct=15.0, seed=42)
    cfg_shallow = SimulationConfig(pool_a_tvl_usd=50_000_000.0, shock_pct=15.0, seed=42)

    res_deep = run_all_scenarios(cfg_deep)
    res_shallow = run_all_scenarios(cfg_shallow)

    # Shallow pool experiences deeper price drop
    assert (
        res_shallow["SC03"].summary.final_eth_price_usd
        < res_deep["SC03"].summary.final_eth_price_usd
    )


def test_st07_deterministic_repeatability():
    """ST-07: Exact determinism across identical runs."""
    config = SimulationConfig(seed=12345)
    run1 = run_all_scenarios(config)
    run2 = run_all_scenarios(config)

    assert run1["SC03"].summary == run2["SC03"].summary
    assert len(run1["SC03"].liquidation_events) == len(run2["SC03"].liquidation_events)

