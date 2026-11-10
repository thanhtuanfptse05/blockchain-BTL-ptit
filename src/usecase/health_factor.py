"""Health Factor, collateral valuation, and liquidation eligibility usecases.

# Implements FR-001, FR-002, FR-003, FR-004, FR-005, FR-006, FR-007, FR-008, FR-010, FR-011
# Implements BR-01, BR-02, BR-03
# Implements UT-04, UT-05, UT-06
"""

import math
from typing import Union
from src.domain.agent import BorrowerAgent, AssetType, AgentStatus


# Numerical tolerance for zero comparisons (FR-010, SRS §8)
EPSILON: float = 1e-9


def compute_collateral_value(
    agent: BorrowerAgent,
    eth_price_usd: float,
    steth_price_usd: float,
) -> float:
    """Calculate the USD valuation of an agent's collateral at current prices.

    # Implements BR-01, FR-001, FR-008

    Args:
        agent: BorrowerAgent position.
        eth_price_usd: Current spot price of ETH in USD (> 0).
        steth_price_usd: Current spot price of stETH in USD (> 0).

    Returns:
        Total collateral value in USD.

    Raises:
        ValueError: If prices are non-positive or non-finite.
    """
    if not (math.isfinite(eth_price_usd) and eth_price_usd > 0):
        raise ValueError(f"Invalid ETH price: {eth_price_usd}")
    if not (math.isfinite(steth_price_usd) and steth_price_usd > 0):
        raise ValueError(f"Invalid stETH price: {steth_price_usd}")

    if agent.collateral_type == AssetType.ETH:
        price = eth_price_usd
    else:
        price = steth_price_usd

    return agent.collateral_amount * price


def compute_current_ltv(
    debt_usdc: float,
    collateral_value_usd: float,
) -> float:
    """Calculate current Loan-To-Value ratio.

    # Implements BR-02, FR-002, FR-003

    Args:
        debt_usdc: Outstanding borrow debt in USDC.
        collateral_value_usd: Current collateral valuation in USD.

    Returns:
        Current LTV as float, or math.inf if debt > 0 and collateral = 0.
    """
    if collateral_value_usd <= EPSILON:
        if debt_usdc > EPSILON:
            return math.inf
        return 0.0

    return debt_usdc / collateral_value_usd


def compute_health_factor(
    collateral_value_usd: float,
    debt_usdc: float,
    liquidation_threshold: float = 0.80,
) -> float:
    """Calculate Health Factor with safe edge-case handling.

    # Implements BR-03, FR-004, FR-005

    HF = (collateral_value_usd * liquidation_threshold) / debt_usdc

    Rules:
        - If debt <= epsilon: HF = +inf (safe, no debt).
        - If collateral <= epsilon and debt > epsilon: HF = 0.0 (bad debt).

    Args:
        collateral_value_usd: Current collateral value in USD.
        debt_usdc: Outstanding debt in USDC.
        liquidation_threshold: Liquidation threshold ratio (default 0.80).

    Returns:
        Health Factor as float.
    """
    if debt_usdc <= EPSILON:
        return math.inf

    if collateral_value_usd <= EPSILON:
        return 0.0

    return (collateral_value_usd * liquidation_threshold) / debt_usdc


def is_liquidatable(
    agent: BorrowerAgent,
    eth_price_usd: float,
    steth_price_usd: float,
    liquidation_threshold: float = 0.80,
) -> bool:
    """Determine whether an agent position is eligible for liquidation.

    # Implements FR-006, FR-007, FR-011

    Eligible if:
        - Status is ACTIVE (not REPAID or BAD_DEBT)
        - debt_usdc > epsilon
        - collateral_amount > epsilon
        - HF < 1.0 (strict inequality; HF >= 1.0 is NOT eligible)

    Args:
        agent: BorrowerAgent position.
        eth_price_usd: Current spot price of ETH in USD.
        steth_price_usd: Current spot price of stETH in USD.
        liquidation_threshold: Protocol threshold ratio (default 0.80).

    Returns:
        True if eligible for partial liquidation, False otherwise.
    """
    if agent.status in (AgentStatus.REPAID, AgentStatus.BAD_DEBT):
        return False

    if agent.debt_usdc <= EPSILON:
        return False

    if agent.collateral_amount <= EPSILON:
        return False

    collateral_val = compute_collateral_value(agent, eth_price_usd, steth_price_usd)
    hf = compute_health_factor(collateral_val, agent.debt_usdc, liquidation_threshold)

    return hf < 1.0

