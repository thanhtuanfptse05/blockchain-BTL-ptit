# Dàn ý Slide Thuyết trình Báo cáo BTL (Slide Deck Outline)
## Đề tài: DeFi Liquidation Cascade Simulator (Mô phỏng Lây lan Rủi ro Thanh lý Chéo trong DeFi Lending)

**Môn học:** Công nghệ Chuỗi khối (Blockchain Technology) — Học viện Công nghệ Bưu chính Viễn thông (PTIT)  
**Quy mô:** Nhóm 2 sinh viên  
**Thời lượng:** 7 - 10 phút thuyết trình + 5 phút hỏi đáp (Q&A)  
**Công cụ khuyến nghị:** PowerPoint, Canva, hoặc Google Slides  

---

### Slide 1: Trang Bìa (Title Slide)
- **Tiêu đề lớn:** DeFi Liquidation Cascade Simulator
- **Tiêu đề phụ:** Khảo sát Sự Lây lan Rủi ro Thanh lý Chéo Tài sản và Trượt giá AMM trong DeFi Lending bằng Mô hình Agent-Based Model
- **Thông tin nhóm:**
  - Giảng viên hướng dẫn: [Tên Thầy/Cô]
  - Thành viên 1: [Họ và tên SV 1] - Core Simulator Lead (Kiến trúc Nghiệp vụ & Mô hình Toán)
  - Thành viên 2: [Họ và tên SV 2] - UI & Data Visualization Lead (Giao diện & Trực quan hóa Dữ liệu)
- **Speaker Note (0.5 phút - Cả 2):**
  - Chào Thầy/Cô và Hội đồng. Giới thiệu đề tài nghiên cứu về rủi ro hệ thống trong tài chính phi tập trung (DeFi).

---

### Slide 2: Vấn đề Nghiên cứu & Động lực Thực tiễn (Problem Statement)
- **Bối cảnh thực tế:**
  - Các giao thức DeFi Lending (Aave, Compound) yêu cầu thế chấp vượt mức (Over-collateralization).
  - Khi thị trường biến động mạnh, giá tài sản giảm $\to$ Kích hoạt thanh lý vị thế nợ.
- **Vòng xoáy phản hồi tiêu cực (Contagion Feedback Loop):**
  - Liquidator thanh lý nợ $\to$ Tịch thu tài sản thế chấp $\to$ Bán tháo ngay lên sàn AMM (Uniswap, Curve) $\to$ Gây trượt giá (Slippage) $\to$ Kéo giá thị trường giảm sâu hơn nữa $\to$ Đẩy thêm các vị thế khác vào diện bị thanh lý!
- **Rủi ro lây lan chéo tài sản (Cross-Asset Contagion):**
  - Sự xuất hiện của tài sản phái sinh staking thanh khoản (**stETH**) làm cầu nối lây lan: Bán stETH làm mất peg so với ETH, đồng thời gián tiếp xả ETH vào pool thanh khoản USD.
- **Speaker Note (1 phút - Thành viên 1):**
  - Nhấn mạnh: Rủi ro lớn nhất không phải là cú sốc ban đầu, mà là sự khuếch đại do cơ chế thanh lý bán tháo vào AMM.

---

### Slide 3: Kiến trúc Phần mềm & Phương pháp Tiếp cận (Architecture & Methodology)
- **Phương pháp tiếp cận:**
  - **Agent-Based Modeling (ABM):** Mô phỏng vi mô hành vi của 100 tác tử người vay độc lập.
  - **Spec-Driven Development (SDD):** Xây dựng 10 bản đặc tả EARS chuẩn GitHub Spec Kit trước khi viết code.
  - **Clean Architecture:** Tách biệt triệt để 4 tầng:
    * `domain/`: Thực thể bất biến (`BorrowerAgent`, `AMMPool`, `LiquidationEvent`, `BlockResult`).
    * `usecase/`: Logic toán học (`agent_generator`, `health_factor`, `liquidation_engine`, `amm_engine`, `scenario_runner`).
    * `infra/`: Xuất dữ liệu CSV chuẩn RFC 4180.
    * `interface/`: Streamlit Dashboard, biểu đồ Plotly tương tác.
