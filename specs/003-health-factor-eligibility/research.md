# Research & Technical Decisions: Health Factor & Collateral Valuation

**Feature**: `003-health-factor-eligibility`  
**Date**: 2026-11-10  
**Status**: Completed  

## 1. Technical Context & Formulas

- **Định giá tài sản thế chấp (BR-01)**:
  $$\text{collateral\_value\_usd} = \text{collateral\_amount} \times P_{asset}$$
  Trong đó:
  - Nếu `asset == AssetType.ETH`: $P_{asset} = P_{ETH\_USD}$ (lấy từ Pool A).
  - Nếu `asset == AssetType.STETH`: $P_{asset} = P_{stETH\_USD} = P_{ETH\_USD} \times P_{stETH\_per\_ETH}$ (Pool A $\times$ Pool B).
- **Tính LTV hiện thời (BR-02)**:
  $$\text{current\_ltv} = \frac{\text{debt\_usdc}}{\text{collateral\_value\_usd}}$$
- **Tính Health Factor (BR-03)**:
  $$HF = \frac{\text{collateral\_value\_usd} \times LT}{\text{debt\_usdc}}$$
  với $LT = 0.80$ thống nhất cho cả ETH và stETH.

## 2. Edge Cases & Numerical Stability Research

- **Trường hợp $\text{debt\_usdc} \le 10^{-9}$ (Epsilon)**:
  - Khi người vay đã trả hết nợ hoặc nợ còn lại chỉ là phần thập phân siêu nhỏ do làm tròn, $HF = \infty$ (`math.inf`). Vị thế hoàn toàn an toàn, không thể bị thanh lý.
- **Trường hợp $\text{collateral\_amount} \le 10^{-9}$ và $\text{debt\_usdc} > 0$**:
  - Vị thế đã cạn sạch tài sản thế chấp nhưng vẫn còn nợ. $HF = 0.0$. Đánh dấu trạng thái `BAD_DEBT`. Không thể thanh lý tiếp vì không còn tài sản để thu giữ.
- **Ví dụ đối chiếu tính tay (§8)**:
  - Cho Agent có $10$ ETH, $P_{ETH} = \$3,000$, $\text{debt} = \$22,000$, $LT = 0.80$:
    $$HF = \frac{10 \times 3000 \times 0.80}{22000} = \frac{24000}{22000} \approx 1.0909 > 1.0 \quad (\text{An toàn})$$
  - Sau shock $15\%$ ($P_{ETH} = \$2,550$):
    $$HF = \frac{10 \times 2550 \times 0.80}{22000} = \frac{20400}{22000} \approx 0.9273 < 1.0 \quad (\text{Đủ điều kiện thanh lý})$$

