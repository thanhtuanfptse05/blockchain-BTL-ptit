# Tasks: Partial Liquidation Engine

**Feature**: `004-partial-liquidation-engine`  
**Input**: [`specs/004-partial-liquidation-engine/spec.md`](file:///d:/wd/c/sang/d/Documents/BTL-block-chain/specs/004-partial-liquidation-engine/spec.md)  
**Plan**: [`specs/004-partial-liquidation-engine/plan.md`](file:///d:/wd/c/sang/d/Documents/BTL-block-chain/specs/004-partial-liquidation-engine/plan.md)  

## Task List

- [x] **T004-01** [US1] Cài đặt schema `LiquidationEvent` trong `src/domain/liquidation_event.py` với đúng 10 trường chuẩn theo SRS §7.3.
- [x] **T004-02** [US1] Viết unit test `tests/unit/test_liquidation_engine.py` kiểm tra thanh lý vị thế bình thường: trả đúng 50% nợ, thu đúng collateral quy đổi từ $(1 + 0.05) \times \text{debt\_repaid}$, cập nhật số dư còn lại (UT-07).
- [x] **T004-03** [US2] Viết unit test cho trường hợp tài sản không đủ trả nợ: thu toàn bộ collateral còn lại, xác định nợ xấu (bad debt) chính xác (UT-08).
- [x] **T004-04** Cài đặt hàm `liquidate_borrower_position` trong `src/usecase/liquidation_engine.py`.
- [x] **T004-05** Chạy `pytest tests/unit/test_liquidation_engine.py` xác nhận 100% test pass.

