# Tasks: AMM Constant Product Pools

**Feature**: `005-amm-pools`  
**Input**: [`specs/005-amm-pools/spec.md`](file:///d:/wd/c/sang/d/Documents/BTL-block-chain/specs/005-amm-pools/spec.md)  
**Plan**: [`specs/005-amm-pools/plan.md`](file:///d:/wd/c/sang/d/Documents/BTL-block-chain/specs/005-amm-pools/plan.md)  

## Task List

- [x] **T005-01** [US1] Cài đặt thực thể `AMMPool` trong `src/domain/amm_pool.py` với các thuộc tính `reserve_x`, `reserve_y`, `k`, `spot_price`.
- [x] **T005-02** [US1] Viết unit test `tests/unit/test_amm_engine.py` kiểm tra swap zero-fee: $\Delta y = \frac{y \cdot \Delta x}{x + \Delta x}$, $k$ sau swap bằng $k$ trước swap (UT-09).
- [x] **T005-03** [US2] Viết unit test kiểm tra cú sốc ngoại sinh 15%: Pool A giá giảm từ 3000 xuống 2550, $k_A$ không đổi, Pool B giữ nguyên (UT-12, UT-13).
- [x] **T005-04** [US3] Viết unit test kiểm tra tính tỉ lệ discount stETH: ban đầu đúng 1.0%, sau khi bán stETH discount tăng lên tương ứng.
- [x] **T005-05** Cài đặt các hàm `swap_exact_input`, `apply_exogenous_shock`, `calculate_steth_discount` trong `src/usecase/amm_engine.py`.
- [x] **T005-06** Chạy `pytest tests/unit/test_amm_engine.py` xác nhận 100% test pass.

