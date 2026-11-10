# Tài liệu Hướng dẫn Thuyết trình & Trả lời Phản biện BTL
## Đề tài: DeFi Liquidation Cascade Simulator (Mô phỏng lây lan rủi ro thanh lý chéo trong DeFi Lending)

**Môn học:** Công nghệ Chuỗi khối (Blockchain Technology)  
**Quy mô:** Nhóm 2 sinh viên  
**Thành viên 1:** Core Simulator Lead (`src/domain/`, `src/usecase/`, logic toán, unit tests)  
**Thành viên 2:** UI & Data Viz Lead (`src/interface/`, `src/infra/`, Plotly, dashboard, export CSV)

---

## PHẦN 1: KỊCH BẢN THUYẾT TRÌNH & PHÂN VAI BẢO VỆ (Thời lượng: 7 - 10 phút)

### 1. Mở đầu & Đặt vấn đề (1.5 phút — Cả 2 thành viên)
- **Lời mở đầu:** Kính chào Thầy/Cô trong Hội đồng chấm Bài tập lớn. Hôm nay nhóm em xin trình bày đề tài: *"Mô phỏng lây lan rủi ro thanh lý chéo tài sản trong DeFi Lending bằng mô hình Agent-Based Model"*.
- **Vấn đề thực tiễn:** Trong DeFi Lending (như Aave), rủi ro lớn nhất không chỉ là giá giảm mà là **vòng xoáy phản hồi giảm giá (Liquidation Feedback Loop)**:
  - Khi giá tài sản thế chấp giảm $\to$ Vị thế vay bị thanh lý $\to$ Liquidator bán tháo tài sản lên sàn AMM để chốt lời $\to$ Gây trượt giá làm giá thị trường giảm sâu hơn $\to$ Kích hoạt làn sóng thanh lý kế tiếp đối với các tài khoản khác.
  - Hiện tượng này càng nghiêm trọng khi có sự xuất hiện của tài sản phái sinh staking thanh khoản (**stETH**), gây ra lây lan rủi ro chéo (**Cross-Asset Contagion**).

---

### 2. Phần trình bày của Thành viên 1 — Core Simulator Lead (3.5 phút)
- **Kiến trúc phần mềm & Phương pháp luận:**
  - Nhóm áp dụng **Clean Architecture** và phương pháp **Spec-Driven Development (SDD)**: Tách biệt hoàn toàn giữa Tầng Thực thể (`domain/`), Tầng Nghiệp vụ (`usecase/`) và Tầng Giao diện (`interface/`).
  - Toàn bộ kết quả tính toán được sinh ra động từ công thức toán học, **tuyệt đối không gán cứng (hardcode)** số liệu.
- **Mô hình toán học cốt lõi:**
  1. **Khởi tạo Quần thể Tác tử (Agent Generation):** 100 Borrower Agents độc lập, phân bổ 50 vị thế ETH và 50 vị thế stETH. Mỗi agent có $LTV \in [0.55, 0.72]$, ban đầu $HF > 1.0$ (an toàn). Hạt giống ngẫu nhiên (`seed=42`) đảm bảo tính tất định và lặp lại kết quả 100%.
  2. **Health Factor ($HF$):** 
     $$HF = \frac{\sum (Collateral_i \times Price_i \times LT_i)}{Debt}$$
     Với $LT = 0.80$. Khi $HF < 1.0$, vị thế rơi vào diện bị thanh lý.
  3. **Thanh lý một phần (Partial Liquidation):**
     - Áp dụng Close Factor $50\%$ và Penalty Bonus $5\%$.
     - Tịch thu Collateral: $\text{Seized} = \frac{\text{Repaid} \times 1.05}{Price}$.
     - Nếu vị thế không đủ tài sản thế chấp để trả nợ kèm phí thưởng $\to$ Ghi nhận nợ xấu (**Bad Debt**).
  4. **Hai Pool AMM Constant-Product ($x \cdot y = k$):**
     - Pool A: ETH/USDC (\$150M TVL).
     - Pool B: stETH/ETH (\$80M TVL).
     - Áp dụng công thức swap zero-fee: $\Delta y = \frac{y \cdot \Delta x}{x + \Delta x}$. Giá giao ngay thay đổi tự nhiên qua tỷ lệ dự trữ sau swap, bảo toàn tích số $k$.
