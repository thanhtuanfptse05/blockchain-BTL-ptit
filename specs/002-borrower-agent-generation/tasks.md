# Tasks: Borrower Agent Generation

**Feature**: `002-borrower-agent-generation`  
**Input**: [`specs/002-borrower-agent-generation/spec.md`](file:///d:/wd/c/sang/d/Documents/BTL-block-chain/specs/002-borrower-agent-generation/spec.md)  
**Plan**: [`specs/002-borrower-agent-generation/plan.md`](file:///d:/wd/c/sang/d/Documents/BTL-block-chain/specs/002-borrower-agent-generation/plan.md)  

## Task List

- [x] **T002-01** [US1] Cài đặt `AssetType` và `BorrowerAgent` trong `src/domain/agent.py`.
- [x] **T002-02** [US1] Viết unit test `tests/unit/test_agent_generator.py` kiểm tra sinh đúng `num_borrowers` (mặc định 100), đúng 50 ETH và 50 stETH (UT-02).
- [x] **T002-03** [US1, US2] Viết unit test kiểm tra LTV ban đầu $\in [0.55, 0.72]$, collateral USD $\in [250\text{k}, 1\text{M}]$, và mọi $HF > 1.0$.
- [x] **T002-04** [US3] Viết unit test kiểm tra tính tất định: cùng seed sinh danh sách giống hệt nhau; khác seed sinh danh sách khác nhau (UT-03).
- [x] **T002-05** Cài đặt hàm `generate_borrower_agents` trong `src/usecase/agent_generator.py`.
- [x] **T002-06** Chạy `pytest tests/unit/test_agent_generator.py` xác nhận 100% test pass.

