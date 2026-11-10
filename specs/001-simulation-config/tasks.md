# Tasks: Simulation Config & Validation

**Feature**: `001-simulation-config`  
**Input**: [`specs/001-simulation-config/spec.md`](file:///d:/wd/c/sang/d/Documents/BTL-block-chain/specs/001-simulation-config/spec.md)  
**Plan**: [`specs/001-simulation-config/plan.md`](file:///d:/wd/c/sang/d/Documents/BTL-block-chain/specs/001-simulation-config/plan.md)  

## Task List

- [x] **T001-01** [US1] Viết unit test `tests/unit/test_config.py` kiểm tra khởi tạo giá trị mặc định chuẩn P-01..P-06.
- [x] **T001-02** [US2] Viết unit test trong `tests/unit/test_config.py` kiểm tra các trường hợp vi phạm biên C-01..C-10 (`shock_pct < 0`, `shock_pct > 50`, `pool_a_tvl < 10M`, v.v.).
- [x] **T001-03** [US1, US2] Cài đặt `SimulationConfig` trong `src/domain/config.py` với đầy đủ validator và immutability.
- [x] **T001-04** [US3] Viết test kiểm tra tính bất biến (immutability): gán đè thuộc tính sinh lỗi `ValidationError` hoặc `FrozenInstanceError`.
- [x] **T001-05** Chạy `pytest tests/unit/test_config.py` xác nhận 100% test pass.

