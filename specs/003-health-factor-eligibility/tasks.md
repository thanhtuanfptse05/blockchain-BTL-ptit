# Tasks: Health Factor & Collateral Valuation

**Feature**: `003-health-factor-eligibility`  
**Input**: [`specs/003-health-factor-eligibility/spec.md`](file:///d:/wd/c/sang/d/Documents/BTL-block-chain/specs/003-health-factor-eligibility/spec.md)  
**Plan**: [`specs/003-health-factor-eligibility/plan.md`](file:///d:/wd/c/sang/d/Documents/BTL-block-chain/specs/003-health-factor-eligibility/plan.md)  

## Task List

- [x] **T003-01** [US1] Viết unit test `tests/unit/test_health_factor.py` cho ví dụ tính tay (§8): $10$ ETH, $P_{ETH} = \$3,000 \rightarrow HF = 1.0909$; sau shock $15\%$ ($P_{ETH} = \$2,550$) $\rightarrow HF = 0.9273$ (UT-04).
- [x] **T003-02** [US2] Viết unit test cho tài sản stETH: nhân giá chéo $P_{stETH} = P_{ETH} \times P_{stETH\_per\_ETH}$ và kiểm tra HF (UT-05).
- [x] **T003-03** [US3] Viết unit test cho các trạng thái biên: nợ $\le 10^{-9} \implies HF = \infty$; collateral $\le 10^{-9} \implies HF = 0.0$ và không cho thanh lý (UT-06).
- [x] **T003-04** Cài đặt `compute_collateral_value`, `compute_health_factor`, và `is_liquidatable` trong `src/usecase/health_factor.py`.
- [x] **T003-05** Chạy `pytest tests/unit/test_health_factor.py` xác nhận 100% test pass.

