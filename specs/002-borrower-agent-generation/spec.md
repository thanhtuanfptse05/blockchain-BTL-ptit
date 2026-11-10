# Feature Specification: Sinh Borrower Agents

**Feature Branch**: `002-borrower-agent-generation`
**Created**: 2026-11-10
**Status**: Draft
**Input**: User description: "Sinh danh sách Borrower Agents (mặc định 100: 50 ETH + 50 stETH) tái lập được theo seed, mỗi Agent có collateral, debt, LTV ban đầu hợp lệ và HF > 1." (requirements.md §7.1, §10.1, FR-02, IN-03, UT-12)

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Danh sách Agent mặc định (Priority: P1)

Với cấu hình mặc định, hệ thống tạo đúng 100 Agent: 50 thế chấp ETH và 50 thế chấp stETH, mọi Agent an toàn (HF > 1).

**Why this priority**: Mọi kịch bản đều xuất phát từ danh sách này.

**Independent Test**: Sinh với `num_agents = 100, seed = 42` → đếm 100 Agent, 50 ETH, 50 stETH, `agent_id` = 1…100 không trùng, mọi `HF > 1`.

**Acceptance Scenarios**:

1. **Given** cấu hình mặc định, **When** sinh Agent, **Then** có đúng 100 Agent; `agent_id` 1…50 là ETH, 51…100 là stETH.
2. **Given** danh sách vừa sinh, **When** kiểm tra từng Agent, **Then** `collateral_amount > 0`, `debt_usdc > 0`, `0.55 ≤ initial_ltv ≤ 0.72`, `status = ACTIVE`, `ever_liquidated = False`, `liquidation_count = 0`, `liquidation_threshold = 0.80`.
3. **Given** giá ban đầu (ETH 3000, stETH 2970), **When** tính HF, **Then** mọi Agent có `HF = 0.80 / initial_ltv ≥ 0.80/0.72 ≈ 1.1111 > 1`.

---

### User Story 2 - Tái lập theo seed (Priority: P1)

Chạy lại cùng seed và cùng `num_agents` luôn ra cùng danh sách; đổi seed ra danh sách khác; đổi tham số pool KHÔNG đổi danh sách Agent.

**Why this priority**: Bảo đảm so sánh công bằng SC01/SC02/SC03 và thí nghiệm ST-05/ST-06.

**Independent Test**: Sinh 2 lần cùng cấu hình → so sánh từng trường, bằng nhau tuyệt đối.

**Acceptance Scenarios**:

1. **Given** hai lần sinh cùng `seed=42, num_agents=100`, **When** so sánh, **Then** mọi trường của mọi Agent giống hệt nhau (UT-12).
2. **Given** `seed=42` và `seed=43`, **When** so sánh `collateral_amount`/`debt_usdc`, **Then** danh sách khác nhau.
3. **Given** cùng seed nhưng `pool_b_tvl_usd` khác, **When** sinh Agent, **Then** danh sách Agent KHÔNG đổi (Agent không phụ thuộc TVL pool).

---

### User Story 3 - Số lượng Agent thay đổi được (Priority: P2)

Người dùng chọn `num_agents` từ 20 đến 200; hệ thống chia đều ETH/stETH.

**Why this priority**: Tham số P-04.

**Independent Test**: `num_agents = 20` → 10 ETH + 10 stETH; `200` → 100 + 100.

**Acceptance Scenarios**:

1. **Given** `num_agents = 20`, **When** sinh, **Then** 10 Agent ETH (id 1–10) và 10 Agent stETH (id 11–20).
2. **Given** `num_agents = 200`, **Then** 100 ETH (id 1–100) và 100 stETH (id 101–200).

---

### Edge Cases

- `num_agents` lẻ → không đến bước sinh (bị chặn ở spec 001).
- Nếu vì lỗi bất kỳ có Agent với `HF ≤ 1` lúc khởi tạo → báo lỗi "lỗi sinh dữ liệu" nêu `agent_id`, dừng, không chạy (SRS §10.1 bước 6).
- Hằng số sai (`ltv_max ≥ lt`) → chặn từ spec 001, không sinh.

## Requirements *(mandatory)*

### Thuật toán sinh (xác định hoàn toàn)

1. Đặt `n = num_agents`, `half = n / 2`, `P = 3000`, `r = 0.99`, `P_steth0 = P × r = 2970`.
2. Tạo một bộ sinh ngẫu nhiên riêng `random.Random(random_seed)` — chỉ dùng cho việc sinh Agent.
3. Với `agent_id` từ 1 đến n theo thứ tự tăng dần: loại = ETH nếu `agent_id ≤ half`, ngược lại stETH. Rút theo đúng thứ tự: (a) `collateral_value_usd = rng.uniform(250000, 1000000)`; (b) `initial_ltv = rng.uniform(0.55, 0.72)`.
4. `initial_price = 3000` nếu ETH, `2970` nếu stETH. `collateral_amount = collateral_value_usd / initial_price`. `debt_usdc = collateral_value_usd × initial_ltv`.
5. Trạng thái: `status = ACTIVE`, `ever_liquidated = False`, `liquidation_count = 0`, `liquidation_threshold = 0.80`.