- **Nguyên tắc kỹ thuật cốt lõi:**
  - 100% kết quả sinh ra động từ công thức toán học, **không gán cứng (hardcode)**.
  - Bảo toàn tuyệt đối tích số bất biến $x \cdot y = k$ qua mọi giao dịch swap.
  - Tất định 100% thông qua cơ chế hạt giống ngẫu nhiên (`seed=42`).
- **Speaker Note (1 phút - Thành viên 1):**
  - Giải thích việc áp dụng Clean Architecture giúp mô hình độc lập hoàn toàn với giao diện và dễ dàng mở rộng.

---

### Slide 4: Mô hình Toán học Cốt lõi (Mathematical Foundations)
- **1. Hệ số an toàn vị thế (Health Factor - $HF$):**
  $$HF = \frac{\sum (Collateral_i \times Price_i \times LT_i)}{Debt}$$
  - Ngưỡng thanh lý: $LT_{ETH} = LT_{stETH} = 0.80$. Vị thế bị thanh lý khi $HF < 1.0$.
- **2. Thanh lý một phần (Partial Liquidation):**
  - Close Factor = $50\%$; Liquidation Penalty Bonus = $5\%$.
  - Lượng tài sản tịch thu: $\text{Seized} = \frac{\text{Repaid} \times 1.05}{Price}$.
  - Nếu thiếu tài sản thế chấp $\to$ Ghi nhận nợ xấu (**Bad Debt**).
- **3. Mô hình AMM tích số không đổi ($x \cdot y = k$):**
  - Phí giao dịch zero-fee để cách ly thuần túy trượt giá:
    $$y_{out} = \frac{y \cdot \Delta x}{x + \Delta x}$$
  - Giá giao ngay $P = y / x$ biến động tự nhiên sau mỗi giao dịch swap.
- **4. Tỷ lệ chiết khấu stETH (Discount / Depeg):**
  $$\text{Discount}(\%) = \frac{P_{ETH} - P_{stETH}}{P_{ETH}} \times 100\%$$
- **Speaker Note (1 phút - Thành viên 1):**
  - Trình bày công thức tính toán và giải thích tại sao sử dụng mô hình thanh lý một phần 50% theo chuẩn Aave v3.

---

### Slide 5: Lộ trình Bán tháo & 3 Kịch bản Mô phỏng (Scenarios & Selling Routes)
- **Lộ trình bán tháo thanh lý (Liquidation Route):**
  - **Tài sản ETH:** Bán trực tiếp vào **Pool A (ETH/USDC, $150M TVL)** $\to$ Làm giảm giá ETH.
  - **Tài sản stETH:** 
    * Chặng 1: Bán vào **Pool B (stETH/ETH, $80M TVL)** lấy ETH $\to$ Làm stETH mất peg.
    * Chặng 2: Lấy lượng ETH vừa nhận bán tiếp vào **Pool A (ETH/USDC)** $\to$ Kéo giá ETH sập tầng thứ hai!
- **Thiết kế 3 Kịch bản Đối chứng (3 Scenarios):**
  1. **SC01 (Baseline):** Môi trường tĩnh, giá ETH = $3,000 không đổi $\to$ Chuẩn đối chứng (0 thanh lý, 0 nợ xấu).
  2. **SC02 (Direct Shock):** Cú sốc ngoại sinh -15% tại block 1 (giá $2,550), KHÔNG bán vào AMM $\to$ Đo lường tác động ban đầu độc lập.
  3. **SC03 (Cascade Contagion):** Cú sốc -15% + Bán collateral vào 2 pool AMM qua từng block $\to$ Khảo sát hiệu ứng lây lan khuếch đại.
- **Speaker Note (1 phút - Thành viên 1 chuyển giao sang Thành viên 2):**
  - Nhấn mạnh vai trò của SC02 là chiếc "cầu nối đối chứng" để chứng minh tác động thực sự của AMM trong SC03.

---

### Slide 6: Kết quả Thực nghiệm Định lượng (Empirical Benchmark Results)
*(Hiển thị Bảng đối chứng số liệu thực tế đo lường được từ mô hình)*

