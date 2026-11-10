# Research & Technical Decisions: Partial Liquidation Engine

**Feature**: `004-partial-liquidation-engine`  
**Date**: 2026-11-10  
**Status**: Completed  

## 1. Technical Context & Formulas (BR-04, BR-10)

- **Quy tắc thanh lý một phần (Close Factor = 0.50)**:
  - Khi $HF < 1.0$, người thanh lý (liquidator) trả nợ thay tối đa:
    $$\text{debt\_repaid\_usd} = \text{debt\_usdc} \times \text{close\_factor} = \text{debt\_usdc} \times 0.50$$
- **Lượng tài sản thế chấp bị thu giữ (Liquidation Penalty = 0.05)**:
  - Giá trị tài sản thanh lý đòi hỏi (bao gồm 5% tiền thưởng cho liquidator):
    $$\text{required\_collateral\_usd} = \text{debt\_repaid\_usd} \times (1 + \text{liquidation\_penalty}) = \text{debt\_repaid\_usd} \times 1.05$$
  - Quy đổi ra số lượng tài sản tại giá spot trước giao dịch:
    $$\text{seized\_amount\_ideal} = \frac{\text{required\_collateral\_usd}}{P_{asset}}$$
  - Lượng tài sản thực tế bị thu giữ (không vượt quá số collateral người vay đang có):
    $$\text{collateral\_seized} = \min(\text{collateral\_amount}, \text{seized\_amount\_ideal})$$
- **Cập nhật trạng thái Agent**:
  $$\text{remaining\_debt\_usd} = \text{debt\_usdc} - \text{debt\_repaid\_usd}$$
  $$\text{remaining\_collateral} = \text{collateral\_amount} - \text{collateral\_seized}$$
- **Xác định Nợ Xấu (Bad Debt)**:
  - Nếu $\text{remaining\_collateral} \le 10^{-9}$ mà $\text{remaining\_debt\_usd} > 0 \implies$ phần nợ còn lại trở thành Bad Debt của giao thức.

