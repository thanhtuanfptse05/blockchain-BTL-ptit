# AGENTS.md — Project Context for AI Coding Agents
# Version: 1.1.0 | Updated: 2026-11-10 | Project: DeFi Liquidation Cascade Simulator

## 1. PROJECT OVERVIEW
- Tên dự án: DeFi Liquidation Cascade Simulator (Mô phỏng lây lan rủi ro thanh lý chéo tài sản trong DeFi Lending).
- Mục tiêu: Xây dựng ứng dụng mô phỏng học thuật (Agent-Based Model) chạy local, khảo sát tác động giảm giá và bán tháo collateral lên 2 pool AMM giả lập (ETH/USDC và stETH/ETH).
- Quy mô: Nhóm 2 sinh viên.
- Nguyên tắc cốt lõi: Kết quả tính toán từ code, không gán cứng, bảo toàn công thức toán học AMM x*y=k.

## 2. TEAM ROLES & ASSIGNMENTS (Dựa theo requirements.md §16)
- Thành viên 1 (Core Simulator Lead):
  - Chịu trách nhiệm: `src/domain/`, `src/usecase/`, logic tính HF, AMM swaps, Liquidation Engine, Scenario Runner, Unit tests.
- Thành viên 2 (UI & Data Viz Lead):
  - Chịu trách nhiệm: `src/interface/` (Streamlit dashboard), `src/infra/` (CSV export), KPI metrics cards, biểu đồ Plotly, Báo cáo và slide demo.

## 3. STRICT TECH STACK
- Python >= 3.10
- Data validation: Pydantic v2 / Dataclasses
- UI: Streamlit >= 1.30
- Charts: Plotly
- Data processing: Pandas, NumPy
- Testing: Pytest

## 4. ARCHITECTURAL PATTERNS & DIRECTORY STRUCTURE
```text
src/
├── domain/       # BorrowerAgent, AMMPool, LiquidationEvent, BlockResult, SimulationResult
├── usecase/      # agent_generator, amm_engine, liquidation_engine, scenario_runner
├── interface/    # app.py, components/sidebar.py, components/charts.py, components/metrics.py
└── infra/        # exporter.py, logger.py
```

## 5. FORBIDDEN PATTERNS (AI TUYỆT ĐỐI KHÔNG LÀM)
1. NEVER viết code trực tiếp khi chưa có file đặc tả (Spec) được soạn thảo và thông qua. KHÔNG CÓ SPEC = CẤM VIẾT CODE!
2. NEVER gán cứng (hardcode) số lượng vị thế thanh lý, giá ETH hoặc số liệu nợ xấu.
3. NEVER can thiệp sửa giá AMM bằng phép gán trực tiếp (e.g. `pool.price = new_price`). Giá chỉ được thay đổi do thay đổi tỉ lệ dự trữ x và y sau swap!
4. NEVER cho phép sinh số ngẫu nhiên mà không có `seed` (phải đảm bảo 100% lặp lại được kết quả).
5. NEVER viết logic nghiệp vụ (tính HF, swap AMM) trực tiếp bên trong file Streamlit UI `app.py`.
6. NEVER sử dụng `eval()`, `exec()` hoặc raw dynamic code execution.
7. NEVER dùng grep/read thủ công duyệt code khi repository đã có chỉ mục CodeGraph.
8. NEVER sửa code trực tiếp để "vá" bug khi test fail — bắt buộc phải áp dụng nguyên tắc "Fix the Spec, not the Code".

## 6. DEFINITION OF DONE (Mỗi Task)
- [ ] Có file `SPEC.md` tương ứng đã được duyệt với đầy đủ cú pháp EARS.
- [ ] Code tuân thủ đúng đặc tả EARS trong feature spec tương ứng.
- [ ] Có Unit test với Pytest tương ứng và pass 100%.
- [ ] Type hints đầy đủ, docstring chuẩn Google Style có gắn `# Implements BR-XX`.
- [ ] Chạy linter không có lỗi.
- [ ] Không có file nào vượt quá 300 dòng code.

## 7. GIT CONVENTIONS
- Branch: `spec/[feature-name]` (soạn spec), `agent/[feature-name]` (thực thi code), `main` (code hoàn thiện đã test).
- Commit format: `[type]([scope]): [description]` (e.g., `feat(amm): implement constant-product swap with 0.3% fee`).

## 8. MANDATORY WORKFLOW RULES: SPEC-FIRST & CODEGRAPH
- **SPEC-FIRST (BẮT BUỘC SPEC TRƯỚC CODE):** Khi người dùng muốn code bất kỳ tính năng hay sửa đổi nào, Agent BẮT BUỘC phải dừng lại kiểm tra hoặc soạn thảo `SPEC.md` (bằng `/speckit-specify`), lập kế hoạch `PLAN.md` (bằng `/speckit-plan`), và chia nhỏ `TASKS.md` (bằng `/speckit-tasks`). Chỉ khi Spec đã được duyệt, mới được chuyển sang pha viết code (`/speckit-implement`).
- **ĐỌC & KHÁM PHÁ CODE:** BẮT BUỘC sử dụng **CodeGraph** (`codegraph_explore` MCP tool hoặc `codegraph explore "<query>"`, `codegraph callers`, `codegraph callees`, `codegraph impact`, `codegraph affected`). Không đọc file thủ công làm loãng ngữ cảnh.