| Chỉ số Khảo sát | SC01 Baseline | SC02 Direct Shock | SC03 Cascade Contagion | Chênh lệch (SC03 - SC02) | Tỷ lệ Tăng tương đối |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Giá ETH cuối cùng** | $3,000.00 | $2,550.00 (-15.0%) | **$988.92** | -$1,561.08 | **-61.22%** |
| **Giá stETH cuối cùng** | $2,970.00 | $2,524.50 (-15.0%) | **$318.72** | -$2,205.78 | **-87.37%** |
| **Tỷ lệ chiết khấu stETH** | 1.00% | 1.00% | **67.77%** | +66.77% | **+66.77% (Depeg)** |
| **Số Agent bị thanh lý** | 0 / 100 (0%) | 17 / 100 (17%) | **100 / 100 (100%)** | +83 agents | **+488.24%** |
| **Tổng số lượt thanh lý** | 0 | 17 | **214** | +197 lượt | **+1,158.82%** |
| **Nợ xấu phát sinh (Bad Debt)** | $0.00 | $0.00 | **$14,265,389.56** | +$14.27M | **Bùng nổ nợ xấu** |

- **Nhận định then chốt:**
  - Cơ chế phản hồi thanh lý đã khuếch đại số người vay vỡ nợ từ 17 lên toàn bộ 100 người vay (+488%).
  - stETH mất peg nghiêm trọng (chiết khấu lên tới 67.77%).
  - Phát sinh hơn $14.26 triệu USD nợ xấu không thể thu hồi.
- **Speaker Note (1.5 phút - Thành viên 2):**
  - Đi sâu vào từng con số. So sánh trực quan giữa SC02 và SC03 để làm nổi bật hiệu ứng cascade.

---

### Slide 7: Trực quan hóa Dữ liệu (Plotly Charts Breakdown)
*(Hiển thị ảnh chụp 4 biểu đồ tương tác trích xuất từ giao diện)*
- **Biểu đồ 1 - Biến động giá ETH:**
  - SC01 đi ngang ($3,000); SC02 giảm 1 nhịp rồi đi ngang ($2,550).
  - SC03 dốc xuống liên tục theo từng block và kết thúc dưới $1,000. Vạch chú thích rõ ràng tại Block 1.
- **Biểu đồ 2 - Tỷ lệ depeg stETH:**
  - Chiết khấu giữ phẳng 1% ở SC01 và SC02, nhưng bùng nổ lên 67.77% trong SC03 phản ánh thanh khoản Pool B bị rút cạn.
- **Biểu đồ 3 - Phân bổ sự kiện thanh lý (ETH vs stETH):**
  - Biểu đồ cột chồng thể hiện các đợt thanh lý ồ ạt ở các block đầu và giảm dần khi cạn kiệt tài sản.
- **Biểu đồ 4 - Số lượng người vay bị thanh lý lũy kế:**
  - Biểu đồ bậc thang minh chứng rõ ràng: SC02 dừng lại ở 17 người, trong khi SC03 leo thang cuốn chiếu chạm ngưỡng 100 người.
- **Speaker Note (1 phút - Thành viên 2):**
  - Thuyết minh ý nghĩa từng biểu đồ và cách các biểu đồ bổ trợ lẫn nhau để kể một câu chuyện tài chính hoàn chỉnh.

---

### Slide 8: Giao diện Người dùng Streamlit (Dashboard Demo)
- **Thiết kế chuẩn mực con người (Humanized Light Mode):**
  - Tone màu sáng hiện đại, tối giản, thanh lịch (lấy cảm hứng từ Stripe và Dune Analytics).
  - Loại bỏ hoàn toàn các emoji rườm rà; sử dụng typography sắc nét và font số tài chính *JetBrains Mono*.
  - Tự động nạp sẵn dữ liệu chuẩn trong 0.007 giây khi vừa mở trang (không bị màn hình trống).
- **Cấu trúc 4 Tabs chuyên biệt:**
  - Tab 1: Biến động giá và chiết khấu (2 biểu đồ giá & depeg).
  - Tab 2: Diễn biến thanh lý (2 biểu đồ thanh lý & bảng so sánh chỉ số).
  - Tab 3: Bảng dữ liệu chi tiết & Xuất CSV (Block Results 12 cột & Liquidation Events 10 cột).
  - Tab 4: Cơ sở phương pháp luận (Sơ đồ luồng, công thức toán học KaTeX).
