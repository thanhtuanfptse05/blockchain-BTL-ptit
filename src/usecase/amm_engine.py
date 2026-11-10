"""AMM pool management, swap execution, and price discovery usecases.

# Implements FR-001, FR-002, FR-003, FR-004, FR-005, FR-006, FR-007, FR-008, FR-009, FR-010, FR-011, FR-012, FR-013
# Implements BR-05, BR-06, BR-07, BR-09
# Implements UT-09, UT-12, UT-13
"""

import math
from typing import Tuple, Dict
from src.domain.config import SimulationConfig
from src.domain.amm_pool import AMMPool


INITIAL_ETH_PRICE: float = 3000.0
INITIAL_STETH_DISCOUNT_RATIO: float = 0.99  # 1% initial discount (stETH/ETH = 0.99)


def initialize_pools(config: SimulationConfig) -> Tuple[AMMPool, AMMPool]:
    """Initialize Pool A (ETH/USDC) and Pool B (stETH/ETH) based on TVL config.

    # Implements BR-06, FR-001

    Pool A TVL is split 50/50 between ETH and USDC at $3,000/ETH.
    Pool B TVL is split 50/50 in USD value between stETH ($2,970) and ETH ($3,000).

    Args:
        config: SimulationConfig containing pool_a_tvl_usd and pool_b_tvl_usd.

    Returns:
        Tuple of (pool_a, pool_b).
    """
    # 1. Pool A: ETH/USDC
    # reserve_y = USDC, reserve_x = ETH
    pool_a_half_tvl = config.pool_a_tvl_usd / 2.0
    reserve_a_usdc = pool_a_half_tvl
    reserve_a_eth = pool_a_half_tvl / INITIAL_ETH_PRICE

    pool_a = AMMPool(
        name="ETH_USDC",
        token_x="ETH",
        token_y="USDC",
        reserve_x=reserve_a_eth,
        reserve_y=reserve_a_usdc,
    )

    # 2. Pool B: stETH/ETH
    # reserve_y = ETH, reserve_x = stETH
    pool_b_half_tvl = config.pool_b_tvl_usd / 2.0
    reserve_b_eth = pool_b_half_tvl / INITIAL_ETH_PRICE
    initial_steth_usd = INITIAL_ETH_PRICE * INITIAL_STETH_DISCOUNT_RATIO  # $2,970
    reserve_b_steth = pool_b_half_tvl / initial_steth_usd

    pool_b = AMMPool(
        name="STETH_ETH",
        token_x="stETH",
        token_y="ETH",
        reserve_x=reserve_b_steth,
        reserve_y=reserve_b_eth,
    )

    return pool_a, pool_b


def swap_exact_input(pool: AMMPool, delta_x: float) -> float:
    """Execute a zero-fee swap depositing delta_x and returning received delta_y.

    # Implements BR-05, FR-004

    Args:
        pool: AMMPool instance to execute swap on.
        delta_x: Positive quantity of token x to sell.

    Returns:
        Quantity of token y received.
    """
    return pool.sell_x(delta_x)


def apply_exogenous_shock(pool_a: AMMPool, shock_pct: float) -> None:
    """Apply exogenous price shock to Pool A at block 1 preserving invariant k_A.

    # Implements BR-07, FR-009

    Rebalances Pool A reserves such that spot price drops to P * (1 - shock_pct/100)
    while k_A = reserve_x * reserve_y remains strictly invariant. Pool B is unaffected.

    Args:
        pool_a: Pool A (ETH/USDC) instance.
        shock_pct: Percentage price drop (e.g., 15.0).
    """
    if shock_pct <= 0.0:
        return

    p_after = INITIAL_ETH_PRICE * (1.0 - shock_pct / 100.0)
    k_a = pool_a.k

    new_reserve_eth = math.sqrt(k_a / p_after)
    new_reserve_usdc = math.sqrt(k_a * p_after)

    pool_a.reserve_x = new_reserve_eth
    pool_a.reserve_y = new_reserve_usdc


def get_market_prices(pool_a: AMMPool, pool_b: AMMPool) -> Dict[str, float]:
    """Derive current market prices and stETH discount from pool reserves.

    # Implements BR-09, FR-008

    Returns:
        Dict with keys:
            - eth_price_usd: Spot price of ETH in USD.
            - steth_eth_ratio: Price of stETH denominated in ETH.
            - steth_price_usd: Cross spot price of stETH in USD.
            - steth_discount_pct: stETH discount percentage (not truncated at 0).
    """
    eth_price_usd = pool_a.spot_price
    steth_eth_ratio = pool_b.spot_price
    steth_price_usd = eth_price_usd * steth_eth_ratio
    steth_discount_pct = (1.0 - steth_eth_ratio) * 100.0

    return {
        "eth_price_usd": eth_price_usd,
        "steth_eth_ratio": steth_eth_ratio,
        "steth_price_usd": steth_price_usd,
        "steth_discount_pct": steth_discount_pct,
    }

