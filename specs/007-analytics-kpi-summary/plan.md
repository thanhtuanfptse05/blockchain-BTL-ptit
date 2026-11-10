# Implementation Plan: Analytics & Summary KPIs

**Feature**: `007-analytics-kpi-summary`  
**Date**: 2026-11-10  
**Spec**: [`specs/007-analytics-kpi-summary/spec.md`](file:///d:/wd/c/sang/d/Documents/BTL-block-chain/specs/007-analytics-kpi-summary/spec.md)  
**Status**: Ready for Implementation  

## 1. Summary

Xây dựng module `metrics.py` tại `src/interface/components/` để tổng hợp 6 thẻ KPI cho kịch bản SC03, tính toán bảng đối chiếu so sánh $\Delta(SC03 - SC02)$, định dạng tiền tệ và phần trăm, phòng vệ an toàn phép chia cho 0.

## 2. Technical Context

- **Target File**: `src/interface/components/metrics.py`
- **Test File**: `tests/unit/test_metrics.py`
- **Dependencies**: `src/domain/simulation_result.py`

## 3. Architecture & Interfaces

```python
from dataclasses import dataclass
from typing import Dict, Any, Optional
from src.domain.simulation_result import KPISummary, SimulationResult

def calculate_kpi_summary(sim_result: SimulationResult, total_agents: int) -> KPISummary:
    """Trích xuất và tính toán đầy đủ 6 chỉ số KPI cốt lõi."""
    pass

def generate_comparison_table(
    sc01: SimulationResult,
    sc02: SimulationResult,
    sc03: SimulationResult
) -> Dict[str, Any]:
    """Sinh bảng dữ liệu so sánh 3 kịch bản kèm cột delta và relative increase."""
    pass
```

## 4. Risks & Mitigations

- *Rủi ro*: SC02 không có thanh lý nào dẫn đến crash chia cho 0.
- *Giải pháp*: Cài đặt guard condition tường minh: `if unique_sc02 == 0: return "N/A"`.

