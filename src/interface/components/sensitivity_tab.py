"""Sensitivity and Capital at Risk (CAR) Component for Streamlit Dashboard.

Presents quantitative benchmark matrix and capital at risk analysis across scenarios.

# Implements FR-11, SRS §11, §12.2
"""

from typing import Dict
import streamlit as st
import pandas as pd
from src.domain.simulation_result import SimulationResult
from src.interface.components.metrics import generate_comparison_table


def render_sensitivity_tab(results: Dict[str, SimulationResult]) -> None:
    """Render Tab 'Độ nhạy (CAR)' with benchmark table and risk metrics."""
    st.markdown("### Phân tích Độ nhạy & Rủi ro Vốn (Capital at Risk - CAR)")
    st.caption("Đối chứng định lượng tác động khuếch đại rủi ro từ cơ chế phản hồi AMM (FR-11).")

    comp_table = generate_comparison_table(
        results["SC01"],
        results["SC02"],
        results["SC03"],
    )
    df_comp = pd.DataFrame(comp_table)

    # Rename columns for clean human-readable presentation
    df_display = df_comp.rename(columns={
        "metric": "Chỉ số",
        "unit": "Đơn vị",
        "sc01_value": "SC01 Baseline",
        "sc02_value": "SC02 Direct Shock",
        "sc03_value": "SC03 Cascade",
        "delta_sc03_sc02": "Chênh lệch (SC03 - SC02)",
        "relative_change": "Tỷ lệ tăng tương đối (%)",
    })
    st.dataframe(df_display, width="stretch")

    st.markdown("---")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("**Hệ số khuếch đại thanh lý:**")
        b2_liq = len([e for e in results["SC02"].liquidation_events])
        b3_liq = len([e for e in results["SC03"].liquidation_events])
        mult = (b3_liq / max(b2_liq, 1))
        st.markdown(f"<span style='font-size:1.6rem; font-weight:700; color:#D9383A;'>{mult:.1f}x</span> lần so với cú sốc thuần túy", unsafe_allow_html=True)

    with c2:
        st.markdown("**Tổng nợ xấu giao thức (Bad Debt):**")
        st.markdown(f"<span style='font-size:1.6rem; font-weight:700; color:#D9383A;'>${results['SC03'].final_bad_debt_usd:,.0f} USD</span>", unsafe_allow_html=True)

    with c3:
        st.markdown("**Mức độ depeg stETH tối đa:**")
        st.markdown(f"<span style='font-size:1.6rem; font-weight:700; color:#D9383A;'>{results['SC03'].final_steth_discount_pct:.1f}%</span>", unsafe_allow_html=True)
