# Feature Specification: Liquidation Engine (thanh lý một phần)

**Feature Branch**: `004-partial-liquidation-engine`
**Created**: 2026-11-10
**Status**: Draft
**Input**: User description: "Khi Agent đủ điều kiện thanh lý, liquidator trả tối đa 50% nợ, thu collateral cộng bonus 5%, cập nhật trạng thái Agent, sinh LiquidationEvent, ghi nhận nợ xấu." (requirements.md BR-04, BR-10, BR-11, §7.1, §7.3, FR-04, UT-04, UT-05, UT-13)

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Thanh lý thông thường (Priority: P1)

Agent có HF < 1 và đủ collateral: liquidator trả 50% nợ và nhận collateral trị giá 105% số nợ đã trả.

**Why this priority**: Là bước trung tâm của chuỗi Shock → Liquidation → Swap → Price.

**Independent Test**: UT-04.

**Acceptance Scenarios**:

1. **Given** nợ 10,000 USDC, close_factor 0.5, collateral đủ, bonus 5%, **When** thanh lý, **Then** `debt_repaid = 5,000` và collateral thu giữ có giá trị `5,250` USD tính theo giá spot TRƯỚC giao dịch.
2. **Given** Agent ETH 166.6667 ETH (trị 500,000 USD ở giá 3000), nợ 350,000, giá ETH sau shock 2,550 (HF 0.9714), **When** thanh lý, **Then** `debt_repaid = 175,000`, `collateral_seized = 175000×1.05/2550 = 72.0588 ETH`, `debt_new = 175,000`, `collateral_new = 94.6078 ETH`, `status = ACTIVE`, `ever_liquidated = True`, `liquidation_count = 1`.
3. **Given** Agent ở scenario 2 sau thanh lý, **When** tính lại HF cùng giá 2,550, **Then** `HF = 94.6078×2550×0.8/175000 ≈ 1.1029` (> 1; Agent không bị thanh lý tiếp ở block sau nếu giá không đổi).

---

### User Story 2 - Collateral không đủ (Priority: P1)

Collateral còn lại không đủ trả 50% nợ cộng bonus: giới hạn mức trả theo collateral; số dư không âm; nợ còn lại thành nợ xấu.

**Why this priority**: Bad debt là chỉ số KPI bắt buộc.

**Independent Test**: UT-05, UT-13.

**Acceptance Scenarios**:

1. **Given** nợ 10,000, collateral 2 ETH, giá 2,000 (trị 4,000), **When** thanh lý, **Then** `candidate_repay = 5,000`; `max_repay_from_collateral = 4000/1.05 = 3,809.5238`; `debt_repaid = 3,809.5238`; `collateral_seized = 3809.5238×1.05/2000 = 2.0 ETH`; `collateral_new = 0`; `debt_new = 6,190.4762`; `status = BAD_DEBT`.
2. **Given** Agent đã `BAD_DEBT`, **When** vòng lặp xét thanh lý, **Then** không có event mới và không bị cộng lại vào tổng nợ xấu lần nữa.

---

### User Story 3 - Event đầy đủ để truy vết (Priority: P2)

Mỗi lần thanh lý sinh đúng một `LiquidationEvent` đủ 10 trường để đưa ra CSV và đối chiếu.

**Why this priority**: Dữ liệu cho CSV, bảng và kiểm thử.

**Independent Test**: Sau 1 thanh lý, kiểm tra 10 trường có mặt và đúng.

**Acceptance Scenarios**:

1. **Given** thanh lý ở Story 1 scenario 2, **When** đọc event, **Then** `scenario` (do caller gán SC02/SC03), `block`, `agent_id`, `asset = ETH`, `hf_before = 0.9714…`, `debt_repaid_usd = 175000`, `collateral_seized = 72.0588`, `collateral_value_at_oracle_usd = 183,750`, `remaining_debt_usd = 175000`, `remaining_collateral = 94.6078`.

---

### Edge Cases

- `debt_repaid ≤ epsilon` → KHÔNG tạo event, KHÔNG đổi trạng thái (BR-04 bước 6).
- Agent đủ điều kiện nhưng đã bị thanh lý trong block hiện tại → KHÔNG thanh lý lần 2 trong cùng block (BR-04 bước 9, do vòng lặp block bảo đảm — spec 006).
- Nợ còn lại cực nhỏ (≤ 1e-9) sau giao dịch → coi như hết nợ, `status = REPAID`.
- Hết cả nợ và collateral cùng lúc: `REPAID` ưu tiên hơn `BAD_DEBT`.
- Sai số float: `collateral_seized` có thể vượt `collateral_before` một lượng ≤ epsilon → kẹp về `collateral_before`.

## Requirements *(mandatory)*

### Thuật toán (BR-04, đúng thứ tự)

Cho Agent đủ điều kiện, `price` = giá spot hiện hành của asset NGAY TRƯỚC giao dịch:

1. `candidate_repay = close_factor × current_debt` (0.5).
2. `max_repay_from_collateral = collateral_amount × price / (1 + liquidation_bonus)` (bonus = 0.05).
3. `debt_repaid = min(candidate_repay, max_repay_from_collateral)`.
4. Nếu `debt_repaid ≤ epsilon` → dừng, không event.
5. `collateral_seized = debt_repaid × (1 + liquidation_bonus) / price`.
6. `debt_new = max(0, debt_old − debt_repaid)`; `collateral_new = max(0, collateral_old − collateral_seized)`.
7. `ever_liquidated = True`; `liquidation_count += 1`.
8. Trạng thái: nếu `debt_new ≤ epsilon` → `REPAID`; ngược lại nếu `collateral_new ≤ epsilon` → `BAD_DEBT`; ngược lại `ACTIVE`.

