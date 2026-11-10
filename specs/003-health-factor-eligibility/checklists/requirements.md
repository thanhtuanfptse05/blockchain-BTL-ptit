# Requirements Quality Review Checklist: Health Factor & Collateral Valuation

**Feature**: `003-health-factor-eligibility`  
**Reviewer**: SDD Spec Auditor  
**Standard**: Chapter 16.7 (Spec Quality Review) — *Spec-Driven & Agent-Driven Development*  

## 1. Context & Business Value
- [x] CHK001 [Context] Health Factor là thước đo cốt lõi của giao thức lending để phát hiện các vị thế dưới chuẩn thế chấp cần thanh lý.

## 2. Completeness & Boundaries
- [x] CHK002 [Completeness] Công thức tính toán cho cả 2 loại tài sản (ETH trực tiếp, stETH qua giá chéo) được định nghĩa đầy đủ.
- [x] CHK003 [Scope] Out-of-Scope: Không sử dụng Oracle bên ngoài (Chainlink) mà lấy trực tiếp từ tỷ lệ dự trữ AMM spot price nội bộ.

## 3. Clarity & Testability (EARS)
- [x] CHK004 [Clarity] Cú pháp EARS định nghĩa rõ các trường hợp Ubiquitous, Event-driven và Unwanted.
- [x] CHK005 [Clarity] Số liệu ví dụ tính tay được ghi chính xác tới 4 chữ số thập phân, không có sự mập mờ.
- [x] CHK006 [Testability] Có kịch bản kiểm thử riêng biệt cho 3 trường hợp: $HF > 1$ (an toàn), $HF < 1$ (thanh lý), và $\text{debt} = 0$ ($HF = \infty$).

## 4. Consistency & Architecture
- [x] CHK007 [Consistency] Sử dụng thống nhất $LT = 0.80$ theo đúng SRS C-03.
- [x] CHK008 [Architecture] Logic tính toán thuần túy (pure functions), không phụ thuộc vào trạng thái toàn cục.

