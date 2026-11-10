"""Unit tests for Partial Liquidation Engine and LiquidationEvent.

# Implements FR-001, FR-002, FR-003, FR-004, FR-005, FR-006, FR-007, FR-008, FR-009, FR-010, FR-011, FR-012
# Implements BR-04, BR-10, BR-11
# Implements UT-07, UT-08
"""

import pytest
from src.domain.agent import BorrowerAgent, AssetType, AgentStatus
from src.domain.liquidation_event import LiquidationEvent
from src.usecase.liquidation_engine import (
    liquidate_borrower_position,
    compute_total_bad_debt,
)


def test_normal_partial_liquidation_story_1():
    """Verify normal liquidation: 50% debt repaid, 105% collateral seized, agent remains active (UT-07)."""
    # Agent with 166.6667 ETH, debt 350,000 USDC, post-shock price = 2,550 USD
    agent = BorrowerAgent(
        agent_id=10,
        collateral_type=AssetType.ETH,
        collateral_amount=166.6667,
        debt_usdc=350_000.0,
        initial_ltv=0.70,
        liquidation_threshold=0.80,
    )

    event = liquidate_borrower_position(
        agent=agent,
        scenario="SC03",
        block=1,
        spot_price_usd=2550.0,
        close_factor=0.50,
        liquidation_penalty=0.05,
    )

    assert event is not None
    assert isinstance(event, LiquidationEvent)

    # 1. 10 Fields verification
    assert event.scenario == "SC03"
    assert event.block == 1
    assert event.agent_id == 10
    assert event.asset == "ETH"
    assert event.hf_before == pytest.approx(166.6667 * 2550.0 * 0.80 / 350_000.0, rel=1e-5)
    assert event.debt_repaid_usd == pytest.approx(175_000.0, rel=1e-5)

    expected_seized = 175_000.0 * 1.05 / 2550.0
    assert event.collateral_seized == pytest.approx(expected_seized, rel=1e-5)
    assert event.collateral_value_at_oracle_usd == pytest.approx(183_750.0, rel=1e-5)
    assert event.remaining_debt_usd == pytest.approx(175_000.0, rel=1e-5)
    assert event.remaining_collateral == pytest.approx(166.6667 - expected_seized, rel=1e-5)

    # 2. Agent state update
    assert agent.ever_liquidated is True
    assert agent.liquidation_count == 1
    assert agent.status == AgentStatus.ACTIVE
    assert agent.debt_usdc == pytest.approx(175_000.0, rel=1e-5)
    assert agent.collateral_amount == pytest.approx(166.6667 - expected_seized, rel=1e-5)

    # Post-liquidation HF should be restored above 1.0
    post_hf = (agent.collateral_amount * 2550.0 * 0.80) / agent.debt_usdc
    assert post_hf > 1.0


def test_insufficient_collateral_leads_to_bad_debt_story_2():
    """Verify liquidation when collateral is insufficient to cover 50% debt + penalty (UT-08).

    Debt = 10,000 USDC, Collateral = 2 ETH @ $2,000 = $4,000.
    Max repay from collateral = 4,000 / 1.05 = 3,809.5238 USDC.
    Remaining debt = 10,000 - 3,809.5238 = 6,190.4762 USDC -> BAD_DEBT.
    """
    agent = BorrowerAgent(
        agent_id=20,
        collateral_type=AssetType.ETH,
        collateral_amount=2.0,
        debt_usdc=10_000.0,
        initial_ltv=0.70,
        liquidation_threshold=0.80,
    )

    event = liquidate_borrower_position(
        agent=agent,
        scenario="SC02",
        block=2,
        spot_price_usd=2000.0,
        close_factor=0.50,
        liquidation_penalty=0.05,
    )

    assert event is not None
    assert event.debt_repaid_usd == pytest.approx(3809.5238, rel=1e-4)
    assert event.collateral_seized == pytest.approx(2.0, rel=1e-5)
    assert event.remaining_collateral == 0.0
    assert event.remaining_debt_usd == pytest.approx(6190.4762, rel=1e-4)

    # Agent must be marked as BAD_DEBT
    assert agent.status == AgentStatus.BAD_DEBT
    assert agent.collateral_amount == 0.0
    assert agent.debt_usdc == pytest.approx(6190.4762, rel=1e-4)

    # Subsequent attempt to liquidate BAD_DEBT agent must return None
    event_again = liquidate_borrower_position(
        agent=agent,
        scenario="SC02",
        block=3,
        spot_price_usd=2000.0,
        close_factor=0.50,
        liquidation_penalty=0.05,
    )
    assert event_again is None


def test_full_repay_marks_agent_repaid():
    """Verify that when debt becomes zero after liquidation, agent is marked REPAID."""
    # Undercollateralized agent: 0.05 ETH @ $2,000 = $100 collateral, debt = $90 USDC
    # HF = 100 * 0.80 / 90 = 0.8888 < 1.0 (Eligible for liquidation)
    agent = BorrowerAgent(
        agent_id=30,
        collateral_type=AssetType.ETH,
        collateral_amount=0.05,
        debt_usdc=90.0,
        initial_ltv=0.70,
        liquidation_threshold=0.80,
    )

    # Custom close factor of 1.0 to repay all debt
    event = liquidate_borrower_position(
        agent=agent,
        scenario="SC03",
        block=1,
        spot_price_usd=2000.0,
        close_factor=1.00,
        liquidation_penalty=0.05,
    )

    assert event is not None
    assert event.debt_repaid_usd == pytest.approx(90.0, rel=1e-5)
    assert agent.debt_usdc == 0.0
    assert agent.status == AgentStatus.REPAID


def test_zero_repay_returns_none():
    """Verify that if debt is 0 or collateral is 0, liquidation returns None."""
    agent = BorrowerAgent(
        agent_id=40,
        collateral_type=AssetType.ETH,
        collateral_amount=0.0,
        debt_usdc=0.0,
        initial_ltv=0.0,
    )
    event = liquidate_borrower_position(
        agent=agent,
        scenario="SC03",
        block=1,
        spot_price_usd=2500.0,
    )
    assert event is None


def test_compute_total_bad_debt():
    """Verify total bad debt aggregation across agent population (BR-10, FR-009)."""
    agents = [
        BorrowerAgent(1, AssetType.ETH, 0.0, 5000.0, 0.7, status=AgentStatus.BAD_DEBT),
        BorrowerAgent(2, AssetType.ETH, 10.0, 20000.0, 0.6, status=AgentStatus.ACTIVE),
        BorrowerAgent(3, AssetType.STETH, 0.0, 8000.0, 0.7, status=AgentStatus.BAD_DEBT),
        BorrowerAgent(4, AssetType.STETH, 5.0, 0.0, 0.0, status=AgentStatus.REPAID),
    ]

    total_bad_debt = compute_total_bad_debt(agents)
    assert total_bad_debt == pytest.approx(13_000.0, rel=1e-5)
