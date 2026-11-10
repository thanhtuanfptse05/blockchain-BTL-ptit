"""Unit tests for AMM Constant Product Pools and MarketState.

# Implements FR-001, FR-002, FR-003, FR-004, FR-005, FR-006, FR-007, FR-008, FR-009, FR-010, FR-011, FR-012, FR-013
# Implements BR-05, BR-06, BR-07, BR-09
# Implements UT-09, UT-12, UT-13
"""

import math
import pytest
from src.domain.config import SimulationConfig
from src.domain.amm_pool import AMMPool
from src.usecase.amm_engine import (
    initialize_pools,
    swap_exact_input,
    apply_exogenous_shock,
    get_market_prices,
)


def test_pool_initialization_defaults(default_config: SimulationConfig):
    """Verify default initialization: ETH = $3000, stETH/ETH = 0.99, discount = 1.0% (UT-09)."""
    pool_a, pool_b = initialize_pools(default_config)

    # 1. Pool A: ETH/USDC ($150M TVL)
    assert pool_a.name == "ETH_USDC"
    assert pool_a.token_x == "ETH"
    assert pool_a.token_y == "USDC"
    assert pool_a.reserve_x == pytest.approx(25_000.0, rel=1e-6)
    assert pool_a.reserve_y == pytest.approx(75_000_000.0, rel=1e-6)
    assert pool_a.spot_price == pytest.approx(3000.0, rel=1e-6)
    assert pool_a.k == pytest.approx(1.875e12, rel=1e-6)

    # 2. Pool B: stETH/ETH ($80M TVL)
    assert pool_b.name == "STETH_ETH"
    assert pool_b.token_x == "stETH"
    assert pool_b.token_y == "ETH"
    assert pool_b.reserve_y == pytest.approx(13_333.3333, rel=1e-4)
    assert pool_b.reserve_x == pytest.approx(13_468.0135, rel=1e-4)
    assert pool_b.spot_price == pytest.approx(0.99, rel=1e-6)

    # 3. Market prices derivation (BR-09)
    prices = get_market_prices(pool_a, pool_b)
    assert prices["eth_price_usd"] == pytest.approx(3000.0, rel=1e-6)
    assert prices["steth_eth_ratio"] == pytest.approx(0.99, rel=1e-6)
    assert prices["steth_price_usd"] == pytest.approx(2970.0, rel=1e-6)
    assert prices["steth_discount_pct"] == pytest.approx(1.0, rel=1e-6)


def test_swap_zero_fee_math_invariance():
    """Verify zero-fee constant product swap preserves k = x * y (UT-06, UT-09).

    Initial: x = 100, y = 10,000, k = 1,000,000.
    Sell dx = 10:
    dy = 10,000 * 10 / 110 = 909.090909...
    new_x = 110, new_y = 9090.909091...
    k_after = 110 * 9090.909091 = 1,000,000.
    """
    pool = AMMPool("TEST", "TOKEN_X", "TOKEN_Y", 100.0, 10_000.0)
    initial_k = pool.k

    amount_out = swap_exact_input(pool, delta_x=10.0)
    assert amount_out == pytest.approx(909.090909, rel=1e-6)
    assert pool.reserve_x == pytest.approx(110.0, rel=1e-6)
    assert pool.reserve_y == pytest.approx(9090.909091, rel=1e-6)
    assert pool.k == pytest.approx(initial_k, rel=1e-9)


def test_sell_eth_into_pool_a_causes_price_drop(default_config: SimulationConfig):
    """Verify selling ETH into Pool A depresses ETH price (UT-07)."""
    pool_a, _ = initialize_pools(default_config)
    price_before = pool_a.spot_price

    # Sell 72.0588 ETH into Pool A
    usdc_received = swap_exact_input(pool_a, delta_x=72.0588)
    assert usdc_received > 0
    assert pool_a.spot_price < price_before


def test_sell_steth_into_pool_b_causes_depeg(default_config: SimulationConfig):
    """Verify selling stETH into Pool B increases discount (UT-08)."""
    pool_a, pool_b = initialize_pools(default_config)
    prices_before = get_market_prices(pool_a, pool_b)

    # Dump 100 stETH into Pool B
    eth_received = swap_exact_input(pool_b, delta_x=100.0)
    assert eth_received > 0

    prices_after = get_market_prices(pool_a, pool_b)
    assert prices_after["steth_eth_ratio"] < prices_before["steth_eth_ratio"]
    assert prices_after["steth_discount_pct"] > prices_before["steth_discount_pct"]


def test_exogenous_shock_preserves_k_and_leaves_pool_b_unchanged(default_config: SimulationConfig):
    """Verify 15% shock on Pool A preserves k_A, sets price to 2550, leaves Pool B untouched (UT-10, UT-12, UT-13)."""
    pool_a, pool_b = initialize_pools(default_config)
    k_a_before = pool_a.k
    res_b_x_before = pool_b.reserve_x
    res_b_y_before = pool_b.reserve_y

    # Apply 15% shock
    apply_exogenous_shock(pool_a, shock_pct=15.0)

    # 1. Pool A post-shock verification
    assert pool_a.spot_price == pytest.approx(2550.0, rel=1e-6)
    assert pool_a.k == pytest.approx(k_a_before, rel=1e-9)

    expected_eth = math.sqrt(k_a_before / 2550.0)
    expected_usdc = math.sqrt(k_a_before * 2550.0)
    assert pool_a.reserve_x == pytest.approx(expected_eth, rel=1e-6)
    assert pool_a.reserve_y == pytest.approx(expected_usdc, rel=1e-6)
    assert pool_a.reserve_x == pytest.approx(27_116.3072, rel=1e-4)
    assert pool_a.reserve_y == pytest.approx(69_146_583.43, rel=1e-4)

    # 2. Pool B post-shock verification (must be unchanged)
    assert pool_b.reserve_x == res_b_x_before
    assert pool_b.reserve_y == res_b_y_before

    # 3. Market prices post-shock
    prices = get_market_prices(pool_a, pool_b)
    assert prices["eth_price_usd"] == pytest.approx(2550.0, rel=1e-6)
    assert prices["steth_price_usd"] == pytest.approx(2550.0 * 0.99, rel=1e-6)
    assert prices["steth_discount_pct"] == pytest.approx(1.0, rel=1e-6)


def test_invalid_swap_delta_raises_error():
    """Verify non-positive swap inputs raise ValueError (FR-005)."""
    pool = AMMPool("TEST", "X", "Y", 100.0, 100.0)
    with pytest.raises(ValueError):
        swap_exact_input(pool, delta_x=0.0)

    with pytest.raises(ValueError):
        swap_exact_input(pool, delta_x=-5.0)

