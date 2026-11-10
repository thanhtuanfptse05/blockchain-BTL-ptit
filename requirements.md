# SOFTWARE REQUIREMENTS SPECIFICATION (SRS)

## DeFi Liquidation Cascade Simulator

**Tên tiếng Việt:** Mô phỏng cơ chế lây lan rủi ro thanh lý chéo tài sản trong DeFi Lending bằng mô hình Agent-Based  
**Loại sản phẩm:** Ứng dụng mô phỏng học thuật chạy trên máy cá nhân (local)  
**Phiên bản tài liệu:** 1.0 — 10/11/2026  
**Quy mô triển khai:** Nhóm 2 sinh viên  
**Mức ưu tiên:** Hoàn thiện logic mô phỏng, kiểm thử và biểu đồ; không phát triển thành nền tảng DeFi thương mại.

> **Nguyên tắc xuyên suốt:** Mọi số liệu đầu vào đều là **giả định phục vụ thí nghiệm**, không phải dữ liệu thị trường thật. Kết quả phải được **tính từ code**, tuyệt đối không gán cứng số Agent bị thanh lý hoặc ép kịch bản SC03 luôn xấu hơn SC02.

---

## 1. Tổng quan đề tài

### 1.1. Bối cảnh

Trong DeFi Lending, người vay thế chấp tài sản mã hóa (ví dụ ETH hoặc stETH) để vay stablecoin giả định là USDC. Khi giá tài sản thế chấp giảm, **Health Factor (HF)** giảm. Nếu `HF < 1`, vị thế đủ điều kiện thanh lý.

Thanh lý có thể tạo **áp lực bán** trên các sàn phi tập trung (AMM). Giá giảm thêm do bán ra có thể tiếp tục khiến các vị thế khác bị thanh lý. Nếu tài sản liên kết qua các pool giao dịch, rủi ro còn có thể lan từ ETH sang stETH hoặc ngược lại. Đây là hiện tượng **liquidation cascade / cross-asset contagion**.

Đề tài xây dựng mô hình **Agent-Based Model (ABM)**: mỗi người vay là một Agent có tài sản thế chấp, khoản nợ và trạng thái riêng; các Agent tương tác gián tiếp thông qua giá chung trên các pool thanh khoản. Hệ thống chạy nhiều bước mô phỏng (gọi là **block mô phỏng**, không phải block Ethereum thật) và trực quan hóa kết quả bằng biểu đồ.

### 1.2. Mục tiêu

- **G1.** Xây dựng chương trình Python có thể tạo và quản lý nhiều Borrower Agents.
- **G2.** Tính đúng giá trị tài sản thế chấp, LTV, Health Factor và điều kiện thanh lý.
- **G3.** Mô phỏng thanh lý một phần và tác động lên giá ETH/stETH qua 2 pool AMM giả lập.
- **G4.** So sánh 3 kịch bản: Baseline, Direct Shock và Contagion trên **cùng bộ Agent ban đầu**.
- **G5.** Hiển thị biểu đồ giá, discount stETH/ETH, số vụ thanh lý theo bước và các chỉ số tổng hợp.
- **G6.** Cho phép thay đổi tham số rồi chạy lại mô phỏng và xuất kết quả để viết báo cáo.
- **G7.** Có mã nguồn rõ ràng, kiểm thử được, chạy local và demo cho giảng viên.

### 1.3. Câu hỏi nghiên cứu

1. Cú sốc giảm giá ETH ảnh hưởng như thế nào đến số vị thế bị thanh lý?
2. Khi thanh lý làm giá biến động thêm, thiệt hại tăng bao nhiêu so với trường hợp **không có phản hồi giá**?
3. Thanh khoản ETH/USDC và stETH/ETH tác động thế nào đến tốc độ và mức độ lây lan rủi ro?
4. Khi bán stETH vào pool stETH/ETH, mức **discount** của stETH so với ETH thay đổi như thế nào?

### 1.4. Tiêu chí thành công

Đề tài được xem là hoàn thành khi:

- Chạy được chương trình bằng lệnh `streamlit run app.py` trên máy local.
- Tạo được ít nhất 100 Agents mặc định (50 ETH, 50 stETH).
- Có **SC01, SC02, SC03**, mỗi kịch bản có dữ liệu theo block và biểu đồ tương ứng.
- Có thể thay đổi cú sốc giá và độ sâu 2 pool; chạy lại thấy kết quả được tính lại.
- Có mô hình **thanh lý → bán collateral → tác động giá → đánh giá HF lại** thật sự trong code.
- Có kiểm thử những công thức then chốt và một ví dụ đối chiếu bằng tay.
- Xuất CSV được, đủ dữ liệu cho báo cáo và trình bày.

---

## 2. Phạm vi và giới hạn

### 2.1. Trong phạm vi — bắt buộc

| Mã | Hạng mục | Mô tả |
|---|---|---|
| IN-01 | 2 loại tài sản thế chấp | ETH và stETH |
| IN-02 | 1 loại tài sản nợ | USDC, quy ước **1 USDC = 1 USD** |
| IN-03 | 100 Borrower Agents mặc định | 50 ETH + 50 stETH; cho phép chỉnh tổng số Agent |
| IN-04 | 1 Liquidator giả lập | Được mô phỏng dưới dạng thành phần quy tắc, không cần ví riêng |
| IN-05 | Oracle giá đơn giản | Giá đánh giá collateral lấy từ giá spot của AMM sau mỗi bước |
| IN-06 | 2 pool AMM | Pool A: ETH/USDC; Pool B: stETH/ETH |
| IN-07 | 3 kịch bản | SC01, SC02, SC03 |
| IN-08 | Dashboard | Streamlit với sidebar, KPI, tab biểu đồ |
| IN-09 | Xuất kết quả | CSV tổng hợp theo block và CSV sự kiện thanh lý |
| IN-10 | Kiểm thử | Unit test + kiểm tra tính hợp lý bằng các tình huống mẫu |

### 2.2. Ngoài phạm vi — không làm trong bản chính

- Không triển khai blockchain thật, Ethereum mainnet/testnet, token thật hoặc ví MetaMask.
- Không cần Smart Contract, API server, cơ sở dữ liệu, chức năng tài khoản, đăng nhập hoặc phân quyền.
- Không cần React/Node.js, Docker, microservices hoặc deploy Internet.
- Không lấy giá từ sàn real-time; không nghiên cứu MEV, gas fee, oracle manipulation hay lãi vay thay đổi theo thời gian.
- Không tái dựng toàn bộ quy tắc Aave, Uniswap, Curve hoặc thị trường thực tế.
- Không cần hàng nghìn Agent, mô hình học máy, mạng lưới đồ thị tương tác phức tạp hay tối ưu hiệu năng nâng cao.

### 2.3. Phần mở rộng **chỉ làm khi bản chính đã hoàn thành**

Tùy thời gian, có thể dùng **Hardhat local blockchain** và một Smart Contract tối giản để ghi lại sự kiện `LiquidationRecorded(agentId, amount, blockIndex)` từ kết quả mô phỏng. Đây là **bản ghi minh họa**, không phải thực thi giao thức lending on-chain. Phần này không tính vào điều kiện hoàn thành bắt buộc.

---

## 3. Thuật ngữ cơ bản

