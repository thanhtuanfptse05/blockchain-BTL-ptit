# BÁO CÁO BÀI TẬP LỚN MÔN CÔNG NGHỆ CHUỖI KHỐI (BLOCKCHAIN TECHNOLOGY)
# Đề tài: Mô phỏng Lây lan Rủi ro Thanh lý Chéo Tài sản trong DeFi Lending bằng Mô hình Tác tử (Agent-Based Model)

**Đơn vị đào tạo:** Học viện Công nghệ Bưu chính Viễn thông (PTIT)  
**Khoa:** Công nghệ Thông tin  
**Nhóm sinh viên thực hiện:**
- Sinh viên 1: [Họ và tên SV 1] — Mã sinh viên: [MSV 1] (Core Simulator Lead)
- Sinh viên 2: [Họ và tên SV 2] — Mã sinh viên: [MSV 2] (UI & Data Visualization Lead)  
**Giảng viên hướng dẫn:** [Học hàm, Học vị, Họ và tên Giảng viên]  
**Hà Nội, 2026**

---

## MỤC LỤC
- **LỜI CẢM ƠN**
- **DANH MỤC TỪ VIẾT TẮT VÀ THUẬT NGỮ**
- **CHƯƠNG 1: GIỚI THIỆU VÀ TỔNG QUAN BÀI TOÁN**
  - 1.1. Bối cảnh nghiên cứu rủi ro hệ thống trong DeFi Lending
  - 1.2. Vấn đề trượt giá AMM và vòng xoáy thanh lý (Liquidation Feedback Loop)
  - 1.3. Rủi ro lây lan chéo tài sản (Cross-Asset Contagion với stETH)
  - 1.4. Mục tiêu và phạm vi nghiên cứu của đề tài
- **CHƯƠNG 2: CƠ SỞ LÝ THUYẾT VÀ MÔ HÌNH TOÁN HỌC**
  - 2.1. Cơ chế cho vay thế chấp và tỷ lệ sức khỏe (Health Factor)
  - 2.2. Cơ chế thanh lý một phần (Partial Liquidation)
  - 2.3. Mô hình sàn giao dịch phi tập trung tích số không đổi (AMM Constant-Product)
  - 2.4. Công thức đo lường tỷ lệ mất peg / chiết khấu stETH (Discount)
  - 2.5. Cơ chế ghi nhận nợ xấu giao thức (Bad Debt)
- **CHƯƠNG 3: THIẾT KẾ KIẾN TRÚC VÀ CÀI ĐẶT HỆ THỐNG**
  - 3.1. Phương pháp luận phát triển hướng đặc tả (Spec-Driven Development)
  - 3.2. Kiến trúc phần mềm phân tầng sạch (Clean Architecture)
  - 3.3. Mô hình hóa quần thể tác tử người vay (Borrower Agents)
  - 3.4. Thiết kế lộ trình xả tài sản thế chấp (Liquidation Selling Route)
  - 3.5. Thiết kế 3 kịch bản thí nghiệm đối chứng (SC01, SC02, SC03)
- **CHƯƠNG 4: KẾT QUẢ THỰC NGHIỆM VÀ PHÂN TÍCH ĐÁNH GIÁ**
  - 4.1. Bảng số liệu đối chứng tổng hợp giữa 3 kịch bản
  - 4.2. Phân tích diễn biến giá ETH và tỷ lệ chiết khấu stETH
  - 4.3. Phân tích phân bổ sự kiện thanh lý và người vay vỡ nợ lũy kế
  - 4.4. Phân tích sự hình thành và bùng nổ nợ xấu giao thức
  - 4.5. Đánh giá độ nhạy cảm của độ sâu thanh khoản (Pool TVL Sensitivity)
- **CHƯƠNG 5: GIỚI HẠN NGHIÊN CỨU VÀ HƯỚNG PHÁT TRIỂN**
  - 5.1. Các giả định đơn giản hóa và giới hạn của mô hình
  - 5.2. Đề xuất hướng phát triển mở rộng
- **KẾT LUẬN**
- **TÀI LIỆU THAM KHẢO**

---

## DANH MỤC TỪ VIẾT TẮT VÀ THUẬT NGỮ

