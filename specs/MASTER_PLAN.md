# Master Implementation Plan: DeFi Liquidation Cascade Simulator

**Project**: DeFi Liquidation Cascade Simulator (Agent-Based Model)  
**Standard**: GitHub Spec Kit / Spec-Driven Development (SDD) Playbook  
**Date**: 2026-11-10  
**Status**: Ready for Tasks Breakdown  
**Related Specs**: [`specs/001-simulation-config/`](file:///d:/wd/c/sang/d/Documents/BTL-block-chain/specs/001-simulation-config/spec.md) through [`specs/010-streamlit-dashboard-ui/`](file:///d:/wd/c/sang/d/Documents/BTL-block-chain/specs/010-streamlit-dashboard-ui/spec.md)  
**Traceability Index**: [`specs/MASTER_SPEC_INDEX.md`](file:///d:/wd/c/sang/d/Documents/BTL-block-chain/specs/MASTER_SPEC_INDEX.md)

---

## 1. Summary

Dự án xây dựng ứng dụng mô phỏng học thuật (Agent-Based Model) nghiên cứu hiện tượng lây lan rủi ro thanh lý chéo (cross-asset liquidation contagion) giữa 2 tài sản ETH và stETH thông qua 2 hồ thanh khoản AMM giả lập (Pool A: ETH/USDC và Pool B: stETH/ETH). Hệ thống chạy hoàn toàn ở môi trường local, không phụ thuộc blockchain testnet/mainnet, và bảo toàn 100% công thức định giá tự động Constant Product $x \cdot y = k$.

Kế hoạch kiến trúc này xác định rõ ranh giới giữa 4 tầng (Domain, Usecase, Infra, Interface), hợp đồng giao tiếp giữa Thành viên 1 (Core Engine Lead) và Thành viên 2 (UI & Data Viz Lead), cùng lộ trình kiểm thử tự động (TDD/Unit tests) đạt 100% độ bao phủ logic nghiệp vụ.

---

## 2. Technical Context

- **Language / Runtime**: Python >= 3.10 (tested with Python 3.14).
- **Domain Modeling & Validation**: Python `@dataclass(frozen=True)` kết hợp Pydantic v2 cho kiểm định chặt chẽ và immutability.
- **Math & Data Processing**: `pandas`, `numpy`, thư viện chuẩn `math`, `random.Random(seed)` tất định.
- **Interactive Visualization**: `plotly.graph_objects` (render charts nhúng trực tiếp trong Streamlit).
- **Frontend / Dashboard**: `streamlit >= 1.30`.
- **Testing Framework**: `pytest >= 8.0` (Unit test + Scenario test).
- **Target Platform**: Windows / macOS / Linux (Local CLI & Web Dashboard).
- **Performance Goals**: Toàn bộ quá trình chạy mô phỏng 3 kịch bản với 100 Agent, 30 block hoàn tất $\le 2$ giây (vượt xa mục tiêu 10s của SRS NFR-01).
- **Constraints**:
  - Không có file mã nguồn nào vượt quá 300 dòng code (Definition of Done §6).
  - Không hardcode bất kỳ chỉ số KPI hoặc kết quả kịch bản nào (§14.3).
  - Tách biệt hoàn toàn tầng logic nghiệp vụ khỏi giao diện `app.py` (NFR-05).

---

## 3. Constitution Check (Tuân Thủ Hiến Pháp Dự Án)

*Cổng kiểm soát: Bắt buộc thỏa mãn 8 nguyên tắc của `CONSTITUTION.md` trước khi phân rã task:*

1. **Spec-First Gate (Bắt buộc Spec trước Code)**: ✅ ĐÃ ĐẠT. Cả 10 bản đặc tả chi tiết đã hoàn thiện, không có dòng code nào được viết vội trước khi qua cổng.
2. **Mathematical Invariance (Bảo toàn toán học AMM)**: ✅ ĐÃ ĐẠT. Pool AMM áp dụng phí 0% (zero-fee swap), bảo toàn tích số $k = x \cdot y$. Cú sốc ngoại sinh tại block 1 tái cân bằng dự trữ giữ nguyên $k_A$.
3. **No Hardcoded Output (Nghiêm cấm gán cứng)**: ✅ ĐÃ ĐẠT. Mọi giá trị KPI, bảng so sánh và dữ liệu biểu đồ đều được trích xuất động từ `SimulationResult`.
4. **Deterministic Reproducibility (Tất định 100%)**: ✅ ĐÃ ĐẠT. Quần thể 100 Agent được sinh bằng instance `random.Random(seed)`. Với cùng một bộ tham số và seed, kết quả mô phỏng luôn trùng khớp 100%.
5. **No Spec-Code Drift (Sửa Spec trước khi sửa Code)**: ✅ ĐÃ ĐẠT. Toàn bộ logic sửa đổi sau này đều phải cập nhật lại tài liệu spec tương ứng trước.
6. **CodeGraph-First Exploration**: ✅ ĐÃ ĐẠT. Mọi thao tác truy vết code đều đi qua CodeGraph MCP và CLI.
7. **Clean Architecture Separation (Phân tách kiến trúc)**: ✅ ĐÃ ĐẠT. `src/domain/` không import usecase; `src/interface/` không chứa logic tính HF hoặc swap AMM.
8. **Definition of Done (Tiêu chuẩn hoàn thành)**: ✅ ĐÃ ĐẠT. Mọi module phải có Unit test tương ứng, type hints đầy đủ, docstring chuẩn Google Style có gắn `# Implements BR-XX`.

---

## 4. Concrete Project Structure

```text
d:\wd c sang d\Documents\BTL-block-chain\
├── specs/                                # 10 bản đặc tả tính năng Spec Kit
│   ├── 001-simulation-config/spec.md
│   ├── 002-borrower-agent-generation/spec.md
│   ├── 003-health-factor-eligibility/spec.md
│   ├── 004-partial-liquidation-engine/spec.md
│   ├── 005-amm-pools/spec.md
│   ├── 006-scenario-block-simulation/spec.md
│   ├── 007-analytics-kpi-summary/spec.md
│   ├── 008-charts-visualization/spec.md
│   ├── 009-data-tables-csv-export/spec.md
│   ├── 010-streamlit-dashboard-ui/spec.md
│   ├── MASTER_SPEC_INDEX.md
│   ├── MASTER_PLAN.md                    # File này
│   └── MASTER_TASKS.md                   # File phân rã công việc tiếp theo
│
├── src/
│   ├── __init__.py
│   ├── domain/                           # Core Data Entities & Immutable Schemas
│   │   ├── __init__.py
│   │   ├── config.py                     # SimulationConfig, validation rules (BR-01, P-01..P-06)
│   │   ├── agent.py                      # BorrowerAgent, AssetType enum
│   │   ├── amm_pool.py                   # AMMPool (x, y, k, spot price, discount)
│   │   ├── liquidation_event.py          # LiquidationEvent (10 fields)
│   │   ├── block_result.py               # BlockResult (12 fields)
│   │   └── simulation_result.py          # KPISummary, SimulationResult
│   │
│   ├── usecase/                          # Business Rules & Simulation Logic
│   │   ├── __init__.py
│   │   ├── agent_generator.py            # generate_borrower_agents(config, seed)
│   │   ├── health_factor.py              # compute_collateral_value, compute_hf, is_liquidatable
│   │   ├── liquidation_engine.py         # execute_partial_liquidation, bad_debt
│   │   ├── amm_engine.py                 # swap_exact_input, apply_exogenous_shock
│   │   └── scenario_runner.py            # run_scenario, run_all_scenarios (Integration API)
│   │
│   ├── infra/                            # Infrastructure & Exporting
│   │   ├── __init__.py
│   │   ├── exporter.py                   # CSV exports (Block Results, Liquidation Events)
│   │   └── logger.py                     # Structured debug logging
│   │
│   └── interface/                        # Presentation Layer (Streamlit Dashboard)
│       ├── __init__.py
│       ├── app.py                        # Streamlit Main App entry point
│       └── components/
│           ├── __init__.py
│           ├── sidebar.py                # Parameter sliders, Run & Reset buttons
│           ├── metrics.py                # 6 KPI cards & delta comparison table
│           ├── charts.py                 # 4 Plotly interactive charts
│           ├── data_tab.py               # Raw tables & CSV download buttons
│           └── methodology_tab.py        # Cascade diagram, formulas, limitations
│
└── tests/                                # Test Suite (Pytest)
    ├── __init__.py
    ├── conftest.py                       # Shared fixtures (default config, mock agents, pools)
    ├── unit/                             # Kiểm thử đơn vị các usecase và domain
    │   ├── test_config.py                # UT-01: Config bounds validation
    │   ├── test_agent_generator.py       # UT-02, UT-03: Population seed & distribution
    │   ├── test_health_factor.py         # UT-04..UT-06: HF calculation & hand-check
    │   ├── test_liquidation_engine.py    # UT-07, UT-08: Close factor, penalty, bad debt
    │   ├── test_amm_engine.py            # UT-09, UT-12, UT-13: Swap x*y=k, shock rebalance
    │   ├── test_scenario_runner.py       # UT-10, UT-11, UT-14: SC01/02/03 runner & deepcopy
    │   ├── test_metrics.py               # Test KPI calculation & div-by-zero protection
    │   ├── test_charts.py                # Test Plotly Figure generation
    │   └── test_exporter.py              # ST-08: CSV export & Pandas round-trip
    └── system/                           # Kiểm thử tích hợp toàn diện hệ thống
        └── test_system_scenarios.py      # ST-01..ST-07: Scenario invariants & contagion proof
```

---

## 5. Architectural Contracts & Interfaces

### 5.1. Integration Contract giữa Thành viên 1 và Thành viên 2 (SRS §15.1)

Điểm kết nối duy nhất giữa Core Simulator Engine và Giao diện Dashboard là hàm:

```python
def run_all_scenarios(config: SimulationConfig) -> Dict[str, SimulationResult]:
    """
    Chạy song song hoặc tuần tự cả 3 kịch bản SC01, SC02, SC03
    từ một bản sao độc lập của trạng thái ban đầu.
    
    Returns:
        dict gồm 3 khóa "SC01", "SC02", "SC03", mỗi giá trị là một SimulationResult.
    """
```

Cấu trúc đối tượng `SimulationResult`:
```python
@dataclass(frozen=True)
class SimulationResult:
    scenario_id: str                      # "SC01", "SC02", hoặc "SC03"
    config: SimulationConfig              # Cấu hình đầu vào đã chạy
    block_results: List[BlockResult]      # Đúng max_blocks + 1 phần tử (từ block 0 đến max_blocks)
    liquidation_events: List[LiquidationEvent]  # Toàn bộ sự kiện thanh lý đã xảy ra
    summary: KPISummary                   # Tóm tắt 6 chỉ số cuối cùng
```

---

## 6. Implementation Phasing & Work Breakdown

- **Phase 1: Foundation & Domain Entities** (Specs 001, 002, 003, 005)
  - Khởi tạo models domain: `SimulationConfig`, `BorrowerAgent`, `AMMPool`.
  - Viết bộ kiểm thử xác thực cấu hình (`test_config.py`).
  - Viết module sinh Agent tất định (`agent_generator.py`) và test phân phối (`test_agent_generator.py`).
- **Phase 2: Core Business Engines** (Specs 003, 004, 005)
  - Hoàn thiện module tính Health Factor (`health_factor.py`) và test đối chiếu tay (`test_health_factor.py`).
  - Hoàn thiện AMM Engine (`amm_engine.py`) cho swap 0-fee và shock tái cân bằng bảo toàn $k$.
  - Hoàn thiện Liquidation Engine (`liquidation_engine.py`) thực thi thanh lý 50% nợ và bonus 5%.
- **Phase 3: Scenario Simulation Loop** (Spec 006)
  - Xây dựng `scenario_runner.py` điều phối SC01, SC02, SC03.
  - Xử lý deepcopy state ban đầu, ghi nhận `BlockResult` 12 cột và `LiquidationEvent` 10 cột.
  - Viết test hệ thống ST-01..ST-07 kiểm chứng tính ổn định của SC01, tính cố định giá của SC02, và vòng lặp cascade của SC03.
- **Phase 4: Analytics & Exporter** (Specs 007, 009)
  - Xây dựng module trích xuất KPI và tính toán delta so sánh (`metrics.py`).
  - Xây dựng module xuất CSV (`exporter.py`) và kiểm thử đọc lại bằng Pandas (ST-08).
- **Phase 5: Visualizations & Streamlit Dashboard** (Specs 008, 010)
  - Xây dựng 4 biểu đồ Plotly (`charts.py`).
  - Xây dựng các components Streamlit (`sidebar.py`, `data_tab.py`, `methodology_tab.py`).
  - Ghép nối vào `app.py` và kiểm thử End-to-End trên trình duyệt.
- **Phase 6: Verification, Audit & Delivery**
  - Chạy linter, format code chuẩn PEP 8.
  - Chạy toàn bộ test suite Pytest (yêu cầu 100% pass).
  - Chuẩn bị tài liệu README, hướng dẫn chạy và ảnh chụp demo báo cáo.

