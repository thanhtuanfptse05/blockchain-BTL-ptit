"""Unit tests for collateral valuation, Health Factor, and liquidation eligibility.

# Implements FR-001, FR-002, FR-003, FR-004, FR-005, FR-006, FR-007, FR-008, FR-009, FR-010
# Implements BR-01, BR-02, BR-03
# Implements UT-04, UT-05, UT-06, SC-001, SC-002, SC-003
"""

import math
import pytest
from src.domain.agent import BorrowerAgent, AssetType, AgentStatus
from src.usecase.health_factor import (
    compute_collateral_value,
    compute_current_ltv,
    compute_health_factor,
    is_liquidatable,
    EPSILON,
)


def test_hand_check_eth_agent_before_and_after_shock():
    """Verify hand calculation from SRS §8 (UT-04 / SC-001).

    Agent has 10 ETH, debt = 22,000 USDC, LT = 0.80.
    - Pre-shock ($3,000): HF = 1.090909... -> Safe (is_liquidatable = False).
    - Post-shock ($2,550): HF = 0.927272... -> Eligible (is_liquidatable = True).
    """
    agent = BorrowerAgent(
        agent_id=1,
        collateral_type=AssetType.ETH,
        collateral_amount=10.0,
        debt_usdc=22_000.0,
        initial_ltv=22_000.0 / 30_000.0,
        liquidation_threshold=0.80,
    )

    # 1. Pre-shock: ETH price = $3,000
    val_pre = compute_collateral_value(agent, eth_price_usd=3000.0, steth_price_usd=2970.0)
    assert val_pre == 30_000.0

    ltv_pre = compute_current_ltv(agent.debt_usdc, val_pre)
    assert ltv_pre == pytest.approx(22_000.0 / 30_000.0, rel=1e-6)

    hf_pre = compute_health_factor(val_pre, agent.debt_usdc, agent.liquidation_threshold)
    assert hf_pre == pytest.approx(10.0 * 3000.0 * 0.80 / 22_000.0, rel=1e-6)
    assert hf_pre == pytest.approx(1.090909, abs=1e-5)
    assert not is_liquidatable(agent, eth_price_usd=3000.0, steth_price_usd=2970.0)

    # 2. Post-shock (15% drop): ETH price = $2,550
    val_post = compute_collateral_value(agent, eth_price_usd=2550.0, steth_price_usd=2524.5)
    assert val_post == 25_500.0

    hf_post = compute_health_factor(val_post, agent.debt_usdc, agent.liquidation_threshold)
    assert hf_post == pytest.approx(10.0 * 2550.0 * 0.80 / 22_000.0, rel=1e-6)
    assert hf_post == pytest.approx(0.927273, abs=1e-5)
    assert is_liquidatable(agent, eth_price_usd=2550.0, steth_price_usd=2524.5)


def test_steth_agent_cross_price_and_depeg():
    """Verify stETH valuation using stETH USD price and boundary HF = 1.0 (UT-05)."""
    agent = BorrowerAgent(
        agent_id=2,
        collateral_type=AssetType.STETH,
        collateral_amount=100.0,
        debt_usdc=200_000.0,
        initial_ltv=0.6734,
        liquidation_threshold=0.80,
    )

    # Initial stETH price = $2,970 (ETH $3,000 * 0.99)
    val_initial = compute_collateral_value(agent, eth_price_usd=3000.0, steth_price_usd=2970.0)
    assert val_initial == 297_000.0

    hf_initial = compute_health_factor(val_initial, agent.debt_usdc, agent.liquidation_threshold)
    assert hf_initial == pytest.approx(1.188, rel=1e-6)
    assert not is_liquidatable(agent, eth_price_usd=3000.0, steth_price_usd=2970.0)

    # Depeg to exactly $2,500 -> HF = 1.0 (Boundary check: HF == 1 is NOT liquidatable)
    val_boundary = compute_collateral_value(agent, eth_price_usd=2600.0, steth_price_usd=2500.0)
    hf_boundary = compute_health_factor(val_boundary, agent.debt_usdc, agent.liquidation_threshold)
    assert hf_boundary == pytest.approx(1.0, rel=1e-6)
    assert not is_liquidatable(agent, eth_price_usd=2600.0, steth_price_usd=2500.0)

    # Further drop to $2,490 -> HF < 1.0 -> Liquidatable
    assert is_liquidatable(agent, eth_price_usd=2600.0, steth_price_usd=2490.0)


