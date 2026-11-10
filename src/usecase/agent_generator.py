"""Deterministic Borrower Agent population generator.

# Implements FR-001, FR-002, FR-003, FR-004, FR-005, FR-006, FR-007, FR-008
# Implements UT-02, UT-03, UT-12
"""

import random
from typing import List
from src.domain.config import SimulationConfig
from src.domain.agent import BorrowerAgent, AssetType, AgentStatus


# Initial asset spot prices (SRS §10.1, Spec 002)
INITIAL_ETH_PRICE_USD: float = 3000.0
INITIAL_STETH_PRICE_USD: float = 2970.0  # 3000.0 * 0.99 (1% discount)


def generate_borrower_agents(config: SimulationConfig) -> List[BorrowerAgent]:
    """Generate a reproducible population of borrower agents from config.

    Uses an isolated random.Random(seed) instance to guarantee that the agent
    population is completely identical across repeated simulation runs.

    Args:
        config: Validated SimulationConfig instance.

    Returns:
        List of BorrowerAgent instances (default 100: 50 ETH and 50 stETH).

    Raises:
        ValueError: If any generated agent has initial Health Factor <= 1.0.
    """
    rng = random.Random(config.seed)
    n = config.num_borrowers
    half = n // 2

    agents: List[BorrowerAgent] = []

    for agent_id in range(1, n + 1):
        if agent_id <= half:
            collateral_type = AssetType.ETH
            price = INITIAL_ETH_PRICE_USD
        else:
            collateral_type = AssetType.STETH
            price = INITIAL_STETH_PRICE_USD

        # Draw values in fixed deterministic sequence (SRS §10.1 bước 3)
        collateral_usd = rng.uniform(250_000.0, 1_000_000.0)
        initial_ltv = rng.uniform(0.55, 0.72)

        collateral_amount = collateral_usd / price
        debt_usdc = collateral_usd * initial_ltv

        # Health Factor verification (FR-006)
        hf = (collateral_amount * price * config.liquidation_threshold) / debt_usdc
        if hf <= 1.0:
            raise ValueError(
                f"Lỗi sinh dữ liệu: Agent {agent_id} có HF <= 1 ({hf:.4f})"
            )

        agent = BorrowerAgent(
            agent_id=agent_id,
            collateral_type=collateral_type,
            collateral_amount=collateral_amount,
            debt_usdc=debt_usdc,
            initial_ltv=initial_ltv,
            liquidation_threshold=config.liquidation_threshold,
            ever_liquidated=False,
            liquidation_count=0,
            status=AgentStatus.ACTIVE,
        )
        agents.append(agent)

    return agents

