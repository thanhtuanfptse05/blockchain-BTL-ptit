# Implementation Plan: Data Tables & CSV Exporter

**Feature**: `009-data-tables-csv-export`  
**Date**: 2026-11-10  
**Spec**: [`specs/009-data-tables-csv-export/spec.md`](file:///d:/wd/c/sang/d/Documents/BTL-block-chain/specs/009-data-tables-csv-export/spec.md)  
**Status**: Ready for Implementation  

## 1. Summary

Xây dựng module hạ tầng `src/infra/exporter.py` để trích xuất dữ liệu mô phỏng thành các file CSV chuẩn hóa và module giao diện `src/interface/components/data_tab.py` hiển thị 2 bảng tương tác và nút download.

## 2. Technical Context

- **Target Files**:
  - `src/infra/exporter.py` (Chuyển đổi dữ liệu và xuất CSV)
  - `src/interface/components/data_tab.py` (Giao diện hiển thị bảng và nút tải)
- **Test File**: `tests/unit/test_exporter.py`
- **Dependencies**: `pandas`, `io`, `src/domain/block_result.py`, `src/domain/liquidation_event.py`

## 3. Architecture & Interfaces

```python
import io
import pandas as pd
from typing import Dict, Any
from src.domain.simulation_result import SimulationResult

def block_results_to_dataframe(results: Dict[str, SimulationResult]) -> pd.DataFrame:
    """Gộp BlockResult của cả 3 kịch bản thành 1 DataFrame duy nhất."""
    pass

def liquidation_events_to_dataframe(results: Dict[str, SimulationResult]) -> pd.DataFrame:
    """Gộp toàn bộ LiquidationEvent thành 1 DataFrame duy nhất."""
    pass

def export_block_results_to_csv(results: Dict[str, SimulationResult]) -> str:
    """Xuất Block Results thành chuỗi CSV định dạng UTF-8."""
    pass

def export_liquidation_events_to_csv(results: Dict[str, SimulationResult]) -> str:
    """Xuất Liquidation Events thành chuỗi CSV định dạng UTF-8."""
    pass
```

## 4. Risks & Mitigations

- *Rủi ro*: Người dùng bấm tải CSV khi chưa bấm Run Simulation làm sinh file rỗng.
- *Giải pháp*: Khóa nút download (`disabled=True` hoặc ẩn hoàn toàn) khi session state chưa có dữ liệu.

