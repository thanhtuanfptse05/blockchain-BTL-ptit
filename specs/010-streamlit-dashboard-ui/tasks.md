# Tasks: Streamlit Dashboard UI & Methodology

**Feature**: `010-streamlit-dashboard-ui`  
**Input**: [`specs/010-streamlit-dashboard-ui/spec.md`](file:///d:/wd/c/sang/d/Documents/BTL-block-chain/specs/010-streamlit-dashboard-ui/spec.md)  
**Plan**: [`specs/010-streamlit-dashboard-ui/plan.md`](file:///d:/wd/c/sang/d/Documents/BTL-block-chain/specs/010-streamlit-dashboard-ui/plan.md)  

## Task List

- [x] **T010-01** [US1] Cài đặt `src/interface/components/sidebar.py` render các widget tham số P-01..P-06 và 2 nút "Run Simulation", "Reset Defaults".
- [x] **T010-02** [US3] Cài đặt `src/interface/components/methodology_tab.py` trình bày sơ đồ chu trình lây lan Markdown/Mermaid, công thức toán học KaTeX (HF, AMM $x \cdot y = k$, discount) và danh sách giả định giới hạn (FR-10).
- [x] **T010-03** [US1, US2] Cài đặt `src/interface/app.py` thiết lập layout trang, tiêu đề, disclaimer nghiên cứu, quản lý `st.session_state` và điều phối 4 Tabs.
- [x] **T010-04** Kiểm tra tính độc lập: chạy thử giao diện bằng lệnh `streamlit run src/interface/app.py` xác nhận không có warning hoặc lỗi phân giải import.
- [x] **T010-05** Kiểm tra tiêu chuẩn kỹ thuật: tất cả các file trong `src/interface/` đều $\le 300$ dòng code.

