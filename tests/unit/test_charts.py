"""Unit tests for Charts & Visualizations component.

# Implements FR-08, SRS §11, §14.4
"""

import pytest
import plotly.graph_objects as go
from src.domain.block_result import BlockResult
from src.interface.components.charts import (
    create_eth_price_chart,
    create_steth_discount_chart,
    create_liquidation_breakdown_chart,
    create_cumulative_liquidated_agents_chart,
)


def make_dummy_block(
    scenario: str,
    block: int,
    eth_price: float,
    steth_price: float,
    discount: float,
    liq_eth: int = 0,
    liq_steth: int = 0,
    cumulative_agents: int = 0,
) -> BlockResult:
    return BlockResult(
        scenario=scenario,
        block=block,
        eth_price_usd=eth_price,
        steth_price_usd=steth_price,
        steth_discount_pct=discount,
        liquidations_eth=liq_eth,
        liquidations_steth=liq_steth,
        liquidations_total=liq_eth + liq_steth,
        liquidated_agents_unique_cumulative=cumulative_agents,
        liquidation_debt_repaid_usd=0.0,
        liquidation_debt_repaid_cumulative_usd=0.0,
        bad_debt_usd=0.0,
    )


@pytest.fixture
def sample_blocks():
    sc01 = [
        make_dummy_block("SC01", 0, 2500.0, 2500.0, 0.0),
        make_dummy_block("SC01", 1, 2500.0, 2500.0, 0.0),
        make_dummy_block("SC01", 2, 2500.0, 2500.0, 0.0),
    ]
    sc02 = [
        make_dummy_block("SC02", 0, 2500.0, 2500.0, 0.0, 0, 0, 0),
        make_dummy_block("SC02", 1, 2125.0, 2125.0, 0.0, 2, 0, 2),
        make_dummy_block("SC02", 2, 2125.0, 2125.0, 0.0, 0, 0, 2),
    ]
    sc03 = [
        make_dummy_block("SC03", 0, 2500.0, 2500.0, 0.0, 0, 0, 0),
        make_dummy_block("SC03", 1, 2100.0, 2050.0, 2.38, 3, 2, 4),
        make_dummy_block("SC03", 2, 2050.0, 1980.0, 3.41, 1, 1, 6),
    ]
    return sc01, sc02, sc03


def test_create_eth_price_chart(sample_blocks):
    sc01, sc02, sc03 = sample_blocks
    fig = create_eth_price_chart(sc01, sc02, sc03)

    assert isinstance(fig, go.Figure)
    assert len(fig.data) == 3
    # Check trace names
    trace_names = [trace.name for trace in fig.data]
    assert any("SC01" in name for name in trace_names)
    assert any("SC02" in name for name in trace_names)
    assert any("SC03" in name for name in trace_names)

    # Check vertical shock line or annotation at x=1
    has_shock_marker = False
    if fig.layout.shapes:
        has_shock_marker = any(shape.x0 == 1 and shape.x1 == 1 for shape in fig.layout.shapes)
    if not has_shock_marker and fig.layout.annotations:
        has_shock_marker = any(ann.x == 1 for ann in fig.layout.annotations)
    assert has_shock_marker, "Shock annotation/line at x=1 must be present"


def test_create_steth_discount_chart(sample_blocks):
    sc01, sc02, sc03 = sample_blocks
    fig = create_steth_discount_chart(sc01, sc02, sc03)

    assert isinstance(fig, go.Figure)
    assert len(fig.data) == 3
    assert "%" in fig.layout.yaxis.title.text or fig.layout.yaxis.ticksuffix == "%"


def test_create_liquidation_breakdown_chart(sample_blocks):
    _, _, sc03 = sample_blocks
    fig = create_liquidation_breakdown_chart(sc03)

    assert isinstance(fig, go.Figure)
    assert len(fig.data) == 2  # ETH and stETH traces
    assert all(trace.type == "bar" for trace in fig.data)
    assert fig.layout.barmode in ("stack", "group")


def test_create_cumulative_liquidated_agents_chart(sample_blocks):
    _, sc02, sc03 = sample_blocks
    fig = create_cumulative_liquidated_agents_chart(sc02, sc03)

    assert isinstance(fig, go.Figure)
    assert len(fig.data) == 2  # SC02 and SC03 traces
    trace_names = [trace.name for trace in fig.data]
    assert any("SC02" in name for name in trace_names)
    assert any("SC03" in name for name in trace_names)


def test_empty_or_single_block_does_not_crash():
    single = [make_dummy_block("SC01", 0, 2500.0, 2500.0, 0.0)]
    fig1 = create_eth_price_chart(single, single, single)
    fig2 = create_steth_discount_chart(single, single, single)
    fig3 = create_liquidation_breakdown_chart(single)
    fig4 = create_cumulative_liquidated_agents_chart(single, single)

    assert isinstance(fig1, go.Figure)
    assert isinstance(fig2, go.Figure)
    assert isinstance(fig3, go.Figure)
    assert isinstance(fig4, go.Figure)


def test_charts_with_live_scenario_runner():
    # UT: End-to-end integration with live simulation results
    from src.domain.config import SimulationConfig
    from src.usecase.scenario_runner import run_all_scenarios

    config = SimulationConfig(num_borrowers=50, max_blocks=5, seed=42)
    results = run_all_scenarios(config)

    b01 = results["SC01"].block_results
    b02 = results["SC02"].block_results
    b03 = results["SC03"].block_results

    f1 = create_eth_price_chart(b01, b02, b03)
    f2 = create_steth_discount_chart(b01, b02, b03)
    f3 = create_liquidation_breakdown_chart(b03)
    f4 = create_cumulative_liquidated_agents_chart(b02, b03)

    assert len(f1.data) == 3
    assert len(f2.data) == 3
    assert len(f3.data) == 2
    assert len(f4.data) == 2
    assert all(len(trace.x) == 6 for trace in f1.data)  # blocks 0 to 5 = 6 points