| Thuật ngữ | Ý nghĩa trong dự án |
|---|---|
| Borrower Agent | Người vay giả lập với một loại collateral và một khoản nợ |
| Collateral | Tài sản thế chấp (ETH hoặc stETH) |
| Debt | Khoản nợ USDC, tính theo USD |
| LTV | `Debt / Collateral Value`, đo tỷ lệ vay trên thế chấp |
| Liquidation Threshold (LT) | Ngưỡng dùng để tính HF; mặc định 80% |
| Health Factor (HF) | Chỉ số an toàn khoản vay; dưới 1 thì có thể bị thanh lý |
| Liquidation | Liquidator trả một phần nợ và nhận collateral tương ứng cộng bonus |
| Close Factor | Tỷ lệ nợ tối đa được trả trong **một lần thanh lý**, mặc định 50% |
| Liquidation Bonus | Phần collateral cộng thêm cho liquidator, mặc định 5% |
| AMM | Automated Market Maker: pool trao đổi token theo công thức |
| Pool A | ETH/USDC, quyết định giá ETH tính theo USD |
| Pool B | stETH/ETH, quyết định tỷ giá stETH so với ETH |
| Discount / Depeg | Mức stETH rẻ hơn ETH, có thể tính âm nếu stETH cao giá hơn |
| Price Shock | Mức giảm giá ETH ban đầu do tác động bên ngoài mô hình |
| Contagion | Giá thay đổi thêm vì các đợt thanh lý gây áp lực bán |
| Simulation Block | Một bước tính toán ABM; **không phải block blockchain thật** |
| Bad Debt | Phần nợ còn lại khi Agent đã hết tài sản thế chấp |
| Random Seed | Giá trị để tạo cùng bộ dữ liệu giả định khi chạy lại |

---

## 4. Công nghệ và kiến trúc

### 4.1. Stack tối thiểu

| Thành phần | Công nghệ | Vai trò |
|---|---|---|
| Ngôn ngữ | Python 3.11+ | Toàn bộ ứng dụng |
| ABM | Mesa 3.x (phiên bản ổn định được khóa trong requirements) | Borrower Agents và Model |
| Giao diện | Streamlit | Chạy local trên trình duyệt |
| Tính toán & xử lý bảng | Python chuẩn, pandas, NumPy (nếu cần) | Sinh dữ liệu, tổng hợp |
| Biểu đồ | Matplotlib | 3–4 biểu đồ cơ bản |
| Kiểm thử | pytest | Unit test và scenario test |
| Lưu kết quả | CSV | Không cần database |

**Lưu ý:** Không dùng API cũ của Mesa nếu phiên bản cài đặt không còn hỗ trợ. Khóa phiên bản thư viện khi bắt đầu code và ghi trong `requirements.txt`.

### 4.2. Kiến trúc xử lý

```text
[Streamlit UI: người dùng chọn tham số]
                    |
                    v
[Scenario Runner: SC01, SC02, SC03]
                    |
                    v
[Agent-Based Model (Mesa)]
    |                   |
    v                   v
[Borrower Agents]   [Market/2 AMM Pools]
    |                   ^
    v                   |
[Health Factor + Liquidation Rules]
    |                   |
    +----> [Bán collateral] ----+
                    |
                    v
    [Ghi lịch sử theo Simulation Block]
                    |
                    v
[Dashboard KPI, biểu đồ, bảng, CSV]
```

### 4.3. Nguyên tắc tách lớp

- **UI không chứa công thức tài chính cốt lõi.** UI chỉ nhận input, gọi mô phỏng và hiển thị output.
- **Simulation Engine không gọi Streamlit.** Có thể chạy test trực tiếp từ Python.
- **Cùng một random seed + cùng tham số → cùng kết quả.**
- **Mỗi kịch bản dùng bản sao độc lập của Agent và pool.** Không chia sẻ biến trạng thái có thể bị sửa.

---

## 5. Các giả định mô hình

Các giả định dưới đây phải được viết rõ trong README và báo cáo:

1. Mỗi Borrower chỉ có **một loại collateral** (ETH **hoặc** stETH) và chỉ vay USDC.
2. Mỗi Agent có khoản nợ ban đầu, không tự vay thêm, nạp/rút collateral hoặc chủ động trả nợ trong quá trình chạy.
3. Giá USDC luôn bằng 1 USD.
4. Không tính lãi vay, phí giao dịch, gas, phí AMM hoặc trượt giá bên ngoài 2 pool.
5. Các pool sử dụng **constant-product AMM** không phí: `x * y = k`.
6. Giá tài sản dùng tính HF là **spot price trong mô hình**, không dùng oracle độc lập hay TWAP. Đây là giản lược có thể làm phản hồi giá mạnh hơn thực tế.
7. Liquidator có đủ USDC để thực hiện thanh lý hợp lệ, **không kiểm tra lợi nhuận của liquidator**; khoản lỗ khi đổi collateral trên AMM không được hạch toán là bad debt của bên vay.
8. Liquidation Bonus mặc định 5%, Close Factor 50% cố định cho mỗi lần thanh lý; **không khẳng định đây là quy tắc đầy đủ của Aave thực tế**.
9. Một Agent có thể bị thanh lý qua nhiều block; danh sách vị thế đã từng bị thanh lý phải được tính **không trùng lặp**.
10. Cú sốc ngoại sinh chỉ áp dụng **một lần tại đầu block 1**; các thay đổi giá tiếp theo trong SC03 chỉ do giao dịch thanh lý.
11. Không thêm Agent mới hoặc tạo thêm thanh khoản sau khi mô phỏng bắt đầu.
12. Đơn vị tiền tệ thống nhất là USD/USDC; tài sản là số lượng ETH hoặc stETH.
13. Các giá trị đều được làm tròn **khi hiển thị**, còn tính toán dùng `float` đủ chính xác cho bài học thuật và chấp nhận sai số nhỏ (`epsilon`).

---

## 6. Tham số đầu vào và giá trị mặc định

### 6.1. Tham số được chỉnh trên giao diện

| ID | Tham số | Mặc định | Miền hợp lệ | Ý nghĩa |
|---|---|---:|---:|---|
| P-01 | `shock_pct` | 15% | 0–40%, bước 5% | Cú sốc giá ETH tại block 1 |
| P-02 | `pool_a_tvl_usd` | 150,000,000 | 10–300 triệu USD | Tổng giá trị thanh khoản ETH/USDC **trước cú sốc** |
| P-03 | `pool_b_tvl_usd` | 80,000,000 | 5–200 triệu USD | Tổng giá trị thanh khoản stETH/ETH **trước cú sốc** |
| P-04 | `num_agents` | 100 | 20–200, bước 20 | Số Agent; chia đều ETH/stETH |
| P-05 | `max_blocks` | 30 | 5–50, số nguyên | Giới hạn bước mô phỏng |
| P-06 | `random_seed` | 42 | 0–99,999 | Tái lập bộ dữ liệu đầu vào |

> **Không cần đưa toàn bộ tham số kỹ thuật lên UI.** Những tham số dưới đây để cố định trong `config.py` để nhóm không bị phân tán.

### 6.2. Tham số cố định trong mã nguồn

