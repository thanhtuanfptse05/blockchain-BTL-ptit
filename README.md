# DeFi Liquidation Cascade Simulator

**Mô phỏng lây lan rủi ro thanh lý chéo tài sản trong DeFi Lending (Agent-Based Model)**

Dự án Bài tập lớn môn Công nghệ Chuỗi khối (Blockchain Technology).

---

## 1. Giới thiệu Đề tài

Trong các giao thức cho vay phi tập trung (DeFi Lending Protocols như Aave, Compound), các vị thế vay nợ được đảm bảo bằng tài sản thế chấp (Collateral). Khi thị trường xảy ra biến động giá mạnh, giá trị tài sản thế chấp sụt giảm khiến tỷ lệ sức khỏe (**Health Factor - $HF$**) rơi xuống dưới ngưỡng an toàn ($HF < 1.0$). 

Cơ chế thanh lý được kích hoạt: bên thứ ba (Liquidator) trả nợ thay cho người vay để tịch thu tài sản thế chấp với mức chiết khấu ưu đãi (Liquidation Bonus). Liquidator sau đó ngay lập tức bán tháo lượng tài sản này lên các sàn giao dịch phi tập trung (**Automated Market Maker - AMM**) để thu hồi vốn và chốt lời. Việc bán tháo ồ ạt này tạo ra trượt giá (**Slippage**), kéo giá tài sản trên AMM giảm sâu hơn nữa, kích hoạt làn sóng thanh lý tiếp theo đối với các tài khoản khác.

Dự án **DeFi Liquidation Cascade Simulator** xây dựng một ứng dụng mô phỏng dựa trên tác tử (**Agent-Based Model - ABM**) chạy local hoàn toàn bằng Python, khảo sát hiệu ứng phản hồi giảm giá và sự lây lan rủi ro chéo (**Cross-Asset Contagion**) giữa hai tài sản thế chấp phổ biến: **ETH** và phái sinh staking thanh khoản **stETH** qua 2 AMM Pool (Pool A: ETH/USDC và Pool B: stETH/ETH).

---

## 2. Phân công Thành viên & Vai trò (Nhóm 2 Sinh viên)

| Thành viên | Vai trò | Trách nhiệm chính | Thư mục phụ trách |
| :--- | :--- | :--- | :--- |
| **Thành viên 1** | **Core Simulator Lead** | - Kiến trúc Domain Entities và Usecase lõi.<br>- Công thức Health Factor, AMM Swaps ($x \cdot y = k$), Partial Liquidation Engine.<br>- Scenario Runner (3 kịch bản: SC01, SC02, SC03) và Pytest suite (Unit & System tests). | `src/domain/`<br>`src/usecase/`<br>`tests/` |
| **Thành viên 2** | **UI & Data Viz Lead** | - Xây dựng giao diện Streamlit Dashboard tương tác.<br>- 6 Thẻ KPI tổng kết, bảng so sánh đối chứng delta (FR-11).<br>- 4 Biểu đồ Plotly động (Giá ETH, Discount stETH, Breakdown thanh lý, Lũy kế Agent).<br>- Module xuất file CSV chuẩn RFC 4180 và Tab Cơ chế học thuật (FR-10). | `src/interface/`<br>`src/infra/` |

---

## 3. Kiến trúc Phần mềm (Clean Architecture)

Dự án tuân thủ nghiêm ngặt nguyên tắc phân lớp Clean Architecture và nguyên tắc Spec-First (Spec-Driven Development):

