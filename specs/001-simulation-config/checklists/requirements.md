# Requirements Quality Review Checklist: Simulation Config & Validation

**Feature**: `001-simulation-config`  
**Reviewer**: SDD Spec Auditor  
**Standard**: Chapter 16.7 (Spec Quality Review) — *Spec-Driven & Agent-Driven Development*  

## 1. Context & Business Value
- [x] CHK001 [Context] Mục đích của cấu hình và validation được giải thích rõ ràng (bảo vệ hệ thống mô phỏng không crash, kiểm soát các điều kiện thí nghiệm khoa học).

## 2. Completeness & Boundaries
- [x] CHK002 [Completeness] Tất cả 6 tham số P-01..P-06 và 10 ràng buộc C-01..C-10 được liệt kê đầy đủ.
- [x] CHK003 [Scope] Ranh giới Out-of-Scope được định nghĩa rõ (không đọc từ remote API, không cho phép thay đổi cấu hình giữa chừng khi đang chạy block).

## 3. Clarity & Testability (EARS)
- [x] CHK004 [Clarity] Tất cả yêu cầu sử dụng cú pháp EARS chuẩn xác (Ubiquitous, Event-driven, State-driven, Unwanted).
- [x] CHK005 [Clarity] Không có từ ngữ định tính mơ hồ ("giá trị phù hợp", "hợp lý"); toàn bộ giới hạn có con số cụ thể ($10\text{M} \le TVL \le 500\text{M}$).
- [x] CHK006 [Testability] Mỗi ràng buộc biên C-01..C-10 đều có Acceptance Scenario tương ứng kiểu Given-When-Then để viết thành automated test.

## 4. Consistency & Architecture
- [x] CHK007 [Consistency] Tên các trường (`shock_pct`, `pool_a_tvl_usd`, v.v.) nhất quán 100% với `requirements.md` và `CONSTITUTION.md`.
- [x] CHK008 [Architecture] Model thuộc tầng `domain/`, độc lập hoàn toàn, không phụ thuộc vào `usecase` hay `interface`.

## 5. Non-Functional & Edge Cases
- [x] CHK009 [Robustness] Các tình huống ngoại lệ (chuỗi không ép kiểu được thành số, số âm, giá trị vượt ngưỡng) đều có mã lỗi và thông báo lỗi tường minh.
- [x] CHK010 [Readiness] Không còn bất kỳ câu hỏi mở (Open Questions) nào chưa được giải quyết.

