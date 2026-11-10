# Implementation Plan: Scenario Simulation & Block Loop

**Feature**: `006-scenario-block-simulation`  
**Date**: 2026-11-10  
**Spec**: [`specs/006-scenario-block-simulation/spec.md`](file:///d:/wd/c/sang/d/Documents/BTL-block-chain/specs/006-scenario-block-simulation/spec.md)  
**Status**: Ready for Implementation  

## 1. Summary

Xây dựng schema `BlockResult`, `SimulationResult` tại `src/domain/` và module `scenario_runner.py` tại `src/usecase/` để cung cấp hàm hợp đồng `run_all_scenarios(config)`, điều phối 3 kịch bản SC01/SC02/SC03 qua vòng lặp block độc lập.

## 2. Technical Context

- **Target Files**:
  - `src/domain/block_result.py` (12 trường chuẩn theo SRS §7.4)
  - `src/domain/simulation_result.py` (Container kết quả theo SRS §7.5)
  - `src/usecase/scenario_runner.py` (Bộ điều phối mô phỏng)
- **Test Files**:
  - `tests/unit/test_scenario_runner.py`
  - `tests/system/test_system_scenarios.py`
- **Dependencies**: `copy.deepcopy`, `src/usecase/agent_generator.py`, `src/usecase/health_factor.py`, `src/usecase/liquidation_engine.py`, `src/usecase/amm_engine.py`

## 3. Architecture & Interfaces

```python
from dataclasses import dataclass
from typing import List, Dict, Any
from src.domain.config import SimulationConfig
from src.domain.block_result import BlockResult
from src.domain.liquidation_event import LiquidationEvent
from src.domain.simulation_result import SimulationResult

def run_scenario(scenario_id: str, config: SimulationConfig) -> SimulationResult:
    """Chạy một kịch bản đơn lẻ từ block 0 đến max_blocks."""
    pass

def run_all_scenarios(config: SimulationConfig) -> Dict[str, SimulationResult]:
    """Hợp đồng tích hợp: Chạy cả 3 kịch bản SC01, SC02, SC03 từ trạng thái ban đầu giống nhau."""
    pass
```

## 4. Risks & Mitigations

- *Rủi ro*: Agent mới bị thanh lý gây sụt giá, làm các Agent khác trong cùng block bị lôi vào thanh lý liên tục vô tận.
- *Giải pháp*: Tuân thủ thuật toán SRS §10: Danh sách ứng viên chốt tại đầu block; Agent nguy hiểm do giá giảm trong block chỉ được xét ở block tiếp theo; mỗi Agent chỉ bị thanh lý tối đa 1 lần trong 1 block.