| ID | Tham số | Mặc định | Ghi chú |
|---|---|---:|---|
| C-01 | `initial_eth_price_usd` | 3,000 USD | Giá tại block 0 |
| C-02 | `initial_steth_discount_pct` | 1% | Giá stETH ban đầu = 0.99 × ETH |
| C-03 | `lt` | 0.80 | Dùng chung cho ETH/stETH |
| C-04 | `initial_ltv_min` | 0.55 | Dữ liệu giả định |
| C-05 | `initial_ltv_max` | 0.72 | Nhỏ hơn LT |
| C-06 | `collateral_value_min_usd` | 250,000 | Giá trị collateral mỗi Agent lúc tạo |
| C-07 | `collateral_value_max_usd` | 1,000,000 | Giúp giao dịch đủ lớn để thấy tác động lên pool |
| C-08 | `close_factor` | 0.50 | Mỗi lần trả tối đa 50% khoản nợ còn lại |
| C-09 | `liquidation_bonus` | 0.05 | Liquidator nhận collateral trị giá 105% nợ đã trả |
| C-10 | `epsilon` | 1e-9 | Ngưỡng tính toán cho số rất nhỏ |

### 6.3. Kiểm tra dữ liệu đầu vào

- Số Agent phải là **số chẵn**, để chia đều hai nhóm tài sản.
- `pool_a_tvl_usd`, `pool_b_tvl_usd`, `initial_eth_price_usd` phải dương.
- `shock_pct` phải trong 0–40%, không cho đầu vào khiến giá bằng 0.
- Các tỷ lệ phần trăm nội bộ lưu dạng thập phân: `15% = 0.15`.
- `0 <= initial_ltv_min <= initial_ltv_max < lt < 1`.
- Nếu đầu vào không hợp lệ: hiển thị thông báo cụ thể, không chạy mô phỏng, không crash.

---

## 7. Mô hình dữ liệu

### 7.1. `BorrowerAgent`

| Thuộc tính | Kiểu dữ liệu | Mô tả |
|---|---|---|
| `agent_id` | `int` | ID duy nhất, từ 1 đến N |
| `collateral_type` | `str` | `ETH` hoặc `stETH` |
| `collateral_amount` | `float` | Số token còn đang thế chấp |
| `debt_usdc` | `float` | Dư nợ hiện tại |
| `initial_ltv` | `float` | LTV khi tạo |
| `liquidation_threshold` | `float` | 0.80 |
| `ever_liquidated` | `bool` | Đã từng bị thanh lý ít nhất 1 lần |
| `liquidation_count` | `int` | Tổng số sự kiện thanh lý |
| `status` | `str` | `ACTIVE`, `REPAID` hoặc `BAD_DEBT` |

**Phương thức cần có:**

- `collateral_value(price)`: giá trị collateral theo USD.
- `health_factor(price)`: tính HF, nếu nợ = 0 thì trả `inf` và coi là an toàn.
- `is_liquidatable(price)`: `debt > epsilon and collateral > epsilon and HF < 1`.
- `apply_liquidation(debt_repaid, collateral_seized)`: trừ nợ và collateral; không cho âm.

### 7.2. `AMMPool`

| Thuộc tính | Kiểu | Mô tả |
|---|---|---|
| `name` | `str` | `ETH_USDC` hoặc `STETH_ETH` |
| `token_x` | `str` | ETH đối với pool A; stETH đối với pool B |
| `token_y` | `str` | USDC đối với pool A; ETH đối với pool B |
| `reserve_x` | `float` | Số token x trong pool |
| `reserve_y` | `float` | Số token y trong pool |

**Phương thức cần có:**

- `spot_price_y_per_x()`: `reserve_y / reserve_x`.
- `sell_x(amount_x)`: đưa x vào pool, trả y ra; cập nhật reserves.
- `reset()` hoặc dùng `deepcopy` để khởi tạo lại kịch bản.

**Đơn vị giá:**

- Pool A: `P_ETH_USD = reserve_USDC / reserve_ETH`.
- Pool B: `P_stETH_per_ETH = reserve_ETH / reserve_stETH` (1 stETH đổi được bao nhiêu ETH).
- Giá USD của stETH: `P_stETH_USD = P_ETH_USD * P_stETH_per_ETH`.

### 7.3. `LiquidationEvent`

| Trường | Ý nghĩa |
|---|---|
| `scenario` | SC02 hoặc SC03 |
| `block` | Block xảy ra thanh lý |
| `agent_id` | ID Agent |
| `asset` | ETH/stETH |
| `hf_before` | HF trước giao dịch |
| `debt_repaid_usd` | USDC liquidator trả thay |
| `collateral_seized` | Số ETH/stETH bị thu giữ |
| `collateral_value_at_oracle_usd` | Giá trị collateral tại spot price trước giao dịch |
| `remaining_debt_usd` | Nợ còn lại |
| `remaining_collateral` | Collateral còn lại |

### 7.4. `BlockResult`

**Mỗi scenario/block sinh đúng một bản ghi** với các cột tối thiểu:

```text
scenario,block,eth_price_usd,steth_price_usd,
steth_discount_pct,liquidations_eth,liquidations_steth,
liquidations_total,liquidated_agents_unique_cumulative,
liquidation_debt_repaid_usd,liquidation_debt_repaid_cumulative_usd,
bad_debt_usd
```

Trong đó:

- `liquidations_*`: **số sự kiện** trong block, có thể lớn hơn số người duy nhất nếu xét cả quá trình.
- `liquidated_agents_unique_cumulative`: số `agent_id` khác nhau đã từng bị thanh lý tính đến block đó.
- `bad_debt_usd`: tổng nợ còn lại của vị thế đã hết collateral ở thời điểm đó.
- `liquidation_debt_repaid_usd`: tổng nợ được liquidator trả thay tại block đó, không đồng nghĩa với giá trị giao dịch thực hiện trên AMM.

### 7.5. `SimulationResult`

Một kết quả kịch bản gồm:

```python
{
    "scenario_id": "SC03",
    "parameters": { ... },
    "block_results": [ ... ],
    "liquidation_events": [ ... ],
    "summary": {
        "final_eth_price_usd": ..., 
        "final_steth_price_usd": ..., 
        "final_steth_discount_pct": ..., 
        "liquidated_agents_unique": ..., 
        "liquidation_events_total": ..., 
        "total_debt_repaid_usd": ..., 
        "bad_debt_usd": ...
    }
}
```

---

## 8. Quy tắc nghiệp vụ và công thức

### BR-01. Tính giá trị tài sản thế chấp

```text
collateral_value_usd = collateral_amount * current_asset_price_usd
```

Nếu Agent thế chấp ETH thì dùng giá ETH; nếu thế chấp stETH thì dùng giá stETH.

### BR-02. Tính LTV hiện tại

```text
current_ltv = debt_usdc / collateral_value_usd
```

Nếu collateral = 0 và nợ > 0, không tính phép chia; vị thế được đánh dấu `BAD_DEBT`.

### BR-03. Tính Health Factor

```text
HF = collateral_value_usd * liquidation_threshold / debt_usdc
```

- `HF >= 1`: chưa đủ điều kiện thanh lý.
- `HF < 1`: đủ điều kiện thanh lý nếu vẫn còn collateral và debt.
- `debt_usdc <= epsilon`: HF = vô cùng (không còn nợ).

