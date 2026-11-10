# Feature Specification: Hệ Thống Biểu Đồ Trực Quan Hóa (Charts & Visualizations)

**Feature Branch**: `008-charts-visualization`  
**Created**: 2026-11-10  
**Status**: Draft  
**Input**: User description: "Xây dựng 4 biểu đồ cốt lõi theo block: (1) Đường giá ETH SC01/SC02/SC03; (2) Tỉ lệ depeg/discount stETH; (3) Biểu đồ cột thanh lý theo asset (ETH vs stETH) ở SC03; (4) Đường số Agent bị thanh lý lũy kế so sánh SC02 vs SC03; có trục X là block (0..max_blocks), trục Y có đơn vị rõ ràng, có legend và chú thích shock tại block 1; dùng Plotly tương tác." (requirements.md §11 FR-08, §12.2, §14.4, NFR-06, NFR-07)

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Biểu đồ so sánh giá ETH qua 3 kịch bản (Priority: P1)

Người dùng cần quan sát quỹ đạo giá ETH từ block 0 đến block cuối cùng trên cả 3 kịch bản (SC01: đi ngang $3,000; SC02: tụt xuống sau shock tại block 1 rồi đi ngang $2,550; SC03: tụt do shock tại block 1 rồi tiếp tục dốc xuống do áp lực bán tháo collateral từ các đợt thanh lý).

**Why this priority**: Minh chứng trực quan quan trọng nhất cho thấy vòng lặp phản hồi giảm giá (price feedback loop) trong SC03.

**Independent Test**: Truyền 3 danh sách `BlockResult` vào hàm `create_eth_price_chart(results_sc01, results_sc02, results_sc03)` và kiểm tra đối tượng Plotly Figure:
- Có đúng 3 trace tương ứng với SC01, SC02, SC03.
- Có đường kẻ dọc (vertical dashed line) hoặc annotation tại `x = 1` ghi nhận sự kiện "Shock block 1".
- Trục X chạy từ 0 đến `max_blocks`.
- Trục Y có tiêu đề "ETH Price (USD)".

**Acceptance Scenarios**:

1. **Given** 3 kịch bản chạy hoàn tất với 30 block, **When** tạo biểu đồ ETH Price, **Then** figure chứa:
   - Trace SC01: Đường thẳng nằm ngang giá trị $3,000.
   - Trace SC02: Giá trị $3,000 tại block 0, sau đó chuyển thành $2,550 tại block 1 và giữ phẳng đến block 30.
   - Trace SC03: Bắt đầu từ $3,000, block 1 rơi xuống $\le 2,550$ và các block có thanh lý tiếp tục giảm dần.
2. **Given** dữ liệu có shock tại block 1, **When** render biểu đồ, **Then** hiển thị vạch kẻ đứng ngắt nét màu xám tại block 1 kèm chú thích "⚡ Price Shock (-15%)".

---

### User Story 2 - Biểu đồ Discount stETH (Depeg Dynamics) (Priority: P1)

Người dùng cần theo dõi mức độ mất peg của stETH qua từng block để thấy tác động của việc liquidator bán tháo stETH sang Pool B (stETH/ETH).

**Why this priority**: Minh chứng cho hiện tượng lây lan chéo tài sản (cross-asset contagion): thanh lý vị thế stETH làm giảm giá stETH/ETH, kéo theo giá trị USD của stETH của các Agent khác giảm sâu hơn.

**Independent Test**: Gọi hàm `create_steth_discount_chart(results_sc01, results_sc02, results_sc03)` và kiểm tra trace.

**Acceptance Scenarios**:

1. **Given** 3 kịch bản, **When** tạo biểu đồ Discount stETH, **Then**:
   - Trục Y có đơn vị là `%` ("stETH Discount vs ETH (%)").
   - Trace SC01 và SC02 duy trì discount ban đầu 1.00% qua mọi block.
   - Trace SC03 tăng vọt vượt 1.00% tại những block có sự kiện thanh lý vị thế thế chấp bằng stETH.
   - Trục X biểu diễn các block từ 0 đến `max_blocks`.

---

### User Story 3 - Biểu đồ cột thanh lý phân loại theo tài sản trong SC03 (Priority: P1)

