# Implementation Plan: Simulation Config & Validation

**Feature**: `001-simulation-config`  
**Date**: 2026-11-10  
**Spec**: [`specs/001-simulation-config/spec.md`](file:///d:/wd/c/sang/d/Documents/BTL-block-chain/specs/001-simulation-config/spec.md)  
**Status**: Ready for Implementation  

## 1. Summary

Xây dựng schema dữ liệu cấu hình bất biến `SimulationConfig` tại `src/domain/config.py` để đóng gói toàn bộ tham số thí nghiệm, kiểm tra nghiêm ngặt 10 ràng buộc C-01..C-10 và cung cấp thông báo lỗi chi tiết khi người dùng nhập sai tham số.

## 2. Technical Context

- **Target File**: `src/domain/config.py`
- **Test File**: `tests/unit/test_config.py`
- **Dependencies**: `pydantic >= 2.0` hoặc `dataclasses`
- **Design Pattern**: Value Object (Immutable, Type-Safe)

## 3. Architecture & Interfaces

```python
from pydantic import BaseModel, Field, field_validator

class SimulationConfig(BaseModel):
    model_config = {"frozen": True}
    
    shock_pct: float = Field(default=15.0, ge=0.0, le=50.0)
    liquidation_threshold: float = Field(default=0.80, ge=0.60, le=0.90)
    close_factor: float = Field(default=0.50, ge=0.10, le=1.00)
    liquidation_penalty: float = Field(default=0.05, ge=0.00, le=0.20)
    pool_a_tvl_usd: float = Field(default=150_000_000.0, ge=10_000_000.0, le=500_000_000.0)
    pool_b_tvl_usd: float = Field(default=80_000_000.0, ge=5_000_000.0, le=200_000_000.0)
    num_borrowers: int = Field(default=100, ge=10, le=500)
    max_blocks: int = Field(default=30, ge=5, le=100)
    seed: int = Field(default=42, ge=0)
```

## 4. Risks & Mitigations

- *Rủi ro*: Kiểu dữ liệu nhập từ giao diện Streamlit truyền sang dạng chuỗi hoặc số thực không chuẩn.
- *Giải pháp*: Pydantic validator tự động ép kiểu và ném ngoại lệ rõ ràng nếu không thể chuyển đổi.

