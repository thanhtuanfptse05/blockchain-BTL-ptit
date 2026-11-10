# Requirements Quality Review Checklist: Borrower Agent Generation

**Feature**: `002-borrower-agent-generation`  
**Reviewer**: SDD Spec Auditor  
**Standard**: Chapter 16.7 (Spec Quality Review) — *Spec-Driven & Agent-Driven Development*  

## 1. Context & Business Value
- [x] CHK001 [Context] Mục đích tạo quần thể Agent đại diện cho cộng đồng người vay DeFi có phân bổ tài sản thế chấp và đòn bẩy thực tế.

## 2. Completeness & Boundaries
- [x] CHK002 [Completeness] Quy tắc phân bổ 50/50, khoảng LTV, khoảng giá trị tài sản thế chấp và công thức tính nợ ban đầu được xác định rõ.
- [x] CHK003 [Scope] Out-of-Scope: Không sinh vị thế mới trong quá trình mô phỏng; Agent không tự nạp thêm tiền bảo chứng (no dynamic collateral top-up).

## 3. Clarity & Testability (EARS)
- [x] CHK004 [Clarity] Cú pháp EARS phân định rõ các ràng buộc Ubiquitous, Event-driven và Unwanted.
- [x] CHK005 [Clarity] Mọi Agent ban đầu bắt buộc có $HF > 1.0$ (không có vị thế nào bị thanh lý ở block 0 trước cú sốc).
- [x] CHK006 [Testability] Kiểm tra tính tất định 100% bằng cách so sánh 2 instance độc lập cùng `seed`.

## 4. Consistency & Architecture
- [x] CHK007 [Consistency] Sử dụng đúng giá tham chiếu ban đầu ($P_{ETH} = \$3,000$, $P_{stETH} = \$2,970$).
- [x] CHK008 [Architecture] Tách biệt `BorrowerAgent` (Domain entity) và `generate_borrower_agents` (Usecase).