- **Lộ trình xả Collateral trong Kịch bản lây lan (SC03):**
  - Collateral ETH $\to$ Bán trực tiếp vào Pool A (ETH/USDC) $\to$ Đè bẹp giá ETH.
  - Collateral stETH $\to$ Bán vào Pool B (stETH/ETH) để lấy ETH (làm stETH bị depeg/discount) $\to$ Sau đó bán tiếp lượng ETH nhận được vào Pool A $\to$ Kéo giá ETH giảm thêm tầng thứ hai!
- **Hệ thống Kiểm thử:** Đã xây dựng **73 bài kiểm thử tự động (100% Pass Rate)** bao gồm cả Unit Tests và System Invariant Tests (ST-01..ST-07).

---

### 3. Phần trình bày của Thành viên 2 — UI & Data Viz Lead (3.5 phút)
- **Giới thiệu Giao diện Streamlit Dashboard:**
  - Chạy local bằng lệnh `python -m streamlit run src/interface/app.py`.
  - Thiết kế trực quan, khoa học gồm: Sidebar điều khiển tham số, 6 Thẻ KPI tổng kết trên đỉnh màn hình, và 4 Tabs chuyên biệt.
- **Trực tiếp Thực hiện Demo trên màn hình:**
  1. *Thao tác Sidebar:* Giữ nguyên các tham số chuẩn (\$150M Pool A, \$80M Pool B, 100 Borrowers, Shock 15%, 30 blocks, Seed 42) $\to$ Bấm **🚀 Run Simulation**.
  2. *Phân tích 6 Thẻ KPI cốt lõi (SC03 vs SC02):*
     - **Giá ETH:** Từ \$3,000 ban đầu, trong SC02 dừng ở \$2,550 (-15%), nhưng trong SC03 bị kéo sập xuống **\$988.92** (giảm tới **-61.22%**).
     - **Giá stETH & Depeg:** Trong SC03, stETH bị bán tháo vào Pool B khiến tỷ lệ discount tăng vọt lên **67.77%**, kéo giá stETH xuống **\$318.72** (giảm **-87.37%**).
     - **Số lượng Agent bị thanh lý:** SC02 chỉ có 17 agents bị thanh lý do cú sốc ban đầu. Trong SC03, toàn bộ **100/100 agents (100%)** bị thanh lý cuốn chiếu (tăng thêm **+83 agents**, tức tăng **+488.24%**).
     - **Nợ xấu (Bad Debt):** SC02 không phát sinh nợ xấu (\$0), nhưng trong SC03 phát sinh tới **\$14.26 triệu USD nợ xấu** do giá sập quá nhanh khiến collateral không đủ bù đắp nợ.
  3. *Duyệt 4 Tabs chức năng:*
     - **Tab 1 (Giá & Discount):** Chỉ rõ vạch kẻ ngắt nét tại block 1 (thời điểm shock ngoại sinh) và đường cong dốc xuống liên tục của SC03 so với đường đi ngang của SC02.
     - **Tab 2 (Diễn biến Thanh lý):** Quan sát biểu đồ cột chồng phân bổ thanh lý ETH vs stETH dồn dập ở các block đầu và bảng đối chứng so sánh chi tiết.
     - **Tab 3 (Bảng Dữ liệu & Xuất CSV):** Thao tác tải 2 file `block_results.csv` (12 cột) và `liquidation_events.csv` (10 cột) chuẩn UTF-8, minh chứng tính minh bạch và khả năng tái kiểm toán.
     - **Tab 4 (Cơ chế & Phương pháp luận):** Giải thích sơ đồ luồng cascade và 5 giả định giới hạn mô hình.
- **Lời kết:** Mô hình đã chứng minh thành công cơ chế lây lan rủi ro chéo tài sản trong DeFi Lending. Em xin cảm ơn Thầy/Cô và mời Thầy/Cô đặt câu hỏi phản biện.

---

## PHẦN 2: BỘ CÂU HỎI & CÂU TRẢ LỜI PHẢN BIỆN THƯỜNG GẶP (Q&A)

