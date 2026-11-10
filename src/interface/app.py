"""Main Streamlit Application for DeFi Liquidation Cascade Simulator.

# Implements FR-10, FR-10-01..FR-10-07, NFR-06, SRS §11, §12, §13, §14, §15.1
"""

from typing import Dict
import streamlit as st
import pandas as pd

from src.domain.config import SimulationConfig
from src.domain.simulation_result import SimulationResult
from src.usecase.scenario_runner import run_all_scenarios
from src.interface.theme import apply_theme
from src.interface.components.sidebar import render_sidebar
from src.interface.components.metrics import calculate_kpi_summary, render_kpi_metrics, generate_comparison_table
from src.interface.components.charts import (
    create_eth_price_chart,
    create_steth_discount_chart,
    create_liquidation_breakdown_chart,
    create_cumulative_liquidated_agents_chart,
)
from src.interface.components.data_tab import render_data_tab
from src.interface.components.methodology_tab import render_methodology_tab


def main() -> None:
    """Main Streamlit application entry point.

    # Implements FR-10-01, FR-10-02, FR-10-07, NFR-06
    """
    st.set_page_config(
        page_title="DeFi Liquidation Cascade Simulator",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Apply Custom Light Theme
    apply_theme()

    # Header Container with Academic Disclaimer (FR-10-02, SRS §12.3)
    st.markdown(
        """
        <div class="header-container">
            <div class="header-badge">Mô hình Agent-Based Model</div>
            <h1 class="header-title">Mô phỏng lây lan rủi ro thanh lý trong DeFi Lending</h1>
            <p class="header-subtitle">
                Khảo sát cơ chế lây lan rủi ro khi thanh lý tài sản thế chấp (ETH và stETH) tác động lên các pool AMM qua từng khối.
            </p>
            <div class="header-disclaimer">
                Ghi chú: Dữ liệu giả lập phục vụ nghiên cứu học thuật, không phải dự báo thị trường thực tế.
            </div>
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
        with st.spinner("Khởi tạo mô phỏng mặc định..."):
            st.session_state["simulation_results"] = run_all_scenarios(st.session_state["simulation_config"])

    if run_clicked:
        with st.spinner("Đang tính toán mô phỏng 3 kịch bản..."):
            results: Dict[str, SimulationResult] = run_all_scenarios(config)
            st.session_state["simulation_results"] = results
            st.session_state["simulation_config"] = config
        st.toast("Hoàn tất tính toán mô phỏng.")

    results: Dict[str, SimulationResult] = st.session_state["simulation_results"]
    active_config: SimulationConfig = st.session_state["simulation_config"]

    # Top KPI Metrics Cards (FR-07)
    st.markdown(
        """
        <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:0.6rem;">
            <span style="font-size:0.95rem; font-weight:700; color:#0F172A;">
                Chỉ số kịch bản lây lan (SC03 so với SC02)
            </span>
            <span style="font-size:0.8rem; color:#64748B;">Độ dài: <strong>%d khối</strong> | Hạt giống: <strong>%d</strong></span>
        </div>
        """ % (active_config.max_blocks, active_config.seed),
        unsafe_allow_html=True,
    )
    kpi_summary = calculate_kpi_summary(
        sim_result=results["SC03"],
        total_agents=active_config.num_borrowers,
        ref_sc02=results["SC02"],
    )
    render_kpi_metrics(kpi_summary)

    # Scenario Items Strip
    st.markdown(
        """
        <div class="scenarios-strip">
            <div class="scenario-item sc-01">SC01: Baseline (Đối chứng tĩnh)</div>
            <div class="scenario-item sc-02">SC02: Direct Shock (Cú sốc ngoại sinh)</div>
            <div class="scenario-item sc-03">SC03: Cascade Contagion (Lây lan thanh lý)</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 4 Main Tabs (SRS §12.2)
    tab1, tab2, tab3, tab4 = st.tabs([
        "Biến động giá và chiết khấu",
        "Diễn biến thanh lý",
        "Bảng dữ liệu chi tiết",
        "Cơ sở phương pháp luận",
    ])

    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            fig_eth = create_eth_price_chart(
                results["SC01"].block_results,
                results["SC02"].block_results,
                results["SC03"].block_results,
            )
            st.plotly_chart(fig_eth, use_container_width=True)
        with c2:
            fig_discount = create_steth_discount_chart(
                results["SC01"].block_results,
                results["SC02"].block_results,
                results["SC03"].block_results,
            )
            st.plotly_chart(fig_discount, use_container_width=True)

    with tab2:
        c3, c4 = st.columns(2)
        with c3:
            fig_breakdown = create_liquidation_breakdown_chart(results["SC03"].block_results)
            st.plotly_chart(fig_breakdown, use_container_width=True)
        with c4:
            fig_cumulative = create_cumulative_liquidated_agents_chart(
                results["SC02"].block_results,
                results["SC03"].block_results,
            )
            st.plotly_chart(fig_cumulative, use_container_width=True)

        st.markdown("### So sánh chỉ số giữa các kịch bản")
        st.caption("Đối chứng định lượng hiệu ứng khuếch đại rủi ro từ cơ chế phản hồi AMM.")
        comp_table = generate_comparison_table(
            results["SC01"],
            results["SC02"],
            results["SC03"],
        )
        df_comp = pd.DataFrame(comp_table)
        st.dataframe(df_comp, width="stretch")

    with tab3:
        render_data_tab(results)

    with tab4:
        render_methodology_tab()


if __name__ == "__main__":
    main()
