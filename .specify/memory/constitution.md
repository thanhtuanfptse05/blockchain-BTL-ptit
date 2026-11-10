# PROJECT CONSTITUTION — DeFi Liquidation Cascade Simulator
# Version: 1.0.0 | Status: LOCKED | Ratified: 2026-11-10
# Team: Nhóm 2 Sinh viên (Thành viên 1: Core Simulator, Thành viên 2: Streamlit UI/Data)
# Tài liệu nền tảng: requirements.md (SRS v1.0) & Sách SDD Playbook (LinhNDM, 2026)
# RULE: Mọi thay đổi tài liệu này bắt buộc phải có sự đồng thuận 100% của cả hai thành viên.

═══════════════════════════════════════════════════════════════════════════════
  LAYER 1: HARD RULES (BẤT BIẾN — TUYỆT ĐỐI KHÔNG ĐƯỢC VI PHẠM)
═══════════════════════════════════════════════════════════════════════════════

## HARD-01: No Hardcoding Invariant (Nguyên tắc tính toán thực tế)
THE system SHALL tính toán toàn bộ kết quả mô phỏng (số Agent bị thanh lý, giá AMM, nợ xấu, discount) trực tiếp từ công thức toán học và logic vòng lặp block.
THE system SHALL NOT gán cứng (hardcode) bất kỳ số liệu đầu ra nào, và SHALL NOT ép buộc kịch bản SC03 luôn có kết quả xấu hơn SC02 nếu thông số tính toán không dẫn đến điều đó.

## HARD-02: Deterministic Reproducibility (Tính tất định và công bằng)
THE system SHALL sử dụng cùng một bộ tham số khởi tạo và random seed cố định (mặc định seed=42) khi tạo quần thể Borrower Agents ban đầu.
WHEN so sánh 3 kịch bản SC01 (Baseline), SC02 (Direct Shock), SC03 (Contagion), THE system SHALL chạy trên cùng một danh sách Agent ban đầu được sao chép độc lập (deep copy) trước mỗi kịch bản.

## HARD-03: AMM Constant-Product Integrity (Bảo toàn toán học AMM)
THE system SHALL tuân thủ tuyệt đối công thức AMM Constant-Product (x * y = k) có trừ phí giao dịch 0.3% (fee=0.003, tức nhân với 0.997 cho lượng token nộp vào).
THE system SHALL NOT cho phép swap lượng token vượt quá dự trữ khả dụng của pool hoặc dẫn đến dự trữ âm.

## HARD-04: Health Factor & Partial Liquidation Strictness
THE system SHALL xác định vị thế đủ điều kiện thanh lý khi và chỉ khi Health Factor (HF) < 1.0.
WHEN thanh lý vị thế, THE system SHALL tuân thủ:
1. close_factor = 0.5 (chỉ trả nợ tối đa 50% số nợ hiện tại).
2. liquidation_penalty = 0.05 (thưởng 5% giá trị thế chấp tịch thu cho liquidator).
3. Giá trị thế chấp bị tịch thu = (repay_debt * 1.05) / collateral_price.
4. WHERE tài sản thế chấp còn lại không đủ trả nợ: tịch thu 100% tài sản thế chấp và ghi nhận phần nợ không thể thu hồi vào `bad_debt`.

## HARD-05: SC03 Collateral Selling Cascade Order
WHERE kịch bản là SC03 (Contagion), THE system SHALL bán toàn bộ tài sản thế chấp bị tịch thu lên các AMM pool theo đúng trình tự:
- Thế chấp là ETH: Bán trực tiếp vào Pool ETH/USDC -> Giảm giá ETH trên AMM.
- Thế chấp là stETH: Bán stETH vào Pool stETH/ETH để lấy ETH -> Tiếp tục bán lượng ETH nhận được vào Pool ETH/USDC -> Gây áp lực giảm giá kép (cả discount stETH/ETH và giá ETH/USDC).

═══════════════════════════════════════════════════════════════════════════════
  LAYER 2: ARCHITECTURAL CONSTRAINTS (RÀNG BUỘC KIẾN TRÚC)
═══════════════════════════════════════════════════════════════════════════════

## ARCH-01: Clean Layered Architecture (Tách bạch tầng trách nhiệm)
THE system SHALL phân chia mã nguồn theo 4 tầng rõ rệt:
1. `src/domain/`: Chứa các thực thể dữ liệu độc lập (`BorrowerAgent`, `AMMPool`, `LiquidationEvent`, `BlockResult`, `SimulationResult`). Không phụ thuộc bất kỳ thư viện ngoài nào ngoại trừ standard library và Pydantic/dataclasses.
2. `src/usecase/`: Chứa business logic, các động cơ tính toán (`LiquidationEngine`, `AMMEngine`, `ScenarioRunner`, `SimulationOrchestrator`).
3. `src/interface/`: Chứa giao diện Streamlit (`app.py`, components, sidebar, visualizers, KPI cards).
4. `src/infra/`: Chứa các hàm hỗ trợ xuất dữ liệu, export CSV, logging.

