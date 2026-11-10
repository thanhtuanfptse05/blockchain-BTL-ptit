# Tasks: Charts & Visualizations

**Feature**: `008-charts-visualization`  
**Input**: [`specs/008-charts-visualization/spec.md`](file:///d:/wd/c/sang/d/Documents/BTL-block-chain/specs/008-charts-visualization/spec.md)  
**Plan**: [`specs/008-charts-visualization/plan.md`](file:///d:/wd/c/sang/d/Documents/BTL-block-chain/specs/008-charts-visualization/plan.md)  

## Task List

- [x] **T008-01** [US1] Viết unit test `tests/unit/test_charts.py` kiểm tra `create_eth_price_chart`: trả về `go.Figure`, có đúng 3 traces, có vạch vertical line hoặc annotation tại x=1.
- [x] **T008-02** [US2] Viết unit test kiểm tra `create_steth_discount_chart`: trục Y có đơn vị %, vạch shock tại x=1.
- [x] **T008-03** [US3] Viết unit test kiểm tra `create_liquidation_breakdown_chart`: trả về Bar chart, 2 traces (ETH vs stETH), giá trị $\ge 0$.
- [x] **T008-04** [US4] Viết unit test kiểm tra `create_cumulative_liquidated_agents_chart`: 2 traces (SC02 vs SC03), dạng đường bậc thang hoặc line, giá trị $\ge 0$.
- [x] **T008-05** Cài đặt 4 hàm tạo biểu đồ trong `src/interface/components/charts.py`.
- [x] **T008-06** Chạy `pytest tests/unit/test_charts.py` xác nhận 100% test pass.
- [x] **T008-07** [US3, SC-04, SC-05] Tái thiết kế biểu đồ cột thanh lý: gỡ bỏ `dtick=1` trên trục Y, thay màu sắc sang Slate Blue (`#2563EB`) và Amber Gold (`#F59E0B`), thêm viền bar tinh tế.
- [x] **T008-08** [US1, US2, SC-03, SC-04] Tối ưu hóa trục X toàn bộ biểu đồ: set `tickangle=0`, `nticks=10`, `tickformat="d"` để chữ số hiển thị nằm ngang, không đè lấn nhau. Đưa vạch chú thích shock B1 xuống vị trí `bottom right` với pill badge nền để không đè lên đường cong và legend.
- [x] **T008-09** Re-build WebAssembly `index.html`, chạy toàn bộ test Pytest, và đẩy code lên GitHub.