**Ví dụ tính tay:** Agent có 10 ETH, giá ETH = 3,000 USD, debt = 22,000 USDC, LT = 0.8.

- Trước shock: `HF = 10 × 3,000 × 0.8 / 22,000 = 1.0909` → an toàn.
- Sau shock 15%: ETH = 2,550 USD; `HF = 10 × 2,550 × 0.8 / 22,000 = 0.9273` → đủ điều kiện thanh lý.

### BR-04. Quy tắc thanh lý một phần

Khi Agent đủ điều kiện thanh lý:

1. Tính mức trả nợ đề xuất: `candidate_repay = close_factor * current_debt`.
2. Vì liquidator nhận bonus, giới hạn nợ trả bởi collateral còn lại:

   `max_repay_from_collateral = collateral_amount * current_asset_price / (1 + liquidation_bonus)`.

3. Nợ thực trả:

   `debt_repaid = min(candidate_repay, max_repay_from_collateral)`.

4. Collateral được lấy:

   `collateral_seized = debt_repaid * (1 + liquidation_bonus) / current_asset_price`.

5. Cập nhật:

   `debt_new = max(0, debt_old - debt_repaid)`;

   `collateral_new = max(0, collateral_old - collateral_seized)`.

6. Nếu `debt_repaid <= epsilon`, không phát sinh sự kiện thanh lý.
7. Nếu collateral hết nhưng còn nợ, chuyển `status = BAD_DEBT`; phần nợ còn lại được cộng vào chỉ số nợ xấu.
8. Nếu nợ hết, chuyển `status = REPAID`.
9. Một Agent tối đa **1 lần thanh lý trong mỗi block**, nhưng có thể bị thanh lý tiếp ở block sau.

**Ghi chú:** Đây là quy tắc đóng vị thế giản lược do nhóm đặt ra. Không triển khai chi tiết `dust`, các close factor động hoặc cấu hình tài sản của một giao thức thật.

### BR-05. Mô hình AMM constant-product

Hai pool đều dùng:

```text
reserve_x * reserve_y = k
```

Khi **bán** `dx` token x vào pool đang có `x` token x và `y` token y (không phí):

```text
amount_y_out = (y * dx) / (x + dx)
reserve_x_new = x + dx
reserve_y_new = y - amount_y_out
```

Các giá trị dự trữ phải luôn dương. Mỗi lần bán làm `reserve_y / reserve_x` giảm, từ đó tạo tác động giá nội sinh.

### BR-06. Khởi tạo hai pool

Đặt `P = initial_eth_price_usd`, `r = 1 - initial_steth_discount_pct`.

**Pool A (ETH/USDC), TVL = A:**

```text
reserve_A_USDC = A / 2
reserve_A_ETH  = (A / 2) / P
```

**Pool B (stETH/ETH), TVL quy USD = B:**

```text
reserve_B_ETH   = (B / 2) / P
reserve_B_stETH = (B / 2) / (P * r)
```

Từ đó tại block 0:

```text
P_ETH_USD = 3000
P_stETH_per_ETH = 0.99
P_stETH_USD = 2970
Discount = (1 - P_stETH_USD / P_ETH_USD) * 100 = 1%
```

### BR-07. Áp dụng cú sốc giá ngoại sinh

Tại đầu **block 1**, đặt giá ETH mục tiêu:

```text
P_after_shock = initial_eth_price_usd * (1 - shock_pct)
```

Để pool A phản ánh cú sốc mà vẫn giữ hằng số `k_A` (giả định giao dịch arbitrage ngoài mô hình), cân bằng lại:

```text
new_reserve_A_ETH  = sqrt(k_A / P_after_shock)
new_reserve_A_USDC = sqrt(k_A * P_after_shock)
```

**Không thay đổi tỷ giá pool B khi áp dụng shock**: tỷ giá stETH/ETH tạm thời vẫn là 0.99, nên giá stETH tính theo USD giảm tương ứng với ETH. Việc stETH **depeg thêm** chỉ xảy ra khi có bán stETH vào pool B trong SC03.

### BR-08. Đường bán collateral trong SC03

**Nếu liquidator nhận ETH:**

```text
ETH -> Pool A (bán lấy USDC)
       -> reserve Pool A thay đổi
       -> giá ETH/USD giảm thêm
```

**Nếu liquidator nhận stETH:**

```text
stETH -> Pool B (bán lấy ETH)
         -> tỷ giá stETH/ETH giảm
         -> ETH nhận được -> Pool A (bán lấy USDC)
                          -> giá ETH/USD giảm thêm
```

Vậy cùng một sự kiện thanh lý stETH có thể gây áp lực lên **cả pool B và pool A**. Đây là **cơ chế lây lan chéo tài sản trọng tâm** của bài.

### BR-09. Giá stETH và discount

```text
eth_price_usd = reserve_A_USDC / reserve_A_ETH
steth_eth_ratio = reserve_B_ETH / reserve_B_stETH
steth_price_usd = eth_price_usd * steth_eth_ratio
steth_discount_pct = (1 - steth_price_usd / eth_price_usd) * 100
```

- Discount dương: stETH thấp giá hơn ETH.
- Discount bằng 0: ngang giá.
- Discount âm: stETH cao giá hơn ETH (premium); **không cắt về 0**.

### BR-10. Nợ xấu

```text
bad_debt_usd = sum(agent.debt_usdc
                   for agent in agents
                   if agent.collateral_amount <= epsilon
                   and agent.debt_usdc > epsilon)
```

Tổng nợ xấu phải tính từ **trạng thái hiện tại của Agent** để tránh cộng trùng qua nhiều block.

### BR-11. Ràng buộc giữ nhất quán

- Tài sản và khoản nợ của Agent không được âm.
- `debt_repaid <= debt_before`.
- `collateral_seized <= collateral_before` (cho phép sai số `epsilon`).
- Mọi giao dịch AMM giữ `k` gần không đổi trong sai số số thực (riêng shock cân bằng lại theo đúng `k`).
- Không dùng giá *sau* giao dịch để tính lại số token thu giữ của **chính** giao dịch vừa thực hiện; sử dụng giá spot **trước** giao dịch đó.
- Chỉ số `unique liquidated agents` không được vượt `num_agents`.

---

## 9. Kịch bản thí nghiệm

### SC01 — Baseline (đối chứng)

- Không áp dụng shock (coi `shock_pct = 0` cho riêng SC01).
- Không có Agent chủ động thay đổi trạng thái.
- Ban đầu các Agent có LTV thấp hơn LT, nên không phát sinh thanh lý.
- Giá ETH, stETH và discount giữ nguyên qua các block.
- **Mục đích:** Chứng minh môi trường mô phỏng ở trạng thái ổn định khi không chịu cú sốc.

### SC02 — Direct Shock (cú sốc trực tiếp, không phản hồi giá)

- Áp dụng `shock_pct` vào pool A tại đầu block 1.
- Chạy kiểm tra HF và thanh lý theo BR-04 như bình thường.
- **Không thực hiện giao dịch bán collateral lên pool A/B**, nên giá thị trường **giữ ở mức ngay sau cú sốc**.
- Vị thế Agent và debt vẫn thay đổi khi bị thanh lý, nhưng không tạo thêm price impact.
- **Mục đích:** Đo hệ quả trực tiếp của shock, làm nhóm đối chứng cho SC03.

