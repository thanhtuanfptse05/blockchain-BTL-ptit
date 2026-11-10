# CLAUDE.md — Agent & Project Memory
# Đọc file CONSTITUTION.md và AGENTS.md trước khi bắt đầu bất kỳ session nào.

## MANUAL MEMORY (Human-Maintained)

### Architecture Decisions (ADR)
- # ADR-001: Sử dụng Pure Python Standard Library + Dataclasses cho Domain Entities để tối đa hóa tốc độ vòng lặp mô phỏng.
- # ADR-002: Mô hình AMM Constant-Product (x * y = k) được trừ phí 0.3% trước khi nhân theo chuẩn Uniswap v2: `dy = (y * dx * 0.997) / (x + dx * 0.997)`.
- # ADR-003: Deep copy danh sách Agents khởi tạo cho từng kịch bản (SC01, SC02, SC03) để đảm bảo 100% tính công bằng khi đối chứng kết quả.
- # ADR-004: Tách Streamlit UI thành các module nhỏ trong `src/interface/components/` để tránh file `app.py` phình to quá 300 dòng.

### Business Rules Reference (Tra cứu nhanh từ requirements.md)
- # BR-01: Collateral Value = collateral_amount * collateral_price.
- # BR-02: LTV = debt_amount / collateral_value.
- # BR-03: Health Factor (HF) = (collateral_amount * price * liquidation_threshold) / debt_amount.
- # BR-04: Thanh lý một phần: repay_debt = min(debt * 0.5, debt); seized_collateral = (repay_debt * 1.05) / price.
- # BR-05: AMM constant-product swap với fee 0.3%.
- # BR-06: Khởi tạo Pool 1 (ETH/USDC: 3,333.33 ETH & 10M USDC) và Pool 2 (stETH/ETH: 10,000 stETH & 10,000 ETH).
- # BR-07: Block 1 áp dụng cú sốc ngoại sinh (giảm giá ETH).
- # BR-08: SC03: Tịch thu ETH -> Bán sang USDC; Tịch thu stETH -> Bán sang ETH -> Bán tiếp sang USDC.
- # BR-09: Giá stETH = Giá ETH * (stETH_reserve_ETH / stETH_reserve_stETH); Discount = 1 - (stETH_price / ETH_price).
- # BR-10: Nợ xấu ghi nhận khi seized_collateral tính toán vượt quá collateral hiện có của Agent.

### Patterns to Follow
- Domain entity: `src/domain/[entity].py`
- Engine/Usecase: `src/usecase/[engine].py`
- Tests: `tests/unit/test_[module].py`
- Docstring: Google style kèm EARS tag: `# Implements BR-XX (EARS-YY)`.

## AUTO MEMORY (Agent appends here)
- Project initialized with SDD 5-phase structure and Spec Kit skills.
