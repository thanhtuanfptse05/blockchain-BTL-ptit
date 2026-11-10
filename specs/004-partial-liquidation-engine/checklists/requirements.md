# Requirements Quality Review Checklist: Partial Liquidation Engine

**Feature**: `004-partial-liquidation-engine`  
**Reviewer**: SDD Spec Auditor  
**Standard**: Chapter 16.7 (Spec Quality Review) — *Spec-Driven & Agent-Driven Development*  

## 1. Context & Business Value
- [x] CHK001 [Context] Thanh lý từng phần giúp giảm thiểu nợ xấu của giao thức mà không ép bán toàn bộ tài sản trong một lần khi thị trường biến động.

## 2. Completeness & Boundaries
- [x] CHK002 [Completeness] Các công thức tính lượng nợ trả thay (50%), giá trị collateral tịch thu (105%) và nợ xấu được định nghĩa tường minh.
- [x] CHK003 [Scope] Out-of-Scope: Không cho phép Agent thanh lý nhiều lần trong cùng 1 block (giới hạn tối đa 1 lần/block).

## 3. Clarity & Testability (EARS)
- [x] CHK004 [Clarity] Cú pháp EARS định nghĩa rõ quy tắc Ubiquitous, Event-driven và Unwanted.
- [x] CHK005 [Clarity] Schema `LiquidationEvent` đủ 10 trường dữ liệu chi tiết, không thiếu bất kỳ cột nào của SRS §7.3.
- [x] CHK006 [Testability] Tách biệt test case cho trường hợp đủ tài sản và trường hợp thiếu tài sản dẫn đến nợ xấu.

## 4. Consistency & Architecture
- [x] CHK007 [Consistency] Sử dụng `close_factor = 0.50` và `liquidation_penalty = 0.05` nhất quán với config.
- [x] CHK008 [Architecture] Đảm bảo trả về event bất biến (`frozen=True`) và số lượng nợ xấu phát sinh.