- **Speaker Note (1 phút - Thành viên 2):**
  - Trình bày điểm mạnh về UX/UI và thực hiện thao tác demo trực tiếp trên màn hình nếu có yêu cầu.

---

### Slide 9: Kiểm thử & Đảm bảo Chất lượng Phần mềm (Testing & Quality Assurance)
- **Hệ thống Kiểm thử Tự động Toàn diện:**
  - **73 / 73 bài kiểm thử đạt 100% Pass Rate** với Pytest trong 2.11 giây.
  - Bao phủ: Unit tests cho từng tầng (`domain`, `usecase`, `infra`, `interface`) và System Tests kiểm chứng bất biến thực nghiệm (ST-01..ST-07).
- **Quy chuẩn mã nguồn nghiêm ngặt:**
  - Không có bất kỳ file code nào vượt quá 300 dòng (file dài nhất là 249 dòng).
  - 100% Type Hints và Docstrings chuẩn Google Style có gắn mã nghiệp vụ `# Implements BR-XX`.
  - Tích hợp **GitHub Actions CI Pipeline** tự động chạy test trên Python 3.10, 3.11, 3.12.
  - Mã nguồn mở giấy phép MIT trên GitHub: `https://github.com/thanhtuanfptse05/blockchain-BTL-ptit`.
- **Speaker Note (0.5 phút - Thành viên 1):**
  - Khẳng định tính hoàn thiện về mặt kỹ thuật phần mềm, độ tin cậy và khả năng tái lặp của nghiên cứu.

---

### Slide 10: Giả định, Hướng Phát triển & Kết luận (Conclusion & Future Work)
- **Giới hạn nghiên cứu (§13):**
  - Mô hình AMM cơ bản ($x \cdot y = k$ không phí); chưa xét Concentrated Liquidity (Uniswap v3).
  - Chưa xét tác tử kinh doanh chênh lệch giá (Arbitrageurs) bơm vốn cân bằng hai pool.
  - Phí gas mạng lưới giả định bằng 0 và thanh lý diễn ra tức thời trong block.
- **Hướng phát triển:**
  - Bổ sung bot Arbitrageur để nghiên cứu ngưỡng thanh khoản phục hồi peg.
  - Mô phỏng cơ chế Dynamic Interest Rate theo tỷ lệ sử dụng vốn (Utilization Rate).
- **Lời kết:**
  - Đề tài đã xây dựng thành công công cụ mô phỏng vi mô trực quan, minh chứng khoa học cho cơ chế lây lan rủi ro chéo tài sản trong DeFi Lending.
  - Nhóm xin chân thành cảm ơn Thầy/Cô và kính mời Hội đồng đặt câu hỏi phản biện.
- **Speaker Note (0.5 phút - Cả 2):**
  - Cảm ơn và chuyển sang phần Q&A.

---

### Bảng Phân bổ Thời gian & Vai trò Thuyết trình

| Slide | Nội dung | Người trình bày | Thời gian |
| :---: | :--- | :---: | :---: |
| **1** | Trang bìa & Giới thiệu đề tài | Cả 2 thành viên | 0.5 phút |
| **2** | Đặt vấn đề & Động lực thực tiễn | Thành viên 1 | 1.0 phút |
| **3** | Kiến trúc Phần mềm & Phương pháp SDD | Thành viên 1 | 1.0 phút |
| **4** | Mô hình Toán học Cốt lõi (HF, AMM, Discount) | Thành viên 1 | 1.0 phút |
| **5** | Lộ trình Bán tháo & 3 Kịch bản Mô phỏng | Thành viên 1 | 1.0 phút |
| **6** | Kết quả Thực nghiệm Định lượng Benchmark | Thành viên 2 | 1.5 phút |
| **7** | Trực quan hóa Dữ liệu (4 Biểu đồ Plotly) | Thành viên 2 | 1.0 phút |
| **8** | Giao diện Streamlit Dashboard & Live Demo | Thành viên 2 | 1.0 phút |
| **9** | Kiểm thử Tự động & Chất lượng Mã nguồn | Thành viên 1 | 0.5 phút |
| **10** | Giới hạn, Hướng phát triển & Kết luận | Cả 2 thành viên | 0.5 phút |
| **Tổng** | **Toàn bộ bài báo cáo** | **Cả 2 thành viên** | **9.0 phút** |
