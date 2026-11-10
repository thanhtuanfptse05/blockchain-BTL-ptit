# Implementation Plan: Borrower Agent Generation

**Feature**: `002-borrower-agent-generation`  
**Date**: 2026-11-10  
**Spec**: [`specs/002-borrower-agent-generation/spec.md`](file:///d:/wd/c/sang/d/Documents/BTL-block-chain/specs/002-borrower-agent-generation/spec.md)  
**Status**: Ready for Implementation  

## 1. Summary

Xây dựng entity `BorrowerAgent` tại `src/domain/agent.py` và usecase `generate_borrower_agents` tại `src/usecase/agent_generator.py` để sinh quần thể vị thế người vay tất định 100% dựa trên `seed`.

## 2. Technical Context

- **Target Files**:
  - `src/domain/agent.py` (Entity `BorrowerAgent`, Enum `AssetType`)
  - `src/usecase/agent_generator.py` (Generator logic)
- **Test File**: `tests/unit/test_agent_generator.py`
- **Algorithm**: Deterministic Pseudo-Random Generation qua `random.Random(seed)`

## 3. Architecture & Interfaces

```python
from enum import Enum
from dataclasses import dataclass
from typing import List
from src.domain.config import SimulationConfig

class AssetType(str, Enum):
    ETH = "ETH"
    STETH = "stETH"

@dataclass
class BorrowerAgent:
    agent_id: int
    asset: AssetType
    collateral_amount: float
    debt_usdc: float
    initial_ltv: float
    initial_collateral_usd: float
    is_liquidated: bool = False

def generate_borrower_agents(config: SimulationConfig) -> List[BorrowerAgent]:
    """Sinh danh sách BorrowerAgent tất định."""
    pass
```

## 4. Verification & Constraints

- Hai lần gọi với cùng config và seed phải trả về danh sách Agent giống hệt nhau từng bit (reproducibility guarantee).

