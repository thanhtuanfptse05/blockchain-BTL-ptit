# Feature Specification: Tính Health Factor và điều kiện thanh lý

**Feature Branch**: `003-health-factor-eligibility`
**Created**: 2026-11-10
**Status**: Draft
**Input**: User description: "Tính giá trị collateral, LTV, Health Factor và xác định Agent đủ điều kiện thanh lý, kể cả các trường hợp nợ = 0 hoặc hết collateral." (requirements.md §7.1, BR-01, BR-02, BR-03, FR-03, UT-01, UT-02, UT-03)

## User Scenarios & Testing *(mandatory)*

### User Story 1 - HF đúng công thức (Priority: P1)

Người dùng/giảng viên có thể đối chiếu bằng tay: Agent 10 ETH, giá 3,000, nợ 22,000, LT 0.8 → HF 1.0909; sau shock 15% (giá 2,550) → HF 0.9273.

**Why this priority**: HF là điều kiện kích hoạt toàn bộ chuỗi thanh lý; sai ở đây là sai toàn bộ.

**Independent Test**: UT-01 và UT-02.

**Acceptance Scenarios**:

1. **Given** Agent ETH có 10 ETH, nợ 22,000, LT 0.8 và giá ETH 3,000, **When** tính HF, **Then** `HF = 10×3000×0.8/22000 = 1.090909…` và `is_liquidatable = False`.
2. **Given** cùng Agent, giá ETH 2,550, **When** tính HF, **Then** `HF = 0.927272…` và `is_liquidatable = True`.
3. **Given** Agent có `debt_usdc ≤ 1e-9`, **When** tính HF, **Then** HF = +∞, `is_liquidatable = False`, không bao giờ bị xử lý thanh lý.

---

### User Story 2 - Giá đúng theo loại collateral (Priority: P1)

Agent ETH dùng giá ETH; Agent stETH dùng giá stETH tính bằng USD.

**Why this priority**: Đây chính là con đường truyền lây chéo tài sản.

**Independent Test**: Cùng số lượng token và nợ, Agent stETH có HF thấp hơn Agent ETH khi stETH rẻ hơn ETH.

**Acceptance Scenarios**:

1. **Given** Agent stETH có 100 stETH, nợ 200,000, giá stETH 2,970, **When** tính HF, **Then** `HF = 100×2970×0.8/200000 = 1.188`.
2. **Given** discount stETH tăng làm giá stETH giảm còn 2,500, **When** tính lại, **Then** `HF = 100×2500×0.8/200000 = 1.0` và `is_liquidatable = False` (HF = 1 chưa đủ điều kiện, cần HF < 1).

---

### User Story 3 - Trạng thái biên (Priority: P2)

Agent hết collateral nhưng còn nợ, hoặc hết nợ, không bị xử lý lặp.

**Why this priority**: Tránh vòng lặp vô hạn và đếm trùng (SRS §19).

**Independent Test**: UT-03, UT-13.

**Acceptance Scenarios**:

1. **Given** Agent có `collateral_amount ≤ 1e-9` và `debt_usdc > 1e-9`, **When** gọi `is_liquidatable`, **Then** False.
2. **Given** Agent có `status = BAD_DEBT` hoặc `REPAID`, **When** gọi `is_liquidatable`, **Then** False.

---

### Edge Cases

- HF đúng bằng 1 (sau float) → KHÔNG thanh lý; so sánh dùng giá trị chưa làm tròn (FR-03). Ví dụ biên: LTV 0.72, shock 10% → HF = 0.8/0.72×0.9 = 1.0 (chỉ chính xác trong số học thực; test dùng sai số epsilon).
- `collateral_value = 0` và `debt > 0`: KHÔNG chia cho 0 cho LTV; LTV trả về giá trị đặc biệt "không xác định" và Agent là `BAD_DEBT`; HF = 0.0 (từ công thức).
- `price ≤ 0` truyền vào → lỗi tham số (giá tài sản phải dương).
- Giá cực nhỏ nhưng dương → HF rất nhỏ, vẫn hợp lệ.

