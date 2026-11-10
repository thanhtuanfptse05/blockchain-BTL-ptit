# Research & Technical Decisions: AMM Constant Product Pools

**Feature**: `005-amm-pools`  
**Date**: 2026-11-10  
**Status**: Completed  

## 1. Technical Context & Formulas (BR-05, BR-06, BR-09)

- **Nguyên lý Constant Product & Zero Fee**:
  - Tích số bất biến: $k = x \cdot y$.
  - Phí giao dịch: **0% (zero-fee swap)** theo đúng SRS §5.5 và BR-05.
  - Khi bán một lượng $\Delta x$ vào pool, lượng $\Delta y$ nhận về là:
    $$\Delta y = \frac{y \cdot \Delta x}{x + \Delta x}$$
  - Sau giao dịch:
    $$x_{new} = x + \Delta x, \quad y_{new} = y - \Delta y$$
    $$x_{new} \cdot y_{new} = (x + \Delta x) \cdot \left(y - \frac{y \cdot \Delta x}{x + \Delta x}\right) = (x + \Delta x) \cdot \frac{x \cdot y}{x + \Delta x} = x \cdot y = k \quad (\text{Bảo toàn tuyệt đối!})$$

## 2. Pool Initial State & Rebalancing Research

- **Pool A (ETH/USDC)**:
  - TVL mặc định: $\$150,000,000$. Mỗi bên trị giá $\$75,000,000$.
  - $P_{ETH} = \$3,000.0$.
  - $x_0 = \frac{75,000,000}{3,000} = 25,000$ ETH.
  - $y_0 = 75,000,000$ USDC.
  - $k_A = 25,000 \times 75,000,000 = 1,875,000,000,000$.
  - Spot price: $P_{ETH} = \frac{y_A}{x_A} = \frac{75,000,000}{25,000} = 3,000$ USD.
- **Pool B (stETH/ETH)**:
  - TVL mặc định: $\$80,000,000$ (tương đương $\frac{80,000,000}{3,000} \approx 26,666.67$ ETH).
  - Tỉ lệ giá ban đầu: $1$ stETH $= 0.99$ ETH (discount 1.0%).
  - Spot price: $P_{stETH\_per\_ETH} = \frac{y_B}{x_B} = 0.99$.
  - $x_0 = 13,400.99$ stETH, $y_0 = 13,266.98$ ETH sao cho tổng giá trị quy đổi sang USD bằng $\$80,000,000$.
- **Cú sốc ngoại sinh tại Block 1**:
  - Giá ETH sau shock: $P_{after} = 3000 \times (1 - \text{shock\_pct}/100)$.
  - Tái cân bằng Pool A giữ nguyên $k_A$:
    $$x_{new} = \sqrt{\frac{k_A}{P_{after}}}, \quad y_{new} = \sqrt{k_A \cdot P_{after}}$$
  - Pool B **không bị shock trực tiếp** mà giữ nguyên reserves; chỉ biến động khi có lệnh bán stETH từ liquidator.

