# Feature Specification: Dashboard Thống Kê & Bảng So Sánh Chỉ Số (KPIs & Summary Analytics)

**Feature Branch**: `007-analytics-kpi-summary`  
**Created**: 2026-11-10  
**Status**: Draft  
**Input**: User description: "Tính toán và tổng hợp 6 chỉ số KPI cốt lõi cho kịch bản SC03 (Giá ETH cuối, Giá stETH cuối, Discount stETH cuối, Số Agent bị thanh lý duy nhất, Tổng số event thanh lý, Nợ xấu cuối), cùng bảng so sánh đối chứng delta giữa SC03 và SC02; xử lý an toàn phép chia cho 0; lấy dữ liệu động từ SimulationResult, tuyệt đối không hardcode." (requirements.md §7.5, §11 FR-07, FR-11, §12.2, §14.3, NFR-06, NFR-07)

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Hiển thị 6 thẻ KPI cốt lõi cho SC03 (Priority: P1)

Người dùng (giảng viên, sinh viên) sau khi bấm "Run Simulation" cần nhìn thấy ngay trên đầu màn hình kết quả tổng thể của kịch bản lây lan (SC03) qua 6 thẻ metric chuẩn mực, có đơn vị rõ ràng.

**Why this priority**: Yêu cầu bắt buộc Must Have (FR-07) và là bằng chứng đánh giá tác động thanh lý chéo.

**Independent Test**: Gọi hàm tính KPI summary `calculate_kpi_summary(sim_result_sc03, total_agents)` với dữ liệu `SimulationResult` độc lập, kiểm tra 6 giá trị trả về khớp 100% với dòng cuối cùng của `block_results` và aggregation từ `liquidation_events`.

**Acceptance Scenarios**:

1. **Given** một `SimulationResult` của SC03 hợp lệ, **When** hệ thống trích xuất KPI, **Then** hệ thống trả về chính xác:
   - `final_eth_price_usd`: Số thực float, định dạng tiền tệ USD (ví dụ: `$2,412.35`).
   - `final_steth_price_usd`: Số thực float, định dạng tiền tệ USD (ví dụ: `$2,364.10`).
   - `final_steth_discount_pct`: Số thực float, định dạng phần trăm (ví dụ: `2.00%`).
   - `liquidated_agents_unique`: Số nguyên và tỉ lệ trên tổng số Agent (ví dụ: `38 / 100 (38.0%)`).
   - `liquidation_events_total`: Số nguyên tổng các sự kiện thanh lý (ví dụ: `52`).
   - `bad_debt_usd`: Số thực float, định dạng USD (ví dụ: `$0.00`).
2. **Given** mô phỏng SC03 không có bất kỳ vụ thanh lý nào, **When** trích xuất KPI, **Then** `liquidated_agents_unique = 0`, `liquidation_events_total = 0`, `bad_debt_usd = 0.0`.

---

### User Story 2 - So sánh đối chứng SC03 vs SC02 (Delta Analytics) (Priority: P2)

Người dùng muốn xem hiệu ứng khuếch đại (contagion effect) do cơ chế AMM feedback gây ra bằng cách so sánh trực diện kết quả giữa SC03 và SC02 (FR-11).

**Why this priority**: Yêu cầu Should Have (FR-11) làm sáng tỏ sự khác biệt giữa mô hình thanh lý tĩnh (SC02) và mô hình thanh lý động kèm trượt giá AMM (SC03).

**Independent Test**: Gọi hàm `compare_scenarios(sc02_result, sc03_result)` và đối chiếu hiệu số $\Delta = SC03 - SC02$.

**Acceptance Scenarios**:

1. **Given** kết quả của SC02 và SC03, **When** hệ thống tính toán bảng so sánh, **Then** trả về các trường delta:
   - $\Delta \text{ETH Price} = \text{ETH}_{SC03} - \text{ETH}_{SC02}$ (thường $\le 0$).
   - $\Delta \text{stETH Price} = \text{stETH}_{SC03} - \text{stETH}_{SC02}$ (thường $\le 0$).
   - $\Delta \text{Discount} = \text{Discount}_{SC03} - \text{Discount}_{SC02}$ (thường $\ge 0$).
   - `additional_liquidated_agents` $= \text{Unique}_{SC03} - \text{Unique}_{SC02}$.
   - $\Delta \text{Liquidation Events} = \text{Events}_{SC03} - \text{Events}_{SC02}$.
   - $\Delta \text{Bad Debt} = \text{BadDebt}_{SC03} - \text{BadDebt}_{SC02}$.
2. **Given** `unique_SC02 > 0`, **When** tính tỉ lệ tăng tương đối `relative_increase_pct`, **Then** công thức là `((unique_SC03 - unique_SC02) / unique_SC02) * 100.0`.
3. **Given** `unique_SC02 == 0` và `unique_SC03 > 0`, **When** tính tỉ lệ tăng tương đối, **Then** hệ thống trả về giá trị đặc biệt `None` (hoặc hiển thị `"N/A"`), KHÔNG ĐƯỢC sinh lỗi chia cho 0 (`ZeroDivisionError`).
4. **Given** `unique_SC02 == 0` và `unique_SC03 == 0`, **When** tính tỉ lệ tăng tương đối, **Then** hiển thị `"0.0%"`.

---

### Edge Cases & Error Handling

