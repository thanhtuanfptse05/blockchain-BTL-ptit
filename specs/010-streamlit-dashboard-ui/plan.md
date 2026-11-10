# Implementation Plan: Streamlit Dashboard UI & Methodology

**Feature**: `010-streamlit-dashboard-ui`  
**Date**: 2026-11-10  
**Spec**: [`specs/010-streamlit-dashboard-ui/spec.md`](file:///d:/wd/c/sang/d/Documents/BTL-block-chain/specs/010-streamlit-dashboard-ui/spec.md)  
**Status**: Ready for Implementation  

## 1. Summary

Xây dựng ứng dụng Streamlit hoàn chỉnh tại `src/interface/app.py` kết nối các components: `sidebar.py`, `metrics.py`, `charts.py`, `data_tab.py`, và `methodology_tab.py`, tuân thủ thiết kế phân lớp, không để rò rỉ logic nghiệp vụ vào tầng giao diện.

## 2. Technical Context

- **Target Files**:
  - `src/interface/app.py` (Main Streamlit Entrypoint)
  - `src/interface/components/sidebar.py`
  - `src/interface/components/methodology_tab.py`
- **Dependencies**: `streamlit >= 1.30.0`, `src/usecase/scenario_runner.py`

## 3. Architecture & Interfaces

```text
src/interface/
├── app.py                      # Main App: Header, Disclaimer, Session State, Tabs router
└── components/
    ├── sidebar.py              # Sliders, Run & Reset buttons
    ├── metrics.py              # 6 KPI cards & delta comparison table
    ├── charts.py               # 4 Plotly charts
    ├── data_tab.py             # Dataframes & CSV download buttons
    └── methodology_tab.py      # Diagram, KaTeX formulas, limitations
```

## 4. Risks & Mitigations

- *Rủi ro*: Kích thước file `app.py` phình to quá 300 dòng code vi phạm Definition of Done.
- *Giải pháp*: Phân tách triệt để các tab và sidebar thành các component riêng biệt trong thư mục `src/interface/components/`, mỗi component $\le 150$ dòng code.

