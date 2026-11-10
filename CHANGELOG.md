# Changelog — DeFi Liquidation Cascade Simulator

Tất cả các thay đổi, cập nhật kiến trúc, bổ sung đặc tả và tiến độ triển khai dự án được ghi nhận tại đây theo chuẩn [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) và [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.1.0] — 2026-11-10

### 🎨 Changed (Tái thiết kế Toàn diện Giao diện — Humanized Light Theme)
- **Tích hợp Kỹ năng Humanizer (`blader/humanizer` v4.0.0)**:
  - Cài đặt cục bộ tại `.agents/skills/humanizer` và toàn cục tại `C:\Users\DELL\.gemini\config\skills\humanizer`.
  - Áp dụng nguyên tắc Humanizer: loại bỏ toàn bộ văn phong giật gân, câu chữ kiểu AI chatbot, dùng câu từ tự nhiên, chuẩn mực kỹ thuật và học thuật.
- **Chuyển đổi hoàn toàn sang Light Mode tối giản (Stripe & Notion style)**:
  - Cấu hình `.streamlit/config.toml`: `base="light"`, `backgroundColor="#FFFFFF"`, `secondaryBackgroundColor="#F8FAFC"`, `primaryColor="#2563EB"`, `textColor="#0F172A"`.
  - `src/interface/theme.py`: Tái cấu trúc CSS toàn diện theo phong cách phẳng, viền xám mảnh `#E2E8F0`, đổ bóng mềm, font chữ *Plus Jakarta Sans* và *JetBrains Mono*.
- **Loại bỏ triệt để Emoji trang trí kiểu AI**:
  - Xóa sạch toàn bộ các icon thừa (⚡, 🚀, 💥, 🛡️, 🧠, 📊, 📋, 📈, 🎯, 💧, 👥, 📌, ⚠️, 🟢, 🟡, 🔴) trên header, sidebar, nút bấm, nhãn thanh trượt, tabs điều hướng và các thẻ số liệu KPI.
- **Thẻ KPI Phẳng Tối giản (Flat Metric Cards)**:
  - `src/interface/components/metrics.py`: Bỏ các dải dạ quang neon lòe loẹt; thiết kế lại thẻ số liệu màu trắng tinh tế, font số dạng bảng tabular monospace, badge delta chênh lệch xám/đỏ/xanh chuẩn mực.
- **Biểu đồ Plotly Light Mode**:
  - `src/interface/components/charts.py`: Nền biểu đồ trắng trong suốt, lưới xám nhạt `#F1F5F9`, vạch đánh dấu cú sốc tại block 1 sắc nét và trang nhã, màu sắc đường biểu đồ có độ tương phản cao.
- **Trải nghiệm tức thời (Instant Data Hydration)**:
  - `src/interface/app.py`: Tự động khởi tạo kết quả mô phỏng mặc định ngay trong 0.007 giây khi vừa mở trang; triệt tiêu hoàn toàn màn hình trống hoặc thông báo cảnh báo khó chịu.
- **Kịch bản mẫu nhanh (Presets)**:
  - `src/interface/components/sidebar.py`: Bổ sung 2 nút thiết lập 1-click "Căng thẳng cao" (Shock 30%, Pool hẹp) và "Thanh khoản sâu" (Shock 5%, Pool sâu $300M).

---

## [1.0.0-spec] — 2026-11-10

### 💻 Implemented (Mã nguồn & Kiểm thử Hoàn thiện 10/10 Tính năng)
- **Feature 010 — Streamlit Dashboard UI (`010-streamlit-dashboard-ui`)**:
  - `src/interface/app.py`: Ứng dụng Streamlit một trang hoàn chỉnh, layout wide, disclaimer nghiên cứu bắt buộc, quản lý `st.session_state` lưu trữ kết quả và điều phối 4 Tabs chức năng.
  - `src/interface/components/sidebar.py`: Thanh bên tham số P-01..P-06 với các slider và nút "Run Simulation", "Reset Defaults", chống auto-rerun khi kéo thả slider.
  - `src/interface/components/methodology_tab.py`: Tab Cơ chế & Phương pháp luận (FR-10) với sơ đồ cascade ASCII, công thức toán học KaTeX ($HF$, AMM $x \cdot y = k$, discount), so sánh 3 kịch bản và 5 giả định/giới hạn học thuật.
  - `tests/unit/test_app.py`: Bài kiểm thử xác nhận toàn bộ component giao diện được nạp hợp lệ.