Người dùng cần quan sát cường độ thanh lý qua từng block trong SC03, phân biệt rõ bao nhiêu vụ thanh lý là tài sản ETH và bao nhiêu vụ là tài sản stETH.

**Why this priority**: Giúp nhận diện đỉnh điểm thanh lý (liquidation wave/cascade peak) thường dồn dập ở các block đầu (block 1, block 2) sau shock.

**Independent Test**: Gọi hàm `create_liquidation_bar_chart(results_sc03)` và kiểm tra cấu trúc cột.

**Acceptance Scenarios**:

1. **Given** kết quả `BlockResult` của SC03, **When** tạo biểu đồ cột thanh lý, **Then**:
   - Biểu đồ dạng Bar Chart (cột nhóm hoặc cột chồng - stacked bar).
   - Trace 1: `liquidations_eth` (Màu đại diện: Xanh dương nhạt).
   - Trace 2: `liquidations_steth` (Màu đại diện: Tím / Cam).
   - Trục Y: "Số sự kiện thanh lý (Events)", chỉ nhận giá trị nguyên $\ge 0$.
   - Trục X: Block index (0..max_blocks).
2. **Given** một block không có vụ thanh lý nào, **When** vẽ cột, **Then** cột tại block đó có chiều cao bằng 0, không bị crash hoặc vẽ số âm.

---

### User Story 4 - Biểu đồ số Agent bị thanh lý lũy kế SC02 vs SC03 (Priority: P1)

Người dùng cần so sánh tốc độ gia tăng số lượng Borrower duy nhất rơi vào cảnh thanh lý giữa mô hình tĩnh (SC02) và mô hình cascade (SC03).

**Why this priority**: Bằng chứng định lượng về số lượng người vay bị "oan" (thêm vào danh sách thanh lý) do chính tác động giảm giá thứ cấp gây ra.

**Independent Test**: Gọi `create_cumulative_liquidated_agents_chart(results_sc02, results_sc03)` và kiểm tra trace.

**Acceptance Scenarios**:

1. **Given** kết quả SC02 và SC03, **When** tạo biểu đồ lũy kế, **Then**:
   - Vẽ 2 đường: SC02 (Direct Shock) và SC03 (Contagion Cascade).
   - Giá trị trục Y là `liquidated_agents_unique_cumulative` (nguyên, đơn vị "Số Agent duy nhất").
   - Đường SC02 đạt đỉnh ngay tại block 1 (hoặc sớm dừng lại) vì giá không đổi.
   - Đường SC03 tiếp tục tăng bậc thang (step/line) qua các block tiếp theo nếu vòng xoáy thanh lý tiếp diễn.
   - Không bao giờ có giá trị âm.

---

### Edge Cases & Visual Quality Standards

- **Tất cả các kịch bản đều 0 thanh lý (Shock = 0%)**:
  - Các đường biểu đồ giá phẳng hoàn toàn ở mức ban đầu.
  - Biểu đồ cột thanh lý phẳng ở 0.
  - Biểu đồ lũy kế nằm ngang ở 0.
  - Biểu đồ không bị co cụm trục Y (phải set range trục Y hợp lý hoặc auto-margin của Plotly).
- **Trục X không rời rạc lộn xộn**: Trục X chỉ hiển thị số nguyên đại diện cho Block (0, 1, 2, ..., N), không hiển thị số thập phân như `1.5`, `2.3`.
- **Legend & Tooltip**: Mọi biểu đồ đều có hover tooltip hiển thị rõ giá trị chính xác và tên kịch bản khi rê chuột vào điểm dữ liệu.

---

## Requirements (EARS) *(mandatory)*

### Ubiquitous Requirements
- **FR-08-01 (Phạm vi 4 biểu đồ)**: Hệ thống SHALL cung cấp tối thiểu 4 biểu đồ phân tích độc lập:
  1. `ETH Price vs Block` (3 đường: SC01, SC02, SC03).
  2. `stETH Discount vs Block` (3 đường: SC01, SC02, SC03).
  3. `Liquidations per Block by Asset` (Cột chồng/nhóm cho SC03: ETH vs stETH).
  4. `Cumulative Unique Liquidated Agents` (2 đường: SC02 vs SC03).
