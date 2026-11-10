"""Data Tables and CSV Exporter infrastructure.

# Implements FR-09, FR-09-01..FR-09-05, ST-08, SRS §7.3, §7.4, §15.1
"""

import io
from typing import Dict, List, Any
import pandas as pd
from src.domain.simulation_result import SimulationResult
from src.domain.block_result import BlockResult
from src.domain.liquidation_event import LiquidationEvent

BLOCK_RESULT_COLUMNS = [
    "scenario",
    "block",
    "eth_price_usd",
    "steth_price_usd",
    "steth_discount_pct",
    "liquidations_eth",
    "liquidations_steth",
    "liquidations_total",
    "liquidated_agents_unique_cumulative",
    "liquidation_debt_repaid_usd",
    "liquidation_debt_repaid_cumulative_usd",
    "bad_debt_usd",
]

LIQUIDATION_EVENT_COLUMNS = [
    "scenario",
    "block",
    "agent_id",
    "asset",
    "hf_before",
    "debt_repaid_usd",
    "collateral_seized",
    "collateral_value_at_oracle_usd",
    "remaining_debt_usd",
    "remaining_collateral",
]


def block_results_to_dataframe(results: Dict[str, SimulationResult]) -> pd.DataFrame:
    """Consolidate block results from all scenarios into a single Pandas DataFrame.

    # Implements FR-09-01, SRS §7.4

    Args:
        results: Dictionary mapping scenario IDs to their SimulationResult objects.

    Returns:
        DataFrame with exactly 12 standardized columns.
    """
    rows: List[Dict[str, Any]] = []
    for sc_id in sorted(results.keys()):
        sim_res = results[sc_id]
        for b in sim_res.block_results:
            rows.append({
                "scenario": b.scenario,
                "block": b.block,
                "eth_price_usd": b.eth_price_usd,
                "steth_price_usd": b.steth_price_usd,
                "steth_discount_pct": b.steth_discount_pct,
                "liquidations_eth": b.liquidations_eth,
                "liquidations_steth": b.liquidations_steth,
                "liquidations_total": b.liquidations_total,
                "liquidated_agents_unique_cumulative": b.liquidated_agents_unique_cumulative,
                "liquidation_debt_repaid_usd": b.liquidation_debt_repaid_usd,
                "liquidation_debt_repaid_cumulative_usd": b.liquidation_debt_repaid_cumulative_usd,
                "bad_debt_usd": b.bad_debt_usd,
            })

    if not rows:
        return pd.DataFrame(columns=BLOCK_RESULT_COLUMNS)
    return pd.DataFrame(rows, columns=BLOCK_RESULT_COLUMNS)


def liquidation_events_to_dataframe(results: Dict[str, SimulationResult]) -> pd.DataFrame:
    """Consolidate liquidation events from all scenarios into a single Pandas DataFrame.

    # Implements FR-09-02, SRS §7.3

    Args:
        results: Dictionary mapping scenario IDs to their SimulationResult objects.

    Returns:
        DataFrame with exactly 10 standardized columns.
    """
    rows: List[Dict[str, Any]] = []
    for sc_id in sorted(results.keys()):
        sim_res = results[sc_id]
        for ev in sim_res.liquidation_events:
            rows.append({
                "scenario": ev.scenario,
                "block": ev.block,
                "agent_id": ev.agent_id,
                "asset": ev.asset,
                "hf_before": ev.hf_before,
                "debt_repaid_usd": ev.debt_repaid_usd,
                "collateral_seized": ev.collateral_seized,
                "collateral_value_at_oracle_usd": ev.collateral_value_at_oracle_usd,
                "remaining_debt_usd": ev.remaining_debt_usd,
                "remaining_collateral": ev.remaining_collateral,
            })

    if not rows:
        return pd.DataFrame(columns=LIQUIDATION_EVENT_COLUMNS)
    return pd.DataFrame(rows, columns=LIQUIDATION_EVENT_COLUMNS)


def export_block_results_to_csv(results: Dict[str, SimulationResult]) -> str:
    """Export block results from all scenarios to a CSV string.

    # Implements FR-09-01, FR-09-03, ST-08

    Args:
        results: Dictionary mapping scenario IDs to their SimulationResult objects.

    Returns:
        RFC 4180 compliant CSV string with header.
    """
    df = block_results_to_dataframe(results)
    return df.to_csv(index=False)


def export_liquidation_events_to_csv(results: Dict[str, SimulationResult]) -> str:
    """Export liquidation events from all scenarios to a CSV string.

    # Implements FR-09-02, FR-09-03, ST-08

    Args:
        results: Dictionary mapping scenario IDs to their SimulationResult objects.

    Returns:
        RFC 4180 compliant CSV string with header.
    """
    df = liquidation_events_to_dataframe(results)
    return df.to_csv(index=False)

