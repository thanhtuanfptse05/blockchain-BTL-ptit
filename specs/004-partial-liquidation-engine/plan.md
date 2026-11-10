# Implementation Plan: Partial Liquidation Engine

**Feature**: `004-partial-liquidation-engine`  
**Date**: 2026-11-10  
**Spec**: [`specs/004-partial-liquidation-engine/spec.md`](file:///d:/wd/c/sang/d/Documents/BTL-block-chain/specs/004-partial-liquidation-engine/spec.md)  
**Status**: Ready for Implementation  

## 1. Summary

Xây dựng schema `LiquidationEvent` tại `src/domain/liquidation_event.py` và usecase `liquidate_borrower_position` tại `src/usecase/liquidation_engine.py` để xử lý trả nợ 50%, tịch thu collateral kèm 5% penalty, cập nhật vị thế và ghi nhận nợ xấu.

## 2. Technical Context

- **Target Files**:
  - `src/domain/liquidation_event.py` (Schema sự kiện 10 trường theo SRS §7.3)
  - `src/usecase/liquidation_engine.py` (Engine thực thi)
- **Test File**: `tests/unit/test_liquidation_engine.py`
- **Dependencies**: `src/domain/agent.py`, `src/domain/config.py`

## 3. Architecture & Interfaces

```python
from dataclasses import dataclass
from typing import Tuple
from src.domain.agent import BorrowerAgent, AssetType
from src.domain.config import SimulationConfig

@dataclass(frozen=True)
class LiquidationEvent:
    scenario: str
    block: int
    agent_id: int
    asset: str
    hf_before: float
    debt_repaid_usd: float
    collateral_seized: float
    collateral_value_at_oracle_usd: float
    remaining_debt_usd: float
    remaining_collateral: float

def liquidate_borrower_position(
    agent: BorrowerAgent,
    scenario: str,
    block: int,
    eth_price_usd: float,
    steth_per_eth_price: float,
    config: SimulationConfig
) -> Tuple[LiquidationEvent, float]:
    """Thực thi thanh lý vị thế và trả về (LiquidationEvent, bad_debt_phát_sinh)."""
    pass
```

## 4. Risks & Mitigations

- *Rủi ro*: Agent còn quá ít collateral không đủ trả phần phạt 5%.
- *Giải pháp*: `collateral_seized = min(agent.collateral_amount, seized_ideal)` và ghi nhận nợ còn lại là nợ xấu.