## Requirements *(mandatory)*

### Functional Requirements (EARS)

- **FR-001** *(Ubiquitous)*: THE system SHALL tính `collateral_value_usd = collateral_amount × current_asset_price_usd` (BR-01); Agent ETH dùng giá ETH, Agent stETH dùng giá stETH.
- **FR-002** *(Ubiquitous)*: THE system SHALL tính `current_ltv = debt_usdc / collateral_value_usd` (BR-02).
- **FR-003** *(Unwanted)*: IF `collateral_value_usd ≤ epsilon` AND `debt_usdc > epsilon`, THEN THE system SHALL NOT thực hiện phép chia của FR-002, SHALL trả LTV "không xác định" và SHALL coi vị thế là `BAD_DEBT`.
- **FR-004** *(Ubiquitous)*: THE system SHALL tính `HF = collateral_value_usd × liquidation_threshold / debt_usdc` (BR-03), không làm tròn trước khi so sánh.
- **FR-005** *(Unwanted)*: IF `debt_usdc ≤ epsilon`, THEN THE system SHALL trả `HF = +∞` và coi vị thế an toàn.
- **FR-006** *(Ubiquitous)*: THE system SHALL xác định `is_liquidatable(price) = (debt_usdc > epsilon) AND (collateral_amount > epsilon) AND (HF < 1)`; `HF ≥ 1` là chưa đủ điều kiện.
- **FR-007** *(State)*: WHILE `status ∈ {REPAID, BAD_DEBT}`, THE system SHALL cho `is_liquidatable = False`.
- **FR-008** *(Unwanted)*: IF `current_asset_price_usd ≤ 0` hoặc không hữu hạn, THEN THE system SHALL từ chối tính và báo lỗi tham số.
- **FR-009** *(Ubiquitous)*: THE system SHALL cung cấp đủ 3 phương thức trên `BorrowerAgent`: `collateral_value(price)`, `health_factor(price)`, `is_liquidatable(price)` (cùng `apply_liquidation` ở spec 004).
- **FR-010** *(Ubiquitous)*: THE system SHALL dùng `epsilon = 1e-9` cho mọi so sánh với 0 của nợ/collateral.
- **FR-011** *(Ubiquitous)*: THE system SHALL NOT hardcode danh sách Agent đủ điều kiện; mọi kết quả suy ra từ trạng thái Agent và giá hiện hành.

### Key Entities

- **BorrowerAgent**: xem spec 002 (thuộc tính) và spec 004 (cập nhật sau thanh lý).
- **AssetPrice**: giá USD của ETH (từ Pool A) hoặc stETH (Pool A × tỷ giá Pool B), spec 005.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: UT-01: HF = 1.090909 ± 1e-6; UT-02: HF = 0.927273 ± 1e-6; UT-03: HF = ∞.
- **SC-002**: Với mọi Agent khởi tạo (spec 002) và giá ban đầu, `is_liquidatable = False` (100%).
- **SC-003**: Không có trường hợp chia cho 0 hoặc ngoại lệ khi nợ = 0 hoặc collateral = 0 (kiểm bằng bộ biên).

## Out of Scope

- Lãi vay làm HF thay đổi theo thời gian; oracle độc lập/TWAP (SRS §5.6 — giá = spot trong mô hình).
- Ngưỡng LT khác nhau theo tài sản (dùng chung 0.80).
- Đa tài sản thế chấp.

## Assumptions *(quyết định đã chốt)*

- SRS không nêu giá trị HF khi collateral = 0 và nợ > 0: chốt HF = 0.0 (kết quả công thức) nhưng vị thế không phải đối tượng thanh lý.
- LTV "không xác định" biểu diễn bằng giá trị đặc biệt (vd `None`/`inf`), không dùng cho so sánh.

## Traceability

SRS BR-01 → FR-001; BR-02 → FR-002, FR-003; BR-03 → FR-004…FR-006; §7.1 phương thức → FR-009; FR-03 → toàn bộ; UT-01/02/03 → User Story 1; UT-13 → User Story 3.