- **Feature 009 — Data Tables & CSV Export (`009-data-tables-csv-export`)**:
  - `src/infra/exporter.py`: Chuyển đổi dữ liệu sang Pandas DataFrame và xuất CSV định dạng UTF-8 (`utf-8-sig`) cho Block Results (12 cột chuẩn, SRS §7.4) và Liquidation Events (10 cột chuẩn, SRS §7.3).
  - `src/interface/components/data_tab.py`: Tab Dữ liệu hiển thị bảng DataFrame tương tác và 2 nút tải CSV an toàn (chỉ khả dụng khi đã có kết quả mô phỏng).
  - `tests/unit/test_exporter.py`: 3 bài kiểm thử xác nhận độ chính xác round-trip với `pd.read_csv()`, bảo toàn số cột và xử lý an toàn trường hợp 0 thanh lý (ST-08); pass 100%.
- **Feature 008 — Charts & Visualizations (`008-charts-visualization`)**:
  - `src/interface/components/charts.py`: 4 biểu đồ Plotly tương tác: (1) Đường giá ETH 3 kịch bản kèm vạch shock block 1; (2) Biểu đồ Discount stETH (depeg dynamics); (3) Biểu đồ cột chồng phân bổ thanh lý theo tài sản ETH vs stETH; (4) Biểu đồ bậc thang số lượng Borrower bị thanh lý lũy kế SC02 vs SC03.
  - `tests/unit/test_charts.py`: 5 bài kiểm thử xác nhận cấu trúc Plotly Figure, số lượng trace, annotation tại block 1, trục Y không âm và khả năng xử lý dữ liệu biên; pass 100%.
- **Feature 007 — Analytics & KPI Summary (`007-analytics-kpi-summary`)**:
  - `src/interface/components/metrics.py`: Module `calculate_kpi_summary` (trích xuất 6 KPI cốt lõi SC03), `render_kpi_metrics` (hiển thị thẻ metrics kèm badge delta), `generate_comparison_table` (tính delta và % tăng tương đối giữa SC03 và SC02, xử lý an toàn phép chia cho 0 trả về `"N/A"`).
  - `tests/unit/test_metrics.py`: 4 bài kiểm thử xác nhận tính toán KPI, delta so sánh, phòng vệ lỗi `ZeroDivisionError` và các helper định dạng USD/%; pass 100%.
- **Feature 006 — Scenario Block Simulation (`006-scenario-block-simulation`)**:
  - `src/domain/block_result.py`: Schema `BlockResult` 12 trường dữ liệu chuẩn (SRS §7.4).
  - `src/domain/simulation_result.py`: Schema `SimulationResult` và `KPISummary` đóng gói kết quả mô phỏng (SRS §7.5).
  - `src/usecase/scenario_runner.py`: Động cơ điều phối vòng lặp mô phỏng block-by-block qua 3 kịch bản SC01 (Baseline phẳng), SC02 (Direct Shock không AMM feedback), và SC03 (Cascade Contagion với lộ trình bán collateral vào Pool B & Pool A).
  - `tests/unit/test_scenario_runner.py`: 5 bài kiểm thử xác nhận hợp đồng API, tính chất phẳng của SC01, giá cố định của SC02, và sụt giảm giá/depeg của SC03; pass 100%.
  - `tests/system/test_system_scenarios.py`: 7 bài kiểm thử hệ thống bất biến thực nghiệm (ST-01..ST-07); pass 100%.
- **Feature 005 — AMM Constant Product Pools (`005-amm-pools`)**:
  - `src/domain/amm_pool.py`: Thực thể `AMMPool` bảo toàn tích số bất biến $k = x \cdot y$, cung cấp hàm `spot_price` và `sell_x` theo công thức swap zero-fee $\Delta y = \frac{y \cdot \Delta x}{x + \Delta x}$.
  - `src/usecase/amm_engine.py`: Các module `initialize_pools` (khởi tạo Pool A \$150M và Pool B \$80M), `swap_exact_input`, `apply_exogenous_shock` (tái cân bằng Pool A tại block 1 bảo toàn $k_A$), `get_market_prices` (tính giá ETH, stETH và discount % depeg theo BR-09).
  - `tests/unit/test_amm_engine.py`: 6 bài kiểm thử tự động kiểm tra khởi tạo mặc định (ETH \$3000, stETH \$2970, discount 1%), bảo toàn $k$ qua swap zero-fee, tác động giảm giá khi bán ETH, tăng discount khi bán stETH, cú sốc ngoại sinh 15% giữ nguyên $k_A$ và bắt lỗi swap đầu vào âm; pass 100%.
