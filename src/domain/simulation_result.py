"""SimulationResult and KPISummary domain models.

# Implements FR-018, SRS §7.5
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from src.domain.config import SimulationConfig
from src.domain.block_result import BlockResult
from src.domain.liquidation_event import LiquidationEvent


@dataclass(frozen=True)
class KPISummary:
    """Statistical KPI summary for a completed scenario run.

    # Implements FR-018, SRS §7.5, FR-07, FR-11

    Attributes:
        scenario_id: Scenario identifier ("SC01", "SC02", "SC03").
        final_eth_price_usd: ETH price at final block.
        final_steth_price_usd: stETH price at final block.
        final_steth_discount_pct: stETH discount percentage at final block.
        liquidated_agents_unique: Total distinct agents ever liquidated.
        total_agents: Total count of agents in the simulation.
        liquidated_agents_ratio_pct: Ratio of liquidated agents over total (%).
        liquidation_events_total: Total number of liquidation events across all blocks.
        total_debt_repaid_usd: Total borrow debt repaid across all events.
        bad_debt_usd: Total outstanding bad debt at final block.
        delta_eth_price_usd: Delta vs SC02 (if applicable).
        delta_steth_price_usd: Delta vs SC02 (if applicable).
        delta_steth_discount_pct: Delta vs SC02 (if applicable).
        delta_liquidated_agents: Additional liquidated agents vs SC02.
        delta_liquidation_events: Delta liquidation events vs SC02.
        delta_bad_debt_usd: Delta bad debt vs SC02.
    """

    scenario_id: str
    final_eth_price_usd: float
    final_steth_price_usd: float
    final_steth_discount_pct: float
    liquidated_agents_unique: int
    total_agents: int
    liquidated_agents_ratio_pct: float
    liquidation_events_total: int
    total_debt_repaid_usd: float
    bad_debt_usd: float
    delta_eth_price_usd: Optional[float] = None
    delta_steth_price_usd: Optional[float] = None
    delta_steth_discount_pct: Optional[float] = None
    delta_liquidated_agents: Optional[int] = None
    delta_liquidation_events: Optional[int] = None
    delta_bad_debt_usd: Optional[float] = None


@dataclass(frozen=True)
class SimulationResult:
    """Container holding the complete output of a single scenario simulation.

    # Implements SRS §7.5, FR-018

    Attributes:
        scenario_id: Identifier ("SC01", "SC02", or "SC03").
        parameters: SimulationConfig instance or parameter dictionary.
        block_results: List of exactly max_blocks + 1 BlockResult records.
        liquidation_events: List of all recorded LiquidationEvent objects.
        summary: KPISummary object or summary dictionary with 7 core metrics.
    """

    scenario_id: str
    parameters: SimulationConfig
    block_results: List[BlockResult]
    liquidation_events: List[LiquidationEvent]
    summary: KPISummary