```text
BTL-block-chain/
├── src/
│   ├── domain/               # Tầng Thực thể (Entities & Models)
│   │   ├── agent.py          # BorrowerAgent, AssetType, AgentStatus
│   │   ├── amm_pool.py       # AMMPool (Constant-Product x*y=k)
│   │   ├── block_result.py   # BlockResult (12 trường dữ liệu theo block)
│   │   ├── config.py         # SimulationConfig (Pydantic v2 validation)
│   │   ├── liquidation_event.py # LiquidationEvent (10 trường chi tiết sự kiện)
│   │   └── simulation_result.py # KPISummary & SimulationResult container
│   ├── usecase/              # Tầng Nghiệp vụ Mô phỏng
│   │   ├── agent_generator.py   # Khởi tạo quần thể Borrower ngẫu nhiên có seed
│   │   ├── amm_engine.py        # Swap AMM zero-fee, định giá spot & discount
│   │   ├── health_factor.py     # Tính toán Health Factor & phát hiện nợ xấu
│   │   ├── liquidation_engine.py# Thanh lý một phần (Close Factor 50%, Bonus 5%)
│   │   └── scenario_runner.py   # Điều phối vòng lặp mô phỏng 3 kịch bản
│   ├── infra/                # Tầng Hạ tầng Dữ liệu
│   │   └── exporter.py          # Chuyển đổi DataFrame & xuất CSV chuẩn UTF-8
│   └── interface/            # Tầng Giao diện Người dùng (Presentation)
│       ├── app.py            # Streamlit Main Dashboard & Tab Router
│       ├── theme.py          # Hệ thống CSS Light Theme & Design Tokens
│       └── components/       # Các khối giao diện tái sử dụng
│           ├── sidebar.py    # Sliders tham số, presets và nút bấm Chạy / Đặt lại
│           ├── metrics.py    # 6 Thẻ KPI phẳng tối giản và bảng so sánh delta
│           ├── charts.py     # 4 Biểu đồ Plotly tương tác chuẩn Light Mode
│           ├── data_tab.py   # Bảng dữ liệu tương tác & nút tải CSV
│           └── methodology_tab.py # Tab cơ chế, công thức KaTeX & giới hạn
├── .streamlit/               # Cấu hình Theme Light Mode của Streamlit
│   └── config.toml           # Ép buộc Light Theme và font chữ chuẩn
├── specs/                    # Bộ hồ sơ Đặc tả Spec Kit (001 đến 010)
├── tests/                    # Bộ kiểm thử tự động (Pytest)
│   ├── unit/                 # Unit tests cho từng module thành thành
│   └── system/               # System tests xác minh bất biến 3 kịch bản
├── requirements.txt          # Danh mục thư viện phụ thuộc
└── README.md                 # Tài liệu hướng dẫn sử dụng
```

---

## 4. Yêu cầu Cài đặt & Hướng dẫn Sử dụng

### 4.1. Môi trường yêu cầu
- **Python**: `>= 3.10` (Đã kiểm thử tương thích hoàn hảo trên Python 3.10 - 3.14).
- **Hệ điều hành**: Windows, macOS, hoặc Linux.

### 4.2. Cài đặt thư viện phụ thuộc
Mở terminal tại thư mục gốc của dự án và chạy:

```bash
pip install -r requirements.txt
```

### 4.3. Chạy ứng dụng Streamlit Dashboard
Khởi chạy giao diện người dùng trực quan trên trình duyệt local:

```bash
# Cách 1 (Khuyên dùng - hoạt động trên mọi hệ thống):
python -m streamlit run src/interface/app.py

# Cách 2 (Nếu thư mục Scripts của Python đã có trong PATH):
streamlit run src/interface/app.py
```

Trình duyệt sẽ tự động mở tại địa chỉ `http://localhost:8501`.

---

## 5. Hướng dẫn Chạy Bộ Kiểm thử (Test Suite)

Dự án sở hữu bộ kiểm thử tự động toàn diện với **73 bài kiểm thử (100% Pass Rate)** bao phủ cả Unit Tests và System Tests:

```bash
# Chạy toàn bộ test suite kèm log chi tiết
python -m pytest -v

# Chỉ chạy các bài kiểm thử hệ thống bất biến (System Tests ST-01..ST-07)
python -m pytest tests/system/test_system_scenarios.py -v

# Chỉ chạy kiểm thử các module nghiệp vụ lõi (Unit Tests)
python -m pytest tests/unit/ -v
```

---

## 6. Mô tả 3 Kịch bản Mô phỏng

| Mã Kịch bản | Tên Kịch bản | Cơ chế Hoạt động | Mục đích Khoa học |
| :--- | :--- | :--- | :--- |
| **SC01** | **Baseline (Môi trường tĩnh)** | Giá ETH duy trì không đổi ở $3,000 USD qua tất cả các block. | Làm chuẩn đối chứng: xác nhận hệ thống ổn định, không có thanh lý giả tạo (0 thanh lý, 0 nợ xấu). |
| **SC02** | **Direct Shock (Cú sốc Trực tiếp)** | Giá ETH giảm ngoại sinh 15% tại block 1 (xuống $2,550 USD), nhưng việc thanh lý **KHÔNG** bán collateral vào AMM (giá giữ phẳng ở $2,550). | Đo lường số lượng vị thế mất an toàn thuần túy do biến động giá ban đầu gây ra, không có hiệu ứng phản hồi. |
| **SC03** | **Cascade Contagion (Lây lan Chuỗi)** | Cú sốc 15% tại block 1 kích hoạt thanh lý; Liquidator **bán toàn bộ Collateral vào 2 Pool AMM** (ETH bán vào Pool A; stETH bán vào Pool B đổi lấy ETH rồi bán tiếp vào Pool A). Giá AMM tiếp tục giảm sâu và stETH mất peg. | Chứng minh định lượng hiệu ứng vòng xoáy khuếch đại sụp đổ giá và sự lây lan rủi ro chéo tài sản. |