### Functional Requirements (EARS)

- **FR-001** *(Ubiquitous)*: THE system SHALL sinh đúng `num_agents` Agent, trong đó `num_agents/2` Agent ETH có `agent_id` 1…`num_agents/2` và `num_agents/2` Agent stETH có `agent_id` `num_agents/2+1`…`num_agents`.
- **FR-002** *(Ubiquitous)*: THE system SHALL gán `agent_id` là số nguyên duy nhất từ 1 đến N.
- **FR-003** *(Ubiquitous)*: THE system SHALL sinh `collateral_value_usd` và `initial_ltv` bằng `random.Random(random_seed)` theo thuật toán trên (phân phối đều, thứ tự rút cố định).
- **FR-004** *(Ubiquitous)*: THE system SHALL tính `collateral_amount = collateral_value_usd / initial_asset_price_usd` (ETH: 3000; stETH: 2970) và `debt_usdc = collateral_value_usd × initial_ltv`.
- **FR-005** *(Ubiquitous)*: THE system SHALL khởi tạo mọi Agent với `status = ACTIVE`, `ever_liquidated = False`, `liquidation_count = 0`, `liquidation_threshold = 0.80`, và lưu `initial_ltv`.
- **FR-006** *(Unwanted)*: IF sau khi sinh có Agent với `HF ≤ 1` tại giá ban đầu, THEN THE system SHALL báo lỗi "lỗi sinh dữ liệu" kèm `agent_id`, SHALL NOT trả danh sách và SHALL NOT chạy mô phỏng.
- **FR-007** *(Ubiquitous)*: THE system SHALL cho kết quả sinh độc lập với `shock_pct`, `pool_a_tvl_usd`, `pool_b_tvl_usd`, `max_blocks`.
- **FR-008** *(Ubiquitous)*: THE system SHALL cung cấp danh sách Agent gốc dưới dạng không bị kịch bản nào sửa; mỗi kịch bản SHALL nhận một bản sao sâu (deepcopy) độc lập (xem spec 006).
- **FR-009** *(Ubiquitous)*: THE system SHALL cho `BorrowerAgent` có đủ thuộc tính: `agent_id:int`, `collateral_type:str ∈ {ETH, stETH}`, `collateral_amount:float`, `debt_usdc:float`, `initial_ltv:float`, `liquidation_threshold:float`, `ever_liquidated:bool`, `liquidation_count:int`, `status ∈ {ACTIVE, REPAID, BAD_DEBT}`.
- **FR-010** *(Ubiquitous)*: THE system SHALL xây `BorrowerAgent` như một Agent của framework ABM Mesa 3.x (SRS §4.1, §16 mục 1).

### Key Entities

- **BorrowerAgent**: người vay giả lập, đúng 1 loại collateral, chỉ vay USDC, không tự vay thêm/nạp/rút/trả nợ trong quá trình chạy (SRS §5.2).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Mặc định sinh chính xác 100 Agent = 50 ETH + 50 stETH, 100% có HF > 1.
- **SC-002**: 2 lần sinh cùng cấu hình cho danh sách giống nhau 100% trường.
- **SC-003**: Với mọi `num_agents` chẵn trong 20–200, tỷ lệ ETH:stETH đúng 1:1.
- **SC-004**: 100% Agent có `0.55 ≤ initial_ltv ≤ 0.72` và `250,000 ≤ collateral_value_usd ≤ 1,000,000` (tính tại giá ban đầu).

## Out of Scope

- Agent tự vay thêm, nạp/rút collateral, trả nợ chủ động, nhiều loại collateral/Agent, thêm Agent sau khi bắt đầu (SRS §5.1, 5.2, 5.11).
- Phân phối ngẫu nhiên khác đều, hàng nghìn Agent, mạng tương tác Agent.
- Lãi vay.

## Assumptions *(quyết định đã chốt)*

- SRS nói "chia đều" nhưng không nêu thứ tự: chốt id 1…N/2 = ETH, N/2+1…N = stETH. Hệ quả: khi xử lý theo `agent_id`, Agent ETH luôn được xét trước Agent stETH trong cùng block.
- "Ngẫu nhiên trong khoảng" = phân phối đều liên tục (`uniform`); thứ tự rút (value rồi ltv) cố định.
- Agent stETH dùng giá ban đầu 2970 USD (= 3000 × 0.99) để đổi giá trị USD sang số token (BR-06).

## Traceability

SRS §7.1 → FR-009; §10.1 → thuật toán, FR-001…FR-006; FR-02 → toàn bộ; IN-03; UT-12 → User Story 2; §4.1 → FR-010.

