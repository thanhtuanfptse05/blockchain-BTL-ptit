"""AMM Constant Product Pool domain entity.

# Implements FR-002, FR-003, FR-004, FR-006, FR-007, SRS §7.2
"""

from dataclasses import dataclass
import math


@dataclass
class AMMPool:
    """Constant-product Automated Market Maker (AMM) liquidity pool.

    Implements x * y = k invariant without trading fees.

    Attributes:
        name: Identifier name (e.g., "ETH_USDC" or "STETH_ETH").
        token_x: Base asset symbol (ETH in Pool A, stETH in Pool B).
        token_y: Quote asset symbol (USDC in Pool A, ETH in Pool B).
        reserve_x: Current reserve quantity of token x (> 0).
        reserve_y: Current reserve quantity of token y (> 0).
    """

    name: str
    token_x: str
    token_y: str
    reserve_x: float
    reserve_y: float

    @property
    def k(self) -> float:
        """Constant product invariant k = reserve_x * reserve_y."""
        return self.reserve_x * self.reserve_y

    @property
    def spot_price(self) -> float:
        """Spot price of token x denominated in token y (reserve_y / reserve_x)."""
        return self.reserve_y / self.reserve_x

    def sell_x(self, delta_x: float) -> float:
        """Execute a swap depositing delta_x and withdrawing delta_y with zero fee.

        # Implements BR-05, FR-004

        Args:
            delta_x: Input token x amount (> 0).

        Returns:
            Output token y amount received.

        Raises:
            ValueError: If delta_x is non-positive or non-finite.
        """
        if not (math.isfinite(delta_x) and delta_x > 0):
            raise ValueError(f"Invalid swap input amount: {delta_x}")

        # Zero-fee constant product formula: dy = (y * dx) / (x + dx)
        amount_y_out = (self.reserve_y * delta_x) / (self.reserve_x + delta_x)

        self.reserve_x += delta_x
        self.reserve_y -= amount_y_out

        return amount_y_out