| Thuật ngữ | Tên viết tắt | Định nghĩa / Ý nghĩa trong đề tài |
| :--- | :---: | :--- |
| **Agent-Based Model** | **ABM** | Mô hình tính toán mô phỏng hành vi và tương tác của các tác tử độc lập |
| **Automated Market Maker** | **AMM** | Cơ chế tạo lập thị trường tự động trên sàn phi tập trung (ví dụ: Uniswap) |
| **Health Factor** | **HF** | Chỉ số sức khỏe vị thế nợ; vị thế bị thanh lý khi $HF < 1.0$ |
| **Liquidation Threshold** | **LT** | Ngưỡng thanh lý an toàn (trong đề tài đặt chuẩn $LT = 0.80$) |
| **Loan-to-Value** | **LTV** | Tỷ lệ dư nợ trên giá trị tài sản thế chấp ($Debt / Collateral$) |
| **Close Factor** | — | Tỷ lệ nợ tối đa được phép thanh lý trong một lần (trong đề tài đặt $50\%$) |
| **Liquidation Penalty** | — | Mức phí thưởng chiết khấu cho người thanh lý (trong đề tài đặt $5\%$) |
| **Total Value Locked** | **TVL** | Tổng giá trị tài sản được khóa trong pool thanh khoản |
| **Bad Debt** | — | Nợ xấu; phần nợ giao thức không thể thu hồi do tài sản thế chấp không đủ |
| **Constant-Product** | **CPMM** | Mô hình định giá AMM tuân thủ bất biến $x \cdot y = k$ |

---

## CHƯƠNG 1: GIỚI THIỆU VÀ TỔNG QUAN BÀI TOÁN

### 1.1. Bối cảnh nghiên cứu rủi ro hệ thống trong DeFi Lending
Trong hệ sinh thái tài chính phi tập trung (DeFi), các giao thức cho vay (như Aave, Compound) vận hành theo cơ chế thế chấp vượt mức (Over-collateralization). Người dùng gửi tài sản mã hóa (như ETH, stETH) làm tài sản thế chấp để vay ra các tài sản ổn định (như USDC). Để đảm bảo khả năng thanh toán, giao thức giám sát liên tục tỷ lệ an toàn của từng vị thế. Khi thị trường biến động mạnh, giá trị tài sản thế chấp sụt giảm có thể đẩy các vị thế vào ngưỡng rủi ro thanh lý.

### 1.2. Vấn đề trượt giá AMM và vòng xoáy thanh lý (Liquidation Feedback Loop)
Khác với tài chính truyền thống nơi việc giải chấp có thể được giãn tiến độ hoặc tái cơ cấu nợ, trong DeFi thanh lý được thực thi tự động bởi các tác tử độc lập (Liquidator bots). Sau khi thanh toán một phần nợ để nhận về tài sản thế chấp với mức thưởng 5%, Liquidator lập tức bán tháo lượng tài sản này lên các sàn AMM để chốt lời sang đồng tiền định giá nợ (USDC). 

Hành vi bán tháo khối lượng lớn trong thời gian ngắn tạo ra độ trượt giá (Slippage) đáng kể trên AMM theo quy luật $x \cdot y = k$. Mức trượt giá này kéo giá thị trường tiếp tục sụt giảm, dẫn tới việc làm giảm Health Factor của các vị thế khác vốn đang an toàn, đẩy chúng vào diện thanh lý ở các khối (block) tiếp theo. Đây chính là **Vòng xoáy phản hồi tiêu cực (Contagion Feedback Loop)**.

### 1.3. Rủi ro lây lan chéo tài sản (Cross-Asset Contagion với stETH)
Sự bùng nổ của các sản phẩm phái sinh staking thanh khoản (Liquid Staking Derivatives - LSD), tiêu biểu là Lido stETH, đã tạo ra một lớp rủi ro lây lan chéo phức tạp. stETH được neo giá lý thuyết 1:1 với ETH nhưng giao dịch độc lập trên thị trường thứ cấp. Khi các vị thế thế chấp stETH bị thanh lý, Liquidator không thể bán trực tiếp lấy USDC mà phải thực hiện lộ trình 2 chặng:
1. Bán stETH vào Pool stETH/ETH để nhận ETH $\to$ Kéo dãn chênh lệch tỷ giá, gây ra hiện tượng **mất peg (Depeg)** của stETH so với ETH.
2. Bán lượng ETH vừa nhận vào Pool ETH/USDC $\to$ Làm giá ETH giảm sâu hơn nữa.

