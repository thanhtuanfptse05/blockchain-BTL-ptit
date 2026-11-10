"""Borrower Agent domain model.

# Implements FR-001, FR-002, FR-005, FR-009, FR-011
"""

from dataclasses import dataclass
from enum import Enum
import math


class AssetType(str, Enum):
    """Supported collateral asset types in the lending protocol."""

    ETH = "ETH"
    STETH = "stETH"


class AgentStatus(str, Enum):
    """Lifecycle status of a simulated borrower position."""

    ACTIVE = "ACTIVE"
    REPAID = "REPAID"
    BAD_DEBT = "BAD_DEBT"


@dataclass
class BorrowerAgent:
    """Borrower agent representing a leveraged collateralized debt position.

    Attributes:
        agent_id: Unique integer identifier (1 to N).
        collateral_type: Asset deposited as collateral (ETH or stETH).
        collateral_amount: Quantity of tokens held as collateral.
        debt_usdc: Outstanding borrow debt in USDC.
        initial_ltv: Initial Loan-To-Value ratio drawn from [0.55, 0.72].
        liquidation_threshold: Protocol liquidation threshold ratio (default 0.80).
        ever_liquidated: Flag indicating whether this position was ever liquidated.
        liquidation_count: Total count of liquidation events experienced.
        status: Current position lifecycle status (ACTIVE, REPAID, BAD_DEBT).
    """

    agent_id: int
    collateral_type: AssetType
    collateral_amount: float
    debt_usdc: float
    initial_ltv: float
    liquidation_threshold: float = 0.80
    ever_liquidated: bool = False
    liquidation_count: int = 0
    status: AgentStatus = AgentStatus.ACTIVE

    def collateral_value(self, eth_price_usd: float, steth_price_usd: float) -> float:
        """Calculate USD collateral value at current prices (FR-009)."""
        price = eth_price_usd if self.collateral_type == AssetType.ETH else steth_price_usd
        return self.collateral_amount * price

    def health_factor(self, eth_price_usd: float, steth_price_usd: float) -> float:
        """Calculate current Health Factor (FR-009)."""
        if self.debt_usdc <= 1e-9:
            return math.inf
        val = self.collateral_value(eth_price_usd, steth_price_usd)
        if val <= 1e-9:
            return 0.0
        return (val * self.liquidation_threshold) / self.debt_usdc

    def is_liquidatable(self, eth_price_usd: float, steth_price_usd: float) -> bool:
        """Check if position is eligible for liquidation (FR-009)."""
        if self.status in (AgentStatus.REPAID, AgentStatus.BAD_DEBT):
            return False
        if self.debt_usdc <= 1e-9 or self.collateral_amount <= 1e-9:
            return False
        return self.health_factor(eth_price_usd, steth_price_usd) < 1.0

    def apply_liquidation(self, debt_repaid: float, collateral_seized: float) -> None:
        """Apply the results of a partial liquidation to this agent (FR-011).

        Deducts debt and collateral without allowing negative values, updates
        liquidation flags, and transitions status to REPAID or BAD_DEBT if applicable.
        """
        self.debt_usdc = max(0.0, self.debt_usdc - debt_repaid)
        self.collateral_amount = max(0.0, self.collateral_amount - collateral_seized)
        self.ever_liquidated = True
        self.liquidation_count += 1

        if self.debt_usdc <= 1e-9:
            self.debt_usdc = 0.0
            self.status = AgentStatus.REPAID
        elif self.collateral_amount <= 1e-9:
            self.collateral_amount = 0.0
            self.status = AgentStatus.BAD_DEBT
        else:
            self.status = AgentStatus.ACTIVE
