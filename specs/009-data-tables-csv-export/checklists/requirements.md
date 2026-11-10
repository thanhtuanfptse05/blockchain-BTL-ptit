# Requirements Quality Review Checklist: Data Tables & CSV Exporter

**Feature**: `009-data-tables-csv-export`  
**Reviewer**: SDD Spec Auditor  
**Standard**: Chapter 16.7 (Spec Quality Review) — *Spec-Driven & Agent-Driven Development*  

## 1. Context & Business Value
- [x] CHK001 [Context] Xuất CSV là kênh cung cấp dữ liệu thô độc lập cho hội đồng chấm BTL thẩm định và phân tích lại.

## 2. Completeness & Boundaries
- [x] CHK002 [Completeness] Thứ tự và danh sách 12 cột BlockResult và 10 cột LiquidationEvent được liệt kê chính xác.
- [x] CHK003 [Scope] Out-of-Scope: Không sử dụng cơ sở dữ liệu SQL/NoSQL; toàn bộ lưu trữ và xuất trực tiếp qua file CSV.

## 3. Clarity & Testability (EARS)
- [x] CHK004 [Clarity] Cú pháp EARS định nghĩa rõ quy tắc không hiển thị nút tải dữ liệu rỗng trước khi chạy mô phỏng.
- [x] CHK005 [Clarity] Quy định mã hóa UTF-8 chuẩn RFC 4180.
- [x] CHK006 [Testability] Có bài kiểm thử tự động đọc lại bằng `pandas.read_csv` theo tiêu chuẩn ST-08.

## 4. Consistency & Architecture
- [x] CHK007 [Consistency] Tên cột trong CSV khớp từng ký tự với schema tại SRS §7.3 và §7.4.
- [x] CHK008 [Architecture] Logic xuất file nằm ở tầng `infra/`, tách biệt khỏi giao diện người dùng.

