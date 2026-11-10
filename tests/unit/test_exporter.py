"""Unit tests for Data Tables & CSV Exporter component.

# Implements FR-09, ST-08, SRS §7.3, §7.4, §15.1
"""

import io
import pytest
import pandas as pd
from src.domain.config import SimulationConfig
from src.domain.block_result import BlockResult
from src.domain.liquidation_event import LiquidationEvent
from src.domain.simulation_result import KPISummary, SimulationResult
from src.infra.exporter import (
    BLOCK_RESULT_COLUMNS,
    LIQUIDATION_EVENT_COLUMNS,
    block_results_to_dataframe,
    liquidation_events_to_dataframe,
    export_block_results_to_csv,
    export_liquidation_events_to_csv,
)


@pytest.fixture
def sample_simulation_results():
    config = SimulationConfig(max_blocks=5)

    def make_blocks(scenario: str):
        return [
            BlockResult(
                scenario=scenario,
                block=b,
                eth_price_usd=2500.0 - b * 50.0,
                steth_price_usd=2500.0 - b * 60.0,
                steth_discount_pct=b * 1.5,
                liquidations_eth=b,
                liquidations_steth=0,
                liquidations_total=b,
                liquidated_agents_unique_cumulative=b,
                liquidation_debt_repaid_usd=b * 5000.0,
                liquidation_debt_repaid_cumulative_usd=b * 5000.0,
                bad_debt_usd=0.0,
            )
            for b in range(3)
        ]

    events_sc02 = [
        LiquidationEvent(
            scenario="SC02",
            block=1,
            agent_id=5,
            asset="ETH",
            hf_before=0.92,
            debt_repaid_usd=15000.0,
            collateral_seized=7.5,
            collateral_value_at_oracle_usd=15750.0,
            remaining_debt_usd=15000.0,
            remaining_collateral=7.5,
        )
    ]
    events_sc03 = [
        LiquidationEvent(
            scenario="SC03",
            block=1,
            agent_id=5,
            asset="ETH",
            hf_before=0.92,
            debt_repaid_usd=15000.0,
            collateral_seized=7.5,
            collateral_value_at_oracle_usd=15750.0,
            remaining_debt_usd=15000.0,
            remaining_collateral=7.5,
        ),
        LiquidationEvent(
            scenario="SC03",
            block=2,
            agent_id=12,
            asset="stETH",
            hf_before=0.98,
            debt_repaid_usd=8000.0,
            collateral_seized=4.1,
            collateral_value_at_oracle_usd=8400.0,
            remaining_debt_usd=8000.0,
            remaining_collateral=4.1,
        ),
    ]

    res_01 = SimulationResult("SC01", config, make_blocks("SC01"), [], None)
    res_02 = SimulationResult("SC02", config, make_blocks("SC02"), events_sc02, None)
    res_03 = SimulationResult("SC03", config, make_blocks("SC03"), events_sc03, None)

    return {"SC01": res_01, "SC02": res_02, "SC03": res_03}


def test_block_results_dataframe_and_csv_roundtrip(sample_simulation_results):
    # UT: Export block results has exact 12 columns and reads back identically (ST-08)
    df = block_results_to_dataframe(sample_simulation_results)

    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == BLOCK_RESULT_COLUMNS
    # 3 scenarios * 3 blocks = 9 rows
    assert len(df) == 9

    csv_str = export_block_results_to_csv(sample_simulation_results)
    assert isinstance(csv_str, str)
    assert csv_str.startswith("scenario,block,eth_price_usd")

    # Read back with pandas
    df_read = pd.read_csv(io.StringIO(csv_str))
    assert list(df_read.columns) == BLOCK_RESULT_COLUMNS
    assert len(df_read) == 9
    assert set(df_read["scenario"].unique()) == {"SC01", "SC02", "SC03"}


def test_liquidation_events_dataframe_and_csv_roundtrip(sample_simulation_results):
    # UT: Export liquidation events has exact 10 columns and preserves order
    df = liquidation_events_to_dataframe(sample_simulation_results)

    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == LIQUIDATION_EVENT_COLUMNS
    # 0 in SC01 + 1 in SC02 + 2 in SC03 = 3 rows
    assert len(df) == 3

    csv_str = export_liquidation_events_to_csv(sample_simulation_results)
    assert isinstance(csv_str, str)
    assert csv_str.startswith("scenario,block,agent_id")

    df_read = pd.read_csv(io.StringIO(csv_str))
    assert list(df_read.columns) == LIQUIDATION_EVENT_COLUMNS
    assert len(df_read) == 3


def test_empty_liquidation_events_returns_valid_header():
    # UT: When there are no liquidation events, returns empty dataframe with 10 columns
    config = SimulationConfig(max_blocks=5)
    res_empty = {
        "SC01": SimulationResult("SC01", config, [], [], None),
        "SC02": SimulationResult("SC02", config, [], [], None),
    }

    df = liquidation_events_to_dataframe(res_empty)
    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == LIQUIDATION_EVENT_COLUMNS
    assert len(df) == 0

    csv_str = export_liquidation_events_to_csv(res_empty)
    df_read = pd.read_csv(io.StringIO(csv_str))
    assert list(df_read.columns) == LIQUIDATION_EVENT_COLUMNS
    assert len(df_read) == 0


def test_export_with_live_scenario_runner():
    # UT: End-to-end integration test with live simulation results (ST-08)
    from src.usecase.scenario_runner import run_all_scenarios

    config = SimulationConfig(max_blocks=5, num_borrowers=50, seed=42)
    results = run_all_scenarios(config)

    # 1. Block results CSV
    csv_blocks = export_block_results_to_csv(results)
    df_blocks = pd.read_csv(io.StringIO(csv_blocks))

    # 3 scenarios * (5 + 1) blocks = 18 rows
    assert len(df_blocks) == 18
    assert list(df_blocks.columns) == BLOCK_RESULT_COLUMNS
    assert set(df_blocks["scenario"].unique()) == {"SC01", "SC02", "SC03"}

    # 2. Liquidation events CSV
    csv_events = export_liquidation_events_to_csv(results)
    df_events = pd.read_csv(io.StringIO(csv_events))

    assert list(df_events.columns) == LIQUIDATION_EVENT_COLUMNS
    total_expected_events = sum(len(res.liquidation_events) for res in results.values())
    assert len(df_events) == total_expected_events