- **Chưa chạy mô phỏng**: Khi ứng dụng vừa khởi động, chưa có `SimulationResult`, khu vực KPI và bảng so sánh hiển thị thông báo hướng dẫn `"Vui lòng bấm 'Run Simulation' ở thanh bên để bắt đầu mô phỏng."` thay vì crash hoặc hiển thị NaN.
- **Giá trị âm bất thường**: `liquidated_agents_unique`, `liquidation_events_total`, `bad_debt_usd` luôn $\ge 0$.
- **Dữ liệu SC03 không khuếch đại (SC03 = SC02)**: Nếu thanh khoản pool rất lớn khiến trượt giá gần như bằng 0, hệ thống hiển thị delta = 0 một cách trung thực, tuyệt đối không gán cứng số liệu để giả vờ có lây lan (tuân thủ BR-10, §14.3).

---

## Requirements (EARS) *(mandatory)*

### Ubiquitous Requirements
- **FR-07-01 (Dữ liệu động)**: Hệ thống SHALL tính toán toàn bộ chỉ số KPI và bảng so sánh trực tiếp từ đối tượng `SimulationResult` trả về bởi `run_all_scenarios`, tuyệt đối KHÔNG chứa bất kỳ giá trị hardcode nào.
- **FR-07-02 (Làm tròn và định dạng chuẩn)**:
  - Giá USD (`final_eth_price_usd`, `final_steth_price_usd`, `bad_debt_usd`) SHALL được định dạng với dấu phẩy ngăn cách hàng nghìn và 2 chữ số thập phân (e.g. `2,412.35`).
  - Tỉ lệ phần trăm (`final_steth_discount_pct`, `relative_increase_pct`) SHALL được định dạng với 2 chữ số thập phân kèm ký hiệu `%` (e.g. `2.15%`).
  - Số lượng đếm (`liquidated_agents_unique`, `liquidation_events_total`) SHALL được định dạng kiểu số nguyên nguyên vẹn (`int`).

### Event-driven Requirements
- **FR-07-03 (Tính toán sau khi chạy xong)**: Khi sự kiện chạy mô phỏng hoàn tất (`run_all_scenarios` trả về thành công), hệ thống SHALL tự động kích hoạt tính toán đối tượng `KPISummary` cho SC03 và `ScenarioComparison` giữa SC02 và SC03.
- **FR-07-04 (Xử lý an toàn mẫu số 0)**: Khi tính toán `relative_increase_pct` mà số Agent bị thanh lý trong SC02 bằng 0 (`unique_SC02 == 0`), hệ thống SHALL gán giá trị hiển thị là `"N/A"` nếu `unique_SC03 > 0`, hoặc `"0.0%"` nếu cả hai bằng 0, ngăn chặn hoàn toàn lỗi `ZeroDivisionError`.

### State-driven Requirements
- **FR-07-05 (Trạng thái chờ khởi tạo)**: Trong khi trạng thái phiên làm việc là `NOT_STARTED` (chưa có kết quả mô phỏng), hệ thống SHALL KHÔNG render các thẻ KPI rỗng hoặc các thông số bị lỗi `NoneType`.
- **FR-07-06 (Trạng thái hiển thị Delta tùy chọn)**: Trong khi hiển thị 6 thẻ KPI của SC03, nếu có sẵn kết quả SC02, hệ thống SHALL hiển thị giá trị delta so với SC02 ở dạng chú thích nhỏ (delta caption/badge) bên dưới giá trị chính (ví dụ: `-$137.65 so với SC02`).

---

## Data Model & Interfaces

### Schema `KPISummary` (Python Dataclass / Pydantic)

```python
from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class KPISummary:
    scenario_id: str
    final_eth_price_usd: float
    final_steth_price_usd: float
    final_steth_discount_pct: float
    liquidated_agents_unique: int
    total_agents: int
    liquidated_agents_ratio_pct: float
    liquidation_events_total: int
    total_debt_repaid_usd: float
    bad_debt_usd: float
    
    # Delta so với SC02 (nếu đây là SC03 và có SC02)
    delta_eth_price_usd: Optional[float] = None
    delta_steth_price_usd: Optional[float] = None
    delta_steth_discount_pct: Optional[float] = None
    delta_liquidated_agents: Optional[int] = None
    delta_liquidation_events: Optional[int] = None
    delta_bad_debt_usd: Optional[float] = None
```

### Schema `ScenarioComparisonTable` (FR-11)

```python
@dataclass(frozen=True)
class ScenarioComparisonRow:
    metric_name: str
    unit: str
    sc01_value: str
    sc02_value: str
    sc03_value: str
    delta_sc03_sc02: str
    relative_change: str  # e.g. "+15.2%" hoặc "N/A"
```

---

## Success Criteria *(mandatory)*

- **SC-01**: Kiểm thử đơn vị (Unit Test) cho module tính KPI pass 100% với các fixture:
  - Trường hợp thông thường: SC03 > SC02 (có khuếch đại thanh lý).
  - Trường hợp shock = 0: SC01 = SC02 = SC03 (không có thanh lý).
  - Trường hợp SC02 = 0 thanh lý, SC03 > 0 thanh lý: `relative_increase` hiển thị `"N/A"`, không crash.
- **SC-02**: Mọi số liệu hiển thị trên các thẻ KPI khớp chính xác tới từng cent/đơn vị với dòng cuối cùng của bảng `BlockResult` tương ứng.
- **SC-03**: Không có bất kỳ giá trị hằng số ngẫu nhiên nào được fix cứng trong code hiển thị KPI.