### Functional Requirements (EARS)

- **FR-001** *(Event)*: WHEN một Agent thỏa `is_liquidatable(price)` được thanh lý, THE system SHALL thực hiện đúng các bước 1–8 ở trên.
- **FR-002** *(Ubiquitous)*: THE system SHALL tính mọi đại lượng của giao dịch bằng giá spot TRƯỚC giao dịch đó; SHALL NOT dùng giá sau giao dịch (BR-11).
- **FR-003** *(Ubiquitous)*: THE system SHALL luôn giữ `collateral_amount ≥ 0`, `debt_usdc ≥ 0`, `debt_repaid ≤ debt_before`, `collateral_seized ≤ collateral_before` (± epsilon) (BR-11).
- **FR-004** *(Unwanted)*: IF `debt_repaid ≤ epsilon`, THEN THE system SHALL NOT tạo `LiquidationEvent` và SHALL NOT thay đổi Agent.
- **FR-005** *(Event)*: WHEN thanh lý hoàn tất, THE system SHALL sinh đúng một `LiquidationEvent` gồm 10 trường: `scenario, block, agent_id, asset, hf_before, debt_repaid_usd, collateral_seized, collateral_value_at_oracle_usd, remaining_debt_usd, remaining_collateral`.
- **FR-006** *(Ubiquitous)*: THE system SHALL định nghĩa `collateral_value_at_oracle_usd = collateral_seized × price_before` (giá trị của phần collateral bị thu giữ, bằng `debt_repaid × 1.05`).
- **FR-007** *(State)*: WHILE `collateral_new ≤ epsilon` AND `debt_new > epsilon`, THE system SHALL đặt `status = BAD_DEBT` và SHALL NOT thanh lý Agent đó nữa.
- **FR-008** *(Event)*: WHEN `debt_new ≤ epsilon`, THE system SHALL đặt `status = REPAID`.
- **FR-009** *(Ubiquitous)*: THE system SHALL tính nợ xấu theo BR-10: `bad_debt_usd = Σ debt_usdc` của mọi Agent có `collateral_amount ≤ epsilon` AND `debt_usdc > epsilon`, tính từ TRẠNG THÁI HIỆN TẠI (không cộng dồn qua block).
- **FR-010** *(Ubiquitous)*: THE system SHALL cho phép nhiều event cho cùng Agent ở các block khác nhau, và SHALL đếm `ever_liquidated` không trùng lặp.
- **FR-011** *(Ubiquitous)*: THE system SHALL cung cấp `apply_liquidation(debt_repaid, collateral_seized)` trên `BorrowerAgent`: trừ nợ và collateral, không cho âm, cập nhật `ever_liquidated`, `liquidation_count`, `status`.
- **FR-012** *(Ubiquitous)*: THE system SHALL NOT hardcode số event, số Agent, giá trị nợ xấu.
- **FR-013** *(Ubiquitous)*: THE system SHALL KHÔNG kiểm tra lợi nhuận của liquidator; khoản lỗ khi liquidator đổi collateral trên AMM SHALL NOT được tính vào nợ xấu của bên vay (SRS §5.7).

### Key Entities

- **LiquidationEvent**: bản ghi một lần thanh lý (10 trường FR-005).
- **BorrowerAgent**: cập nhật `collateral_amount`, `debt_usdc`, `ever_liquidated`, `liquidation_count`, `status`.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: UT-04: `debt_repaid = 5000`, giá trị thu giữ `5250` (±1e-6).
- **SC-002**: UT-05: `debt_repaid = 3809.5238 ± 1e-3`, số dư không âm, `status = BAD_DEBT`.
- **SC-003**: Trong mọi lần chạy, `Σ bad_debt_usd` tính lại từ Agent bằng đúng giá trị báo cáo (không lệch).
- **SC-004**: 100% event có đủ 10 trường.

## Out of Scope

- Close factor động, dust, cấu hình tài sản của giao thức thật (SRS BR-04 ghi chú).
- Lợi nhuận/vốn của liquidator, nhiều liquidator.
- Thanh lý nhiều lần cho một Agent trong cùng block.

## Assumptions *(quyết định đã chốt)*

- SRS không nêu nghĩa chính xác của `collateral_value_at_oracle_usd`: chốt = giá trị phần collateral bị thu giữ tại giá spot trước giao dịch (khớp mô tả "trị giá $5,250" ở UT-04).
- `scenario` trong event do lớp gọi (vòng lặp block) gán; engine thanh lý thuần không biết tên kịch bản.
- `REPAID` chỉ xuất hiện khi nợ giảm về ≤ epsilon (do close factor 50% nên hiếm); vẫn phải được xử lý đúng.

## Traceability

SRS BR-04 → thuật toán, FR-001…FR-008; BR-10 → FR-009; BR-11 → FR-002, FR-003; §7.3 → FR-005; §7.1 → FR-011; FR-04 → toàn bộ; UT-04/05/13.

