# Tasks: Data Tables & CSV Exporter

**Feature**: `009-data-tables-csv-export`  
**Input**: [`specs/009-data-tables-csv-export/spec.md`](file:///d:/wd/c/sang/d/Documents/BTL-block-chain/specs/009-data-tables-csv-export/spec.md)  
**Plan**: [`specs/009-data-tables-csv-export/plan.md`](file:///d:/wd/c/sang/d/Documents/BTL-block-chain/specs/009-data-tables-csv-export/plan.md)  

## Task List

- [x] **T009-01** [US1] Cài đặt `block_results_to_dataframe` và `liquidation_events_to_dataframe` trong `src/infra/exporter.py`.
- [x] **T009-02** [US2] Viết unit test `tests/unit/test_exporter.py` kiểm tra xuất `block_results.csv` có đúng 12 cột chuẩn, đọc lại bằng `pd.read_csv()` khớp số dòng và kiểu dữ liệu (ST-08).
- [x] **T009-03** [US2] Viết unit test kiểm tra xuất `liquidation_events.csv` có đúng 10 cột chuẩn, đọc lại bằng `pd.read_csv()` thành công cả khi không có thanh lý nào.
- [x] **T009-04** Cài đặt `export_block_results_to_csv` và `export_liquidation_events_to_csv` trong `src/infra/exporter.py` với encoding `utf-8-sig`.
- [x] **T009-05** [US1] Cài đặt component `src/interface/components/data_tab.py` hiển thị 2 bảng dữ liệu tương tác và 2 nút tải CSV.
- [x] **T009-06** Chạy `pytest tests/unit/test_exporter.py` xác nhận 100% test pass.

