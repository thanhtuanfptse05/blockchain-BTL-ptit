# Implementation Plan: Health Factor & Collateral Valuation

**Feature**: `003-health-factor-eligibility`  
**Date**: 2026-11-10  
**Spec**: [`specs/003-health-factor-eligibility/spec.md`](file:///d:/wd/c/sang/d/Documents/BTL-block-chain/specs/003-health-factor-eligibility/spec.md)  
**Status**: Ready for Implementation  

## 1. Summary

Xây dựng module nghiệp vụ tính toán giá trị tài sản thế chấp, tỷ lệ LTV, chỉ số an toàn Health Factor (HF) và xác định điều kiện kích hoạt thanh lý (`is_liquidatable`) tại `src/usecase/health_factor.py`.

## 2. Technical Context

- **Target File**: `src/usecase/health_factor.py`
- **Test File**: `tests/unit/test_health_factor.py`
- **Dependencies**: `math`, `src/domain/agent.py`, `src/domain/amm_pool.py`

## 3. Architecture & Interfaces

```python
import math
from src.domain.agent import BorrowerAgent, AssetType

EPSILON = 1e-9

def compute_collateral_value(
    agent: BorrowerAgent, 
    eth_price_usd: float, 
    steth_per_eth_price: float
) -> float:
    """Tính giá trị USD của tài sản thế chấp theo giá spot hiện thời."""
    pass

def compute_health_factor(
    collateral_value_usd: float, 
    debt_usdc: float, 
    liquidation_threshold: float = 0.80
) -> float:
    """Tính Health Factor với xử lý an toàn nợ <= epsilon và nợ xấu."""
    pass

def is_liquidatable(
    agent: BorrowerAgent, 
    eth_price_usd: float, 
    steth_per_eth_price: float, 
    liquidation_threshold: float = 0.80
) -> bool:
    """Kiểm tra vị thế có thỏa mãn điều kiện thanh lý (HF < 1 và còn tài sản + nợ)."""
    pass
```

## 4. Risks & Mitigations

- *Rủi ro*: Sai số dấu phẩy động (floating point inaccuracy) dẫn đến $HF = 0.99999999999$ kích hoạt thanh lý nhầm.
- *Giải pháp*: Áp dụng hằng số ngưỡng sai số `EPSILON = 1e-9` trong các phép so sánh với 0.