### Câu hỏi 1: Tại sao $HF < 1.0$ thì vị thế lại được phép thanh lý? Công thức tính $HF$ có ý nghĩa gì?
- **Trả lời:**
  - $HF$ (Health Factor) là tỷ số giữa **Giá trị thanh lý của tài sản thế chấp** chia cho **Tổng dư nợ**:
    $$HF = \frac{\sum (Collateral_i \times Price_i \times LT_i)}{Debt}$$
  - $LT$ (Liquidation Threshold) là tỷ lệ an toàn tối đa (trong bài là $80\%$). Khi $HF = 1.0$, nghĩa là nợ đang chiếm đúng $80\%$ giá trị thị trường của tài sản thế chấp ($20\%$ còn lại là đệm bảo vệ - buffer).
  - Khi $HF < 1.0$, tài sản thế chấp bắt đầu tiệm cận mức rủi ro vỡ nợ. Giao thức bắt buộc phải mở quyền thanh lý cho Liquidator bên ngoài trả nợ thay để thu hồi vốn vay cho giao thức trước khi vị thế rơi vào trạng thái nợ xấu (Bad Debt).

---

### Câu hỏi 2: Tại sao SC02 và SC03 cùng dùng một bộ 100 Agent ban đầu và cùng chịu shock 15%, nhưng kết quả thanh lý lại khác nhau một trời một vực (17 agents vs 100 agents)?
- **Trả lời:**
  - **Trong SC02 (Direct Shock):** Là mô hình tĩnh. Sau khi giá ETH bị giảm 15% tại block 1, việc thanh lý chỉ diễn ra trên sổ sách: nợ được trừ, tài sản bị tịch thu nhưng **không được bán ra thị trường AMM**. Do đó, giá ETH giữ nguyên ở mức \$2,550 qua tất cả các block sau. Chỉ có 17 agents có LTV ban đầu cao bị rơi vào $HF < 1.0$. 83 agents còn lại vẫn an toàn vì giá không giảm thêm.
  - **Trong SC03 (Cascade Contagion):** Là mô hình động có phản hồi (feedback loop). Lượng collateral tịch thu từ 17 agents đợt đầu ngay lập tức bị liquidator xả vào 2 Pool AMM để thu hồi USDC. Lực bán lớn làm cạn kiệt thanh khoản USDC trong Pool A, khiến giá ETH tiếp tục trượt dốc từ \$2,550 xuống \$2,400, \$2,200...
  - Mức giá giảm mới này lại làm giảm giá trị thế chấp của các agents khác ở block kế tiếp, biến các vị thế trước đó đang an toàn thành vị thế mất an toàn ($HF < 1.0$). Quá trình cứ thế lặp lại tạo thành hiệu ứng domino cuốn trôi toàn bộ 100 agents.

---

### Câu hỏi 3: Việc thanh lý vị thế thế chấp bằng stETH làm cho giá ETH sụt giảm bằng lộ trình (selling route) như thế nào?
- **Trả lời:**
  - Liquidator khi thanh lý nợ cần thu lại **USDC** (đơn vị của khoản nợ vay).
  - Với vị thế stETH, Liquidator không thể bán thẳng stETH lấy USDC vì không có pool trực tiếp stETH/USDC. Lộ trình thanh khoản 2 chặng bắt buộc phải diễn ra:
    1. **Chặng 1:** Bán stETH vào **Pool B (stETH/ETH)** để lấy về token ETH. Việc này làm lượng stETH trong Pool B tăng lên và lượng ETH dự trữ giảm đi $\to$ Giá stETH/ETH giảm (hiện tượng **stETH depeg**, discount vọt lên tới 67.77%).
    2. **Chặng 2:** Liquidator lấy toàn bộ số lượng ETH vừa nhận được từ Pool B đem bán ngay vào **Pool A (ETH/USDC)** để lấy ra USDC.
  - Như vậy, việc bán tháo stETH không chỉ làm sập giá stETH mà còn gián tiếp bơm thêm một lượng lớn ETH vào Pool A, khuếch đại áp lực bán tháo lên token ETH, kéo giá ETH rơi tự do. Đây chính là bản chất của **sự lây lan rủi ro chéo tài sản (Cross-Asset Contagion)**.

---

