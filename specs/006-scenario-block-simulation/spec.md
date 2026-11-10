# Feature Specification: Kịch bản SC01/SC02/SC03 và vòng lặp Simulation Block

**Feature Branch**: `006-scenario-block-simulation`
**Created**: 2026-11-10
**Status**: Draft
**Input**: User description: "Chạy 3 kịch bản (Baseline, Direct Shock, Contagion) trên cùng danh sách Agent và cùng trạng thái pool ban đầu, theo từng simulation block từ 0 đến max_blocks; chỉ SC03 có phản hồi giá do bán collateral; ghi BlockResult, LiquidationEvent và SimulationResult; cung cấp hàm run_all_scenarios(config)." (requirements.md §4.3, §7.3–7.5, §9, §10, BR-07, BR-08, BR-10, BR-11, FR-06, §15.1, UT-10, UT-11, UT-14, ST-01…ST-07)

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Một lần gọi cho ra 3 kịch bản (Priority: P1)

Người gọi (UI hoặc test) đưa một config hợp lệ và nhận về `{SC01, SC02, SC03}` mỗi cái là một `SimulationResult` đầy đủ.

**Why this priority**: Hợp đồng tích hợp giữa 2 thành viên (SRS §15.1).

**Independent Test**: Gọi `run_all_scenarios(config)` không cần Streamlit → 3 khóa, mỗi cái có `block_results` đúng `max_blocks + 1` dòng (UT-14).

**Acceptance Scenarios**:

1. **Given** config mặc định, **When** gọi `run_all_scenarios`, **Then** nhận đúng 3 khóa `SC01`, `SC02`, `SC03`, mỗi `block_results` có 31 dòng (block 0…30).
2. **Given** config không hợp lệ, **When** gọi, **Then** lỗi validate (spec 001) và không có kết quả một phần.
3. **Given** hai lần gọi cùng config, **Then** kết quả của cả 3 kịch bản giống hệt nhau (ST-07).

---

### User Story 2 - SC01 là mốc ổn định (Priority: P1)

SC01: không shock, không thanh lý, giá và discount phẳng qua mọi block.

**Why this priority**: Chứng minh môi trường ổn định (SRS §9).

**Independent Test**: ST-01, UT-11.

**Acceptance Scenarios**:

1. **Given** config mặc định, **When** chạy SC01, **Then** ở mọi block: `eth_price_usd = 3000`, `steth_price_usd = 2970`, `steth_discount_pct = 1.0`, `liquidations_total = 0`, `bad_debt_usd = 0`, `liquidated_agents_unique_cumulative = 0`.
2. **Given** `shock_pct = 0`, **When** chạy cả 3 kịch bản, **Then** cả 3 giống nhau về giá và đều 0 thanh lý (SRS §10.4).

---

### User Story 3 - SC02 chịu shock nhưng giá không phản hồi (Priority: P1)

SC02: shock đầu block 1 đưa giá ETH xuống `3000×(1−shock)`; thanh lý vẫn diễn ra nhưng KHÔNG bán collateral lên AMM nên giá giữ nguyên ở mức sau shock.

**Why this priority**: Nhóm đối chứng của SC03.

**Independent Test**: ST-02, UT-10.

**Acceptance Scenarios**:

1. **Given** `shock_pct = 15`, **When** chạy SC02, **Then** từ block 1 đến `max_blocks`: `eth_price_usd = 2550`, `steth_price_usd = 2524.5`, `steth_discount_pct = 1.0` (không đổi dù có thanh lý).
2. **Given** SC02, **When** có thanh lý, **Then** nợ/collateral của Agent đổi nhưng reserves 2 pool không đổi sau cú sốc.

---

### User Story 4 - SC03 lây lan qua AMM (Priority: P1)

SC03: cùng shock như SC02; collateral thu giữ được bán qua AMM theo BR-08; giá thay đổi và Agent khác bị ảnh hưởng ở lần xét sau.

**Why this priority**: Đây là hiện tượng nghiên cứu cốt lõi.

**Independent Test**: ST-03, ST-04.

**Acceptance Scenarios**:

1. **Given** SC03 có thanh lý Agent ETH, **When** sự kiện xảy ra, **Then** toàn bộ ETH thu giữ được bán vào Pool A; Pool A reserves đổi; giá ETH giảm.
2. **Given** SC03 có thanh lý Agent stETH, **When** sự kiện xảy ra, **Then** stETH thu giữ bán vào Pool B lấy ETH; toàn bộ ETH nhận được bán vào Pool A; cả `steth_eth_ratio` và `eth_price_usd` giảm.
3. **Given** SC02 và SC03 cùng config, **When** so sánh Agent ban đầu, **Then** giống nhau về số lượng, nhóm tài sản, collateral, nợ (ST-04).
4. **Given** SC03 không khuếch đại so với SC02, **When** báo cáo kết quả, **Then** hệ thống vẫn hiển thị đúng số liệu thật; KHÔNG ép `SC03 > SC02`.

---

### Edge Cases

- Không còn thanh lý ở các block sau: các block vẫn có dòng dữ liệu, giữ nguyên giá, `liquidations_* = 0`, chỉ số tích lũy giữ nguyên (SRS §10.3).
- Một Agent xuất hiện trong danh sách đầu block nhưng đã an toàn lúc tới lượt (do giá phục hồi nhờ… không có phục hồi — nhưng do thanh lý Agent trước ở SC03 giá chỉ giảm): vẫn PHẢI kiểm tra lại `is_liquidatable` ngay trước giao dịch.
- Agent bị thanh lý ở block t: không bị thanh lý lần nữa trong block t dù HF còn < 1; có thể bị ở block t+1.
- Agent mới nguy hiểm vì giá giảm TRONG block: chỉ được xét từ block kế tiếp.
- Pool nhỏ (TVL tối thiểu) → giá có thể giảm rất mạnh; không đưa reserve về ≤ 0.
- `collateral_seized ≤ epsilon` → bỏ qua swap.
- Shock tại block 1 chỉ một lần; mọi block ≥ 2 không có shock.

## Requirements *(mandatory)*

### Quy ước thứ tự xử lý một block (SRS §10.2–10.3, xác định)

Với mỗi kịch bản, trạng thái khởi tạo là bản sao sâu của danh sách Agent gốc và của 2 pool gốc. Với `block` từ 0 đến `max_blocks`:

1. **block = 0**: chỉ ghi trạng thái ban đầu (không shock, không thanh lý); sang block tiếp theo.
2. **block ≥ 1**:
   a. Nếu `block == 1` và kịch bản ∈ {SC02, SC03}: áp dụng cú sốc ngoại sinh đúng một lần (spec 005 FR-009). SC01 KHÔNG shock (coi `shock = 0`).
   b. Chốt `candidates` = Agent thỏa `is_liquidatable(price)` tại giá hiện hành, sắp theo `agent_id` tăng dần.
   c. Lần lượt từng Agent trong `candidates`: kiểm tra lại `is_liquidatable` với giá hiện hành NGAY TRƯỚC giao dịch; nếu còn đủ điều kiện, thanh lý (spec 004), gán `scenario` và `block` cho event, lưu event; nếu kịch bản là SC03, bán collateral thu giữ qua AMM theo BR-08 ngay lập tức (trước khi xét Agent kế).
   d. Ghi `BlockResult` của block (giá lấy từ reserves sau khi xử lý xong block).
3. Mỗi Agent tối đa 1 lần thanh lý mỗi block.
4. KHÔNG dừng sớm: luôn đủ `max_blocks + 1` dòng cho mỗi kịch bản.

### BR-08: đường bán collateral (SC03)

- Agent ETH: `sell_x(collateral_seized)` trên Pool A (ETH→USDC).
- Agent stETH: `eth_out = PoolB.sell_x(collateral_seized)` (stETH→ETH), rồi `PoolA.sell_x(eth_out)` (ETH→USDC) với TOÀN BỘ `eth_out`.
- Bỏ qua swap nếu lượng cần bán ≤ epsilon.

### Định nghĩa các cột BlockResult (SRS §7.4)

| Cột | Định nghĩa |
|---|---|
| `scenario` | `SC01`/`SC02`/`SC03` |
| `block` | số nguyên 0…max_blocks |
| `eth_price_usd` | `reserve_A_USDC / reserve_A_ETH` cuối block |
| `steth_price_usd` | `eth_price_usd × reserve_B_ETH/reserve_B_stETH` cuối block |
| `steth_discount_pct` | `(1 − steth_price_usd/eth_price_usd)×100` (có thể âm) |
| `liquidations_eth` / `liquidations_steth` | số event trong block có `asset = ETH` / `stETH` |
| `liquidations_total` | tổng 2 cột trên |
| `liquidated_agents_unique_cumulative` | số `agent_id` khác nhau có `ever_liquidated = True` tính đến hết block |
| `liquidation_debt_repaid_usd` | Σ `debt_repaid_usd` của event trong block |
| `liquidation_debt_repaid_cumulative_usd` | Σ `debt_repaid_usd` từ block 1 đến hết block hiện tại |
| `bad_debt_usd` | BR-10 tính từ trạng thái Agent cuối block |

