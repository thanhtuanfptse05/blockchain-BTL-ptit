# AI Agent Safety & Guardrails
# Project: DeFi Liquidation Cascade Simulator

1. **Agent Modification Limits:**
   - AI Agent chỉ được tạo hoặc sửa files trong thư mục được phân công:
     * Task Core: `src/domain/`, `src/usecase/`, `tests/unit/`, `tests/integration/`
     * Task UI: `src/interface/`, `src/infra/`, `app.py`
   - AI Agent KHÔNG ĐƯỢC tự ý sửa file `CONSTITUTION.md` hoặc các file spec đã được đánh dấu `Status: APPROVED`.

2. **Validation Gate Enforcement:**
   - Trước khi coi một task là hoàn thành:
     * Chạy `pytest` để đảm bảo 100% tests pass.
     * Kiểm tra EARS tags trong code comments.
     * Xác nhận không có `print` debug hay hardcoded variables.

3. **Human Explainability:**
   - Nhà phát triển phải có khả năng giải thích từng dòng code mà AI sinh ra trước khi đưa vào codebase chính thức.

