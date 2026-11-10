# Feature Specification: Cấu hình & Kiểm tra tham số mô phỏng

**Feature Branch**: `001-simulation-config`
**Created**: 2026-11-10
**Status**: Draft
**Input**: User description: "Người dùng nhập 6 tham số trên sidebar, kiểm tra hợp lệ trước khi chạy, nút Run Simulation / Reset Defaults; các hằng số nội bộ cố định và được kiểm tra nhất quán." (requirements.md §6, §12.1, §12.3, FR-01, NFR-07)

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Chạy mô phỏng với tham số mặc định (Priority: P1)

Sinh viên mở ứng dụng, thấy sidebar có 6 tham số đã điền sẵn giá trị mặc định, bấm **Run Simulation** và nhận kết quả của cả 3 kịch bản.

**Why this priority**: Đây là đường chạy chính của buổi demo; không có nó thì không có sản phẩm.

**Independent Test**: Mở ứng dụng, không đổi gì, bấm Run → engine nhận đúng `{shock_pct: 15, pool_a_tvl_usd: 150_000_000, pool_b_tvl_usd: 80_000_000, num_agents: 100, max_blocks: 30, random_seed: 42}`.

**Acceptance Scenarios**:

1. **Given** ứng dụng vừa mở, **When** người dùng nhìn sidebar, **Then** thấy đúng 6 điều khiển với giá trị: ETH Price Shock = 15 (%), Pool A TVL = $150M, Pool B TVL = $80M, Number of Borrowers = 100, Maximum Simulation Blocks = 30, Random Seed = 42.
2. **Given** cấu hình hợp lệ, **When** bấm **Run Simulation**, **Then** cả SC01, SC02, SC03 được chạy từ cùng một cấu hình và cùng một seed.
3. **Given** một lần chạy đã xong, **When** người dùng đổi tham số rồi bấm Run lần nữa, **Then** kết quả hiển thị được thay bằng kết quả của cấu hình mới mà không cần khởi động lại ứng dụng.

---

### User Story 2 - Bị chặn khi nhập tham số sai (Priority: P1)

Người dùng (hoặc code gọi engine trực tiếp) đưa tham số ngoài miền hợp lệ; hệ thống từ chối chạy, nêu rõ tham số nào sai, và không crash.

**Why this priority**: SRS §6.3 và NFR-07 yêu cầu "không chạy mô phỏng, không crash".

**Independent Test**: Gọi bước validate với `num_agents = 101` → nhận lỗi nêu `num_agents`, giá trị `101`, miền hợp lệ; engine không bắt đầu chạy.

**Acceptance Scenarios**:

1. **Given** `num_agents = 101`, **When** validate, **Then** có lỗi "Number of Borrowers phải là số chẵn trong khoảng 20–200 (đã nhập: 101)".
2. **Given** `shock_pct = 45`, **When** validate, **Then** có lỗi nêu miền 0–40.
3. **Given** đồng thời `shock_pct = 45` và `max_blocks = 3`, **When** validate, **Then** kết quả chứa CẢ HAI lỗi (không dừng ở lỗi đầu).
4. **Given** có ít nhất một lỗi, **When** người dùng nhìn giao diện, **Then** thông báo lỗi hiển thị và không có kết quả mới nào được sinh ra; kết quả của lần chạy trước (nếu có) KHÔNG bị xóa.

---

### User Story 3 - Reset về mặc định (Priority: P2)

Người dùng bấm **Reset Defaults** để đưa cả 6 điều khiển về giá trị chuẩn.

**Why this priority**: Tiện cho demo nhiều lần; yêu cầu bắt buộc trong FR-01 nhưng không chặn đường chạy chính.

**Independent Test**: Đổi cả 6 tham số, bấm Reset Defaults → 6 giá trị trở về bảng ở Story 1.

**Acceptance Scenarios**:

1. **Given** 6 tham số đã bị đổi, **When** bấm Reset Defaults, **Then** 6 điều khiển hiển thị lại giá trị mặc định của Story 1 scenario 1.
2. **Given** vừa Reset, **When** quan sát vùng kết quả, **Then** kết quả của lần chạy trước KHÔNG tự chạy lại (Reset không kích hoạt Run).

---

### Edge Cases

