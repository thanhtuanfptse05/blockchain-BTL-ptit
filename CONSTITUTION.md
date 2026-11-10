# PROJECT CONSTITUTION — DeFi Liquidation Cascade Simulator
# Version: 1.1.0 | Status: LOCKED | Ratified: 2026-11-10
# Nguồn chân lý (source of truth): `requirements.md` (SRS v1.0). Mọi con số, công thức, tham số trong Hiến pháp này được trích NGUYÊN VĂN từ SRS.
# Quy tắc: thay đổi tài liệu này cần sự đồng thuận của cả 2 thành viên.
# v1.1.0: sửa lỗi v1.0.0 (v1.0.0 từng ghi sai phí AMM 0.3%, LT 0.85/0.80, pool 10M, Python 3.10, Plotly — tất cả SAI so với SRS).

## ARTICLE 1 — HARD RULES (bất biến)

### HARD-01 — Không hardcode kết quả (SRS §14.3)
THE system SHALL tính mọi KPI, đồ thị, số liệu CSV từ danh sách Agent, reserves AMM và `LiquidationEvent` thực tế.
THE system SHALL NOT gán cứng số Agent bị thanh lý, discount, nợ xấu hay ép `SC03 > SC02` (SRS §9 "Không ép").

### HARD-02 — Tái lập (SRS §4.3, NFR-03)
THE system SHALL cho cùng `random_seed` + cùng tham số → cùng kết quả. Mọi sinh số ngẫu nhiên SHALL dùng `random.Random(random_seed)`.
THE system SHALL cho SC01/SC02/SC03 xuất phát từ cùng danh sách Agent và cùng trạng thái pool ban đầu, mỗi kịch bản dùng bản sao độc lập (deepcopy).

### HARD-03 — AMM constant-product KHÔNG PHÍ (SRS §5.5, BR-05)
THE system SHALL dùng `reserve_x * reserve_y = k`, `amount_y_out = (y * dx) / (x + dx)`. KHÔNG có phí giao dịch, KHÔNG có trượt giá ngoài 2 pool (SRS §5.4).
THE system SHALL NOT sửa giá pool bằng phép gán trực tiếp; giá chỉ đổi do swap hoặc do phép cân bằng cú sốc BR-07 (giữ nguyên `k_A`).

### HARD-04 — Quy tắc thanh lý (SRS BR-03, BR-04, §6.2)
`LT = 0.80` (ETH và stETH), `close_factor = 0.50`, `liquidation_bonus = 0.05`, `epsilon = 1e-9`. Thanh lý khi và chỉ khi `debt > eps AND collateral > eps AND HF < 1`.

### HARD-05 — Cơ chế lây lan SC03 (SRS BR-08)
ETH thu giữ → bán vào Pool A. stETH thu giữ → bán vào Pool B lấy ETH → bán toàn bộ ETH nhận được vào Pool A. SC01/SC02 SHALL NOT bán collateral lên AMM.

## ARTICLE 2 — ARCHITECTURAL CONSTRAINTS (SRS §4.3, NFR-05)
- UI (`app.py`) SHALL NOT chứa công thức tài chính; chỉ nhận input, gọi `run_all_scenarios(config)`, hiển thị output.
- Simulation Engine SHALL NOT import Streamlit; chạy được bằng test trực tiếp.
- Hợp đồng tích hợp: `run_all_scenarios(config: dict) -> {'SC01': SimulationResult, 'SC02': ..., 'SC03': ...}` (SRS §15.1).
- Cấu trúc module đề xuất theo SRS §15: `app.py, config.py, agents.py, market.py, simulation.py, scenarios.py, charts.py, tests/`.

## ARTICLE 3 — TECH STACK (SRS §4.1, khóa phiên bản trong `requirements.txt` khi bắt đầu code)
Python 3.11+, Mesa 3.x, Streamlit, pandas, NumPy (nếu cần), Matplotlib, pytest, CSV (không DB). Chạy local Windows.

## ARTICLE 4 — QUY TẮC CHO AI AGENT
- SPEC-FIRST: KHÔNG CÓ SPEC = CẤM VIẾT CODE. Spec viết bằng skill Spec Kit trong `specs/NNN-ten/spec.md`.
- Đọc code bằng CodeGraph (`codegraph_explore` / `codegraph` CLI) khi đã có `.codegraph/`.
- "Fix the Spec, not the Code": test fail → đối chiếu spec trước.
- Không thêm thư viện ngoài Article 3 nếu chưa sửa Hiến pháp.

## ARTICLE 5 — KNOWN OPEN ITEM
`AGENTS.md` (§3, §4) ghi Python ≥ 3.10, Plotly, cấu trúc `src/domain…` — KHÁC SRS §4.1/§15 (Python 3.11+, Matplotlib, module phẳng). Phải được thống nhất trong `/speckit-plan`; trong lúc chờ, SRS là chuẩn.