- **Feature 004 — Partial Liquidation Engine (`004-partial-liquidation-engine`)**:
  - `src/domain/liquidation_event.py`: Schema sự kiện bất biến `LiquidationEvent` với đầy đủ 10 trường theo SRS §7.3.
  - `src/usecase/liquidation_engine.py`: Động cơ thanh lý một phần `liquidate_borrower_position` (close factor 50%, penalty bonus 5%, cập nhật trạng thái vị thế, bảo toàn không âm) và hàm tổng hợp nợ xấu `compute_total_bad_debt` (BR-10).
  - `src/domain/agent.py`: Bổ sung phương thức `apply_liquidation` cập nhật nợ, collateral, cờ `ever_liquidated`, số lần thanh lý và chuyển đổi trạng thái `ACTIVE` / `REPAID` / `BAD_DEBT`.
  - `tests/unit/test_liquidation_engine.py`: 5 bài kiểm thử tự động kiểm tra thanh lý thông thường, trường hợp thiếu collateral phát sinh nợ xấu, trường hợp thanh lý hết nợ, trường hợp không đủ điều kiện và tính toán tổng nợ xấu; pass 100%.
- **Feature 003 — Health Factor & Liquidation Eligibility (`003-health-factor-eligibility`)**:
  - `src/usecase/health_factor.py`: Các hàm `compute_collateral_value`, `compute_current_ltv`, `compute_health_factor`, `is_liquidatable` xử lý chính xác theo công thức BR-01..BR-03, ngưỡng $LT = 0.80$, bảo vệ số học `epsilon = 1e-9`, xử lý nợ = 0 ($HF = \infty$) và nợ xấu.
  - `src/domain/agent.py`: Bổ sung 3 phương thức tiện ích `collateral_value`, `health_factor`, `is_liquidatable` trực tiếp trên thực thể `BorrowerAgent` (FR-009).
  - `tests/unit/test_health_factor.py`: 5 bài kiểm thử đối chiếu ví dụ tính tay (§8: pre-shock HF 1.090909 -> post-shock HF 0.927273), định giá stETH và depeg ranh giới HF=1.0, các trạng thái biên zero-debt và zero-collateral, bắt lỗi giá âm/vô hạn; pass 100%.
- **Feature 002 — Borrower Agent Generation (`002-borrower-agent-generation`)**:
  - `src/domain/agent.py`: Thực thể `BorrowerAgent` và các enum `AssetType` (ETH, stETH), `AgentStatus` (ACTIVE, REPAID, BAD_DEBT).
  - `src/usecase/agent_generator.py`: Module `generate_borrower_agents(config)` sinh 100 Agent tất định theo seed (50 ETH, 50 stETH), LTV ban đầu trong khoảng [0.55, 0.72], collateral USD [$250k, $1M], kiểm tra $HF > 1.0$.
  - `tests/unit/test_agent_generator.py`: 5 bài kiểm thử tự động kiểm tra số lượng và phân bổ tài sản, ranh giới LTV và giá trị thế chấp, tính tái lập theo seed, tính độc lập với tham số pool TVL và khả năng thay đổi số lượng Agent; pass 100%.
- **Feature 001 — Simulation Config & Validation (`001-simulation-config`)**:
  - `src/domain/config.py`: Thực thể bất biến `SimulationConfig` (Pydantic v2 `frozen=True`) với 9 tham số chuẩn hóa (P-01..P-06) và 10 ràng buộc chặn biên (C-01..C-10).
  - `tests/unit/test_config.py`: 21 bài kiểm thử tự động kiểm tra giá trị mặc định, kiểm tra các giá trị biên hợp lệ, các trường hợp vi phạm ngoại lệ và tính bất biến; pass 100% trong 0.05s.
  - `tests/conftest.py`: Fixture dùng chung `default_config`.

