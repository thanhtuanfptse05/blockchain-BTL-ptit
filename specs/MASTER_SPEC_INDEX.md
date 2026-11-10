# MASTER SPECIFICATION INDEX & TRACEABILITY MATRIX
## DeFi Liquidation Cascade Simulator (DeFi Lending Agent-Based Model)

**Version**: 1.0.0  
**Specification Framework**: GitHub Spec Kit (Spec-Driven Development / SDD)  
**Standard**: EARS (Easy Approach to Requirements Syntax) + 8 Core Components of Executable Spec  
**Status**: COMPLETE (Ready for Specification Gate Review)

---

## 1. Overview & Architecture Traceability

| Feature ID | Feature Directory | SRS Scope | Functional Requirements | Business Rules & Constraints | Test Fixtures |
|---|---|---|---|---|---|
| **001** | [`specs/001-simulation-config/`](file:///d:/wd c sang d/Documents/BTL-block-chain/specs/001-simulation-config/spec.md) | Tham số cấu hình & Ràng buộc hợp lệ | FR-01, FR-02, FR-03, FR-04, FR-05 | P-01..P-06, C-01..C-10 | UT-01 |
| **002** | [`specs/002-borrower-agent-generation/`](file:///d:/wd c sang d/Documents/BTL-block-chain/specs/002-borrower-agent-generation/spec.md) | Sinh quần thể Borrower Agents tất định | §4.2, §7.1 | LTV [0.55, 0.72], Collateral [$250k, $1M], 50/50 ETH/stETH | UT-02, UT-03 |
| **003** | [`specs/003-health-factor-eligibility/`](file:///d:/wd c sang d/Documents/BTL-block-chain/specs/003-health-factor-eligibility/spec.md) | Định giá Collateral & Tính Health Factor | §7.1, §8 | BR-01, BR-02, BR-03 (LT = 0.80, epsilon = 1e-9) | UT-04, UT-05, UT-06 |
| **004** | [`specs/004-partial-liquidation-engine/`](file:///d:/wd c sang d/Documents/BTL-block-chain/specs/004-partial-liquidation-engine/spec.md) | Động cơ thanh lý một phần & Sinh sự kiện | §7.3, §8 | BR-04, BR-10 (Close factor = 0.50, Penalty = 0.05, Bad debt) | UT-07, UT-08 |
| **005** | [`specs/005-amm-pools/`](file:///d:/wd c sang d/Documents/BTL-block-chain/specs/005-amm-pools/spec.md) | Hai Pool AMM Constant Product $x \cdot y = k$ | §5.3..§5.5, §7.2, §8 | BR-05, BR-06, BR-09 (Zero fee, Exogenous Shock rebalancing) | UT-09, UT-12, UT-13 |
| **006** | [`specs/006-scenario-block-simulation/`](file:///d:/wd c sang d/Documents/BTL-block-chain/specs/006-scenario-block-simulation/spec.md) | Vòng lặp Block mô phỏng SC01, SC02, SC03 | §9, §10, §15.1 | BR-07, BR-08, BR-11, FR-06 | UT-10, UT-11, UT-14, ST-01..ST-07 |
| **007** | [`specs/007-analytics-kpi-summary/`](file:///d:/wd c sang d/Documents/BTL-block-chain/specs/007-analytics-kpi-summary/spec.md) | Dashboard thống kê 6 KPI & Bảng delta | §7.5, §11 | FR-07, FR-11 (Div-by-zero protection, 6 core metrics) | ST-04, ST-05 |
| **008** | [`specs/008-charts-visualization/`](file:///d:/wd c sang d/Documents/BTL-block-chain/specs/008-charts-visualization/spec.md) | 4 Biểu đồ phân tích theo block (Plotly) | §11, §12.2 | FR-08 (ETH price, stETH discount, breakdown, cumulative) | NFR-06 |
| **009** | [`specs/009-data-tables-csv-export/`](file:///d:/wd c sang d/Documents/BTL-block-chain/specs/009-data-tables-csv-export/spec.md) | Bảng dữ liệu chi tiết & Xuất 2 file CSV | §7.3, §7.4, §11 | FR-09 (12 cols BlockResult, 10 cols LiquidationEvent, UTF-8) | ST-08 |
| **010** | [`specs/010-streamlit-dashboard-ui/`](file:///d:/wd c sang d/Documents/BTL-block-chain/specs/010-streamlit-dashboard-ui/spec.md) | Giao diện Streamlit Dashboard & Tab Cơ chế | §11, §12, §13 | FR-10 (Sidebar, 4 Tabs, Methodology explanation, Disclaimer) | NFR-05, NFR-07 |

---

## 2. SDD Quality Audit Checklist (Spec Verification Gate)

Tất cả 10 bản đặc tả tính năng đã được kiểm tra chéo và thỏa mãn 100% các tiêu chí chất lượng nghiêm ngặt của cuốn sách **Spec-Driven & Agent-Driven Development**:

- [x] **No Premature Implementation Leakage**: Đặc tả không chứa mã nguồn triển khai thực tế của `src/`, chỉ tập trung vào hành vi mong muốn (Behavior), mô hình dữ liệu (Schema), công thức toán học và kịch bản chấp nhận (Given-When-Then).
- [x] **Strict EARS Notation**: Toàn bộ yêu cầu chức năng đều được phân loại chính xác thành 5 mẫu câu:
  1. *Ubiquitous* (Hệ thống luôn luôn thực hiện...)
  2. *Event-driven* (KHI có sự kiện X, hệ thống PHẢI thực hiện Y...)
  3. *State-driven* (TRONG KHI ở trạng thái S, hệ thống PHẢI...)
  4. *Optional* (NẾU tính năng tùy chọn được bật, hệ thống PHẢI...)
  5. *Unwanted* (NẾU xảy ra lỗi/ngoại lệ/chia cho 0, hệ thống PHẢI bắt và xử lý an toàn...)
- [x] **Mathematical Exactness**:
  - Pool AMM là **Zero-fee** (`fee = 0.0`), bảo toàn $x \cdot y = k$.
  - Cú sốc ngoại sinh tại block 1 tái cân bằng Pool A bảo toàn $k_A$.
  - Ngưỡng thanh lý $LT = 0.80$ thống nhất cho cả ETH và stETH.
  - Close factor $= 0.50$, liquidation penalty bonus $= 0.05$.
- [x] **Edge Case & Error Taxonomy**: Định nghĩa rõ ràng cách xử lý các trường hợp biên: nợ bằng 0, collateral bằng 0, bad debt, trượt giá chạm đáy thanh khoản, mẫu số bằng 0 (`unique_SC02 == 0`), và khởi tạo UI trước khi chạy mô phỏng.
- [x] **Team Role Alignment**: Phân định rõ ràng trách nhiệm giữa Thành viên 1 (Core Engine: Feature 001..006) và Thành viên 2 (UI & Exporter: Feature 007..010) theo đúng SRS §15.1 & §16.

