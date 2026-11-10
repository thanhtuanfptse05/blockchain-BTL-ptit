"""BlockResult domain schema.

# Implements FR-013, FR-015, SRS §7.4
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class BlockResult:
    """Record of market prices, liquidations, and debt metrics for a single simulation block.

    # Implements SRS §7.4 (12 columns)

    Attributes:
        scenario: Scenario identifier ("SC01", "SC02", "SC03").
        block: Block index (0 to max_blocks).
        eth_price_usd: Spot price of ETH in USD at end of block.
        steth_price_usd: Spot price of stETH in USD at end of block.
        steth_discount_pct: stETH discount percentage vs ETH.
        liquidations_eth: Number of ETH liquidation events in this block.
        liquidations_steth: Number of stETH liquidation events in this block.
        liquidations_total: Total liquidation events in this block (eth + steth).
        liquidated_agents_unique_cumulative: Unique agents liquidated up to this block.
        liquidation_debt_repaid_usd: Total borrow debt repaid by liquidators in this block.
        liquidation_debt_repaid_cumulative_usd: Cumulative borrow debt repaid up to this block.
        bad_debt_usd: Current snapshot total bad debt across all positions at end of block.
    """

    scenario: str
    block: int
    eth_price_usd: float
    steth_price_usd: float
    steth_discount_pct: float
    liquidations_eth: int
    liquidations_steth: int
    liquidations_total: int
    liquidated_agents_unique_cumulative: int
    liquidation_debt_repaid_usd: float
    liquidation_debt_repaid_cumulative_usd: float
    bad_debt_usd: float