Block 0: các cột `liquidations_*`, `liquidation_debt_repaid_*`, `liquidated_agents_unique_cumulative`, `bad_debt_usd` đều = 0.

### Cấu trúc SimulationResult (SRS §7.5)

`{scenario_id, parameters, block_results, liquidation_events, summary}`; `summary` gồm: `final_eth_price_usd`, `final_steth_price_usd`, `final_steth_discount_pct` (= giá trị ở block `max_blocks`), `liquidated_agents_unique` (= cumulative cuối), `liquidation_events_total` (= số event), `total_debt_repaid_usd` (= cumulative cuối), `bad_debt_usd` (= giá trị cuối).

### Functional Requirements (EARS)

- **FR-001** *(Ubiquitous)*: THE system SHALL cung cấp `run_all_scenarios(config: dict) -> {'SC01': SimulationResult, 'SC02': ..., 'SC03': ...}`, không phụ thuộc Streamlit.
- **FR-002** *(Unwanted)*: IF config không hợp lệ (spec 001), THEN THE system SHALL không chạy kịch bản nào và báo toàn bộ lỗi.
- **FR-003** *(Ubiquitous)*: THE system SHALL sinh danh sách Agent một lần (spec 002) và khởi tạo cặp pool một lần (spec 005), rồi cấp cho mỗi kịch bản MỘT BẢN SAO SÂU độc lập; SHALL NOT chia sẻ trạng thái có thể thay đổi giữa các kịch bản.
- **FR-004** *(Ubiquitous)*: THE system SHALL cho SC01/SC02/SC03 cùng `random_seed`, cùng Agent ban đầu, cùng pool ban đầu; chỉ khác quy tắc shock và phản hồi giá.
- **FR-005** *(State)*: WHILE kịch bản là SC01, THE system SHALL KHÔNG áp dụng shock, SHALL không có thanh lý (nếu Agent ban đầu an toàn) và giá/discount SHALL phẳng.
- **FR-006** *(Event)*: WHEN block = 1 AND kịch bản ∈ {SC02, SC03}, THE system SHALL áp dụng cú sốc `P_after = 3000 × (1 − shock_pct/100)` đúng một lần, ở đầu block, TRƯỚC khi chốt candidates.
- **FR-007** *(Ubiquitous)*: THE system SHALL KHÔNG áp dụng cú sốc ở bất kỳ block nào khác block 1 và SHALL KHÔNG có tự phục hồi giá, mua lại token hay arbitrage.
- **FR-008** *(Ubiquitous)*: THE system SHALL xử lý candidates theo `agent_id` tăng dần, chỉ chọn candidates ở đầu block và kiểm tra lại `is_liquidatable` ngay trước giao dịch của từng Agent.
- **FR-009** *(Ubiquitous)*: THE system SHALL thanh lý mỗi Agent tối đa một lần trong mỗi block.
- **FR-010** *(State)*: WHILE kịch bản là SC02, THE system SHALL KHÔNG bán collateral lên Pool A/B; giá thị trường SHALL giữ ở mức ngay sau cú sốc.
- **FR-011** *(Event)*: WHEN kịch bản là SC03 AND có thanh lý với `collateral_seized > epsilon`, THE system SHALL bán collateral qua AMM theo BR-08 ngay sau sự kiện đó và trước khi xét Agent kế tiếp.
- **FR-012** *(Event)*: WHEN SC03 thanh lý Agent stETH, THE system SHALL bán TOÀN BỘ ETH nhận từ Pool B vào Pool A, để một sự kiện gây áp lực lên cả hai pool.
- **FR-013** *(Ubiquitous)*: THE system SHALL tạo đúng `max_blocks + 1` bản ghi `BlockResult` cho mỗi kịch bản, block 0…`max_blocks`, trục thời gian giống nhau giữa 3 kịch bản.
- **FR-014** *(State)*: WHILE không còn thanh lý ở các block sau, THE system SHALL giữ nguyên giá và chỉ số tích lũy, đặt `liquidations_total = 0`.
- **FR-015** *(Ubiquitous)*: THE system SHALL tính các cột `BlockResult` đúng bảng định nghĩa; `bad_debt_usd` theo BR-10 từ trạng thái Agent (không cộng dồn).
- **FR-016** *(Ubiquitous)*: THE system SHALL tách `liquidation_events_total` (số event) khỏi `liquidated_agents_unique` (số Agent duy nhất); `liquidated_agents_unique ≤ num_agents`.
- **FR-017** *(Ubiquitous)*: THE system SHALL ghi mỗi `LiquidationEvent` với `scenario ∈ {SC02, SC03}` (SC01 không có event), `block ≥ 1`.
- **FR-018** *(Ubiquitous)*: THE system SHALL cung cấp trong `SimulationResult` đủ 5 phần: `scenario_id`, `parameters` (config đã validate), `block_results`, `liquidation_events`, `summary` (7 trường định nghĩa trên).
- **FR-019** *(Ubiquitous)*: THE system SHALL cho kết quả tái lập 100% với cùng seed và cấu hình.
- **FR-020** *(Ubiquitous)*: THE system SHALL tính mọi chỉ số từ Agent, reserves và event thực tế; SHALL NOT chứa câu lệnh gán cứng số Agent/discount/nợ xấu theo kịch bản.
- **FR-021** *(Ubiquitous)*: THE system SHALL cho phép kiểm tra giá "ngay sau shock, trước tác động thanh lý" (UT-10: 2,550 với shock 15%) — qua hàm áp dụng shock riêng hoặc ghi lại khi test.