Hiệu ứng này khuếch đại lẫn nhau: giá ETH giảm làm stETH giảm theo USD; áp lực bán stETH lại dội ngược về đè bẹp giá ETH.

### 1.4. Mục tiêu và phạm vi nghiên cứu
- **Mục tiêu:** Xây dựng công cụ mô phỏng động học tác tử chạy local bằng Python, khảo sát định lượng tác động khuếch đại của cơ chế thanh lý AMM lên độ ổn định hệ thống.
- **Phạm vi:** Mô phỏng 100 tác tử người vay, 2 pool AMM (ETH/USDC và stETH/ETH) qua chuỗi 30 khối liên tiếp dưới tác động của cú sốc ngoại sinh ban đầu 15%.

---

## CHƯƠNG 2: CƠ SỞ LÝ THUYẾT VÀ MÔ HÌNH TOÁN HỌC

### 2.1. Cơ chế cho vay thế chấp và tỷ lệ sức khỏe (Health Factor)
Hệ số an toàn vị thế (Health Factor - $HF$) được định nghĩa theo chuẩn giao thức Aave:
$$HF = \frac{\sum (Collateral_i \times Price_i \times LT_i)}{Debt}$$
- $Collateral_i$: Số lượng tài sản thế chấp loại $i$ (ETH hoặc stETH).
- $Price_i$: Giá thị trường hiện hành của tài sản $i$ quy đổi ra USD.
- $LT_i$: Ngưỡng thanh lý (Liquidation Threshold), đặt cố định $LT = 0.80$ (80%).
- $Debt$: Tổng giá trị dư nợ vay bằng USD.
- **Quy tắc kích hoạt thanh lý:** Vị thế đủ điều kiện thanh lý khi và chỉ khi $HF < 1.0$.

### 2.2. Cơ chế thanh lý một phần (Partial Liquidation)
Để hạn chế việc phạt quá mức người vay, giao thức áp dụng cơ chế thanh lý từng phần (Aave v3 standard):
- **Tỷ lệ nợ tối đa được trả (Close Factor):** $50\%$ tổng dư nợ hiện tại:
  $$\text{DebtRepaid} = Debt \times 0.50$$
- **Mức phí thưởng thanh lý (Liquidation Bonus):** $5\%$ ($Penalty = 1.05$).
- **Số lượng tài sản thế chấp bị tịch thu:**
  $$\text{CollateralSeized} = \frac{\text{DebtRepaid} \times 1.05}{Price_{collateral}}$$
- Nếu $\text{CollateralSeized} > Collateral_{current}$, người thanh lý chỉ tịch thu toàn bộ số tài sản hiện có; khoản nợ tương ứng chưa được bù đắp sẽ trở thành **Nợ xấu (Bad Debt)** của giao thức.