### SC03 — Contagion (cú sốc có phản hồi giá)

- Áp dụng **cùng cú sốc** như SC02 vào bản sao pool A.
- Chạy thanh lý giống SC02, nhưng collateral thu giữ sẽ được **bán qua 2 pool AMM** theo BR-08.
- Sau mỗi block, giá ETH/stETH thay đổi theo trạng thái dự trữ pool; Agent được đánh giá lại để xét thanh lý ở block tiếp theo.
- **Mục đích:** Đánh giá hiệu ứng thanh lý kéo theo giảm giá và tạo thêm thanh lý.

### So sánh công bằng

- SC01/SC02/SC03 xuất phát từ **cùng danh sách Agent**, cùng `random_seed` và trạng thái pool ban đầu.
- Chỉ khác nhau ở quy tắc áp dụng shock và phản hồi giá.
- **Không ép:** `SC03 > SC02`; nếu kết quả bằng nhau hoặc SC03 không khuếch đại, báo cáo giải thích theo tham số.
- Nếu chạy nhiều seeds để phân tích độ nhạy thì lưu riêng kết quả từng seed và có thống kê trung bình; đây là **khuyến khích**, không phải tính năng UI bắt buộc.

---

## 10. Thuật toán mô phỏng theo block

### 10.1. Khởi tạo Agent

1. Tạo `num_agents / 2` Agent ETH và `num_agents / 2` Agent stETH.
2. Dùng `random.Random(random_seed)` để sinh ổn định:
   - Giá trị collateral ban đầu trong khoảng `250,000–1,000,000 USD`.
   - `initial_ltv` ngẫu nhiên trong khoảng `0.55–0.72`.
3. Số token thế chấp ban đầu = `collateral_value_usd / initial_asset_price_usd`.
4. Nợ USDC ban đầu = `collateral_value_usd * initial_ltv`.
5. Tất cả Agent khởi tạo `ACTIVE`, `ever_liquidated=False`, `liquidation_count=0`.
6. Xác minh toàn bộ Agent ban đầu có `HF > 1`; nếu sai, báo lỗi sinh dữ liệu.

### 10.2. Một block mô phỏng

```python
# Mã giả: mô tả thứ tự xử lý, không phải source code hoàn chỉnh.
for block in range(0, max_blocks + 1):
    if block == 0:
        record_initial_state()
        continue

    if block == 1 and scenario in ("SC02", "SC03"):
        apply_external_eth_shock_once()

    # Chốt danh sách Agent đủ điều kiện tại đầu block.
    candidates = sorted(
        [a for a in agents if a.is_liquidatable(current_price(a.asset))],
        key=lambda a: a.agent_id
    )

    for agent in candidates:
        # Dùng giá hiện hành ngay trước giao dịch của Agent này.
        # Mỗi Agent tối đa một lần thanh lý mỗi block.
        if agent.is_liquidatable(current_price(agent.asset)):
            event = liquidate_partial(agent)
            if event:
                save_event(event)
                if scenario == "SC03":
                    sell_seized_collateral_through_amm(event)

    recalculate_market_prices()
    record_block_metrics()
```

### 10.3. Quy ước thứ tự và dừng

- Agent được xử lý theo `agent_id` tăng dần để dễ tái lập và debug.
- **Chỉ chọn Agent ở đầu block**, để Agent mới nguy hiểm vì giá giảm trong block được xét vào **block kế tiếp**.
- Trong cùng block, giá spot có thể đổi sau mỗi giao dịch SC03; kiểm tra lại HF trước khi xử lý Agent đã nằm trong danh sách.
- Nếu không còn thanh lý, dữ liệu các block sau **giữ nguyên giá và các chỉ số tích lũy**, với `liquidations_total = 0` ở các block đó, để cả 3 kịch bản có trục thời gian giống nhau.
- Dữ liệu phải chứa **block 0 đến max_blocks**, tổng `max_blocks + 1` hàng cho mỗi kịch bản.
- Không áp dụng shock nhiều lần.
- **Không có bước tự phục hồi giá**, mua lại token hoặc arbitrage sau cú sốc; đây là giới hạn chủ ý để phạm vi vừa sức.

### 10.4. Trường hợp biên

- `shock_pct = 0`: các kịch bản phải giống nhau về giá và không có thanh lý nếu dữ liệu khởi tạo hợp lệ.
- Agent đã hết debt: không thanh lý nữa.
- Agent hết collateral nhưng còn debt: chuyển `BAD_DEBT`, không bán tiếp.
- Một pool không được có reserve bằng 0 hoặc âm.
- Nếu liquidator có `collateral_seized <= epsilon`, bỏ qua swap.
- Nếu thiếu đầu vào hoặc thông số sai: cảnh báo trước khi tính.

---

## 11. Yêu cầu chức năng (Functional Requirements)

### FR-01. Cấu hình và khởi tạo mô phỏng — Must Have

**Người dùng:** Sinh viên hoặc giảng viên chạy demo.  
**Mô tả:** Nhập 6 tham số ở mục 6.1, xem giá trị mặc định, nhấn **Run Simulation**.

**Acceptance criteria:**
- Sidebar có đầy đủ 6 tham số; giá trị hợp lệ được kiểm tra.
- Nút **Reset Defaults** đưa về tham số chuẩn.
- Khi nhấn Run, cả 3 scenario được tạo từ cùng seed và cấu hình.
- Người dùng không cần khởi động lại ứng dụng để chạy thử lần tiếp theo.

### FR-02. Tạo Borrower Agents — Must Have

**Mô tả:** Sinh danh sách Agent với ETH/stETH, collateral và debt theo cấu hình.  
**Acceptance criteria:**
- Mặc định tạo chính xác 100 Agent, 50 ETH và 50 stETH.
- `agent_id` duy nhất, mọi khoản nợ/collateral dương.
- Cùng seed + cùng tham số tạo cùng danh sách.
- Ban đầu tất cả `HF > 1`.

### FR-03. Tính HF và đánh giá thanh lý — Must Have

**Mô tả:** Tính giá trị collateral, HF và danh sách đủ điều kiện thanh lý.  
**Acceptance criteria:**
- HF được tính theo BR-03, không làm tròn trước khi so sánh.
- `HF < 1` được nhận diện chính xác.
- Các Agent không nợ hoặc đã hết collateral không bị xử lý lặp.

### FR-04. Liquidation Engine — Must Have

**Mô tả:** Thực hiện trả nợ tối đa 50%, thu collateral cộng bonus 5%, lưu event.  
**Acceptance criteria:**
- Nợ và collateral sau xử lý không âm.
- Có thể có nhiều event cho cùng Agent ở các block khác nhau.
- Event ghi đủ các trường mục 7.3.
- Hết collateral vẫn còn nợ thì nợ xấu được thống kê chính xác.

### FR-05. AMM Pools và giao dịch — Must Have

**Mô tả:** Hai pool tính giá và swap theo constant-product.  
**Acceptance criteria:**
- Giá ban đầu A = 3,000 USD/ETH, B = 0.99 ETH/stETH.
- Bán ETH vào A làm ETH/USD giảm.
- Bán stETH vào B làm tỷ giá stETH/ETH giảm.
- Bán collateral trong SC03 tác động lên reserve thực tế; SC02 không tác động.
- Reserve dương và `k` được bảo toàn trong sai số chấp nhận.

