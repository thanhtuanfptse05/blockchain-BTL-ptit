# Tasks: Scenario Simulation & Block Loop

**Feature**: `006-scenario-block-simulation`  
**Input**: [`specs/006-scenario-block-simulation/spec.md`](file:///d:/wd/c/sang/d/Documents/BTL-block-chain/specs/006-scenario-block-simulation/spec.md)  
**Plan**: [`specs/006-scenario-block-simulation/plan.md`](file:///d:/wd/c/sang/d/Documents/BTL-block-chain/specs/006-scenario-block-simulation/plan.md)  

## Task List

- [x] **T006-01** [US1] Cài đặt `BlockResult` (12 trường) trong `src/domain/block_result.py` và `SimulationResult` trong `src/domain/simulation_result.py`.
- [x] **T006-02** [US2] Viết unit test `tests/unit/test_scenario_runner.py` cho SC01: không shock, không thanh lý, giá phẳng ở 3000 USD, discount phẳng ở 1.0% (UT-11).
- [x] **T006-03** [US3] Viết unit test cho SC02: shock tại block 1 xuống 2550 USD, có thanh lý, reserves AMM không đổi, giá giữ nguyên từ block 1 đến max_blocks (UT-10).
- [x] **T006-04** [US4] Viết unit test cho SC03: thanh lý ETH bán vào Pool A, thanh lý stETH bán Pool B rồi bán tiếp vào Pool A, giá ETH và discount thay đổi (UT-14).
- [x] **T006-05** [US1] Cài đặt `run_scenario` và `run_all_scenarios` trong `src/usecase/scenario_runner.py`.
- [x] **T006-06** Viết test hệ thống `tests/system/test_system_scenarios.py` xác minh toàn bộ các điều kiện bất biến ST-01 đến ST-07.
- [x] **T006-07** Chạy `pytest tests/unit/test_scenario_runner.py tests/system/test_system_scenarios.py` xác nhận 100% test pass.

