"""Sidebar Component for Streamlit Dashboard.

Matches the clean academic demo UI layout:
- Tham số thí nghiệm (Shock %, Pool A TVL, Pool B TVL, Display block scrubber)
- Run / Reset controls and presets
- Fixed parameters note at the bottom.

# Implements FR-10-04, FR-10-05, FR-10-06, NFR-06, SRS §5.1, §12.1
"""

from typing import Tuple
import streamlit as st
from src.domain.config import SimulationConfig

DEFAULT_SHOCK_PCT = 15.0
DEFAULT_POOL_A_TVL = 150_000_000.0
DEFAULT_POOL_B_TVL = 80_000_000.0
DEFAULT_NUM_BORROWERS = 100
DEFAULT_MAX_BLOCKS = 30
DEFAULT_SEED = 42


def render_sidebar() -> Tuple[bool, SimulationConfig]:
    """Render sidebar parameter widgets and control buttons matching the demo UI.

    # Implements FR-10-04, FR-10-05, FR-10-06, NFR-06

    Returns:
        Tuple of (run_clicked: bool, config: SimulationConfig).
    """
    st.sidebar.markdown(
        """
        <div class="sidebar-title">Tham số thí nghiệm</div>
        """,
        unsafe_allow_html=True,
    )

    # Initialize session state with defaults
    if "param_shock_pct" not in st.session_state:
        st.session_state["param_shock_pct"] = DEFAULT_SHOCK_PCT
    if "param_pool_a_tvl" not in st.session_state:
        st.session_state["param_pool_a_tvl"] = DEFAULT_POOL_A_TVL
    if "param_pool_b_tvl" not in st.session_state:
        st.session_state["param_pool_b_tvl"] = DEFAULT_POOL_B_TVL
    if "param_num_borrowers" not in st.session_state:
        st.session_state["param_num_borrowers"] = DEFAULT_NUM_BORROWERS
    if "param_max_blocks" not in st.session_state:
        st.session_state["param_max_blocks"] = DEFAULT_MAX_BLOCKS
    if "param_seed" not in st.session_state:
        st.session_state["param_seed"] = DEFAULT_SEED
    if "display_block" not in st.session_state:
        st.session_state["display_block"] = DEFAULT_MAX_BLOCKS

    # Action Buttons
    col_run, col_reset = st.sidebar.columns([1.3, 1])
    with col_run:
        run_top = st.button("Chạy lại", type="primary", use_container_width=True, key="btn_run_top")
    with col_reset:
        if st.button("Mặc định", use_container_width=True, key="btn_reset_top"):
            st.session_state["param_shock_pct"] = DEFAULT_SHOCK_PCT
            st.session_state["param_pool_a_tvl"] = DEFAULT_POOL_A_TVL
            st.session_state["param_pool_b_tvl"] = DEFAULT_POOL_B_TVL
            st.session_state["param_num_borrowers"] = DEFAULT_NUM_BORROWERS
            st.session_state["param_max_blocks"] = DEFAULT_MAX_BLOCKS
            st.session_state["param_seed"] = DEFAULT_SEED
            st.session_state["display_block"] = DEFAULT_MAX_BLOCKS
            st.rerun()

    # Preset Scenarios
    col_p1, col_p2 = st.sidebar.columns(2)
    with col_p1:
        if st.button("Căng thẳng cao", use_container_width=True, key="preset_crisis", help="Shock 30%, Pool hẹp"):
            st.session_state["param_shock_pct"] = 30.0
            st.session_state["param_pool_a_tvl"] = 80_000_000.0
            st.session_state["param_pool_b_tvl"] = 30_000_000.0
            st.rerun()
    with col_p2:
        if st.button("Thanh khoản sâu", use_container_width=True, key="preset_resilient", help="Shock 5%, Pool dày"):
            st.session_state["param_shock_pct"] = 5.0
            st.session_state["param_pool_a_tvl"] = 300_000_000.0
            st.session_state["param_pool_b_tvl"] = 150_000_000.0
            st.rerun()

    st.sidebar.markdown("<div style='margin-top:0.75rem;'></div>", unsafe_allow_html=True)

    # 1. Shock % Slider
    shock_pct = st.sidebar.slider(
        label="Cú sốc giảm giá ETH (%)",
        min_value=0,
        max_value=50,
        value=int(round(float(st.session_state["param_shock_pct"]))),
        step=1,
        help="Mức giảm giá ETH ngoại sinh xảy ra tại Block 1.",
        key="slider_shock_pct",
    )
    st.session_state["param_shock_pct"] = float(shock_pct)

    # 2. Pool A TVL Slider
    curr_a_m = int(round(float(st.session_state["param_pool_a_tvl"]) / 1e6))
    pool_a_m = st.sidebar.slider(
        label="Độ sâu Pool A ETH/USDC (triệu USD)",
        min_value=10,
        max_value=500,
        value=curr_a_m,
        step=5,
        help="Độ sâu thanh khoản của AMM Pool A (ETH/USDC).",
        key="slider_pool_a_tvl",
    )
    st.session_state["param_pool_a_tvl"] = float(pool_a_m * 1e6)

    # 3. Pool B TVL Slider
    curr_b_m = int(round(float(st.session_state["param_pool_b_tvl"]) / 1e6))
    pool_b_m = st.sidebar.slider(
        label="Độ sâu Pool B stETH/ETH (triệu USD mỗi phía)",
        min_value=5,
        max_value=200,
        value=curr_b_m,
        step=5,
        help="Độ sâu thanh khoản của AMM Pool B (stETH/ETH).",
        key="slider_pool_b_tvl",
    )
    st.session_state["param_pool_b_tvl"] = float(pool_b_m * 1e6)

    # 4. Display Block Scrubber Slider (Matching Demo Image 1)
    max_blocks_val = int(st.session_state["param_max_blocks"])
    curr_disp = min(int(st.session_state.get("display_block", max_blocks_val)), max_blocks_val)
    display_block = st.sidebar.slider(
        label="Hiển thị đến block",
        min_value=1,
        max_value=max_blocks_val,
        value=curr_disp,
        step=1,
        help="Tua nhanh hoặc lọc biểu đồ hiển thị đến block chỉ định.",
        key="slider_display_block",
    )
    st.session_state["display_block"] = display_block

    # Advanced Settings in Expander
    with st.sidebar.expander("Tùy chọn nâng cao (Borrowers, Blocks, Seed)"):
        num_borrowers = st.slider(
            label="Số lượng người vay (Borrowers)",
            min_value=10,
            max_value=500,
            value=int(st.session_state["param_num_borrowers"]),
            step=10,
            key="slider_num_borrowers",
        )
        st.session_state["param_num_borrowers"] = num_borrowers

        max_blocks = st.slider(
            label="Số block mô phỏng",
            min_value=5,
            max_value=100,
            value=max_blocks_val,
            step=5,
            key="slider_max_blocks",
        )
        st.session_state["param_max_blocks"] = max_blocks

        seed = st.number_input(
            label="Hạt giống ngẫu nhiên (Seed)",
            min_value=0,
            max_value=2_147_483_647,
            value=int(st.session_state["param_seed"]),
            step=1,
            key="input_seed",
        )
        st.session_state["param_seed"] = seed

    # Fixed Parameters Note at the bottom (Exact match with Demo screenshot)
    st.sidebar.markdown(
        """
        <div class="sidebar-fixed-note">
            <strong>Cố định:</strong> 50 Borrower ETH + 50 Borrower stETH, LTV 55% đến 72%, LT 80%, bonus 5%, close factor 50%, discount ban đầu 1%.
        </div>
        """,
        unsafe_allow_html=True,
    )

    config = SimulationConfig(
        shock_pct=float(shock_pct),
        pool_a_tvl_usd=float(pool_a_m * 1e6),
        pool_b_tvl_usd=float(pool_b_m * 1e6),
        num_borrowers=num_borrowers,
        max_blocks=max_blocks,
        seed=seed,
    )

    return run_top, config