### FR-06. Chạy 3 kịch bản — Must Have

**Mô tả:** SC01, SC02, SC03 theo mục 9.  
**Acceptance criteria:**
- Mỗi scenario có bản sao độc lập của state.
- Cả ba có cùng số block và cùng dữ liệu Agent ban đầu.
- Shock chỉ xảy ra một lần tại block 1.
- Chỉ SC03 có **phản hồi giá do bán collateral**.

### FR-07. Dashboard thống kê — Must Have

**Hiển thị tối thiểu:**

1. Giá ETH cuối SC03 (USD).
2. Giá stETH cuối SC03 (USD).
3. Discount stETH cuối SC03 (%).
4. Số Agent đã từng bị thanh lý trong SC03 (ví dụ `38/100`).
5. Số event thanh lý SC03.
6. Nợ xấu cuối SC03 (USD).

Có thể hiển thị hiệu số SC03–SC02 bên dưới từng KPI nhưng không bắt buộc với tất cả ô.

**Acceptance criteria:** Chỉ số phản ánh dữ liệu do engine tính, không hardcode.

### FR-08. Biểu đồ theo block — Must Have

**Tối thiểu 4 biểu đồ:**

1. **ETH Price:** đường SC01, SC02, SC03 theo block.
2. **stETH Price / Discount:** có thể tách thành 2 biểu đồ/2 tab; tối thiểu biểu đồ discount đủ thể hiện depeg.
3. **Liquidations per Block:** cột số event ETH và stETH trong SC03.
4. **Cumulative Unique Liquidated Agents:** so sánh SC02 và SC03.

**Acceptance criteria:**
- Trục X là block (0..max_blocks).
- Trục Y có tên/đơn vị rõ ràng, có legend phân biệt scenario/asset.
- Không vẽ số âm cho số thanh lý hoặc nợ xấu.
- Có chú thích shock xảy ra tại block 1.

### FR-09. Bảng và xuất CSV — Must Have

- Có tab **Data** hiển thị dữ liệu theo block và danh sách LiquidationEvent.
- Nút tải **Block Results CSV** (gồm cả SC01/SC02/SC03).
- Nút tải **Liquidation Events CSV**.
- CSV có tên cột thống nhất, encoding UTF-8.
- Nếu chưa chạy mô phỏng thì không hiển thị nút tải dữ liệu trống.

### FR-10. Thông tin mô hình — Must Have

Có một tab **Methodology / Cơ chế** giải thích ngắn gọn:

- Sơ đồ `Shock -> HF < 1 -> Liquidation -> AMM Sell -> Price Drop -> Next Block`.
- Công thức HF, AMM và discount.
- Khác nhau giữa SC01, SC02, SC03.
- Danh sách giả định/giới hạn lớn của mô hình.

### FR-11. Tự động so sánh kết quả — Should Have (làm nếu đủ thời gian)

Hiển thị bảng SC02 vs SC03 về:

- Giá ETH cuối.
- Giá stETH cuối.
- Discount cuối.
- Số Agent bị thanh lý duy nhất.
- Tổng số event thanh lý.
- Nợ xấu.

Có thể thêm `additional_liquidated_agents = unique_SC03 - unique_SC02` và chỉ số tăng tương đối nếu `unique_SC02 > 0`. Nếu mẫu số 0, hiển thị `N/A` thay vì chia 0.

---

## 12. Đặc tả giao diện Streamlit

**Mục tiêu UI:** Dễ nhìn, dễ demo; chỉ cần một trang Streamlit với sidebar và tabs, không cần UI cầu kỳ.

### 12.1. Sidebar — Tham số

```text
[ Tham số thí nghiệm ]
ETH Price Shock (%)         [slider, mặc định 15]
Pool A TVL — ETH/USDC       [slider, mặc định $150M]
Pool B TVL — stETH/ETH      [slider, mặc định $80M]
Number of Borrowers        [slider, mặc định 100]
Maximum Simulation Blocks  [slider, mặc định 30]
Random Seed                [number input, 42]

[Run Simulation]   [Reset Defaults]
```

### 12.2. Vùng nội dung

```text
DeFi Liquidation Cascade Simulator
Mô phỏng ABM: ETH / stETH / USDC

[KPI ETH] [KPI stETH] [KPI Discount]
[KPI Unique Liquidated] [KPI Events] [KPI Bad Debt]

[Tab 1: Giá & Discount]
  - ETH Price: 3 đường SC01, SC02, SC03
  - stETH Discount: 3 đường

[Tab 2: Thanh lý]
  - Bar chart thanh lý ETH/stETH theo block (SC03)
  - Line chart số Agent đã từng bị thanh lý lũy kế (SC02 vs SC03)

[Tab 3: Dữ liệu]
  - Dataframe block results
  - Dataframe liquidation events
  - Export CSV buttons

[Tab 4: Cơ chế]
  - Giải thích giả định, công thức, 3 scenario
```

### 12.3. Tương tác

- Bấm Run: hiện spinner trong lúc tính, rồi cập nhật bảng/đồ thị.
- Đổi slider: **chưa cần** auto-run; chỉ chạy lại khi bấm Run để dễ kiểm soát.
- Nếu chạy lại, kết quả trên giao diện thay bằng kết quả của cấu hình mới.
- Có ghi chú rõ: **"Dữ liệu giả lập phục vụ nghiên cứu; không phải dự báo hoặc số liệu thị trường thực."**
- UI ưu tiên tên/giải thích bằng tiếng Việt; giữ thuật ngữ DeFi bằng tiếng Anh khi dễ hiểu hơn.

---

## 13. Yêu cầu phi chức năng (Non-Functional Requirements)

| ID | Yêu cầu | Mức đạt mong muốn |
|---|---|---|
| NFR-01 | Dễ chạy | Chạy local Windows bằng Python và Streamlit; không cần Docker/DB |
| NFR-02 | Tốc độ | Với 100 Agents, 30 blocks, 3 scenarios: mục tiêu dưới **10 giây** trên laptop học tập thông thường; đo thực tế và ghi vào README |
| NFR-03 | Tái lập | Cùng seed + cấu hình cho cùng kết quả trên cùng môi trường |
| NFR-04 | Chính xác logic | Test công thức HF, swap, shock, liquidation và thống kê |
| NFR-05 | Đọc được code | Module tách nhiệm vụ, hàm có tên rõ nghĩa, không dồn logic vào `app.py` |
| NFR-06 | Dễ trình bày | KPI rõ đơn vị, có legend, trục biểu đồ, lời giải thích cơ chế |
| NFR-07 | Ổn định | Không crash với đầu vào UI hợp lệ; xử lý số 0 và các trạng thái biên |
| NFR-08 | Phù hợp 2 người | Không yêu cầu hệ thống triển khai phân tán, API hoặc Smart Contract |

> Mức 10 giây là **mục tiêu kiểm tra**, không phải cam kết đo được khi chưa chạy code.

---

## 14. Bộ kiểm thử tối thiểu và điều kiện nghiệm thu

### 14.1. Unit Test

