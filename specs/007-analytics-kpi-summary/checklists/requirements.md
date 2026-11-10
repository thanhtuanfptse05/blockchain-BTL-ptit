# Requirements Quality Review Checklist: Analytics & Summary KPIs

**Feature**: `007-analytics-kpi-summary`  
**Reviewer**: SDD Spec Auditor  
**Standard**: Chapter 16.7 (Spec Quality Review) — *Spec-Driven & Agent-Driven Development*  

## 1. Context & Business Value
- [x] CHK001 [Context] 6 chỉ số KPI và bảng so sánh trực diện giúp người dùng nắm bắt nhanh mức độ thiệt hại của rủi ro lây lan.

## 2. Completeness & Boundaries
- [x] CHK002 [Completeness] 6 chỉ số cốt lõi và 6 phép tính delta được định nghĩa rõ ràng.
- [x] CHK003 [Scope] Out-of-Scope: Tuyệt đối không hardcode bất kỳ con số nào; mọi dữ liệu đều trích xuất động từ `SimulationResult`.

## 3. Clarity & Testability (EARS)
- [x] CHK004 [Clarity] Cú pháp EARS phân loại các yêu cầu định dạng số tiền, số phần trăm và xử lý lỗi chia cho 0.
- [x] CHK005 [Clarity] Quy định rõ ràng quy tắc làm tròn 2 chữ số thập phân cho USD và %.
- [x] CHK006 [Testability] Kiểm tra tự động các fixture biên: trường hợp không có thanh lý, trường hợp SC02 = 0 và SC03 > 0.

## 4. Consistency & Architecture
- [x] CHK007 [Consistency] Đồng nhất tên các chỉ số giữa `SimulationResult` và giao diện Dashboard.
- [x] CHK008 [Architecture] Logic tổng hợp số liệu được tách biệt thành component độc lập trong `src/interface/components/metrics.py`.

