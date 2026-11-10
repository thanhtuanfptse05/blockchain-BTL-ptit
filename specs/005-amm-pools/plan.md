# Implementation Plan: AMM Constant Product Pools

**Feature**: `005-amm-pools`  
**Date**: 2026-11-10  
**Spec**: [`specs/005-amm-pools/spec.md`](file:///d:/wd/c/sang/d/Documents/BTL-block-chain/specs/005-amm-pools/spec.md)  
**Status**: Ready for Implementation  

## 1. Summary

Xây dựng thực thể `AMMPool` tại `src/domain/amm_pool.py` và module `amm_engine.py` tại `src/usecase/` để quản trị 2 pool thanh khoản (Pool A và Pool B), tính toán trượt giá theo công thức swap zero-fee, tái cân bằng cú sốc ngoại sinh và xác định tỉ lệ depeg stETH.

## 2. Technical Context

- **Target Files**:
  - `src/domain/amm_pool.py` (Entity `AMMPool`)
  - `src/usecase/amm_engine.py` (Logic swap và shock)
- **Test File**: `tests/unit/test_amm_engine.py`
- **Dependencies**: `math`, `src/domain/config.py`

## 3. Architecture & Interfaces

```python
from dataclasses import dataclass
import math

@dataclass
class AMMPool:
    name: str
    reserve_x: float  # Base asset (ETH in Pool A, stETH in Pool B)
    reserve_y: float  # Quote asset (USDC in Pool A, ETH in Pool B)
    
    @property
    def k(self) -> float:
        return self.reserve_x * self.reserve_y
        
    @property
    def spot_price(self) -> float:
        return self.reserve_y / self.reserve_x

def swap_exact_input(pool: AMMPool, delta_x: float) -> float:
    """Thực hiện swap delta_x vào pool, nhận về delta_y, cập nhật reserves."""
    pass

def apply_exogenous_shock(pool_a: AMMPool, shock_pct: float) -> None:
    """Tái cân bằng reserves Pool A tại block 1 theo giá mới, bảo toàn k_A."""
    pass

def calculate_steth_discount(pool_b: AMMPool) -> float:
    """Tính tỉ lệ discount stETH: (1.0 - spot_price_B) * 100.0."""
    pass
```

## 4. Risks & Mitigations

- *Rủi ro*: Lượng bán $\Delta x$ quá lớn làm cạn kiệt reserve $y$.
- *Giải pháp*: Trong công thức $\Delta y = \frac{y \cdot \Delta x}{x + \Delta x}$, khi $\Delta x \to \infty$ thì $\Delta y \to y$, $y_{new} = \frac{x \cdot y}{x + \Delta x} > 0$ luôn dương nghiêm ngặt, không bao giờ $\le 0$.

