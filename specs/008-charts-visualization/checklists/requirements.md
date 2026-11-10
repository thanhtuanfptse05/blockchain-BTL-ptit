# Requirements Quality Review Checklist: Charts & Visualizations

**Feature**: `008-charts-visualization`  
**Reviewer**: SDD Spec Auditor  
**Standard**: Chapter 16.7 (Spec Quality Review) — *Spec-Driven & Agent-Driven Development*  

## 1. Context & Business Value
- [x] CHK001 [Context] 4 biểu đồ là công cụ trực quan then chốt để chứng minh cơ chế lây lan cascade cho bài báo cáo khoa học BTL.

## 2. Completeness & Boundaries
- [x] CHK002 [Completeness] Đầy đủ 4 biểu đồ bắt buộc theo SRS FR-08, kèm trục X (block 0..max_blocks), trục Y rõ đơn vị, legend phân biệt.
- [x] CHK003 [Scope] Out-of-Scope: Không vẽ số âm cho số lượng sự kiện thanh lý, số Agent hoặc nợ xấu.

## 3. Clarity & Testability (EARS)
- [x] CHK004 [Clarity] Cú pháp EARS định nghĩa rõ quy tắc hiển thị vạch kẻ shock tại block 1.
- [x] CHK005 [Clarity] Bảng màu phân biệt nhất quán: SC01 (Xanh lá/Xanh dương), SC02 (Cam), SC03 (Đỏ).
- [x] CHK006 [Testability] Kiểm tra tự động tính hợp lệ của đối tượng `go.Figure` ngay cả khi số lượng thanh lý = 0.

## 4. Consistency & Architecture
- [x] CHK007 [Consistency] Tiêu đề trục và đơn vị ($ và %) đồng nhất với SRS.
- [x] CHK008 [Architecture] Logic vẽ đồ thị độc lập, nhận vào danh sách `BlockResult`, trả về Figure để UI render.