| Test ID | Trường hợp | Kết quả kỳ vọng |
|---|---|---|
| UT-01 | 10 ETH, giá $3,000, debt $22,000, LT 80% | HF khoảng **1.090909**; không thanh lý |
| UT-02 | Giảm ETH còn $2,550, giữ các giá trị UT-01 | HF khoảng **0.927273**; thanh lý được |
| UT-03 | Agent có debt = 0 | Không phát sinh thanh lý; HF = `inf` |
| UT-04 | Nợ $10,000, close factor 50%, collateral đủ, bonus 5% | Liquidator trả $5,000 và thu collateral trị giá $5,250 ở giá trước giao dịch |
| UT-05 | Collateral không đủ trả 50% nợ cộng bonus | Giới hạn trả nợ theo collateral; không âm số dư |
| UT-06 | Pool x=100, y=10,000, bán dx=10 | Nhận `10000*10/110 ≈ 909.0909` token y; reserves mới `110`, `9090.9091` |
| UT-07 | Bán ETH vào Pool A | ETH spot price sau swap **giảm** |
| UT-08 | Bán stETH vào Pool B | stETH/ETH ratio sau swap **giảm** |
| UT-09 | Pool khởi tạo | ETH = $3,000, stETH = $2,970, discount 1% |
| UT-10 | Shock 15% | Giá ETH **ngay sau shock** là $2,550 (trước tác động thanh lý) |
| UT-11 | Không shock, tất cả Agent ban đầu an toàn | Không thanh lý; giá không biến động |
| UT-12 | Cùng seed, cùng cấu hình | Trạng thái Agent sinh ra giống nhau |
| UT-13 | Agent hết collateral nhưng còn nợ | Chỉ ghi `BAD_DEBT` một lần trong tổng, không được tiếp tục thanh lý |
| UT-14 | Dữ liệu mô phỏng | Đúng `max_blocks+1` dòng mỗi scenario, block từ 0 đến max_blocks |
| UT-15 | Bán token qua AMM | `k` gần không đổi với tolerance hợp lý, reserve luôn dương |

### 14.2. Scenario Test

| Test ID | Kịch bản | Kết quả cần kiểm tra |
|---|---|---|
| ST-01 | SC01 mặc định | Không shock; giá phẳng; số thanh lý bằng 0 |
| ST-02 | SC02 shock 15% | Có thể thanh lý trực tiếp; **giá không giảm thêm** sau shock |
| ST-03 | SC03 shock 15% | Swap thực sự làm thay đổi reserve; giá/discount phản ánh các sự kiện bán collateral |
| ST-04 | SC02 và SC03 | Agent ban đầu bằng nhau về số lượng, nhóm tài sản, collateral, debt |
| ST-05 | Đổi Pool B TVL, giữ seed và mọi tham số khác | Cùng lượng bán stETH sẽ gây mức thay đổi tỷ giá khác nhau (nếu có bán stETH) |
| ST-06 | Giảm thanh khoản Pool A, giữ seed và cú sốc | Có thể quan sát độ nhạy giá với cùng khối lượng ETH bán; không bắt buộc số vị thế thanh lý phải tăng trong mọi trường hợp |
| ST-07 | Chạy lại cùng seed và tham số | Kết quả tổng hợp không đổi |
| ST-08 | Xuất CSV | Đọc lại bằng pandas được, không thiếu cột bắt buộc |

### 14.3. Kết quả không được hardcode

**Không được viết** các câu lệnh kiểu:

```python
if scenario == "SC03":
    liquidated_agents = 50
    discount_pct = 29.3
```

Thay vào đó, dữ liệu KPI/đồ thị phải lấy từ danh sách Agent, reserves AMM và `LiquidationEvent` thực tế.

### 14.4. Checklist nghiệm thu cuối cùng

- [ ] Code chạy local sạch từ file `requirements.txt`.
- [ ] UI có thể chỉnh tham số và bấm Run.
- [ ] 100 Agents mặc định, đúng 50/50.
- [ ] 2 AMM Pool hoạt động theo `x*y=k`.
- [ ] Có đầy đủ SC01, SC02, SC03.
- [ ] Có cơ chế feedback trong SC03, tắt feedback trong SC02.
- [ ] Có tối thiểu 4 biểu đồ theo mục FR-08.
- [ ] Có bảng dữ liệu và export 2 CSV.
- [ ] Có test tối thiểu cho công thức HF, thanh lý, shock và swap.
- [ ] Có README giải thích mô hình, cách chạy và giới hạn.
- [ ] Có ảnh chụp dashboard và dữ liệu để viết báo cáo BTL.

---

## 15. Cấu trúc mã nguồn đề xuất

```text
DeFi-Liquidation-Cascade/
|
|-- app.py                  # Streamlit: sidebar, KPI, tabs
|-- config.py               # Cấu hình mặc định, validation
|-- agents.py               # BorrowerAgent (Mesa)
|-- market.py               # AMMPool và spot/swap
|-- simulation.py           # Mesa Model, liquidation, từng block
|-- scenarios.py            # SC01/SC02/SC03, kết quả tổng hợp
|-- charts.py               # Biểu đồ Matplotlib
|-- requirements.txt        # Khóa các phiên bản thư viện
|-- README.md               # Hướng dẫn cài đặt, chạy, mô hình
|-- requirements.md         # Tài liệu đặc tả này
|
|-- tests/
|   |-- test_agents.py
|   |-- test_market.py
|   |-- test_simulation.py
|
`-- results/                # Tùy chọn: CSV kết quả xuất thủ công
```

### 15.1. Hợp đồng tích hợp giữa 2 người

Engine phải cung cấp một hàm chính, ví dụ:

```python
def run_all_scenarios(config: dict) -> dict:
    """
    Input: cấu hình đã validate.
    Output: {'SC01': SimulationResult,
             'SC02': SimulationResult,
             'SC03': SimulationResult}
    Không phụ thuộc Streamlit.
    """
```

**Người làm UI không sửa công thức trong Engine**; chỉ gọi `run_all_scenarios(...)` và đọc result theo đúng cấu trúc đã thống nhất.

### 15.2. Ví dụ cấu hình truyền vào

```python
config = {
    "shock_pct": 15,
    "pool_a_tvl_usd": 150_000_000,
    "pool_b_tvl_usd": 80_000_000,
    "num_agents": 100,
    "max_blocks": 30,
    "random_seed": 42,
}
```

### 15.3. Cách chạy dự kiến

```bash
python -m venv .venv

# Windows PowerShell:
.venv\Scripts\Activate.ps1

pip install -r requirements.txt
streamlit run app.py
```

Mở trình duyệt theo địa chỉ do Streamlit hiển thị (thông thường là `http://localhost:8501`).

Chạy test:

```bash
pytest -q
```

---

## 16. Phân công nhóm 2 người

### Thành viên 1 — Simulation / Core Logic

**Phụ trách:** `agents.py`, `market.py`, `simulation.py`, `scenarios.py`.

**Nhiệm vụ:**

1. Tạo BorrowerAgent bằng Mesa.
2. Khởi tạo dữ liệu giả lập bằng random seed.
3. Viết công thức HF và xử lý thanh lý một phần.
4. Xây dựng 2 pool AMM, tính giá và hàm swap.
5. Implement shock + 3 scenarios + vòng lặp block.
6. Chuẩn hóa `SimulationResult` cho người 2 sử dụng.
7. Viết unit test cho logic, xử lý lỗi biên.

