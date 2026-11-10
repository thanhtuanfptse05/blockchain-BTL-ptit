"""Simulation configuration domain model with strict validation.

# Implements FR-01, FR-02, FR-03, FR-04, FR-05
# Implements P-01, P-02, P-03, P-04, P-05, P-06
# Implements C-01, C-02, C-03, C-04, C-05, C-06, C-07, C-08, C-09, C-10
"""

from pydantic import BaseModel, ConfigDict, Field


class SimulationConfig(BaseModel):
    """Immutable configuration object for DeFi Liquidation Cascade Simulation.

    Attributes:
        shock_pct: Percentage drop of ETH price at block 1 (0.0 to 50.0).
        liquidation_threshold: Collateral threshold ratio (0.60 to 0.90).
        close_factor: Maximum portion of debt repayable per liquidation (0.10 to 1.00).
        liquidation_penalty: Bonus incentive paid to liquidator (0.00 to 0.20).
        pool_a_tvl_usd: Total Value Locked in Pool A ETH/USDC ($10M to $500M).
        pool_b_tvl_usd: Total Value Locked in Pool B stETH/ETH ($5M to $200M).
        num_borrowers: Total number of generated borrower agents (10 to 500).
        max_blocks: Total number of discrete blocks to simulate (5 to 100).
        seed: Random seed for deterministic simulation reproducibility (>= 0).
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    # Implements P-01, C-01, C-02: ETH price shock percentage
    shock_pct: float = Field(
        default=15.0,
        ge=0.0,
        le=50.0,
        description="Percentage of initial ETH price drop at block 1.",
    )

    # Implements C-03: Liquidation Threshold (unified for ETH and stETH)
    liquidation_threshold: float = Field(
        default=0.80,
        ge=0.60,
        le=0.90,
        description="Liquidation threshold ratio (LT).",
    )

    # Implements C-04: Close Factor
    close_factor: float = Field(
        default=0.50,
        ge=0.10,
        le=1.00,
        description="Portion of debt repayable in one liquidation call.",
    )

    # Implements C-05: Liquidation Penalty Bonus
    liquidation_penalty: float = Field(
        default=0.05,
        ge=0.0,
        le=0.20,
        description="Bonus collateral paid to liquidator as incentive.",
    )

    # Implements P-02, C-06, C-07: Pool A TVL in USD
    pool_a_tvl_usd: float = Field(
        default=150_000_000.0,
        ge=10_000_000.0,
        le=500_000_000.0,
        description="Total Value Locked in Pool A (ETH/USDC) in USD.",
    )

    # Implements P-03, C-08, C-09: Pool B TVL in USD
    pool_b_tvl_usd: float = Field(
        default=80_000_000.0,
        ge=5_000_000.0,
        le=200_000_000.0,
        description="Total Value Locked in Pool B (stETH/ETH) in USD.",
    )

    # Implements P-04, C-10: Number of Borrowers
    num_borrowers: int = Field(
        default=100,
        ge=10,
        le=500,
        description="Total count of simulated borrower agent positions.",
    )

    # Implements P-05: Maximum simulation blocks
    max_blocks: int = Field(
        default=30,
        ge=5,
        le=100,
        description="Total duration of discrete simulation blocks.",
    )

    # Implements P-06: Deterministic Seed
    seed: int = Field(
        default=42,
        ge=0,
        description="Seed for pseudo-random deterministic number generation.",
    )

