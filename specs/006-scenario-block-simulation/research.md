# Research & Technical Decisions: Scenario Simulation & Block Loop

**Feature**: `006-scenario-block-simulation`  
**Date**: 2026-11-10  
**Status**: Completed  

## 1. Technical Context & State Isolation Research

- **Deepcopy Isolation**: Cả 3 kịch bản SC01, SC02, SC03 phải nhận cùng một danh sách Agent ban đầu và cùng trạng thái pool ban đầu, nhưng phải được clone bằng `copy.deepcopy()` để việc thay đổi nợ, collateral hay reserves trong kịch bản này tuyệt đối không làm biến đổi trạng thái của kịch bản khác.
- **Thuật toán điều phối từng Block (SRS §10)**:
  - **Block 0**: Khởi tạo ban đầu, ghi nhận giá, $HF > 1$, $0$ thanh lý.
  - **Block 1**:
    - Với SC01: Không có shock, giá giữ nguyên.
    - Với SC02 & SC03: Áp dụng cú sốc ngoại sinh `apply_exogenous_shock(pool_a, shock_pct)`.
  - **Duyệt thanh lý trong Block**:
    1. Lấy danh sách ứng viên có $HF < 1$ tại đầu block, sắp xếp theo `agent_id` tăng dần.
    2. Trước mỗi lượt thanh lý, kiểm tra lại `is_liquidatable` với giá spot ngay trước giao dịch.
    3. Thực thi thanh lý vị thế.
    4. **Cơ chế phản hồi giá (Selling Route)**:
       - Trong SC02: KHÔNG bán collateral vào AMM (giá giữ nguyên).
       - Trong SC03: Bán collateral thu giữ vào AMM:
         - Nếu là ETH: Bán trực tiếp vào Pool A (ETH $\to$ USDC).
         - Nếu là stETH: Bán vào Pool B lấy ETH (stETH $\to$ ETH), sau đó bán toàn bộ ETH nhận được vào Pool A (ETH $\to$ USDC).
       - Cập nhật giá spot mới.
    5. Ghi nhận `BlockResult` cuối block và chuyển sang block tiếp theo.
- **Dừng mô phỏng**: Chạy đủ `max_blocks + 1` dòng (từ block 0 đến block `max_blocks`). Nếu không còn vị thế thanh lý ở các block sau, giá đi ngang và `liquidations_total = 0`.