---

## 7. Các Chỉ số & Biểu đồ Phân tích

### 7.1. 6 Thẻ KPI Cốt lõi (SC03 Summary)
1. **Giá ETH cuối ($)**: Giá giao ngay trên Pool A tại block cuối cùng.
2. **Giá stETH cuối ($)**: Giá giao dịch quy đổi của stETH sang USD tại block cuối cùng.
3. **Discount stETH (%)**: Mức chiết khấu/mất peg của stETH so với ETH ($P_{ETH} - P_{stETH}) / P_{ETH}$.
4. **Agents bị thanh lý**: Số lượng Borrower duy nhất rơi vào diện bị thanh lý và tỷ lệ trên tổng số.
5. **Tổng event thanh lý**: Tổng số lần kích hoạt thanh lý một phần qua các block.
6. **Nợ xấu cuối ($)**: Tổng nợ không thể thu hồi do tài sản thế chấp không đủ bù đắp nợ và phí thưởng.

### 7.2. 4 Biểu đồ Phân tích Trực quan (Plotly)
1. **Biến động giá ETH theo Block**: So sánh đường giá ETH của SC01 (đi ngang), SC02 (giảm 1 lần), và SC03 (dốc xuống liên tục). Có vạch chú thích tại block 1.
2. **Tỉ lệ Chiết khấu / Depeg của stETH**: Phản ánh hiện tượng stETH bị depeg sâu trong SC03 khi lượng stETH thanh lý bị xả ồ ạt vào Pool B.
3. **Phân bổ thanh lý theo Tài sản**: Biểu đồ cột chồng phân loại số sự kiện thanh lý vị thế nợ ETH và stETH theo từng block.
4. **Số lượng Borrower bị thanh lý lũy kế**: So sánh số người vay duy nhất bị ảnh hưởng giữa SC02 và SC03.

---

## 8. Bảng Dữ liệu & Xuất File CSV

Người dùng có thể tải về 2 file CSV phục vụ công tác nghiên cứu độc lập:
1. `block_results.csv`: 12 cột chuẩn ghi nhận biến động giá, dự trữ AMM, số vụ thanh lý và nợ xấu theo từng block của cả 3 kịch bản.
2. `liquidation_events.csv`: 10 cột chuẩn ghi nhận chi tiết từng vụ thanh lý (Block, Agent ID, Asset, HF trước thanh lý, Nợ đã trả, Collateral bị tịch thu, v.v.).

---

## 9. Khuyến cáo & Giới hạn Nghiên cứu (§13)

- **Mục đích học thuật**: Dữ liệu và kết quả hoàn toàn được sinh ra từ mô hình mô phỏng giả lập; không cấu thành dự báo thị trường thực tế hay lời khuyên đầu tư tài chính.
- **Giới hạn mô hình**:
  - AMM sử dụng mô hình Constant-Product ($x \cdot y = k$) phí 0%; chưa mô phỏng Concentrated Liquidity (Uniswap v3).
  - Giả định không có Arbitrageur cân bằng lại giá lệch giữa các pool trong lúc khủng hoảng.
  - Phí gas mạng lưới giả định bằng 0 và quá trình thanh lý hoàn tất tức thì trong block.

## 10. Tài liệu Thuyết trình & Hướng dẫn Bảo vệ Đồ án

- **Kịch bản Thuyết trình & Trả lời Phản biện (Q&A)**: Xem chi tiết tại [`docs/DEFENSE_GUIDE.md`](file:///d:/wd/c/sang/d/Documents/BTL-block-chain/docs/DEFENSE_GUIDE.md).
  - Phân vai thuyết trình giữa 2 thành viên (Thời lượng 7-10 phút).
  - Phân tích số liệu thực nghiệm thực tế thu được từ mô hình.
  - Bộ 6 câu hỏi phản biện kinh điển của Hội đồng kèm câu trả lời chuẩn mực toán học.

---
*Dự án hoàn thành đúng thời hạn, tuân thủ 100% nguyên tắc Spec-First và Clean Architecture.*

