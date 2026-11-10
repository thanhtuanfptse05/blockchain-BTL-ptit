# Research & Technical Decisions: Data Tables & CSV Exporter

**Feature**: `009-data-tables-csv-export`  
**Date**: 2026-11-10  
**Status**: Completed  

## 1. Technical Context & CSV Formatting Research

- **Encoding**: Sử dụng `utf-8-sig` (UTF-8 có BOM) để đảm bảo khi mở file CSV trực tiếp bằng Microsoft Excel trên Windows, toàn bộ tiêu đề cột tiếng Việt và ký tự đặc biệt không bị vỡ font (mojibake).
- **Delimiter**: Dấu phẩy chuẩn `,` theo RFC 4180; dấu chấm thập phân `.`.
- **Cấu trúc 12 cột Block Results CSV (SRS §7.4)**:
  `scenario,block,eth_price_usd,steth_price_usd,steth_discount_pct,liquidations_eth,liquidations_steth,liquidations_total,liquidated_agents_unique_cumulative,liquidation_debt_repaid_usd,liquidation_debt_repaid_cumulative_usd,bad_debt_usd`
- **Cấu trúc 10 cột Liquidation Events CSV (SRS §7.3)**:
  `scenario,block,agent_id,asset,hf_before,debt_repaid_usd,collateral_seized,collateral_value_at_oracle_usd,remaining_debt_usd,remaining_collateral`

## 2. Pandas Compatibility Research (ST-08)

- File CSV xuất ra phải đảm bảo khi chạy `pd.read_csv(...)` thành công ngay lập tức:
  - Kiểu dữ liệu nhận diện tự động đúng (`scenario` dạng chuỗi, `block` dạng số nguyên, giá và nợ dạng số thực float).
  - Không sinh ra cột rác kiểu `Unnamed: 0` (không lưu index của DataFrame).
  - Khi không có sự kiện thanh lý, file vẫn có header 10 cột và đọc vào thành DataFrame rỗng hợp lệ với đúng 10 cột.

