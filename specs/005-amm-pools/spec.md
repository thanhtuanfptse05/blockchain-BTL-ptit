# Feature Specification: Hai AMM Pool (constant-product) và giá thị trường

**Feature Branch**: `005-amm-pools`
**Created**: 2026-11-10
**Status**: Draft
**Input**: User description: "Hai pool constant-product không phí: Pool A (ETH/USDC) và Pool B (stETH/ETH); khởi tạo từ TVL, bán token, tính giá ETH/stETH, discount, và áp dụng cú sốc giá bằng cân bằng lại Pool A giữ nguyên k." (requirements.md §7.2, BR-05, BR-06, BR-07, BR-09, FR-05, UT-06…UT-10, UT-15)

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Khởi tạo giá chuẩn (Priority: P1)

Với TVL mặc định, ETH = $3,000, tỷ giá stETH/ETH = 0.99, stETH = $2,970, discount 1%.

**Why this priority**: Mốc block 0 của mọi biểu đồ.

**Independent Test**: UT-09.

**Acceptance Scenarios**:

1. **Given** `pool_a_tvl_usd = 150,000,000`, **When** khởi tạo, **Then** `reserve_A_USDC = 75,000,000`, `reserve_A_ETH = 25,000`, giá ETH = 3,000.
2. **Given** `pool_b_tvl_usd = 80,000,000`, **When** khởi tạo, **Then** `reserve_B_ETH = 13,333.3333`, `reserve_B_stETH = 13,468.0135`, `steth_eth_ratio = 0.99`.
3. **Given** hai pool vừa khởi tạo, **When** tính giá, **Then** `steth_price_usd = 2,970` và `steth_discount_pct = 1.0`.

---

### User Story 2 - Bán token gây tác động giá nội sinh (Priority: P1)

Bán ETH vào Pool A làm giá ETH giảm; bán stETH vào Pool B làm tỷ giá stETH/ETH giảm; `k` được bảo toàn.

**Why this priority**: Cơ chế phản hồi giá của SC03.

**Independent Test**: UT-06, UT-07, UT-08, UT-15.

**Acceptance Scenarios**:

1. **Given** pool x = 100, y = 10,000, **When** bán dx = 10, **Then** nhận `10000×10/110 = 909.0909` y; reserves mới `110` và `9,090.9091`; k = 1,000,000 không đổi (UT-06).
2. **Given** Pool A mặc định, **When** bán ETH vào Pool A, **Then** giá ETH/USD sau swap thấp hơn trước (UT-07).
3. **Given** Pool B mặc định, **When** bán stETH vào Pool B, **Then** `steth_eth_ratio` sau swap thấp hơn trước (UT-08).
4. **Given** Pool A sau shock 15% (x = 27,116.3072, y = 69,146,583.43), **When** bán 72.0588 ETH, **Then** nhận ≈ 183,262.997 USDC và giá ETH giảm từ 2,550 xuống ≈ 2,536.50.

---

### User Story 3 - Cú sốc giá giữ nguyên k (Priority: P1)

Cú sốc shock_pct đưa giá Pool A về `P×(1−shock)` mà không đổi `k_A`; Pool B không đổi.

**Why this priority**: Định nghĩa của cú sốc ngoại sinh.

**Independent Test**: UT-10.

**Acceptance Scenarios**:

1. **Given** Pool A mặc định (k_A = 1.875e12) và shock 15%, **When** áp dụng shock, **Then** `reserve_A_ETH = 27,116.3072`, `reserve_A_USDC = 69,146,583.43`, giá ETH = 2,550.00, `k_A` giữ nguyên (sai số tương đối ≤ 1e-9).
2. **Given** shock vừa áp dụng, **When** xem Pool B, **Then** reserves Pool B không đổi, `steth_eth_ratio = 0.99` và `steth_price_usd = 2,550×0.99 = 2,524.5`; discount vẫn 1%.

---

### Edge Cases

- `dx ≤ 0` → từ chối (không bán 0 hoặc âm); caller SHALL bỏ qua swap khi `collateral_seized ≤ epsilon` (SRS §10.4).
- Reserve không bao giờ ≤ 0 sau swap; nếu kết quả không hữu hạn/≤ 0 → từ chối giao dịch.
- Pool nhỏ (TVL tối thiểu 10M/5M): cùng lượng bán gây trượt giá lớn hơn; không có trần giá — vẫn tính đúng.
- Discount âm (stETH đắt hơn ETH, tức `steth_eth_ratio > 1`): giữ nguyên giá trị âm, KHÔNG cắt về 0.
- `shock_pct = 0` → áp dụng shock không đổi gì (reserves giữ nguyên trong sai số).

## Requirements *(mandatory)*

### Công thức

- BR-06: `P = 3000`, `r = 1 − 0.01 = 0.99`. Pool A: `reserve_A_USDC = A/2`, `reserve_A_ETH = (A/2)/P`. Pool B: `reserve_B_ETH = (B/2)/P`, `reserve_B_stETH = (B/2)/(P×r)`.
- BR-05: bán `dx` token x: `amount_y_out = y×dx/(x+dx)`; `reserve_x ← x+dx`; `reserve_y ← y − amount_y_out`. KHÔNG phí.
- BR-09: `eth_price_usd = reserve_A_USDC / reserve_A_ETH`; `steth_eth_ratio = reserve_B_ETH / reserve_B_stETH`; `steth_price_usd = eth_price_usd × steth_eth_ratio`; `steth_discount_pct = (1 − steth_price_usd/eth_price_usd) × 100`.
- BR-07 (phần pool): `P_after = P×(1−shock)`; `new_reserve_A_ETH = sqrt(k_A/P_after)`; `new_reserve_A_USDC = sqrt(k_A×P_after)`.
- Đơn vị: Pool A `token_x = ETH`, `token_y = USDC`; Pool B `token_x = stETH`, `token_y = ETH`.