VIOLATION RULE: UI layer (`src/interface/`) TUYỆT ĐỐI KHÔNG chứa logic thanh lý hoặc tính toán AMM swap. Mọi thao tác phải thông qua `usecase/`.

## ARCH-02: Pure Functions & Immutability where Possible
Các hàm tính toán công thức (HF, LTV, AMM swap output, Seized Collateral) SHALL là pure functions, dễ kiểm thử độc lập mà không gây side-effect ngoài ý muốn.

═══════════════════════════════════════════════════════════════════════════════
  LAYER 3: ENGINEERING STANDARDS (TIÊU CHUẨN KỸ THUẬT)
═══════════════════════════════════════════════════════════════════════════════

## TECH STACK (Khóa cố định — không đổi)
- Ngôn ngữ: Python >= 3.10
- Data modeling: `dataclasses` hoặc `pydantic >= 2.0`
- Giao diện: `streamlit >= 1.30`
- Trực quan hóa dữ liệu: `plotly >= 5.18` (kết hợp `matplotlib` khi cần xuất tĩnh)
- Xử lý mảng/bảng: `pandas >= 2.0`, `numpy >= 1.24`
- Testing: `pytest >= 8.0`

## CODING & QUALITY STANDARDS
- Type hints: Bắt buộc 100% cho tất cả public functions và methods.
- Docstring: Định dạng Google Style, có chú thích tham chiếu EARS/BR: `# Implements BR-XX`.
- Đặt tên:
  - Classes: PascalCase (e.g., `BorrowerAgent`, `AMMPool`)
  - Functions/Variables: snake_case (e.g., `calculate_health_factor`, `execute_swap`)
  - Constants: UPPER_SNAKE_CASE (e.g., `DEFAULT_LIQUIDATION_PENALTY`)
- Giới hạn hàm: Tối đa 50 dòng code/hàm. Tối đa 300 dòng/file.
- Linter/Formatter: `ruff` check sạch 100%, không để sót `print` debug hoặc `# TODO`.

## TESTING REQUIREMENTS (Universal Definition of Done)
- Unit test coverage: >= 85% cho tầng `domain/` và `usecase/`.
- Zero-mocking cho logic toán học: Không mock các phép tính AMM hay HF, dùng test cases thực nghiệm.
- Kiểm thử kịch bản: Bắt buộc có kiểm thử tự động so sánh SC01, SC02, SC03 xác nhận thứ tự tác động.
- Mọi PR/Commit phải chạy pass lệnh: `pytest tests/` với 0 lỗi.

═══════════════════════════════════════════════════════════════════════════════
  LAYER 4: AI AGENT RULES (QUY TẮC DÀNH CHO AI AGENT)
═══════════════════════════════════════════════════════════════════════════════
- Đọc kỹ `CONSTITUTION.md` và `AGENTS.md` trước khi bắt đầu session.
- QUY TẮC BẤT DI BẤT DỊCH — SPEC-FIRST (KHÔNG CÓ SPEC, CẤM VIẾT CODE):
  * Khi người dùng yêu cầu code, Agent BẮT BUỘC phải dừng lại kiểm tra hoặc soạn thảo đặc tả `SPEC.md` trước.
  * TUYỆT ĐỐI CẤM sinh code (trong `src/`) khi chưa có đặc tả `SPEC.md` với cú pháp EARS và danh sách `TASKS.md` tương ứng đã được duyệt.
  * Mọi quy trình đặc tả phải sử dụng Spec Kit (`/speckit-specify`, `/speckit-plan`, `/speckit-tasks`, `/speckit-clarify`, `/speckit-converge`).
- BẮT BUỘC DÙNG CODEGRAPH ĐỂ ĐỌC CODE: Mọi hoạt động đọc, khám phá kiến trúc, truy vết call graph, phân tích blast radius hoặc tìm test bị ảnh hưởng đều phải gọi công cụ CodeGraph (`codegraph_explore` hoặc `codegraph` CLI), tuyệt đối không duyệt file thủ công.
- Áp dụng nguyên tắc "Fix the Spec, not the Code": Khi test fail hoặc phát sinh điểm chưa rõ, cập nhật spec trước khi sửa code.
- Tuyệt đối không tự ý import thêm thư viện ngoài danh sách Tech Stack đã khóa.
- Luôn tạo unit test đi kèm với mỗi module mới sinh ra (DoD $\ge 85\%$ coverage).

