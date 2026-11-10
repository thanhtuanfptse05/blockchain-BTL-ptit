"""Unit tests for BorrowerAgent entity and generation logic.

# Implements FR-001, FR-002, FR-003, FR-004, FR-005, FR-006, FR-007, FR-009
# Implements UT-02, UT-03, UT-12, SC-001, SC-002, SC-003, SC-004
"""

import pytest
from src.domain.config import SimulationConfig
from src.domain.agent import BorrowerAgent, AssetType, AgentStatus
from src.usecase.agent_generator import generate_borrower_agents


def test_default_generation_count_and_distribution(default_config: SimulationConfig):
    """Verify default generation yields 100 agents with 50 ETH and 50 stETH (UT-02)."""
    agents = generate_borrower_agents(default_config)
    assert len(agents) == 100

    # Verify agent IDs are 1 to 100 in strict sequence
    agent_ids = [a.agent_id for a in agents]
    assert agent_ids == list(range(1, 101))

    # First 50 must be ETH, next 50 must be stETH
    for a in agents[:50]:
        assert a.collateral_type == AssetType.ETH
        assert a.agent_id <= 50

    for a in agents[50:]:
        assert a.collateral_type == AssetType.STETH
        assert a.agent_id > 50


def test_agent_initial_attributes_and_ranges(default_config: SimulationConfig):
    """Verify initial LTV in [0.55, 0.72], collateral in [$250k, $1M], and all HF > 1."""
    agents = generate_borrower_agents(default_config)

    for a in agents:
        assert isinstance(a, BorrowerAgent)
        assert a.status == AgentStatus.ACTIVE
        assert a.ever_liquidated is False
        assert a.liquidation_count == 0
        assert a.liquidation_threshold == 0.80

        # LTV range [0.55, 0.72]
        assert 0.55 <= a.initial_ltv <= 0.72

        # Collateral valuation range [$250k, $1M]
        price = 3000.0 if a.collateral_type == AssetType.ETH else 2970.0
        collateral_usd = a.collateral_amount * price
        assert 250_000.0 <= collateral_usd <= 1_000_000.0

        # Debt calculation
        assert pytest.approx(a.debt_usdc, rel=1e-5) == collateral_usd * a.initial_ltv

        # Health Factor must be strictly greater than 1.0 (FR-006, SC-001)
        hf = (collateral_usd * a.liquidation_threshold) / a.debt_usdc
        assert hf > 1.0
        assert hf == pytest.approx(0.80 / a.initial_ltv, rel=1e-5)


def test_deterministic_reproducibility(default_config: SimulationConfig):
    """Verify determinism: same seed yields identical agents; different seed yields different agents."""
    agents_run1 = generate_borrower_agents(default_config)
    agents_run2 = generate_borrower_agents(default_config)

    # Must be 100% identical in every attribute
    for a1, a2 in zip(agents_run1, agents_run2):
        assert a1.agent_id == a2.agent_id
        assert a1.collateral_type == a2.collateral_type
        assert a1.collateral_amount == a2.collateral_amount
        assert a1.debt_usdc == a2.debt_usdc
        assert a1.initial_ltv == a2.initial_ltv

    # Different seed must produce different numbers
    diff_seed_config = SimulationConfig(seed=999)
    agents_diff = generate_borrower_agents(diff_seed_config)
    assert agents_run1[0].collateral_amount != agents_diff[0].collateral_amount
    assert agents_run1[0].debt_usdc != agents_diff[0].debt_usdc


def test_independence_from_pool_parameters():
    """Verify that changing pool TVL or shock does NOT alter generated agents (FR-007)."""
    cfg1 = SimulationConfig(seed=42, pool_a_tvl_usd=150_000_000.0, shock_pct=15.0)
    cfg2 = SimulationConfig(seed=42, pool_a_tvl_usd=300_000_000.0, shock_pct=30.0)

    agents1 = generate_borrower_agents(cfg1)
    agents2 = generate_borrower_agents(cfg2)

    for a1, a2 in zip(agents1, agents2):
        assert a1.collateral_amount == a2.collateral_amount
        assert a1.debt_usdc == a2.debt_usdc


def test_custom_agent_counts():
    """Verify scaling with custom borrower counts (SC-003)."""
    cfg_20 = SimulationConfig(num_borrowers=20, seed=42)
    agents_20 = generate_borrower_agents(cfg_20)
    assert len(agents_20) == 20
    assert sum(1 for a in agents_20 if a.collateral_type == AssetType.ETH) == 10
    assert sum(1 for a in agents_20 if a.collateral_type == AssetType.STETH) == 10

    cfg_200 = SimulationConfig(num_borrowers=200, seed=42)
    agents_200 = generate_borrower_agents(cfg_200)
    assert len(agents_200) == 200
    assert sum(1 for a in agents_200 if a.collateral_type == AssetType.ETH) == 100
    assert sum(1 for a in agents_200 if a.collateral_type == AssetType.STETH) == 100