### Functional Requirements (EARS)

- **FR-001** *(Ubiquitous)*: THE system SHALL khởi tạo Pool A và Pool B theo BR-06 từ `pool_a_tvl_usd`, `pool_b_tvl_usd`, `initial_eth_price_usd = 3000`, `initial_steth_discount_pct = 0.01`.
- **FR-002** *(Ubiquitous)*: THE system SHALL mô hình `AMMPool` với `name ∈ {ETH_USDC, STETH_ETH}`, `token_x`, `token_y`, `reserve_x`, `reserve_y`.
- **FR-003** *(Ubiquitous)*: THE system SHALL cung cấp `spot_price_y_per_x() = reserve_y / reserve_x`.
- **FR-004** *(Event)*: WHEN `sell_x(amount_x)` được gọi với `amount_x > 0`, THE system SHALL tính `amount_y_out` theo BR-05, cập nhật reserves và trả `amount_y_out`.
- **FR-005** *(Unwanted)*: IF `amount_x ≤ 0` hoặc không hữu hạn, THEN THE system SHALL từ chối giao dịch và SHALL NOT đổi reserves.
- **FR-006** *(Ubiquitous)*: THE system SHALL luôn giữ `reserve_x > 0` và `reserve_y > 0`; IF một giao dịch làm reserve ≤ 0 hoặc không hữu hạn, THEN THE system SHALL từ chối giao dịch.
- **FR-007** *(Ubiquitous)*: THE system SHALL giữ `k = reserve_x × reserve_y` không đổi qua `sell_x` với sai số tương đối ≤ 1e-9.
- **FR-008** *(Ubiquitous)*: THE system SHALL tính `eth_price_usd`, `steth_eth_ratio`, `steth_price_usd`, `steth_discount_pct` theo BR-09 từ reserves hiện tại; discount SHALL NOT bị cắt về 0 khi âm.
- **FR-009** *(Event)*: WHEN cú sốc ngoại sinh được áp dụng với `shock`, THE system SHALL cân bằng lại Pool A theo BR-07 giữ nguyên `k_A` (sai số tương đối ≤ 1e-9) và SHALL NOT thay đổi Pool B.
- **FR-010** *(Ubiquitous)*: THE system SHALL cho phép nhân bản độc lập (deepcopy hoặc `reset()`) trạng thái 2 pool để mỗi kịch bản có bản riêng, sao cho giao dịch ở bản này SHALL NOT ảnh hưởng bản khác.
- **FR-011** *(Ubiquitous)*: THE system SHALL NOT cho phép sửa giá bằng phép gán trực tiếp; giá chỉ thay đổi do `sell_x` hoặc do cân bằng cú sốc FR-009.
- **FR-012** *(Ubiquitous)*: THE system SHALL KHÔNG tính phí giao dịch, phí gas, hay trượt giá ngoài 2 pool; SHALL KHÔNG có arbitrage/phục hồi giá tự động.
- **FR-013** *(Ubiquitous)*: THE system SHALL cung cấp giá tài sản theo loại collateral cho spec 003: ETH → `eth_price_usd`; stETH → `steth_price_usd`.

### Key Entities

- **AMMPool**: một pool constant-product.
- **MarketState**: Pool A + Pool B của một kịch bản; suy ra giá ETH, stETH, discount.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: UT-09 khớp: ETH 3000, stETH 2970, discount 1.0% (sai số 1e-9).
- **SC-002**: UT-06 khớp: 909.0909 và reserves 110 / 9090.9091.
- **SC-003**: UT-10 khớp: giá ngay sau shock 15% = 2,550.00; `k_A` sai lệch tương đối ≤ 1e-9.
- **SC-004**: 100% giao dịch trong bộ test ngẫu nhiên giữ reserve dương và k không đổi trong 1e-9.

## Out of Scope

- Phí swap (0.3% của Uniswap thật), gas, MEV, thêm/rút thanh khoản, concentrated liquidity, Curve.
- Oracle độc lập, TWAP, arbitrage hay tự phục hồi giá sau cú sốc.
- Swap hai chiều (mua token); chỉ có `sell_x`.

## Assumptions *(quyết định đã chốt)*

- Sai số tương đối cho `k` là 1e-9 (SRS chỉ nói "tolerance hợp lý").
- `sell_x` với `amount_x ≤ 0` bị từ chối; lớp gọi tự bỏ qua swap khi lượng ≤ epsilon.
- Trong SC03, giá stETH tính qua Pool A sau mỗi giao dịch; không có thay đổi Pool B khi shock (SRS BR-07).

## Traceability

SRS §7.2 → FR-002, FR-003; BR-05 → FR-004…FR-007; BR-06 → FR-001; BR-07 → FR-009; BR-09 → FR-008, FR-013; FR-05 → toàn bộ; UT-06…UT-10, UT-15.