### 2.3. Mô hình sàn giao dịch AMM tích số không đổi ($x \cdot y = k$)
Áp dụng mô hình Constant-Product Market Maker không thu phí giao dịch ($fee = 0$) để cách ly thuần túy tác động của trượt giá cơ bản:
$$x \cdot y = k$$
Khi người thanh lý bán lượng tài sản đầu vào $\Delta x$, lượng tài sản đầu ra $\Delta y$ nhận về được tính bằng:
$$\Delta y = \frac{y \cdot \Delta x}{x + \Delta x}$$
Dự trữ mới sau swap là $x' = x + \Delta x$ và $y' = y - \Delta y$. Giá giao ngay mới được xác định bởi:
$$P' = \frac{y'}{x'}$$

### 2.4. Công thức đo lường tỷ lệ chiết khấu stETH (Discount)
Đo lường mức độ mất giá của stETH so với tài sản cơ sở ETH:
$$\text{Discount}(\%) = \frac{P_{ETH} - P_{stETH}}{P_{ETH}} \times 100\%$$

### 2.5. Cơ chế ghi nhận nợ xấu (Bad Debt)
Nợ xấu phát sinh khi một vị thế có giá trị tài sản thế chấp không đủ để chi trả cho khoản nợ được giải chấp kèm phí thưởng:
$$\text{BadDebt} = \max\left(0, \text{DebtRepaid} - \frac{Collateral_{available} \times Price}{1.05}\right)$$

---

## CHƯƠNG 3: THIẾT KẾ KIẾN TRÚC VÀ CÀI ĐẶT HỆ THỐNG

### 3.1. Phương pháp luận phát triển hướng đặc tả (Spec-Driven Development)
Nhóm áp dụng quy trình nghiêm ngặt gồm 10 feature specs:
1. `001-simulation-config`: Tham số cấu hình và kiểm tra hợp lệ C-01..C-10.
2. `002-borrower-agent-generation`: Khởi tạo tác tử ngẫu nhiên có hạt giống.
3. `003-health-factor-eligibility`: Định giá vị thế và kiểm tra điều kiện thanh lý.
4. `004-partial-liquidation-engine`: Thực thi thanh lý một phần và tính nợ xấu.
5. `005-amm-pools`: Khởi tạo và thực thi swap trên 2 pool AMM.
6. `006-scenario-block-simulation`: Vòng lặp điều phối mô phỏng theo khối.
7. `007-analytics-kpi-summary`: Trích xuất 6 KPI và bảng so sánh đối chứng.
8. `008-charts-visualization`: Tạo 4 biểu đồ Plotly tương tác.
9. `009-data-tables-csv-export`: Xuất dữ liệu ra file CSV chuẩn RFC 4180.
10. `010-streamlit-dashboard-ui`: Giao diện Dashboard một trang hoàn chỉnh.

### 3.2. Kiến trúc phân tầng sạch (Clean Architecture)
```text
src/
├── domain/       # Thực thể lõi: BorrowerAgent, AMMPool, LiquidationEvent, BlockResult
├── usecase/      # Nghiệp vụ: agent_generator, health_factor, liquidation_engine, amm_engine, scenario_runner
├── infra/        # Hạ tầng: exporter.py (CSV export)
└── interface/    # Giao diện: app.py, theme.py, components/
```

### 3.3. Mô hình hóa 100 Tác tử Người vay
- Phân bổ 50 vị thế thế chấp ETH và 50 vị thế thế chấp stETH.
- Giá trị thế chấp ban đầu: Mỗi tác tử sở hữu lượng collateral tương đương $\$250,000$ đến $\$1,000,000$ USD.
- Tỷ lệ LTV ban đầu phân bổ đều trong khoảng $[0.55, 0.72]$, đảm bảo ban đầu $100\%$ tác tử có $HF > 1.0$ (an toàn tuyệt đối).

### 3.4. Thiết kế 3 Kịch bản Thí nghiệm Đối chứng
1. **SC01 (Baseline - Môi trường tĩnh):** Giá ETH giữ nguyên $\$3,000$ USD qua tất cả các khối $\to$ Làm chuẩn đối chứng ổn định (0 thanh lý, 0 nợ xấu).
2. **SC02 (Direct Shock - Cú sốc ngoại sinh không phản hồi):** Giá ETH giảm $15\%$ tại block 1 (xuống $\$2,550$), nhưng collateral sau thanh lý KHÔNG bán vào AMM $\to$ Đo lường tác động thuần túy của cú sốc ban đầu.
3. **SC03 (Cascade Contagion - Lây lan phản hồi chéo):** Cú sốc $15\%$ tại block 1 kích hoạt thanh lý; Liquidator xả toàn bộ collateral vào 2 pool AMM $\to$ Khảo sát hiệu ứng vòng xoáy lây lan.

---

## CHƯƠNG 4: KẾT QUẢ THỰC NGHIỆM VÀ PHÂN TÍCH ĐÁNH GIÁ

### 4.1. Bảng số liệu đối chứng tổng hợp
Với cấu hình mặc định (Shock 15%, Pool A \$150M, Pool B \$80M, 100 Borrowers, 30 Blocks, Seed 42), kết quả thực nghiệm thu được:

| Chỉ số Khảo sát | SC01 Baseline | SC02 Direct Shock | SC03 Cascade Contagion | Chênh lệch (SC03 - SC02) | Tỷ lệ Tăng tương đối |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Giá ETH cuối cùng** | $3,000.00 | $2,550.00 | **$988.92** | -$1,561.08 | **-61.22%** |
| **Giá stETH cuối cùng** | $2,970.00 | $2,524.50 | **$318.72** | -$2,205.78 | **-87.37%** |
| **Tỷ lệ chiết khấu stETH** | 1.00% | 1.00% | **67.77%** | +66.77% | **+66.77% (Depeg)** |
| **Số Agent bị thanh lý** | 0 / 100 | 17 / 100 | **100 / 100** | +83 agents | **+488.24%** |
| **Tổng số lượt thanh lý** | 0 | 17 | **214** | +197 lượt | **+1,158.82%** |
| **Nợ xấu phát sinh** | $0.00 | $0.00 | **$14,265,389.56** | +$14.27M | **Bùng nổ nợ xấu** |

### 4.2. Phân tích Hiện tượng Depeg và Bùng nổ Nợ xấu
1. **Hiệu ứng khuếch đại thanh lý:** Cú sốc ban đầu chỉ đủ làm vỡ nợ 17 người vay có LTV cao trong SC02. Tuy nhiên, trong SC03, áp lực bán tháo liên hoàn vào AMM đã đẩy toàn bộ 100 người vay vào tình trạng vỡ nợ cuốn chiếu (+488.24%).
2. **Hiện tượng Depeg nghiêm trọng của stETH:** Tỷ lệ chiết khấu stETH tăng vọt từ 1.00% lên tới 67.77%, kéo giá stETH xuống \$318.72 USD do thanh khoản Pool B (\$80M) bị áp đảo hoàn toàn bởi lượng stETH bán tháo.
3. **Sự hình thành Nợ xấu:** Do giá tài sản sập quá nhanh qua các khối, giá trị tài sản thế chấp còn lại của các vị thế không đủ bù đắp nợ vay, tạo ra hơn \$14.26 triệu USD nợ xấu không thể thu hồi.

---

## CHƯƠNG 5: GIỚI HẠN NGHIÊN CỨU VÀ HƯỚNG PHÁT TRIỂN

### 5.1. Giới hạn nghiên cứu
1. Mô hình AMM cơ bản Constant-Product phí 0%; chưa xét cơ chế thanh khoản tập trung (Uniswap v3).
2. Chưa xét tác tử kinh doanh chênh lệch giá (Arbitrageur) tái cân bằng tỷ giá giữa hai pool.
3. Quá trình thanh lý hoàn tất tức thời trong cùng block; phí gas mạng lưới giả định bằng 0.

### 5.2. Đề xuất hướng phát triển
- Tích hợp mô hình thanh khoản tập trung (Concentrated Liquidity) với các dải thanh khoản động.
- Bổ sung tác tử Arbitrageur với ngưỡng vốn và chi phí vốn thực tế.

---

## KẾT LUẬN
Đề tài **DeFi Liquidation Cascade Simulator** đã hoàn thành xuất sắc toàn bộ mục tiêu đề ra:
1. Xây dựng thành công mô hình toán học và phần mềm mô phỏng vi mô chính xác, tất định 100%, bảo toàn các bất biến tài chính DeFi.
2. Cung cấp giao diện trực quan hóa dữ liệu hiện đại, hỗ trợ xuất báo cáo và biểu đồ chuyên nghiệp.
3. Đạt tiêu chuẩn chất lượng kỹ thuật cao với 73/73 bài kiểm thử tự động vượt qua 100%.

---

## TÀI LIỆU THAM KHẢO
1. Aave Protocol. (2022). *Aave V3 Technical Whitepaper*.
2. Adams, H., Zinsmeister, N., & Robinson, D. (2020). *Uniswap v2 Core Whitepaper*.
3. Lido DAO. (2021). *Lido Liquid Staking on Ethereum Architecture*.
4. Gudgeon, L., et al. (2020). *DeFi Protocols for Loanable Funds: Interest Rates, Liquidation, and Market Efficiency*. ACM Conference.

