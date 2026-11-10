"""Shared pytest fixtures for DeFi Liquidation Cascade Simulator.

# Implements shared testing setup (T003)
"""

from typing import List, Tuple
import pytest
from src.domain.config import SimulationConfig
from src.domain.agent import BorrowerAgent, AssetType, AgentStatus
from src.domain.amm_pool import AMMPool
from src.usecase.agent_generator import generate_borrower_agents
from src.usecase.amm_engine import initialize_pools


@pytest.fixture
def default_config() -> SimulationConfig:
    """Fixture returning a standard default SimulationConfig instance."""
    return SimulationConfig()


@pytest.fixture
def default_agents(default_config: SimulationConfig) -> List[BorrowerAgent]:
    """Fixture returning the standard 100 borrower agents for default config."""
    return generate_borrower_agents(default_config)


@pytest.fixture
def default_pools(default_config: SimulationConfig) -> Tuple[AMMPool, AMMPool]:
    """Fixture returning initialized Pool A and Pool B for default config."""
    return initialize_pools(default_config)


@pytest.fixture
def sample_eth_agent() -> BorrowerAgent:
    """Fixture returning a deterministic sample ETH borrower agent.

    10 ETH @ $3,000 = $30,000 collateral.
    Debt = $22,000 USDC.
    Initial LTV = 22,000 / 30,000 = 0.7333.
    """
    return BorrowerAgent(
        agent_id=1,
        collateral_type=AssetType.ETH,
        collateral_amount=10.0,
        debt_usdc=22_000.0,
        initial_ltv=0.7333,
        liquidation_threshold=0.80,
        ever_liquidated=False,
        liquidation_count=0,
        status=AgentStatus.ACTIVE,
    )


@pytest.fixture
def sample_steth_agent() -> BorrowerAgent:
    """Fixture returning a deterministic sample stETH borrower agent.

    10 stETH @ $2,970 = $29,700 collateral.
    Debt = $20,000 USDC.
    """
    return BorrowerAgent(
        agent_id=2,
        collateral_type=AssetType.STETH,
        collateral_amount=10.0,
        debt_usdc=20_000.0,
        initial_ltv=0.6734,
        liquidation_threshold=0.80,
        ever_liquidated=False,
        liquidation_count=0,
        status=AgentStatus.ACTIVE,
    )