### Key Entities

- **SimulationResult / BlockResult / LiquidationEvent**: như trên và spec 004.
- **Scenario**: SC01 (không shock), SC02 (shock, không phản hồi), SC03 (shock + phản hồi).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Mỗi kịch bản có đúng `max_blocks+1` dòng; 3 kịch bản cùng trục block.
- **SC-002**: SC01 mặc định: 0 thanh lý, giá phẳng ở mọi block (ST-01).
- **SC-003**: SC02 `shock=15`: giá ETH từ block 1 = 2,550 (±1e-6) và không đổi sau đó (ST-02).
- **SC-004**: Ở SC03, ít nhất 1 lần thanh lý ⇒ reserves bị đổi so với sau-shock; ở SC02 reserves không đổi sau shock (ST-03).
- **SC-005**: Hai lần chạy cùng config cho 100% giá trị giống nhau (ST-07).
- **SC-006**: 4 bất biến BR-11 thỏa ở mọi block: số dư không âm; `debt_repaid ≤ debt_before`; `unique ≤ num_agents`; reserve dương.

## Out of Scope

- Nhiều seed/thống kê độ nhạy trong UI (khuyến khích nhưng ngoài bắt buộc; nếu làm thì lưu riêng từng seed).
- Local blockchain / Smart Contract `LiquidationRecorded` (phần mở rộng §2.3).
- Thêm Agent/thanh khoản giữa chừng, arbitrage, tự phục hồi giá, lãi vay.
- Chạy song song/tối ưu hiệu năng nâng cao.

## Assumptions *(quyết định đã chốt)*

- Giá dùng để xét Agent: ETH Agent → giá ETH; stETH Agent → giá stETH, lấy live từ reserves hiện tại (không cache) — nên "recalculate_market_prices" cuối block chỉ là bước đọc lại giá để ghi.
- SC01 coi `shock = 0` và không gọi bước shock; dữ liệu Pool A không đổi chút nào.
- Event của SC02/SC03 mang `scenario` tương ứng; SC01 danh sách event rỗng.
- Thứ tự xử lý Agent theo id, Agent ETH (id nhỏ) luôn được xét trước stETH (spec 002).

## Traceability

SRS §4.3 → FR-001, FR-003, FR-019; §7.3–7.5 → bảng cột, FR-017, FR-018; §9 → User Story 2–4, FR-004…FR-012; §10.2–10.4 → quy ước thứ tự, FR-008, FR-009, FR-013, FR-014; BR-07 → FR-006; BR-08 → FR-011, FR-012; BR-10 → FR-015; BR-11 → SC-006; FR-06 → toàn bộ; §15.1 → FR-001; §14.3 → FR-020; UT-10/11/14; ST-01…ST-07.

