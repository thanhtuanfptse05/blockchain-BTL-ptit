# CLAUDE.md — Project Memory
Đọc `CONSTITUTION.md`, `AGENTS.md`, rồi spec trong `specs/NNN-*/spec.md`. Nguồn chân lý: `requirements.md`.

## Decisions đã chốt (xem mục Assumptions trong từng spec)
- AMM không phí (SRS BR-05). LT 0.80. close_factor 0.5. bonus 0.05. epsilon 1e-9.
- Agent id 1..N/2 = ETH, N/2+1..N = stETH; mỗi Agent rút `collateral_value` rồi `initial_ltv` từ `random.Random(seed)`, phân phối đều.
- `collateral_value_at_oracle_usd` = collateral_seized × giá spot TRƯỚC giao dịch.
- Engine validate trả về TẤT CẢ lỗi cấu hình (không dừng ở lỗi đầu).

## AUTO MEMORY
- (agent ghi thêm tại đây)
