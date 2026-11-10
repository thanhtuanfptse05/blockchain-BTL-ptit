# Feature Specification: Bảng Dữ Liệu & Xuất File CSV (Data Tables & CSV Exporter)

**Feature Branch**: `009-data-tables-csv-export`  
**Created**: 2026-11-10  
**Status**: Draft  
**Input**: User description: "Xây dựng màn hình hiển thị bảng dữ liệu (Data Tab) và chức năng xuất file CSV: (1) Bảng và file CSV kết quả theo block (Block Results) gồm cả SC01/SC02/SC03 với 12 cột chuẩn; (2) Bảng và file CSV chi tiết các sự kiện thanh lý (Liquidation Events) với 10 cột chuẩn; encoding UTF-8, đọc lại trơn tru bằng pandas; chỉ hiển thị nút tải khi đã có dữ liệu mô phỏng." (requirements.md §7.3, §7.4, §11 FR-09, §12.2, §14.2 ST-08, §15.1)

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Xem và duyệt bảng dữ liệu chi tiết trên Dashboard (Priority: P1)

Người dùng (giảng viên, người đánh giá) cần xem xét tường tận các con số thô tại từng block và từng vụ thanh lý cụ thể để kiểm tra tính minh bạch và logic của mô hình.

**Why this priority**: Yêu cầu bắt buộc Must Have (FR-09); phục vụ kiểm chứng thực nghiệm thay vì chỉ nhìn biểu đồ khái quát.

**Independent Test**: Kiểm tra hàm render bảng dữ liệu `render_data_tab(simulation_results)`:
- Chuyển đổi danh sách `BlockResult` thành `pandas.DataFrame` gồm đầy đủ 12 cột.
- Chuyển đổi danh sách `LiquidationEvent` thành `pandas.DataFrame` gồm đầy đủ 10 cột.

**Acceptance Scenarios**:

1. **Given** kết quả mô phỏng của 3 kịch bản, **When** chuyển sang Tab "Dữ liệu", **Then**:
   - Hiển thị bảng tương tác (Streamlit dataframe) cho Block Results với đầy đủ 12 cột chuẩn:
     `scenario`, `block`, `eth_price_usd`, `steth_price_usd`, `steth_discount_pct`, `liquidations_eth`, `liquidations_steth`, `liquidations_total`, `liquidated_agents_unique_cumulative`, `liquidation_debt_repaid_usd`, `liquidation_debt_repaid_cumulative_usd`, `bad_debt_usd`.
   - Hiển thị bảng tương tác cho Liquidation Events với 10 cột chuẩn:
     `scenario`, `block`, `agent_id`, `asset`, `hf_before`, `debt_repaid_usd`, `collateral_seized`, `collateral_value_at_oracle_usd`, `remaining_debt_usd`, `remaining_collateral`.
2. **Given** kịch bản SC01 không có thanh lý, **When** lọc bảng Liquidation Events theo SC01, **Then** bảng rỗng (0 dòng) nhưng vẫn giữ nguyên header 10 cột.

---

### User Story 2 - Xuất dữ liệu ra file CSV chuẩn hóa (Priority: P1)

Người dùng cần tải về máy tính 2 file CSV (`block_results.csv` và `liquidation_events.csv`) để làm phụ lục báo cáo nghiên cứu hoặc xử lý phân tích sâu bằng Jupyter Notebook/Python.

**Why this priority**: Cốt lõi của ST-08 (System Test 8) và nhiệm vụ Thành viên 2 (SRS §15.1, §16).

**Independent Test**: Gọi module `src/infra/exporter.py` để xuất 2 chuỗi CSV (hoặc file) và dùng `pd.read_csv()` đọc lại:
- Đọc lại bằng `pandas.read_csv(io.StringIO(csv_text))` thành công 100%.
- Không mất mát dữ liệu, kiểu dữ liệu các cột số đúng chuẩn (`int` hoặc `float`).
- Không bị lỗi encoding font chữ tiếng Việt hay ký tự đặc biệt.

**Acceptance Scenarios**:

1. **Given** mô phỏng đã hoàn tất, **When** người dùng bấm nút tải "Tải Block Results CSV", **Then** trình duyệt tải xuống file CSV chứa toàn bộ dòng của SC01, SC02, SC03; tổng số dòng là $3 \times (\text{max\_blocks} + 1) + 1$ (tính cả dòng header).
2. **Given** mô phỏng có các sự kiện thanh lý trong SC02 và SC03, **When** bấm "Tải Liquidation Events CSV", **Then** tải xuống file CSV chứa tất cả các sự kiện đã ghi nhận theo thứ tự block và agent_id tăng dần.
3. **Given** file CSV vừa tải về, **When** kiểm tra bằng `pandas.read_csv`, **Then** không có cột nào bị đặt tên `Unnamed: 0`, không có dòng trống ở cuối.

---

### Edge Cases & Constraint Handling

- **Chưa chạy mô phỏng**:
  - Không hiển thị nút tải CSV hoặc các nút tải ở trạng thái `disabled`.
  - Hiển thị thông báo: `"Chưa có dữ liệu để xuất. Vui lòng bấm 'Run Simulation' trước."` (FR-09).
- **Mô phỏng 0 thanh lý (Shock = 0)**:
  - File `liquidation_events.csv` vẫn được sinh ra nhưng chỉ có duy nhất 1 dòng tiêu đề (header) 10 cột và 0 dòng dữ liệu, đọc lại bằng `pandas` vẫn trả về DataFrame rỗng hợp lệ với đúng 10 cột.
