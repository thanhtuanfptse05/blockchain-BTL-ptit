"""Partial liquidation engine and bad debt calculation usecases.

# Implements FR-001, FR-002, FR-003, FR-004, FR-005, FR-006, FR-007, FR-008, FR-009, FR-010, FR-011, FR-012, FR-013
# Implements BR-04, BR-10, BR-11
# Implements UT-07, UT-08
"""

from typing import Optional, List
from src.domain.agent import BorrowerAgent, AgentStatus
from src.domain.liquidation_event import LiquidationEvent
from src.usecase.health_factor import EPSILON


def liquidate_borrower_position(
    agent: BorrowerAgent,
    scenario: str,
    block: int,
    spot_price_usd: float,
    close_factor: float = 0.50,
    liquidation_penalty: float = 0.05,
) -> Optional[LiquidationEvent]:
    """Execute partial liquidation on an eligible borrower agent position.

    # Implements BR-04, BR-11

    Algorithm:
        1. Calculate candidate repayment = close_factor * debt_usdc.
        2. Calculate maximum debt repayable supported by available collateral
           = (collateral_amount * spot_price_usd) / (1.0 + liquidation_penalty).
        3. debt_repaid = min(candidate_repay, max_repay_from_collateral).
        4. If debt_repaid <= EPSILON, abort (return None).
        5. collateral_seized = min(collateral_amount, debt_repaid * (1 + penalty) / spot_price_usd).
        6. Apply updates to agent state.
        7. Return LiquidationEvent with pre-trade spot values.

    Args:
        agent: BorrowerAgent position to liquidate.
        scenario: Scenario identifier ("SC02" or "SC03").
        block: Current simulation block number.
        spot_price_usd: Pre-trade spot price of collateral asset in USD.
        close_factor: Maximum portion of debt repayable (default 0.50).
        liquidation_penalty: Bonus collateral incentive (default 0.05).

    Returns:
        LiquidationEvent if liquidation executed, or None if not eligible/aborted.
    """
    if agent.status in (AgentStatus.REPAID, AgentStatus.BAD_DEBT):
        return None

    if agent.debt_usdc <= EPSILON or agent.collateral_amount <= EPSILON:
        return None

    # Compute HF immediately before trade
    collateral_val_usd = agent.collateral_amount * spot_price_usd
    hf_before = (collateral_val_usd * agent.liquidation_threshold) / agent.debt_usdc

    # Liquidation requires HF < 1.0 (strict inequality)
    if hf_before >= 1.0:
        return None

    # Step 1: Candidate repayment capped by close factor
    candidate_repay = close_factor * agent.debt_usdc

    # Step 2: Maximum repayment supported by current collateral with penalty bonus
    max_repay_from_collateral = collateral_val_usd / (1.0 + liquidation_penalty)

    # Step 3: Actual debt repaid
    debt_repaid = min(candidate_repay, max_repay_from_collateral)

    # Step 4: Abort if debt repaid is negligible
    if debt_repaid <= EPSILON:
        return None

    # Step 5: Quantity of collateral seized
    collateral_seized = min(
        agent.collateral_amount,
        (debt_repaid * (1.0 + liquidation_penalty)) / spot_price_usd,
    )
    collateral_val_oracle = collateral_seized * spot_price_usd

    # Step 6: Apply liquidation on agent
    agent.apply_liquidation(debt_repaid, collateral_seized)

    # Step 7: Record and return LiquidationEvent
    return LiquidationEvent(
        scenario=scenario,
        block=block,
        agent_id=agent.agent_id,
        asset=agent.collateral_type.value,
        hf_before=hf_before,
        debt_repaid_usd=debt_repaid,
        collateral_seized=collateral_seized,
        collateral_value_at_oracle_usd=collateral_val_oracle,
        remaining_debt_usd=agent.debt_usdc,
        remaining_collateral=agent.collateral_amount,
    )


def compute_total_bad_debt(agents: List[BorrowerAgent]) -> float:
    """Aggregate total outstanding bad debt across all borrower agent positions.

    # Implements BR-10, FR-009

    Bad debt is defined as debt of positions where collateral is depleted
    (collateral <= EPSILON) but debt remains (debt > EPSILON). Computed from
    current snapshot state.

    Args:
        agents: List of all borrower agents in the simulation.

    Returns:
        Sum of bad debt in USD/USDC.
    """
    total = 0.0
    for agent in agents:
        if agent.collateral_amount <= EPSILON and agent.debt_usdc > EPSILON:
            total += agent.debt_usdc
    return total