- `shock_pct = 0` hợp lệ (SRS §10.4: các kịch bản phải giống nhau về giá).
- `shock_pct = 40` hợp lệ; giá sau shock = 3000 × 0.6 = 1800 > 0.
- `max_blocks = 5` và `50` hợp lệ (biên).
- `random_seed = 0` và `99999` hợp lệ; `-1`, `100000`, `3.5`, chuỗi → không hợp lệ.
- Tham số thiếu (`None`/vắng key) → lỗi "thiếu tham số <tên>", không `KeyError`.
- `pool_a_tvl_usd = 0` hoặc âm → lỗi "phải dương" và vượt miền.
- Đổi slider KHÔNG tự chạy mô phỏng (SRS §12.3); chỉ Run mới chạy.
- Giá trị `bool` (True/False) KHÔNG được chấp nhận cho tham số số.

## Requirements *(mandatory)*

### Bảng tham số người dùng (P-01…P-06) — nguồn: SRS §6.1

| ID | Khóa config | Nhãn UI | Kiểu | Mặc định | Miền hợp lệ (engine) | Bước UI | Đơn vị |
|---|---|---|---|---:|---|---|---|
| P-01 | `shock_pct` | ETH Price Shock (%) | số thực | 15 | 0 ≤ x ≤ 40 | 5 | % (số phần trăm, vd 15 nghĩa 15%) |
| P-02 | `pool_a_tvl_usd` | Pool A TVL — ETH/USDC | số thực | 150,000,000 | 10,000,000 ≤ x ≤ 300,000,000 | 10,000,000 | USD |
| P-03 | `pool_b_tvl_usd` | Pool B TVL — stETH/ETH | số thực | 80,000,000 | 5,000,000 ≤ x ≤ 200,000,000 | 5,000,000 | USD |
| P-04 | `num_agents` | Number of Borrowers | số nguyên | 100 | chẵn, 20 ≤ x ≤ 200 | 20 | Agent |
| P-05 | `max_blocks` | Maximum Simulation Blocks | số nguyên | 30 | 5 ≤ x ≤ 50 | 1 | block |
| P-06 | `random_seed` | Random Seed | số nguyên | 42 | 0 ≤ x ≤ 99,999 | 1 (ô nhập số) | — |

### Bảng hằng số cố định (C-01…C-10) — nguồn: SRS §6.2, không hiển thị trên UI

| ID | Tên | Giá trị |
|---|---|---:|
| C-01 | `initial_eth_price_usd` | 3000 |
| C-02 | `initial_steth_discount_pct` | 1% (lưu nội bộ 0.01) |
| C-03 | `lt` | 0.80 |
| C-04 | `initial_ltv_min` | 0.55 |
| C-05 | `initial_ltv_max` | 0.72 |
| C-06 | `collateral_value_min_usd` | 250,000 |
| C-07 | `collateral_value_max_usd` | 1,000,000 |
| C-08 | `close_factor` | 0.50 |
| C-09 | `liquidation_bonus` | 0.05 |
| C-10 | `epsilon` | 1e-9 |

### Functional Requirements (EARS)