### 🚀 Added (Khởi tạo toàn diện bộ đặc tả Spec Kit theo chuẩn SDD/ADD)
- **Cấu hình & Quy tắc cốt lõi**:
  - `CONSTITUTION.md`: Ban hành 8 nguyên tắc bất biến (Spec-First, Bảo toàn toán học AMM $x \cdot y = k$, Phí 0%, Không hardcode, Tất định 100%, Sửa Spec trước sửa Code, CodeGraph-First, Phân tách Clean Architecture).
  - `AGENTS.md` & `CLAUDE.md`: Thiết lập bối cảnh dự án, tech stack (Python >= 3.10, Streamlit, Plotly, Pytest), phân chia vai trò 2 thành viên (Thành viên 1: Core Engine; Thành viên 2: UI & Data Viz).
  - `.agents/rules/spec_and_codegraph.md`: Quy tắc bắt buộc Spec-First và CodeGraph tool.
- **10 Bản Đặc Tả Tính Năng Chi Tiết (EARS Notation)** tại `specs/`:
  - `001-simulation-config`: Tham số đầu vào P-01..P-06, ràng buộc kiểm tra C-01..C-10 (FR-01..FR-05).
  - `002-borrower-agent-generation`: Sinh 100 Borrower Agent tất định với `seed`, phân bổ 50/50 ETH/stETH, LTV ban đầu [0.55, 0.72], Collateral [$250k, $1M].
  - `003-health-factor-eligibility`: Định giá tài sản thế chấp, tính Health Factor với $LT = 0.80$, xử lý $debt \le 10^{-9}$ và nợ xấu (BR-01..BR-03).
  - `004-partial-liquidation-engine`: Cơ chế thanh lý một phần 50%, penalty bonus 5%, phát hiện bad debt, sinh `LiquidationEvent` 10 trường (BR-04, BR-10).
  - `005-amm-pools`: Hai Pool AMM Constant Product với **phí 0%**, tính discount stETH, tái cân bằng cú sốc ngoại sinh tại block 1 bảo toàn $k_A$ (BR-05, BR-06, BR-09).
  - `006-scenario-block-simulation`: Vòng lặp mô phỏng block 0..max_blocks cho SC01 (Baseline), SC02 (Direct Shock), SC03 (Cascade Contagion); sinh `BlockResult` 12 trường và `SimulationResult` (FR-06, BR-07, BR-08, BR-11).
  - `007-analytics-kpi-summary`: Trích xuất 6 KPI cốt lõi SC03, bảng so sánh đối chứng delta SC03 vs SC02, xử lý an toàn mẫu số 0 `unique_SC02 == 0` (FR-07, FR-11).
  - `008-charts-visualization`: 4 biểu đồ Plotly tương tác: ETH Price, stETH Discount, Liquidations per block by asset, Cumulative unique liquidated agents (FR-08).
  - `009-data-tables-csv-export`: Tab Dữ liệu tương tác và module xuất 2 file CSV UTF-8 cho Block Results và Liquidation Events, tương thích Pandas (FR-09, ST-08).
  - `010-streamlit-dashboard-ui`: Giao diện Streamlit Dashboard: Sidebar điều khiển tham số, 4 Tabs chức năng, Tab Cơ chế giải thích cascade và công thức, Disclaimer nghiên cứu (FR-10, §12).
- **Hồ sơ Kế hoạch & Quản lý**:
  - `specs/MASTER_SPEC_INDEX.md`: Ma trận đối soát yêu cầu (Traceability Matrix).
  - `specs/MASTER_PLAN.md`: Kế hoạch kiến trúc tổng thể, mô hình phân lớp và hợp đồng tích hợp giữa 2 thành viên.
  - `specs/MASTER_TASKS.md`: Danh sách 34 nhiệm vụ nguyên tử (T001..T034) phân chia theo 2 vai trò TV1 và TV2.

### 🛡️ Fixed & Corrected (Khắc phục sai lệch tài liệu)
- **AMM Fee**: Đính chính phí AMM về chuẩn **0% (zero-fee swap)** theo đúng SRS §5.5 và BR-05 (loại bỏ nhầm lẫn Uniswap 0.3%).
- **Liquidation Threshold**: Thống nhất $LT = 0.80$ cho cả ETH và stETH theo đúng SRS C-03.
- **Shock Rebalance**: Cú sốc ngoại sinh chỉ tác động Pool A tại block 1, giữ nguyên $k_A$; Pool B không bị shock trực tiếp mà biến động tự nhiên qua lệnh swap của liquidator.

