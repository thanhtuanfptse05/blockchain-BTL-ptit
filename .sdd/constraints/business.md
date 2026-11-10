# Business Constraints — trích nguyên văn từ requirements.md

- Collateral: ETH hoặc stETH (mỗi Agent đúng 1 loại). Nợ: USDC, 1 USDC = 1 USD.
- C-01 `initial_eth_price_usd` = 3000 | C-02 `initial_steth_discount_pct` = 1% (r = 0.99) | C-03 `lt` = 0.80
- C-04 `initial_ltv_min` = 0.55 | C-05 `initial_ltv_max` = 0.72 | C-06 `collateral_value_min_usd` = 250000 | C-07 `collateral_value_max_usd` = 1000000
- C-08 `close_factor` = 0.50 | C-09 `liquidation_bonus` = 0.05 | C-10 `epsilon` = 1e-9
- AMM: KHÔNG phí; `amount_y_out = y*dx/(x+dx)`.
- HF = collateral_value * lt / debt; thanh lý khi HF < 1 (và debt > eps, collateral > eps).
- Mỗi Agent tối đa 1 lần thanh lý / block; xử lý theo agent_id tăng dần; chọn candidates ở đầu block, kiểm tra lại HF trước giao dịch.
- Shock: 1 lần, đầu block 1, chỉ SC02/SC03; cân bằng Pool A giữ k_A; Pool B không đổi.
- Chi tiết đầy đủ: thư mục `specs/` (001–010).