- **FR-001** *(Ubiquitous)*: THE system SHALL hiển thị sidebar gồm đúng 6 điều khiển P-01…P-06 với nhãn, mặc định, bước như bảng trên, cộng 2 nút **Run Simulation** và **Reset Defaults**.
- **FR-002** *(Ubiquitous)*: THE system SHALL lưu mọi tỷ lệ phần trăm nội bộ dưới dạng số thập phân (`15%` → `0.15`; `initial_steth_discount_pct 1%` → `0.01`). Khóa `shock_pct` trong config nhận SỐ PHẦN TRĂM (15), và chuyển đổi `shock = shock_pct / 100` ngay khi dùng.
- **FR-003** *(Event)*: WHEN người dùng bấm **Run Simulation**, THE system SHALL validate cấu hình; IF không có lỗi THEN hiển thị spinner trong lúc tính và gọi chạy 3 kịch bản; ELSE hiển thị danh sách lỗi và KHÔNG chạy.
- **FR-004** *(Event)*: WHEN người dùng bấm **Reset Defaults**, THE system SHALL đặt 6 điều khiển về giá trị mặc định và SHALL NOT tự chạy mô phỏng.
- **FR-005** *(Unwanted)*: IF một tham số nằm ngoài miền hợp lệ ở bảng P-01…P-06, THEN THE system SHALL tạo lỗi có đủ 3 thông tin: nhãn tham số, giá trị đã nhập, miền hợp lệ. Mẫu thông báo: `"<Nhãn> không hợp lệ: đã nhập <giá trị>, yêu cầu <miền>."`.
- **FR-006** *(Unwanted)*: IF `num_agents` không phải số nguyên chẵn, THEN THE system SHALL từ chối với lỗi nêu rõ "phải là số chẵn" (để chia đều ETH/stETH).
- **FR-007** *(Unwanted)*: IF nhiều tham số cùng sai, THEN THE system SHALL trả về TẤT CẢ lỗi trong một lần validate (không dừng ở lỗi đầu tiên).
- **FR-008** *(Unwanted)*: IF cấu hình thiếu khóa hoặc có giá trị không phải số (None, chuỗi, bool, NaN, ∞), THEN THE system SHALL báo lỗi cho khóa đó thay vì ném ngoại lệ không kiểm soát.
- **FR-009** *(Ubiquitous)*: THE system SHALL kiểm tra các ràng buộc của hằng số: `initial_eth_price_usd > 0`, `pool_a_tvl_usd > 0`, `pool_b_tvl_usd > 0`, và `0 ≤ initial_ltv_min ≤ initial_ltv_max < lt < 1`; WHERE ràng buộc bị vi phạm THE system SHALL báo lỗi cấu hình hằng số và không chạy.
- **FR-010** *(State)*: WHILE người dùng chỉ đổi slider/ô nhập mà chưa bấm Run, THE system SHALL KHÔNG tự chạy lại mô phỏng và SHALL giữ nguyên kết quả đang hiển thị.
- **FR-011** *(Ubiquitous)*: THE system SHALL cho phép chạy lại nhiều lần trong một phiên mà không cần khởi động lại; kết quả mới thay hoàn toàn kết quả cũ.
- **FR-012** *(Ubiquitous)*: THE system SHALL áp dụng CÙNG validation cho cấu hình gọi trực tiếp vào engine (không phụ thuộc UI), để engine chạy độc lập vẫn an toàn.
- **FR-013** *(Ubiquitous)*: THE system SHALL luôn hiển thị dòng ghi chú: **"Dữ liệu giả lập phục vụ nghiên cứu; không phải dự báo hoặc số liệu thị trường thực."** (SRS §12.3).
- **FR-014** *(Optional)*: WHERE một kết quả đã tồn tại và người dùng chạy lại với cấu hình lỗi, THE system SHALL giữ kết quả cũ trên màn hình cùng với thông báo lỗi.

### Key Entities

- **SimulationConfig**: 6 tham số P-01…P-06 đã validate; không chứa hằng số.
- **FixedConstants**: C-01…C-10, cố định trong mã nguồn.
- **ValidationError**: (tên tham số, giá trị nhập, miền hợp lệ, thông điệp).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Người dùng chạy được demo từ trạng thái mới mở bằng đúng 1 thao tác (bấm Run) và nhận kết quả của 3 kịch bản.
- **SC-002**: 100% đầu vào nằm ngoài miền (kiểm bằng bộ giá trị biên ± 1 bước cho cả 6 tham số) bị từ chối với thông báo đủ 3 thông tin; 0 trường hợp crash.
- **SC-003**: 100% đầu vào trong miền (gồm cả các giá trị biên) được chấp nhận.
- **SC-004**: Sau Reset Defaults, 6/6 điều khiển khớp bảng mặc định.

## Out of Scope

- Không hiển thị/chỉnh các hằng số C-01…C-10 trên UI.
- Không lưu cấu hình giữa các phiên, không preset, không tự chạy khi đổi slider.
- Không đăng nhập, phân quyền, API server.

## Assumptions *(quyết định đã chốt để tránh mơ hồ — cần xác nhận)*

- SRS ghi bước slider nhưng không ghi bước cho TVL: chọn Pool A bước 10M (10…300M, chứa mặc định 150M), Pool B bước 5M (5…200M, chứa mặc định 80M).
- Engine chấp nhận mọi số thực trong miền cho `shock_pct`, mọi số chẵn trong 20–200 cho `num_agents` (bước 5 / 20 chỉ là bước của UI). Lý do: SRS §6.3 chỉ bắt buộc "số chẵn", bước thuộc §6.1 (UI).
- `shock_pct` trong config dùng đơn vị phần trăm (15), nhất quán với ví dụ SRS §15.2.
- Không auto-run khi đổi slider (SRS §12.3).

## Traceability

SRS §6.1 → bảng P; §6.2 → bảng C; §6.3 → FR-005…FR-009; §12.1 → FR-001; §12.3 → FR-003, FR-010, FR-013; FR-01 → toàn bộ; NFR-07 → FR-008, FR-012.

