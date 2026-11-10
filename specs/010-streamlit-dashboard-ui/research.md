# Research & Technical Decisions: Streamlit Dashboard UI & Methodology

**Feature**: `010-streamlit-dashboard-ui`  
**Date**: 2026-11-10  
**Status**: Completed  

## 1. Technical Context & UI Architecture Research

- **Cấu trúc 1 trang với Tabs (SRS §12)**:
  - Sidebar: Chứa 6 widget tham số và 2 nút bấm (`Run Simulation` và `Reset Defaults`).
  - Main area:
    - Header & Disclaimer nghiên cứu (bắt buộc theo §12.3).
    - Top Metrics Zone: 6 thẻ KPI cho SC03.
    - 4 Tabs:
      - Tab 1: "📈 Giá & Discount" (Biểu đồ giá ETH và depeg stETH).
      - Tab 2: "⚡ Thanh lý" (Cột thanh lý theo asset, đường lũy kế Agent bị thanh lý, bảng đối chứng delta).
      - Tab 3: "📋 Dữ liệu" (2 Dataframe và 2 nút download CSV).
      - Tab 4: "🧠 Cơ chế" (Phương pháp luận, sơ đồ chu trình cascade, công thức HF/AMM/Discount, giả định).

## 2. Interaction & State Management Research

- **Chống tự động chạy lại khi kéo slider**: Streamlit mặc định rerun toàn bộ script mỗi khi widget thay đổi giá trị. Để ngăn chạy lại mô phỏng gây giật lag:
  - Lưu kết quả mô phỏng trong `st.session_state["simulation_results"]`.
  - Chỉ khi người dùng bấm nút `[Run Simulation]`, ứng dụng mới đọc các giá trị slider hiện thời, tạo `SimulationConfig`, chạy `run_all_scenarios(config)`, lưu vào session state và hiển thị spinner.
  - Khi người dùng bấm `[Reset Defaults]`, xóa session state hoặc đặt lại giá trị mặc định cho widget qua key của Streamlit.
- **Tuân thủ Clean Architecture (NFR-05 & Forbidden Pattern #5)**:
  - `app.py` và các files trong `components/` chỉ chứa code render giao diện Streamlit.
  - Tuyệt đối không chứa bất kỳ phép tính toán Health Factor hay swap AMM nào trong tầng giao diện.