- **Tính tương thích hệ điều hành (Windows Excel)**:
  - Dữ liệu CSV xuất ra sử dụng encoding `utf-8-sig` (hoặc UTF-8 tiêu chuẩn) để khi người dùng mở trực tiếp bằng Microsoft Excel trên Windows không bị lỗi font ký tự.

---

## Requirements (EARS) *(mandatory)*

### Ubiquitous Requirements
- **FR-09-01 (Cấu trúc cột Block Results CSV)**: Module xuất CSV SHALL tạo file Block Results có chính xác 12 cột theo thứ tự định nghĩa tại SRS §7.4:
  `scenario,block,eth_price_usd,steth_price_usd,steth_discount_pct,liquidations_eth,liquidations_steth,liquidations_total,liquidated_agents_unique_cumulative,liquidation_debt_repaid_usd,liquidation_debt_repaid_cumulative_usd,bad_debt_usd`.
- **FR-09-02 (Cấu trúc cột Liquidation Events CSV)**: Module xuất CSV SHALL tạo file Liquidation Events có chính xác 10 cột theo thứ tự định nghĩa tại SRS §7.3:
  `scenario,block,agent_id,asset,hf_before,debt_repaid_usd,collateral_seized,collateral_value_at_oracle_usd,remaining_debt_usd,remaining_collateral`.
- **FR-09-03 (Chuẩn mã hóa và dấu phân cách)**: File CSV SHALL được xuất theo định dạng chuẩn RFC 4180: phân tách bằng dấu phẩy `,`, dấu chấm thập phân `.`, và mã hóa ký tự UTF-8 (hỗ trợ UTF-8 BOM `utf-8-sig`).

### Event-driven Requirements
- **FR-09-04 (Sinh dữ liệu tải về)**: Khi người dùng nhấp vào nút tải "Download Block Results CSV" hoặc "Download Liquidation Events CSV", hệ thống SHALL tạo nội dung CSV ngay lập tức từ `SimulationResult` hiện thời trong session state mà không cần chạy lại mô phỏng.
- **FR-09-05 (Khả năng đọc lại bằng Pandas)**: Khi file CSV được tải vào bằng thư viện `pandas` (`pd.read_csv`), hệ thống SHALL đảm bảo đọc thành công 100% không văng ngoại lệ `ParserError` hay `EmptyDataError` (ngay cả khi không có sự kiện thanh lý).

### State-driven Requirements
- **FR-09-06 (Khóa tải khi chưa có kết quả)**: Trong khi trạng thái hệ thống là `SIMULATION_NOT_RUN`, hệ thống SHALL KHÔNG cung cấp các nút tải dữ liệu rỗng ra ngoài giao diện (tuân thủ FR-09).
- **FR-09-07 (Tự động cập nhật bảng khi đổi kịch bản)**: Khi người dùng chọn tab hoặc bộ lọc kịch bản trên giao diện, bảng hiển thị SHALL cập nhật dữ liệu tương ứng tức thì.

---

## Technical Specifications & Interfaces

### Exporter Module (`src/infra/exporter.py`)

```python
import io
from typing import List, Dict, Any
import pandas as pd

BLOCK_RESULT_COLUMNS = [
    "scenario",
    "block",
    "eth_price_usd",
    "steth_price_usd",
    "steth_discount_pct",
    "liquidations_eth",
    "liquidations_steth",
    "liquidations_total",
    "liquidated_agents_unique_cumulative",
    "liquidation_debt_repaid_usd",
    "liquidation_debt_repaid_cumulative_usd",
    "bad_debt_usd"
]

LIQUIDATION_EVENT_COLUMNS = [
    "scenario",
    "block",
    "agent_id",
    "asset",
    "hf_before",
    "debt_repaid_usd",
    "collateral_seized",
    "collateral_value_at_oracle_usd",
    "remaining_debt_usd",
    "remaining_collateral"
]

def export_block_results_to_csv(simulation_results: Dict[str, Any]) -> str:
    """Tổng hợp block_results từ cả 3 kịch bản thành chuỗi CSV UTF-8."""
    pass

def export_liquidation_events_to_csv(simulation_results: Dict[str, Any]) -> str:
    """Tổng hợp liquidation_events từ tất cả kịch bản thành chuỗi CSV UTF-8."""
    pass

def block_results_to_dataframe(simulation_results: Dict[str, Any]) -> pd.DataFrame:
    """Chuyển đổi block_results thành pandas DataFrame phục vụ hiển thị trên UI."""
    pass

def liquidation_events_to_dataframe(simulation_results: Dict[str, Any]) -> pd.DataFrame:
    """Chuyển đổi liquidation_events thành pandas DataFrame phục vụ hiển thị trên UI."""
    pass
```

---

## Success Criteria *(mandatory)*

- **SC-01 (ST-08 Passed)**: Test tự động `test_csv_export_compatibility` gọi xuất cả 2 loại CSV từ kết quả chạy mặc định, sau đó dùng `pd.read_csv()` đọc lại:
  - Khớp 100% tên cột và số lượng cột.
  - Số dòng của DataFrame khớp với số bản ghi sinh ra bởi engine.
- **SC-02**: Không có nút tải CSV nào hoạt động khi giao diện ở trạng thái chưa bấm "Run".
- **SC-03**: Tất cả các giá trị số thực trong CSV giữ được độ chính xác toán học cần thiết cho kiểm toán độc lập.

