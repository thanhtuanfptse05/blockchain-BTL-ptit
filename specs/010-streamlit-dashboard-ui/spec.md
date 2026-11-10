# Feature Specification: Giao Diện Người Dùng Streamlit Dashboard & Tab Cơ Chế

**Feature Branch**: `010-streamlit-dashboard-ui`  
**Created**: 2026-11-10  
**Status**: Draft  
**Input**: User description: "Xây dựng giao diện Streamlit tương tác một trang với Sidebar tham số (Shock %, Pool A TVL, Pool B TVL, Number of Borrowers, Max Blocks, Random Seed, nút Run và Reset Defaults); Vùng nội dung gồm Header, Disclaimer nghiên cứu, 6 thẻ KPI trên cùng và 4 Tab: (1) Giá & Discount, (2) Thanh lý, (3) Dữ liệu & Export CSV, (4) Cơ chế / Methodology (FR-10) giải thích sơ đồ cascade, công thức HF/AMM và giả định; không auto-run khi đổi slider; tách biệt UI hoàn toàn khỏi business logic." (requirements.md §4.3, §11 FR-10, §12, §13, §15.1, NFR-05, NFR-06, NFR-07)

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Điều khiển tham số qua Sidebar & Chạy mô phỏng (Priority: P1)

Người dùng muốn dễ dàng điều chỉnh các tham số thí nghiệm (tỉ lệ giảm giá shock, độ sâu thanh khoản 2 pool, quy mô số người vay, số block mô phỏng, và seed ngẫu nhiên) từ thanh bên (sidebar) và chủ động bấm nút "Run Simulation" để chạy thí nghiệm mà không bị giật lag do tự động chạy lại mỗi khi di chuột kéo slider.

**Why this priority**: Yêu cầu cốt lõi về trải nghiệm người dùng (§12.1, §12.3).

**Independent Test**: Kiểm tra component sidebar `render_sidebar()`:
- Đảm bảo trả về đúng đối tượng `SimulationConfig` hợp lệ.
- Nút "Reset Defaults" khôi phục toàn bộ tham số về giá trị chuẩn (§5.1).
- Thay đổi slider không tự động gọi `run_all_scenarios` cho đến khi nút "Run Simulation" được bấm.

**Acceptance Scenarios**:

1. **Given** người dùng mở ứng dụng, **When** nhìn vào Sidebar, **Then** các giá trị mặc định hiển thị:
   - ETH Price Shock (%): `15.0%` (slider từ 0.0 đến 50.0).
   - Pool A TVL — ETH/USDC: `$150,000,000` (slider từ $10M đến $500M).
   - Pool B TVL — stETH/ETH: `$80,000,000` (slider từ $5M đến $200M).
   - Number of Borrowers: `100` (slider từ 10 đến 500).
   - Maximum Simulation Blocks: `30` (slider từ 5 đến 100).
   - Random Seed: `42` (number input $\ge 0$).
2. **Given** người dùng thay đổi các giá trị trên slider, **When** chưa bấm "Run Simulation", **Then** màn hình giữ nguyên trạng thái cũ, không tự ý tính toán lại.
3. **Given** người dùng bấm nút "Reset Defaults", **When** action kích hoạt, **Then** tất cả input quay về bộ giá trị mặc định nêu trên.
4. **Given** người dùng bấm "Run Simulation", **When** engine đang chạy, **Then** giao diện hiển thị spinner thông báo `"Đang chạy mô phỏng 3 kịch bản..."` và cập nhật toàn bộ KPI, biểu đồ, bảng dữ liệu ngay sau khi hoàn tất.

---

### User Story 2 - Tổ chức không gian hiển thị 4 Tabs chuyên biệt (Priority: P1)

Người dùng cần duyệt kết quả một cách mạch lạc, không bị rối mắt, qua cấu trúc phân chia tab rõ ràng theo chủ đề.

**Why this priority**: Yêu cầu cấu trúc giao diện chuẩn tại SRS §12.2.

