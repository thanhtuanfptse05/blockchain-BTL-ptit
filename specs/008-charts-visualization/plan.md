# Implementation Plan: Charts & Visualizations

**Feature**: `008-charts-visualization`  
**Date**: 2026-11-10  
**Spec**: [`specs/008-charts-visualization/spec.md`](file:///d:/wd/c/sang/d/Documents/BTL-block-chain/specs/008-charts-visualization/spec.md)  
**Status**: Ready for Implementation  

## 1. Summary

Xây dựng module `charts.py` tại `src/interface/components/` chứa 4 hàm khởi tạo `plotly.graph_objects.Figure` tương ứng với 4 biểu đồ bắt buộc tại SRS FR-08.

## 2. Technical Context

- **Target File**: `src/interface/components/charts.py`
- **Test File**: `tests/unit/test_charts.py`
- **Dependencies**: `plotly.graph_objects`, `pandas`, `src/domain/block_result.py`

## 3. Architecture & Interfaces

```python
import plotly.graph_objects as go
from typing import List
from src.domain.block_result import BlockResult

def create_eth_price_chart(
    sc01_blocks: List[BlockResult],
    sc02_blocks: List[BlockResult],
    sc03_blocks: List[BlockResult]
) -> go.Figure:
    """Tạo biểu đồ đường giá ETH của 3 kịch bản theo block."""
    pass

def create_steth_discount_chart(
    sc01_blocks: List[BlockResult],
    sc02_blocks: List[BlockResult],
    sc03_blocks: List[BlockResult]
) -> go.Figure:
    """Tạo biểu đồ biến động depeg discount của stETH."""
    pass

def create_liquidation_breakdown_chart(
    sc03_blocks: List[BlockResult]
) -> go.Figure:
    """Tạo biểu đồ cột thanh lý ETH vs stETH trong SC03."""
    pass

def create_cumulative_liquidated_agents_chart(
    sc02_blocks: List[BlockResult],
    sc03_blocks: List[BlockResult]
) -> go.Figure:
    """Tạo biểu đồ đường so sánh số lượng Borrower bị thanh lý lũy kế."""
    pass
```

## 4. Risks & Mitigations

- *Rủi ro*: Trục X hiển thị số thập phân (ví dụ: `1.5`, `2.5`) do auto-tick của Plotly.
- *Giải pháp*: Thiết lập tường minh `fig.update_xaxes(dtick=1, tick0=0)`.

