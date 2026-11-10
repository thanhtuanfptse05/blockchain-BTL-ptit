"""LiquidationEvent domain schema.

# Implements FR-005, SRS §7.3
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class LiquidationEvent:
    """Immutable record of an executed liquidation event.

    Attributes:
        scenario: Scenario identifier ("SC02" or "SC03").
        block: Simulation block number when liquidation occurred.
        agent_id: Identifier of the liquidated BorrowerAgent.
        asset: Collateral asset type ("ETH" or "stETH").
        hf_before: Health Factor value immediately before liquidation.
        debt_repaid_usd: Portion of borrow debt repaid by liquidator in USD/USDC.
        collateral_seized: Quantity of tokens seized from agent's collateral.
        collateral_value_at_oracle_usd: USD valuation of seized collateral at pre-trade spot.
        remaining_debt_usd: Remaining borrow debt after partial liquidation.
        remaining_collateral: Remaining collateral token amount after partial liquidation.
    """

    scenario: str
    block: int
    agent_id: int
    asset: str
    hf_before: float
    debt_repaid_usd: float
    collateral_seized: float
    collateral_value_at_oracle_usd: float
    remaining_debt_usd: float
    remaining_collateral: float

