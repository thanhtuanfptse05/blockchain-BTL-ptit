# Master Tasks List: DeFi Liquidation Cascade Simulator

**Project**: DeFi Liquidation Cascade Simulator  
**Standard**: GitHub Spec Kit / Spec-Driven Development (SDD) Playbook  
**Date**: 2026-11-10  
**Status**: Ready for Implementation Gate Approval  
**Related Specs**: [`specs/001-simulation-config/`](file:///d:/wd/c/sang/d/Documents/BTL-block-chain/specs/001-simulation-config/spec.md) through [`specs/010-streamlit-dashboard-ui/`](file:///d:/wd/c/sang/d/Documents/BTL-block-chain/specs/010-streamlit-dashboard-ui/spec.md)  
**Implementation Plan**: [`specs/MASTER_PLAN.md`](file:///d:/wd/c/sang/d/Documents/BTL-block-chain/specs/MASTER_PLAN.md)

---

## Task Organization & Conventions

- **Format**: `[ID] [P?] [Feature/Role] Description`
- **[P]**: Nhiệm vụ có thể chạy song song (khác file, không phụ thuộc nhau).
- **[TV1]**: Trách nhiệm của Thành viên 1 (Core Simulator Lead - `domain/`, `usecase/`, logic toán, unit tests).
- **[TV2]**: Trách nhiệm của Thành viên 2 (UI & Data Viz Lead - `interface/`, `infra/`, biểu đồ, dashboard, export CSV).
- **Nguyên tắc**: TDD (Viết test trước hoặc song hành), 100% test pass, không file nào vượt quá 300 dòng code.

---

## Phase 1: Setup & Project Infrastructure

**Mục tiêu**: Chuẩn bị cấu trúc thư mục, môi trường dependencies, cấu hình pytest và linting.

- [x] **T001** [P] [TV1] Khởi tạo cấu trúc các thư mục dự án: `src/domain`, `src/usecase`, `src/infra`, `src/interface/components`, `tests/unit`, `tests/system` kèm các file `__init__.py`.
- [x] **T002** [P] [TV2] Tạo file `requirements.txt` cố định các thư viện bắt buộc: `streamlit>=1.30.0`, `plotly>=5.18.0`, `pandas>=2.0.0`, `numpy>=1.24.0`, `pytest>=8.0.0`, `pydantic>=2.0.0`.
- [x] **T003** [P] [TV1] Thiết lập file `tests/conftest.py` định nghĩa các fixture dùng chung: `default_config`, `mock_agent_eth`, `mock_agent_steth`, `mock_pool_a`, `mock_pool_b`.

---

## Phase 2: Domain Entities & Validation (Foundational Prerequisites)

**Mục tiêu**: Xây dựng toàn bộ mô hình dữ liệu lõi (Immutable Dataclasses / Pydantic) theo đúng schema của SRS §7.

- [x] **T004** [TV1] [Spec 001] Viết unit test xác thực cấu hình `tests/unit/test_config.py` kiểm tra các ràng buộc C-01..C-10 (UT-01).
- [x] **T005** [TV1] [Spec 001] Cài đặt `src/domain/config.py` định nghĩa `SimulationConfig` với giá trị mặc định chuẩn P-01..P-06 và logic validate C-01..C-10.
- [x] **T006** [P] [TV1] [Spec 002] Cài đặt `src/domain/agent.py` định nghĩa `AssetType` (ETH, stETH) và entity `BorrowerAgent` (id, asset, collateral, debt, initial_ltv, is_liquidated).
- [x] **T007** [P] [TV1] [Spec 005] Cài đặt `src/domain/amm_pool.py` định nghĩa thực thể `AMMPool` (name, reserve_x, reserve_y, k, spot_price, discount_pct) bảo toàn $x \cdot y = k$.
- [x] **T008** [P] [TV1] [Spec 004] Cài đặt `src/domain/liquidation_event.py` định nghĩa schema `LiquidationEvent` chuẩn 10 trường (SRS §7.3).
- [x] **T009** [P] [TV1] [Spec 006] Cài đặt `src/domain/block_result.py` định nghĩa schema `BlockResult` chuẩn 12 trường (SRS §7.4).
- [x] **T010** [P] [TV1] [Spec 006, 007] Cài đặt `src/domain/simulation_result.py` định nghĩa `KPISummary` và `SimulationResult` đóng gói kết quả kịch bản.

---

## Phase 3: Core Simulation Engines (Thành viên 1)

**Mục tiêu**: Cài đặt logic toán học, sinh Agent, định giá HF, thanh lý một phần, AMM swap và vòng lặp block mô phỏng.

### User Story 2 & 3: Borrower Generator & Health Factor Engine
- [x] **T011** [TV1] [Spec 002] Viết test `tests/unit/test_agent_generator.py` kiểm tra tính tất định của seed, phân bổ 50/50 tài sản, khoảng LTV [0.55, 0.72] và giá trị collateral (UT-02, UT-03).
- [x] **T012** [TV1] [Spec 002] Cài đặt `src/usecase/agent_generator.py` triển khai hàm `generate_borrower_agents(config, seed)` với `random.Random(seed)`.
- [x] **T013** [TV1] [Spec 003] Viết test `tests/unit/test_health_factor.py` đối chiếu công thức BR-01, BR-02, BR-03 và ví dụ tính tay §8 ($LT = 0.80$, epsilon $= 10^{-9}$, xử lý nợ = 0 và nợ xấu) (UT-04, UT-05, UT-06).
- [x] **T014** [TV1] [Spec 003] Cài đặt `src/usecase/health_factor.py` triển khai `compute_collateral_value`, `compute_health_factor`, `is_liquidatable`.

### User Story 4 & 5: AMM Engine & Partial Liquidation Engine
- [x] **T015** [TV1] [Spec 005] Viết test `tests/unit/test_amm_engine.py` kiểm tra công thức swap zero-fee $y_{out} = \frac{y \cdot dx}{x + dx}$, trượt giá, và cơ chế shock ngoại sinh tái cân bằng bảo toàn $k_A$ (UT-09, UT-12, UT-13).
- [x] **T016** [TV1] [Spec 005] Cài đặt `src/usecase/amm_engine.py` triển khai `execute_swap`, `apply_exogenous_shock`, `calculate_steth_discount`.
- [x] **T017** [TV1] [Spec 004] Viết test `tests/unit/test_liquidation_engine.py` kiểm tra close factor 50%, bonus penalty 5%, phát hiện nợ xấu và sinh `LiquidationEvent` (UT-07, UT-08).
- [x] **T018** [TV1] [Spec 004] Cài đặt `src/usecase/liquidation_engine.py` triển khai `liquidate_borrower_position`.

### User Story 6: Scenario Runner & Block Loop Coordination
- [x] **T019** [TV1] [Spec 006] Viết test `tests/unit/test_scenario_runner.py` kiểm tra tính độc lập deepcopy của 3 kịch bản, số block 0..max_blocks, và hợp đồng API `run_all_scenarios(config)` (UT-10, UT-11, UT-14).
- [x] **T020** [TV1] [Spec 006] Cài đặt `src/usecase/scenario_runner.py` triển khai thuật toán mô phỏng §10:
  - SC01: Baseline phẳng, không shock, 0 thanh lý.
  - SC02: Direct shock tại block 1, có thanh lý, không bán vào AMM, giá giữ nguyên.
  - SC03: Contagion cascade, shock tại block 1, bán collateral vào Pool B & Pool A, giá phản hồi qua từng block.
- [x] **T021** [TV1] [Spec 006] Viết test hệ thống `tests/system/test_system_scenarios.py` xác minh các điều kiện bất biến thực nghiệm ST-01 đến ST-07.

---

## Phase 4: Analytics & Exporter (Thành viên 2)

**Mục tiêu**: Xây dựng module trích xuất KPI, bảng so sánh đối chứng delta và module xuất dữ liệu ra file CSV chuẩn.

- [x] **T022** [TV2] [Spec 007] Viết test `tests/unit/test_metrics.py` kiểm tra tính toán 6 KPI cốt lõi, bảng so sánh delta SC03 vs SC02, và xử lý an toàn `unique_SC02 == 0` trả về `"N/A"` (FR-07, FR-11).
- [x] **T023** [TV2] [Spec 007] Cài đặt `src/interface/components/metrics.py` triển khai `extract_kpi_summary` và `generate_comparison_table`.
- [x] **T024** [TV2] [Spec 009] Viết test `tests/unit/test_exporter.py` kiểm tra xuất chuỗi CSV đúng 12 cột Block Results và 10 cột Liquidation Events, đọc lại bằng `pandas.read_csv` không lỗi (ST-08).
- [x] **T025** [TV2] [Spec 009] Cài đặt `src/infra/exporter.py` triển khai `export_block_results_to_csv`, `export_liquidation_events_to_csv`, và chuyển đổi sang `pd.DataFrame`.

---

## Phase 5: Visualizations & Streamlit Dashboard (Thành viên 2)

**Mục tiêu**: Xây dựng 4 biểu đồ Plotly tương tác và toàn bộ giao diện Dashboard một trang với 4 Tabs.

- [x] **T026** [TV2] [Spec 008] Viết test `tests/unit/test_charts.py` kiểm tra 4 hàm sinh Figure Plotly (ETH price, stETH discount, breakdown cột, lũy kế đường) với các tập dữ liệu biên.
- [x] **T027** [TV2] [Spec 008] Cài đặt `src/interface/components/charts.py` triển khai 4 biểu đồ Plotly có vạch shock block 1, legend rõ ràng, trục Y không âm.
- [x] **T028** [P] [TV2] [Spec 010] Cài đặt `src/interface/components/sidebar.py` triển khai các slider tham số (P-01..P-06) và 2 nút "Run Simulation", "Reset Defaults".
- [x] **T029** [P] [TV2] [Spec 009, 010] Cài đặt `src/interface/components/data_tab.py` hiển thị 2 bảng dữ liệu và 2 nút tải CSV (ẩn/khóa khi chưa chạy mô phỏng).
- [x] **T030** [P] [TV2] [Spec 010] Cài đặt `src/interface/components/methodology_tab.py` hiển thị sơ đồ cascade Markdown, công thức KaTeX và các giả định/giới hạn (FR-10).
- [x] **T031** [TV2] [Spec 010] Cài đặt `src/interface/app.py` ghép nối Sidebar, Top KPI metrics và 4 Tabs; hiển thị disclaimer nghiên cứu; kết nối gọi `run_all_scenarios(config)` và quản lý session state.

---

## Phase 6: Verification, System Testing & Final Acceptance

**Mục tiêu**: Kiểm thử toàn diện hệ thống, linter, tối ưu và chuẩn bị bàn giao.

- [x] **T032** [TV1 + TV2] Chạy toàn bộ test suite: `python -m pytest tests/` đảm bảo pass 100% tất cả các unit test và system test (67/67 passed).
- [x] **T033** [TV1 + TV2] Kiểm tra quy chuẩn chất lượng: không file nào vượt quá 300 dòng code, type hints đầy đủ, docstring Google style gắn mã `# Implements BR-XX`.
- [x] **T034** [TV2] Soạn thảo file `README.md` hướng dẫn cài đặt môi trường, cách chạy Streamlit local, giải thích kết quả 4 biểu đồ và cách đối soát kết quả phục vụ bảo vệ đồ án.