**Đầu ra bàn giao:** Hàm `run_all_scenarios(config)` chạy độc lập, trả dữ liệu hợp lệ để vẽ biểu đồ.

### Thành viên 2 — UI / Data / Thuyết trình

**Phụ trách:** `app.py`, `charts.py`, tích hợp CSV, README/báo cáo.

**Nhiệm vụ:**

1. Tạo Streamlit sidebar và validate cấu hình trước khi Run.
2. Xây KPI, các tab biểu đồ và bảng dữ liệu.
3. Kết nối API nội bộ Python `run_all_scenarios(config)`.
4. Làm export block results và liquidation events CSV.
5. Kiểm tra scenario từ góc nhìn người dùng.
6. Chuẩn bị ảnh demo, mô tả biểu đồ, cách trình bày kết quả BTL.
7. Phối hợp người 1 giải thích công thức và giới hạn mô hình.

**Đầu ra bàn giao:** Ứng dụng local chạy được với dữ liệu thực tế từ Engine; báo cáo và hướng dẫn demo rõ ràng.

### Công việc chung

- Thống nhất schema dữ liệu **trước khi bắt đầu code UI**.
- Review code cùng nhau, không để một người chỉ làm PowerPoint mà không hiểu hệ thống.
- Cùng chạy test và thuyết trình được chuỗi `Shock → Liquidation → Swap → Price → New Liquidation`.

---

## 17. Tiến độ tham khảo (10–14 ngày)

| Thời gian | Việc chính | Sản phẩm kiểm tra |
|---|---|---|
| Ngày 1–2 | Đọc yêu cầu, thống nhất công thức, schema | Tài liệu requirement được chốt, test HF bằng tay |
| Ngày 3–4 | Agent + Model + AMM | Test tạo 100 Agents, test swap/giá chạy |
| Ngày 5–7 | Liquidation + SC01/02/03 | Engine trả BlockResult và events, test scenario |
| Ngày 8–9 | Streamlit Dashboard | KPI và biểu đồ lấy dữ liệu thật từ engine |
| Ngày 10–11 | Export CSV, kiểm thử toàn hệ thống | Demo ổn định, có ảnh kết quả |
| Ngày 12–14 | Báo cáo, chỉnh lỗi, chuẩn bị bảo vệ | README, báo cáo, slide/demo (nếu cần) |

Lịch là **kế hoạch tham khảo**, không phải yêu cầu cứng của giảng viên.

---

## 18. Nội dung báo cáo BTL tối thiểu

Báo cáo có thể theo bố cục ngắn gọn sau:

1. **Giới thiệu:** DeFi Lending, vấn đề thanh lý dây chuyền và mục tiêu đề tài.
2. **Cơ sở lý thuyết:** ABM, Agent, HF, Liquidation, AMM, ETH/stETH, contagion.
3. **Thiết kế mô hình:** Các Agent, tham số giả định, 2 pool, 3 scenarios, sơ đồ xử lý.
4. **Cài đặt:** Kiến trúc Python/Mesa/Streamlit, cấu trúc source, công thức và luồng thuật toán.
5. **Kết quả thí nghiệm:** Ảnh dashboard, biểu đồ, so sánh SC02/SC03, thảo luận độ sâu thanh khoản.
6. **Kiểm thử và đánh giá:** Test case quan trọng, giới hạn mô hình, kết quả đúng/sai và giải thích.
7. **Kết luận / hướng mở rộng:** Mô hình minh họa được gì; local blockchain là hướng mở rộng tùy chọn.

### Câu hỏi nên tự trả lời được khi bảo vệ

- Tại sao `HF < 1` thì Agent được thanh lý?
- Tại sao SC02 khác SC03 dù dùng cùng bộ Agent?
- Thanh lý stETH làm ETH giảm giá bằng đường đi nào?
- Vì sao pool thanh khoản nhỏ dễ bị tác động giá mạnh hơn?
- Vì sao kết quả giả lập không phải dự báo giá crypto thực tế?
- Local blockchain có cần để chứng minh hiện tượng đang nghiên cứu không?

---

## 19. Rủi ro triển khai và cách xử lý

| Rủi ro | Cách xử lý |
|---|---|
| Scope quá lớn | Chỉ 2 tài sản collateral, 2 pool, 3 scenario; bỏ blockchain local khỏi MVP |
| Code chạy nhưng kết quả phi lý | Viết unit test công thức trước khi làm dashboard; kiểm tra đơn vị token/USD |
| Không thấy thanh lý dây chuyền | Kiểm tra shock, phân bố LTV, quy mô collateral và thanh khoản; không hardcode kết quả |
| SC03 không khác SC02 | Kiểm tra có gọi swap trong SC03, đổi reserves và tính lại giá/HF không |
| Sai số float | Dùng `epsilon`, không so sánh số thực tuyệt đối trong tests |
| Thống kê đếm trùng | Tách `liquidation_events_total` với `liquidated_agents_unique` |
| Thiếu thời gian | Ưu tiên engine → 3 scenario → chart → test; không làm local blockchain |
| Bị hỏi mô hình có giống Aave thật không | Trả lời rõ đây là **mô hình giản lược lấy cảm hứng từ DeFi Lending**, với giả định công khai |

---

## 20. Definition of Done (DoD) — Chốt phạm vi

**Bản BTL chính thức chỉ cần hoàn thành đủ 6 nhóm việc sau:**

1. **ABM:** 100 Borrower Agents có tài sản, nợ và HF độc lập.
2. **Market:** 2 pool ETH/USDC và stETH/ETH theo AMM constant-product.
3. **Liquidation:** Code thanh lý một phần, giảm nợ, lấy collateral, sinh event.
4. **Contagion:** Trong SC03, bán collateral vào AMM và tác động sang HF của Agent khác qua giá mới.
5. **Experiment:** SC01/SC02/SC03 có kết quả so sánh bằng 4 biểu đồ và KPI.
6. **Evidence:** Có test, CSV, hướng dẫn chạy và giải thích được giả định khi bảo vệ.

**Không cần** làm blockchain thật để đáp ứng 6 nhóm việc trên, trừ khi giảng viên bổ sung yêu cầu bắt buộc.

---

## 21. Nguồn tham khảo kỹ thuật

Các nguồn chỉ để tham khảo nguyên lý. **Thông số cụ thể của hệ thống trong tài liệu là giả định của nhóm**:

- Aave — Health Factor & Liquidations: https://aave.dev/help/borrowing/liquidations
- Uniswap — Constant-product AMM & Swapping: https://developers.uniswap.org/docs/protocols/v2/concepts/swapping
- Mesa — Agent-Based Modeling in Python: https://mesa.readthedocs.io/stable/
- Streamlit — Tài liệu: https://docs.streamlit.io/
- Matplotlib — Tài liệu: https://matplotlib.org/stable/

---

**Trạng thái tài liệu:** Ready for implementation.  
**Ưu tiên thực hiện:** Core Engine → Test → Dashboard → CSV → Báo cáo.  
**Nguyên tắc cuối:** Làm đúng cơ chế và giải thích được kết quả quan trọng hơn giao diện quá đẹp hoặc tích hợp blockchain cho có.