**Independent Test**: Kiểm tra cấu trúc phân trang trên Streamlit UI gồm đúng 4 tabs với tiêu đề:
- Tab 1: "📈 Giá & Discount"
- Tab 2: "⚡ Thanh lý"
- Tab 3: "📋 Dữ liệu"
- Tab 4: "🧠 Cơ chế"

**Acceptance Scenarios**:

1. **Given** mô phỏng đã hoàn tất, **When** người dùng duyệt qua các tab:
   - **Tab 1**: Hiển thị Biểu đồ giá ETH (3 kịch bản) và Biểu đồ stETH Discount.
   - **Tab 2**: Hiển thị Biểu đồ cột thanh lý theo tài sản trong SC03, Biểu đồ lũy kế người vay bị thanh lý (SC02 vs SC03), và Bảng so sánh chỉ số đối chứng (FR-11).
   - **Tab 3**: Hiển thị bảng tương tác Block Results, bảng Liquidation Events, và 2 nút tải CSV.
   - **Tab 4**: Hiển thị nội dung học thuật giải thích mô hình (FR-10).
2. **Given** giao diện ở mọi tab, **When** quan sát vùng Header, **Then** luôn hiển thị:
   - Tiêu đề chính: "DeFi Liquidation Cascade Simulator".
   - Dòng ghi chú pháp lý/nghiên cứu: *"Dữ liệu giả lập phục vụ nghiên cứu; không phải dự báo hoặc số liệu thị trường thực."*

---

### User Story 3 - Tab Cơ chế & Phương pháp luận (FR-10) (Priority: P1)

Người dùng hoặc người chấm thi mở Tab "Cơ chế" để nắm bắt nguyên lý toán học, logic lây lan cascade và các giới hạn giả định của mô hình nghiên cứu.

**Why this priority**: Yêu cầu bắt buộc Must Have (FR-10) đảm bảo tính học thuật và khả năng giải trình khi bảo vệ đồ án.

**Independent Test**: Kiểm tra sự hiện diện đầy đủ của các khối nội dung trong component `render_methodology_tab()`:
- Sơ đồ chu trình lây lan (Contagion Loop Flowchart).
- Công thức Health Factor (BR-03), AMM $x \cdot y = k$ (BR-05), Discount (BR-06).
- So sánh định tính 3 kịch bản (SC01 vs SC02 vs SC03).
- Danh sách các giả định và giới hạn mô hình (§13).

**Acceptance Scenarios**:

1. **Given** người dùng mở Tab "Cơ chế", **Then** hệ thống trình bày:
   - Sơ đồ trực quan: `Shock giá ETH → HF < 1 → Kích hoạt thanh lý vị thế → Bán Collateral vào AMM → Giá trượt giảm sâu → Sang Block tiếp theo → Kích hoạt đợt thanh lý mới`.
   - Công thức toán học định dạng KaTeX/Markdown rõ ràng.
   - Giải thích vai trò của SC01 (Baseline chuẩn), SC02 (Đối chứng shock không phản hồi), SC03 (Thử nghiệm lây lan).
   - Danh sách 5 giới hạn cốt lõi: giả lập AMM đơn giản hóa, không xét bot kinh doanh chênh lệch giá (arbitrageur), thanh lý hoàn tất tức thì trong block, chi phí gas = 0, chưa mô phỏng lãi suất biến đổi.

---

### Edge Cases & Defensive UI

- **Lỗi validate tham số đầu vào**: Nếu người dùng cố tình nhập giá trị không hợp lệ (ví dụ: seed âm), giao diện hiển thị banner cảnh báo đỏ `st.error(...)` và ngăn chặn gọi hàm mô phỏng.
- **Trạng thái trước khi chạy lần đầu**: Khi người dùng vừa mở app, khu vực nội dung hiển thị màn hình chào mừng (Welcome card) giải thích ngắn gọn cách sử dụng và mời bấm "Run Simulation".
- **Không dồn logic vào UI (NFR-05)**: Tuyệt đối không có bất kỳ dòng code nào tính toán Health Factor, trừ reserves AMM hay duyệt vòng lặp block nằm trong `app.py` hoặc các file `components/*.py`. Toàn bộ logic nghiệp vụ được gọi thông qua `usecase/scenario_runner.py` và `infra/exporter.py`.