### Câu hỏi 4: Vì sao độ sâu thanh khoản (TVL) của các Pool AMM lại là yếu tố quyết định mức độ nghiêm trọng của chuỗi thanh lý?
- **Trả lời:**
  - Theo công thức Constant-Product $x \cdot y = k$, độ trượt giá (Price Impact) khi bán lượng token $\Delta x$ là:
    $$\Delta P \approx \frac{P \cdot \Delta x}{x}$$
  - Trong đó $x$ là lượng dự trữ token trong pool (tỷ lệ thuận với TVL).
  - Nếu Pool A có TVL rất lớn (ví dụ \$500M), lượng token thanh lý được hấp thụ dễ dàng với trượt giá không đáng kể $\to$ Vòng xoáy cascade bị chặn đứng sớm.
  - Ngược lại, nếu Pool có TVL mỏng (ví dụ \$20M - \$50M), cùng một lượng bán tháo collateral sẽ gây ra trượt giá khổng lồ $\to$ Kéo sập giá cực nhanh $\to$ Kích hoạt thanh lý diện rộng và tạo ra nợ xấu khổng lồ.
  - Đây là khuyến nghị thực tiễn quan trọng nhất của đề tài dành cho các giao thức DeFi: **Hạn mức vay (Borrow Cap) phải được neo chặt vào độ sâu thanh khoản thực tế trên AMM**.

---

### Câu hỏi 5: Tại sao mô hình này chạy mô phỏng (Simulation) trên Python mà không triển khai Smart Contract trên Local Blockchain (như Hardhat/Ganache)?
- **Trả lời:**
  - **Mục tiêu nghiên cứu:** Mục tiêu trọng tâm của đề tài là khảo sát động lực học kinh tế vĩ mô (Macroeconomic Dynamics), độ nhạy tham số và hành vi tương tác giữa hàng trăm tác tử (Agent-Based Modeling) qua hàng chục block liên tục.
  - **Hiệu năng & Khả năng tái lập:** Nếu chạy trên blockchain cục bộ, việc gửi hàng nghìn giao dịch, mining block và xử lý trạng thái sẽ tốn nhiều phút, phụ thuộc vào EVM overhead và khó thực hiện phân tích độ nhạy hàng loạt (Sensitivity Analysis).
  - Mô phỏng bằng Python thuần cho phép:
    1. Tốc độ thực thi cực nhanh ($< 1$ giây cho 3 kịch bản gồm 30 blocks).
    2. Kiểm soát hạt giống ngẫu nhiên (`seed`) tuyệt đối để tái lặp kết quả 100%.
    3. Bảo toàn chính xác 100% công thức toán học thực tế của AMM Uniswap v2 ($x \cdot y = k$) và Lending Pool Aave v3.
  - Hệ thống cục bộ là hướng mở rộng tương lai (Future Work) khi muốn kiểm thử các khía cạnh kỹ thuật thấp tầng như MEV, Front-running hay tắc nghẽn mạng lưới Gas.

---

### Câu hỏi 6: Các giả định đơn giản hóa của mô hình là gì và tại sao chúng ta chấp nhận các giả định đó?
- **Trả lời:**
  - Nhóm công khai 5 giả định đơn giản hóa (SRS §13):
    1. *AMM Constant-Product phí 0%:* Để cách ly thuần túy tác động của trượt giá cơ bản.
    2. *Không có Arbitrageur:* Giả lập trường hợp thị trường thanh khoản tê liệt trong khủng hoảng (Black Swan event) khi các nhà tạo lập thị trường rút vốn.
    3. *Thanh lý tức thời trong block:* Giả định bot thanh lý luôn túc trực và có đủ vốn ngắn hạn (Flash Loan).
    4. *Phí Gas = 0:* Tập trung vào động lực kinh tế học thay vì cạnh tranh vị trí giao dịch trên mempool.
    5. *Lãi suất tĩnh:* Khảo sát trong ngắn hạn (vài chục block, tương đương vài phút thực tế) nên lãi suất tích lũy là không đáng kể so với mức trượt giá hàng chục phần trăm.
  - Các giả định này giúp mô hình **đủ đơn giản để kiểm chứng toán học minh bạch**, nhưng **đủ sắc bén để bộc lộ toàn bộ cơ chế lây lan rủi ro cốt lõi**.

