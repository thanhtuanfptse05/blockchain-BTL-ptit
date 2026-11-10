"""Unit tests for SimulationConfig validation and defaults.

# Implements FR-01, FR-02, FR-03, FR-04, FR-05
# Implements C-01, C-02, C-03, C-04, C-05, C-06, C-07, C-08, C-09, C-10
# Implements UT-01
"""

import pytest
from pydantic import ValidationError
from src.domain.config import SimulationConfig


def test_default_config_values():
    """Verify default values comply exactly with P-01 to P-06 and C-03 to C-05."""
    config = SimulationConfig()
    assert config.shock_pct == 15.0  # P-01
    assert config.pool_a_tvl_usd == 150_000_000.0  # P-02
    assert config.pool_b_tvl_usd == 80_000_000.0  # P-03
    assert config.num_borrowers == 100  # P-04
    assert config.max_blocks == 30  # P-05
    assert config.seed == 42  # P-06
    assert config.liquidation_threshold == 0.80  # C-03
    assert config.close_factor == 0.50  # C-04
    assert config.liquidation_penalty == 0.05  # C-05


def test_valid_custom_config():
    """Verify valid configurations within boundary limits."""
    config = SimulationConfig(
        shock_pct=25.5,
        liquidation_threshold=0.85,
        close_factor=0.60,
        liquidation_penalty=0.10,
        pool_a_tvl_usd=200_000_000.0,
        pool_b_tvl_usd=100_000_000.0,
        num_borrowers=250,
        max_blocks=50,
        seed=1337,
    )
    assert config.shock_pct == 25.5
    assert config.num_borrowers == 250
    assert config.seed == 1337


def test_valid_boundary_extremes():
    """Verify lowest and highest allowed values succeed."""
    # Minimum boundaries
    min_cfg = SimulationConfig(
        shock_pct=0.0,  # C-01
        liquidation_threshold=0.60,
        close_factor=0.10,
        liquidation_penalty=0.0,
        pool_a_tvl_usd=10_000_000.0,  # C-06
        pool_b_tvl_usd=5_000_000.0,  # C-08
        num_borrowers=10,  # C-10
        max_blocks=5,
        seed=0,
    )
    assert min_cfg.shock_pct == 0.0
    assert min_cfg.num_borrowers == 10

    # Maximum boundaries
    max_cfg = SimulationConfig(
        shock_pct=50.0,  # C-02
        liquidation_threshold=0.90,
        close_factor=1.00,
        liquidation_penalty=0.20,
        pool_a_tvl_usd=500_000_000.0,  # C-07
        pool_b_tvl_usd=200_000_000.0,  # C-09
        num_borrowers=500,
        max_blocks=100,
        seed=2_147_483_647,
    )
    assert max_cfg.shock_pct == 50.0
    assert max_cfg.num_borrowers == 500


@pytest.mark.parametrize(
    "invalid_kwargs",
    [
        {"shock_pct": -0.1},  # C-01: shock < 0
        {"shock_pct": 50.1},  # C-02: shock > 50
        {"liquidation_threshold": 0.59},  # LT < 0.60
        {"liquidation_threshold": 0.91},  # LT > 0.90
        {"close_factor": 0.09},  # close_factor < 0.10
        {"close_factor": 1.01},  # close_factor > 1.00
        {"liquidation_penalty": -0.01},  # penalty < 0.0
        {"liquidation_penalty": 0.21},  # penalty > 0.20
        {"pool_a_tvl_usd": 9_999_999.0},  # C-06: Pool A < $10M
        {"pool_a_tvl_usd": 500_000_001.0},  # C-07: Pool A > $500M
        {"pool_b_tvl_usd": 4_999_999.0},  # C-08: Pool B < $5M
        {"pool_b_tvl_usd": 200_000_001.0},  # C-09: Pool B > $200M
        {"num_borrowers": 9},  # C-10: Borrowers < 10
        {"num_borrowers": 501},  # Borrowers > 500
        {"max_blocks": 4},  # max_blocks < 5
        {"max_blocks": 101},  # max_blocks > 100
        {"seed": -1},  # seed < 0
    ],
)
def test_out_of_bound_constraints_raise_validation_error(invalid_kwargs):
    """Verify that any boundary violation raises ValidationError."""
    with pytest.raises(ValidationError):
        SimulationConfig(**invalid_kwargs)


def test_immutability():
    """Verify that instance is frozen and cannot be modified after instantiation."""
    config = SimulationConfig()
    with pytest.raises((ValidationError, TypeError)):
        config.shock_pct = 20.0

