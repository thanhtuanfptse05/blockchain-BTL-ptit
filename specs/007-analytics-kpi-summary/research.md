# Research & Technical Decisions: Analytics & Summary KPIs

**Feature**: `007-analytics-kpi-summary`  
**Date**: 2026-11-10  
**Status**: Completed  

## 1. Technical Context & Formulas (FR-07, FR-11)

- **6 Chỉ số KPI cốt lõi của SC03**:
  1. `final_eth_price_usd`: Giá ETH tại block cuối cùng của SC03.
  2. `final_steth_price_usd`: Giá stETH tại block cuối cùng của SC03.
  3. `final_steth_discount_pct`: Tỉ lệ depeg discount tại block cuối cùng của SC03.
  4. `liquidated_agents_unique`: Số lượng `agent_id` duy nhất đã từng bị thanh lý ít nhất 1 lần trong SC03 (và tỉ lệ $\%$ trên tổng số người vay).
  5. `liquidation_events_total`: Tổng số sự kiện thanh lý diễn ra trong SC03.
  6. `bad_debt_usd`: Tổng nợ xấu tích lũy của giao thức ở block cuối cùng.

## 2. Delta Comparison & Div-by-Zero Protection Research

- **Bảng đối chiếu $\Delta(SC03 - SC02)$ (FR-11)**:
  - $\Delta \text{ETH} = P_{ETH\_SC03} - P_{ETH\_SC02}$.
  - $\Delta \text{stETH} = P_{stETH\_SC03} - P_{stETH\_SC02}$.
  - $\Delta \text{Discount} = \text{Discount}_{SC03} - \text{Discount}_{SC02}$.
  - `additional_liquidated_agents` $= \text{Unique}_{SC03} - \text{Unique}_{SC02}$.
- **Tỉ lệ tăng tương đối (`relative_increase_pct`)**:
  - Nếu $\text{Unique}_{SC02} > 0$:
    $$\text{relative\_increase\_pct} = \frac{\text{Unique}_{SC03} - \text{Unique}_{SC02}}{\text{Unique}_{SC02}} \times 100\%$$
  - Nếu $\text{Unique}_{SC02} == 0$:
    - Nếu $\text{Unique}_{SC03} > 0 \implies$ Trả về chuỗi `"N/A"` (hoặc `None`), ngăn ngừa hoàn toàn lỗi `ZeroDivisionError`.
    - Nếu cả hai bằng $0 \implies$ Trả về `"0.0%"`.

