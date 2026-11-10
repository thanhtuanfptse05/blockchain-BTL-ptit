"""Main Streamlit Application for DeFi Liquidation Cascade Simulator.

Exact match with the academic demo UI:
- Pure white background, clean coral/crimson & blue accents
- Top title and academic model description
- 6 typographic KPI metrics
- 6 clean tabs: Giá và discount, Thanh lý, Vị thế, Độ nhạy (CAR), Dữ liệu, Cơ chế

# Implements FR-10, FR-10-01..FR-10-07, NFR-06, SRS §11, §12, §13, §14, §15.1
"""

from typing import Dict
import streamlit as st

from src.domain.config import SimulationConfig
from src.domain.simulation_result import SimulationResult
from src.usecase.scenario_runner import run_all_scenarios
from src.interface.theme import apply_theme
from src.interface.components.sidebar import render_sidebar
from src.interface.components.metrics import calculate_kpi_summary, render_kpi_metrics
from src.interface.components.charts import (
    create_eth_price_chart,
    create_steth_price_chart,
    create_steth_discount_chart,
    create_scenario_liquidations_bar_chart,
    create_liquidation_breakdown_chart,
)
from src.interface.components.borrower_tab import render_borrower_tab
from src.interface.components.sensitivity_tab import render_sensitivity_tab
from src.interface.components.data_tab import render_data_tab
from src.interface.components.methodology_tab import render_methodology_tab


def main() -> None:
    """Main Streamlit application entry point."""
    st.set_page_config(
        page_title="Lây lan thanh lý chéo tài sản DeFi",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Apply Demo Light Theme
    apply_theme()

    # Header and Subtitle (Exact match with Demo screenshot)
    st.markdown(
        """
        <div class="demo-header-title">Mô phỏng lây lan thanh lý chéo tài sản trong DeFi Lending</div>
        <div class="demo-header-subtitle">
            Mô hình Agent-Based (Mesa): Oracle, Borrower, Liquidator – hai AMM (ETH/USDC và stETH/ETH). Mọi tham số là giả định minh họa, không phải số liệu thị trường thật.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Render Sidebar and receive user controls (FR-10-04, FR-10-05, FR-10-06)
    run_clicked, config = render_sidebar()

    # Auto-initialize session state with default run on first visit (FR-10-07)
    if "simulation_config" not in st.session_state or st.session_state["simulation_config"] is None:
        st.session_state["simulation_config"] = config
    if "simulation_results" not in st.session_state or st.session_state["simulation_results"] is None:
        with st.spinner("Đang tính toán mô phỏng mặc định..."):
            st.session_state["simulation_results"] = run_all_scenarios(st.session_state["simulation_config"])

    if run_clicked:
        with st.spinner("Đang tính toán mô phỏng 3 kịch bản..."):
            results: Dict[str, SimulationResult] = run_all_scenarios(config)
            st.session_state["simulation_results"] = results
            st.session_state["simulation_config"] = config
        st.toast("Hoàn tất tính toán mô phỏng.")

    results: Dict[str, SimulationResult] = st.session_state["simulation_results"]
    active_config: SimulationConfig = st.session_state["simulation_config"]

    # Slice block results up to display_block scrubber slider
    disp_block = st.session_state.get("display_block", active_config.max_blocks)
    sc01_sliced = [b for b in results["SC01"].block_results if b.block <= disp_block]
    sc02_sliced = [b for b in results["SC02"].block_results if b.block <= disp_block]
    sc03_sliced = [b for b in results["SC03"].block_results if b.block <= disp_block]

    # Top KPI Metrics Row (Exact 6 items from Demo screenshot)
    kpi_summary = calculate_kpi_summary(
        sim_result=results["SC03"],
        total_agents=active_config.num_borrowers,
        ref_sc02=results["SC02"],
    )
    render_kpi_metrics(kpi_summary)

    # 6 Main Tabs (Exact match with Demo screenshot)
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Giá và discount",
        "Thanh lý",
        "Vị thế",
        "Độ nhạy (CAR)",
        "Dữ liệu",
        "Cơ chế",
    ])

    with tab1:
        # 3 Charts side-by-side (Image 1)
        col1, col2, col3 = st.columns(3)
        with col1:
            fig_eth = create_eth_price_chart(sc01_sliced, sc02_sliced, sc03_sliced)
            st.plotly_chart(fig_eth, use_container_width=True)
        with col2:
            fig_steth = create_steth_price_chart(sc01_sliced, sc02_sliced, sc03_sliced)
            st.plotly_chart(fig_steth, use_container_width=True)
        with col3:
            fig_disc = create_steth_discount_chart(sc01_sliced, sc02_sliced, sc03_sliced)
            st.plotly_chart(fig_disc, use_container_width=True)

        st.markdown(
            """
            <div style="text-align:center; font-size:0.85rem; color:#4B5563; margin-top:0.25rem;">
                — <span style="color:#4B5563; font-weight:600;">SC01 Baseline</span> &nbsp;&nbsp;&nbsp;&nbsp;
                — <span style="color:#1D70B8; font-weight:600;">SC02 Direct (không phản hồi)</span> &nbsp;&nbsp;&nbsp;&nbsp;
                — <span style="color:#D9383A; font-weight:600;">SC03 Contagion (có phản hồi)</span>
            </div>
            <div class="chart-caption-note">
                Đường chấm đen là block xảy ra cú sốc. Ở SC02 giá dừng sau cú sốc; ở SC03 giá tiếp tục rơi vì thanh lý bán collateral lên AMM.
            </div>
            """,
            unsafe_allow_html=True,
        )

    with tab2:
        # 2 Charts side-by-side (Image 2)
        col4, col5 = st.columns(2)
        with col4:
            fig_bar = create_scenario_liquidations_bar_chart(sc01_sliced, sc02_sliced, sc03_sliced)
            st.plotly_chart(fig_bar, use_container_width=True)
        with col5:
            fig_breakdown = create_liquidation_breakdown_chart(sc03_sliced)
            st.plotly_chart(fig_breakdown, use_container_width=True)

    with tab3:
        render_borrower_tab(results)

    with tab4:
        render_sensitivity_tab(results)

    with tab5:
        render_data_tab(results)

    with tab6:
        render_methodology_tab()


if __name__ == "__main__":
    main()