def test_edge_cases_zero_debt_and_zero_collateral():
    """Verify numerical boundaries: debt=0 -> HF=inf; collateral=0 -> bad debt (UT-06 / SC-003)."""
    # 1. Debt <= epsilon -> HF = +inf
    agent_zero_debt = BorrowerAgent(
        agent_id=3,
        collateral_type=AssetType.ETH,
        collateral_amount=5.0,
        debt_usdc=0.0,
        initial_ltv=0.0,
    )
    val_zero_debt = compute_collateral_value(agent_zero_debt, 3000.0, 2970.0)
    hf_inf = compute_health_factor(val_zero_debt, agent_zero_debt.debt_usdc, 0.80)
    assert math.isinf(hf_inf)
    assert not is_liquidatable(agent_zero_debt, 3000.0, 2970.0)

    # Small debt <= epsilon
    hf_small_debt = compute_health_factor(val_zero_debt, EPSILON / 2, 0.80)
    assert math.isinf(hf_small_debt)

    # 2. Collateral <= epsilon and debt > 0 -> HF = 0.0, cannot be liquidated further
    agent_bad_debt = BorrowerAgent(
        agent_id=4,
        collateral_type=AssetType.ETH,
        collateral_amount=0.0,
        debt_usdc=10_000.0,
        initial_ltv=0.70,
        status=AgentStatus.BAD_DEBT,
    )
    val_bad_debt = compute_collateral_value(agent_bad_debt, 3000.0, 2970.0)
    assert val_bad_debt == 0.0
    hf_bad_debt = compute_health_factor(val_bad_debt, agent_bad_debt.debt_usdc, 0.80)
    assert hf_bad_debt == 0.0
    assert not is_liquidatable(agent_bad_debt, 3000.0, 2970.0)

    # 3. Status is REPAID
    agent_repaid = BorrowerAgent(
        agent_id=5,
        collateral_type=AssetType.ETH,
        collateral_amount=5.0,
        debt_usdc=0.0,
        initial_ltv=0.60,
        status=AgentStatus.REPAID,
    )
    assert not is_liquidatable(agent_repaid, 3000.0, 2970.0)


def test_invalid_prices_raise_error():
    """Verify non-positive or non-finite prices raise ValueError (FR-008)."""
    agent = BorrowerAgent(
        agent_id=1,
        collateral_type=AssetType.ETH,
        collateral_amount=10.0,
        debt_usdc=1000.0,
        initial_ltv=0.6,
    )
    with pytest.raises(ValueError):
        compute_collateral_value(agent, eth_price_usd=0.0, steth_price_usd=2970.0)

    with pytest.raises(ValueError):
        compute_collateral_value(agent, eth_price_usd=-500.0, steth_price_usd=2970.0)

    with pytest.raises(ValueError):
        compute_collateral_value(agent, eth_price_usd=3000.0, steth_price_usd=float("nan"))


def test_convenience_methods_on_agent():
    """Verify convenience methods on BorrowerAgent entity match usecase calculations (FR-009)."""
    agent = BorrowerAgent(
        agent_id=1,
        collateral_type=AssetType.ETH,
        collateral_amount=10.0,
        debt_usdc=22_000.0,
        initial_ltv=0.7333,
        liquidation_threshold=0.80,
    )
    val = agent.collateral_value(eth_price_usd=3000.0, steth_price_usd=2970.0)
    assert val == 30_000.0

    hf = agent.health_factor(eth_price_usd=3000.0, steth_price_usd=2970.0)
    assert hf == pytest.approx(1.090909, abs=1e-5)
    assert not agent.is_liquidatable(eth_price_usd=3000.0, steth_price_usd=2970.0)

    # After shock
    assert agent.is_liquidatable(eth_price_usd=2550.0, steth_price_usd=2524.5)

