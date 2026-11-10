# Research & Technical Decisions: Simulation Config & Validation

**Feature**: `001-simulation-config`  
**Date**: 2026-11-10  
**Status**: Completed  

## 1. Technical Context & Alternatives

- **Pydantic v2 vs Standard Dataclasses**:
  - *Option A*: Pure Python `@dataclass(frozen=True)` với hàm `validate()` thủ công.
  - *Option B*: `pydantic.BaseModel` v2 với `Field(ge=..., le=...)` và model validators.
  - *Decision*: Sử dụng `pydantic.BaseModel` với `frozen=True` (hoặc `@dataclass` có custom validation hook). Pydantic v2 thực thi kiểm tra kiểu dữ liệu tốc độ C (pydantic-core) và sinh lỗi `ValidationError` có cấu trúc rõ ràng cho UI Streamlit hiển thị.

## 2. Validation Constraints Research (SRS §5.1, C-01..C-10)

| Parameter | Type | Default | Min (C-XX) | Max (C-XX) | Rationale |
|---|---|---|---|---|---|
| `shock_pct` | `float` | 15.0 | 0.0 (C-01) | 50.0 (C-02) | 0% là baseline test; >50% thanh lý ồ ạt làm kiệt quệ pool |
| `liquidation_threshold` | `float` | 0.80 | 0.60 | 0.90 | C-03: Thống nhất cho cả ETH và stETH |
| `close_factor` | `float` | 0.50 | 0.10 | 1.00 | C-04: Tỉ lệ nợ tối đa được trả mỗi lần thanh lý |
| `liquidation_penalty` | `float` | 0.05 | 0.00 | 0.20 | C-05: Thưởng thanh lý 5% |
| `pool_a_tvl_usd` | `float` | 150,000,000 | 10,000,000 (C-06) | 500,000,000 (C-07) | Pool ETH/USDC |
| `pool_b_tvl_usd` | `float` | 80,000,000 | 5,000,000 (C-08) | 200,000,000 (C-09) | Pool stETH/ETH |
| `num_borrowers` | `int` | 100 | 10 (C-10) | 500 | Số lượng vị thế vay giả lập |
| `max_blocks` | `int` | 30 | 5 | 100 | Số bước thời gian mô phỏng |
| `seed` | `int` | 42 | 0 | $2^{31}-1$ | Khóa tái lập kết quả ngẫu nhiên |

