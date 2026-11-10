# Tasks: Analytics & Summary KPIs

**Feature**: `007-analytics-kpi-summary`  
**Input**: [`specs/007-analytics-kpi-summary/spec.md`](file:///d:/wd/c/sang/d/Documents/BTL-block-chain/specs/007-analytics-kpi-summary/spec.md)  
**Plan**: [`specs/007-analytics-kpi-summary/plan.md`](file:///d:/wd/c/sang/d/Documents/BTL-block-chain/specs/007-analytics-kpi-summary/plan.md)  

## Task List

- [x] **T007-01** [US1] Viết unit test `tests/unit/test_metrics.py` kiểm tra trích xuất 6 KPI từ kết quả mô phỏng SC03 (khớp với dòng cuối `BlockResult` và đếm duy nhất từ `LiquidationEvent`).
- [x] **T007-02** [US2] Viết unit test kiểm tra tính bảng delta so sánh SC03 vs SC02: các hiệu số $\Delta$ và tỉ lệ tăng tương đối.
- [x] **T007-03** [US2] Viết unit test kiểm tra trường hợp biên chia cho 0: khi `unique_SC02 == 0`, hàm trả về `"N/A"` thay vì văng exception `ZeroDivisionError`.
- [x] **T007-04** Cài đặt `calculate_kpi_summary` và `generate_comparison_table` trong `src/interface/components/metrics.py`.
- [x] **T007-05** Chạy `pytest tests/unit/test_metrics.py` xác nhận 100% test pass.