---

## Requirements (EARS) *(mandatory)*

### Ubiquitous Requirements
- **FR-10-01 (Cấu trúc phân lớp nghiêm ngặt)**: Ứng dụng Streamlit SHALL đóng vai trò là tầng Presentation (`interface/`), chỉ thực hiện thu thập tham số cấu hình, gọi tầng Usecase qua `run_all_scenarios(config)`, và hiển thị kết quả; tuyệt đối KHÔNG chứa logic nghiệp vụ cốt lõi.
- **FR-10-02 (Thông điệp miễn trừ trách nhiệm)**: Giao diện SHALL luôn hiển thị dòng chữ rõ ràng tại vùng tiêu đề: *"Dữ liệu giả lập phục vụ nghiên cứu; không phải dự báo hoặc số liệu thị trường thực."* theo quy định tại SRS §12.3.
- **FR-10-03 (Nội dung Tab Cơ chế FR-10)**: Tab "Cơ chế / Methodology" SHALL trình bày đầy đủ 4 khối thông tin:
  1. Sơ đồ chu trình cascade.
  2. Các công thức toán cốt lõi (HF, Constant Product AMM, Discount).
  3. Bảng so sánh mục đích của 3 kịch bản (SC01, SC02, SC03).
  4. Danh sách các giả định và giới hạn của mô hình.

### Event-driven Requirements
- **FR-10-04 (Xử lý sự kiện Run Simulation)**: Khi người dùng nhấp vào nút "Run Simulation", hệ thống SHALL thu thập các giá trị hiện thời từ Sidebar, khởi tạo `SimulationConfig`, kích hoạt hiển thị hiệu ứng chờ (loading spinner) và gọi `run_all_scenarios`.
- **FR-10-05 (Xử lý sự kiện Reset Defaults)**: Khi người dùng nhấp vào nút "Reset Defaults", hệ thống SHALL khôi phục toàn bộ các widget trên sidebar về giá trị mặc định của hệ thống mà không bắt buộc phải tải lại trang.
- **FR-10-06 (Ngăn chặn tự động chạy lại)**: Khi người dùng kéo thả slider thay đổi giá trị, hệ thống SHALL CHƯA thực hiện chạy lại mô phỏng cho đến khi có sự kiện bấm nút "Run Simulation".

### State-driven Requirements
- **FR-10-07 (Quản lý Session State)**: Trong suốt phiên làm việc của người dùng, hệ thống SHALL lưu trữ đối tượng kết quả mô phỏng trong `st.session_state["simulation_results"]` để giữ nguyên trạng thái khi người dùng chuyển đổi qua lại giữa 4 Tabs mà không phải chạy lại mô phỏng.

---

## UI Architecture & Component Hierarchy

```text
src/interface/
├── app.py                      # Điểm khởi chạy chính Streamlit (Layout chính, Header, Tabs)
└── components/
    ├── sidebar.py              # Render thanh bên tham số và 2 nút bấm điều khiển
    ├── metrics.py              # Render 6 thẻ KPI và bảng so sánh delta
    ├── charts.py               # Render 4 biểu đồ Plotly trong Tab 1 và Tab 2
    ├── data_tab.py             # Render bảng DataFrame và nút tải CSV trong Tab 3
    └── methodology_tab.py      # Render sơ đồ, công thức và giả định trong Tab 4
```

---

## Success Criteria *(mandatory)*

- **SC-01**: Khởi chạy ứng dụng bằng `streamlit run src/interface/app.py` không phát sinh bất kỳ warning hay deprecation error nào.
- **SC-02**: Đầy đủ 4 Tab và Sidebar hoạt động trơn tru, chuyển đổi qua lại giữa các Tab không làm mất dữ liệu đã mô phỏng.
- **SC-03**: File `app.py` và các file component đều $\le 300$ dòng code (tuân thủ Definition of Done §6).
- **SC-04**: Thể hiện đầy đủ sơ đồ và công thức toán học trong Tab 4 theo yêu cầu FR-10.

