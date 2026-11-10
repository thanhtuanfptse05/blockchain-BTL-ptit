# Research & Technical Decisions: Borrower Agent Generation

**Feature**: `002-borrower-agent-generation`  
**Date**: 2026-11-10  
**Status**: Completed  

## 1. Technical Context & Determinism Research

- **Random Generator**: Bắt buộc sử dụng `random.Random(seed)` riêng biệt (isolated instance), TUYỆT ĐỐI KHÔNG dùng global `random.seed()` vì có thể bị side-effects bởi các thư viện khác (Streamlit hoặc bên thứ ba).
- **Phân bổ tài sản**: Đúng $50\%$ số vị thế là ETH và $50\%$ số vị thế là stETH (với $N=100$: 50 ETH và 50 stETH).
- **Khoảng LTV ban đầu**: Uniform distribution trong đoạn $[0.55, 0.72]$.
- **Khoảng Collateral USD ban đầu**: Uniform distribution trong đoạn $[\$250,000, \$1,000,000]$.
- **Giá tham chiếu ban đầu**:
  - $P_{ETH} = \$3,000.0$.
  - $P_{stETH} = \$3,000.0 \times 0.99 = \$2,970.0$ (discount 1.0%).
- **Công thức tính nợ ban đầu**:
  $$\text{collateral\_amount} = \frac{\text{collateral\_usd}}{P_{asset}}$$
  $$\text{debt\_usdc} = \text{collateral\_usd} \times \text{initial\_ltv}$$
  $$\text{initial\_hf} = \frac{\text{collateral\_usd} \times LT}{\text{debt\_usdc}} = \frac{0.80}{\text{initial\_ltv}}$$
  Với $\text{initial\_ltv} \in [0.55, 0.72] \implies \text{initial\_hf} \in [1.111, 1.455] > 1.0$ $\implies$ Mọi Agent ban đầu đều an toàn 100%!

