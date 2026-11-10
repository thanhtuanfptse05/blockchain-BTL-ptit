# Requirements Quality Review Checklist: AMM Constant Product Pools

**Feature**: `005-amm-pools`  
**Reviewer**: SDD Spec Auditor  
**Standard**: Chapter 16.7 (Spec Quality Review) — *Spec-Driven & Agent-Driven Development*  

## 1. Context & Business Value
- [x] CHK001 [Context] AMM là cơ chế truyền dẫn tác động giá khi tài sản bị thanh lý bị bán tháo, tạo nên hiện tượng lây lan cascade.

## 2. Completeness & Boundaries
- [x] CHK002 [Completeness] Công thức swap zero-fee, công thức shock rebalance giữ nguyên $k_A$, và công thức tính discount được mô tả chi tiết.
- [x] CHK003 [Scope] Out-of-Scope: Không có phí swap (fee = 0), không có Liquidity Provider nạp/rút trong quá trình mô phỏng, không có bot arbitrage cân bằng giá.

## 3. Clarity & Testability (EARS)
- [x] CHK004 [Clarity] Cú pháp EARS phân loại đúng các hành vi bảo toàn tích số $k$.
- [x] CHK005 [Clarity] Giá cả thay đổi duy nhất thông qua thay đổi dự trữ $x$ và $y$, cấm gán cứng `pool.price = new_price`.
- [x] CHK006 [Testability] Kiểm tra bất biến $k_{after} == k_{before}$ với độ chính xác số học `pytest.approx(rel=1e-7)`.

## 4. Consistency & Architecture
- [x] CHK007 [Consistency] Khởi tạo reserves từ TVL mặc định ($150M cho Pool A, $80M cho Pool B) chuẩn xác.
- [x] CHK008 [Architecture] Tách biệt Entity `AMMPool` (Domain) và Engine thực thi swap (Usecase).