- **FR-08-02 (Chuẩn mực đồ họa & Legend)**:
  - Tất cả biểu đồ SHALL có tiêu đề biểu đồ (Title), nhãn trục hoành (X-axis title = "Block"), nhãn trục tung (Y-axis title kèm đơn vị như `USD`, `%`, `Events`, `Agents`), và chú thích phân biệt (Legend) rõ ràng.
  - Trục X SHALL hiển thị các giá trị nguyên từ `0` đến `max_blocks`.
  - Không có biểu đồ nào SHALL vẽ giá trị âm cho số lượng thanh lý, số Agent hoặc nợ xấu.

### Event-driven Requirements
- **FR-08-03 (Vạch đánh dấu Cú sốc)**: Khi tạo biểu đồ giá (`ETH Price`) hoặc biểu đồ discount (`stETH Discount`), hệ thống SHALL vẽ một vạch đứng ngắt nét (dashed vertical line) tại tọa độ `x = 1` kèm chú thích chữ "Cú sốc giá (Block 1)" để người xem nhận biết thời điểm ngoại sinh tác động.
- **FR-08-04 (Tương tác Plotly)**: Khi người dùng tương tác với biểu đồ trong Streamlit, hệ thống SHALL hỗ trợ tooltip hover, zoom/pan và tải ảnh biểu đồ dạng PNG thông qua thanh công cụ tiêu chuẩn của Plotly.

### State-driven Requirements
- **FR-08-05 (Trạng thái dữ liệu trống)**: Trong khi mô phỏng chưa chạy hoặc `BlockResult` rỗng, hệ thống SHALL hiển thị placeholder thông báo thay vì gọi lệnh render đồ thị gây lỗi ngoại lệ.
- **FR-08-06 (Bảo toàn màu sắc nhận diện kịch bản)**: Trên toàn bộ các biểu đồ, hệ thống SHALL giữ nhất quán bảng màu:
  - SC01 (Baseline): Màu Xanh lá cây (Green) hoặc Xanh dương (Blue) biểu trưng cho sự ổn định.
  - SC02 (Direct Shock): Màu Cam (Orange) biểu trưng cho cú sốc ngoại sinh không lây lan.
  - SC03 (Cascade Contagion): Màu Đỏ (Red/Crimson) biểu trưng cho rủi ro lây lan sụp đổ.

---

## Component Interfaces

```python
# src/interface/components/charts.py
import plotly.graph_objects as go
from typing import List, Dict, Any

def create_eth_price_chart(
    sc01_blocks: List[Dict[str, Any]],
    sc02_blocks: List[Dict[str, Any]],
    sc03_blocks: List[Dict[str, Any]]
) -> go.Figure:
    """Tạo biểu đồ so sánh đường giá ETH của 3 kịch bản theo block."""
    pass

def create_steth_discount_chart(
    sc01_blocks: List[Dict[str, Any]],
    sc02_blocks: List[Dict[str, Any]],
    sc03_blocks: List[Dict[str, Any]]
) -> go.Figure:
    """Tạo biểu đồ biến động tỉ lệ discount/depeg của stETH theo block."""
    pass

def create_liquidation_breakdown_chart(
    sc03_blocks: List[Dict[str, Any]]
) -> go.Figure:
    """Tạo biểu đồ cột phân bổ thanh lý ETH vs stETH trong SC03 theo block."""
    pass

def create_cumulative_liquidated_agents_chart(
    sc02_blocks: List[Dict[str, Any]],
    sc03_blocks: List[Dict[str, Any]]
) -> go.Figure:
    """Tạo biểu đồ đường so sánh số lượng Borrower duy nhất bị thanh lý lũy kế."""
    pass
```

---

## Success Criteria *(mandatory)*

- **SC-01**: Cả 4 hàm tạo biểu đồ đều có Unit Test kiểm tra tính hợp lệ của đối tượng `go.Figure` trả về (không văng exception với các tập dữ liệu biên: 0 event, max block = 1, shock = 0).
- **SC-02**: Vạch chú thích shock tại block 1 xuất hiện chính xác trên biểu đồ giá và discount.
- **SC-03**: Trục X và Y được định dạng đẹp mắt, không hiển thị số âm cho các đại lượng số học dương, trục X không chia số lẻ thập phân.

