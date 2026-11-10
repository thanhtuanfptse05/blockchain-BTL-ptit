# Research & Technical Decisions: Charts & Visualizations

**Feature**: `008-charts-visualization`  
**Date**: 2026-11-10  
**Status**: Completed  

## 1. Technical Context & Charting Framework Research

- **Plotly vs Matplotlib**:
  - *Matplotlib*: Tĩnh, khó tương tác trực tiếp trên trình duyệt, tạo ảnh bitmap/svg.
  - *Plotly Graph Objects (`plotly.graph_objects`)*: Tương tác động, hỗ trợ rê chuột xem tooltip chính xác từng điểm dữ liệu, zoom/pan mượt mà, tích hợp native với Streamlit qua `st.plotly_chart(fig, use_container_width=True)`.
  - *Decision*: Sử dụng `plotly.graph_objects` làm công nghệ trực quan hóa chính.

## 2. 4 Mandatory Charts Specifications (SRS §11 FR-08)

1. **ETH Price vs Block**:
   - 3 đường: SC01 (Xanh lá - Baseline), SC02 (Cam - Direct Shock), SC03 (Đỏ - Contagion Cascade).
   - Vạch kẻ đứng ngắt nét (dashed gray line) tại block 1 kèm chú thích `"Shock giá (-15%)"`.
   - Trục X: Block index (0..max_blocks, bước nhảy số nguyên).
   - Trục Y: ETH Price in USD ($).
2. **stETH Discount vs Block**:
   - Biểu thị mức độ mất peg qua từng block cho cả 3 kịch bản.
   - Trục Y: stETH Discount (%) = $(1 - P_{stETH\_per\_ETH}) \times 100\%$.
   - Vạch chú thích shock tại block 1.
3. **Liquidations per Block in SC03**:
   - Bar chart cột nhóm/chồng phân tách theo tài sản: `liquidations_eth` và `liquidations_steth`.
   - Trục Y: Số sự kiện thanh lý (Events $\ge 0$).
4. **Cumulative Unique Liquidated Agents (SC02 vs SC03)**:
   - Line chart so sánh số người vay duy nhất rơi vào cảnh thanh lý lũy kế giữa SC02 và SC03.
   - Trục Y: Số lượng Agent duy nhất.

