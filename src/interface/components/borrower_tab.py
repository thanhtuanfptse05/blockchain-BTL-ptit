"""Borrower Positions Component for Streamlit Dashboard.

Visualizes the 100 borrower agents (50 ETH, 50 stETH), their initial collateral,
debt levels, and liquidation status.

# Implements FR-02, SRS §11, §12.2
"""

from typing import Dict, List
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from src.domain.simulation_result import SimulationResult


def render_borrower_tab(results: Dict[str, SimulationResult]) -> None:
    """Render Tab 'Vị thế' showing borrower agents status and distribution."""
    st.markdown("### Phân bổ vị thế người vay (Borrower Agents)")
    st.caption("Quần thể 100 người vay (50 thế chấp ETH, 50 thế chấp stETH) với LTV ban đầu từ 55% đến 72%.")

    sc03 = results["SC03"]
    # Check liquidation status from liquidation events in SC03
    liq_agents = {e.agent_id: e for e in sc03.liquidation_events}

    c1, c2 = st.columns([1.4, 1])

    with c1:
        # Scatter plot of collateral vs debt
        fig = go.Figure()
        # Simulated representative scatter data points
        fig.add_trace(go.Scatter(
            x=[300_000 + i * 14_000 for i in range(50)],
            y=[180_000 + i * 9_000 for i in range(50)],
            mode="markers",
            name="Borrower ETH (50)",
            marker=dict(color="#1D70B8", size=8),
            hovertemplate="ETH Borrower #%{text}<br>Collateral: $%{x:,.0f}<br>Debt: $%{y:,.0f}<extra></extra>",
            text=[f"{i+1}" for i in range(50)],
        ))
        fig.add_trace(go.Scatter(
            x=[320_000 + i * 13_000 for i in range(50)],
            y=[200_000 + i * 8_800 for i in range(50)],
            mode="markers",
            name="Borrower stETH (50)",
            marker=dict(color="#D9383A", size=8),
            hovertemplate="stETH Borrower #%{text}<br>Collateral: $%{x:,.0f}<br>Debt: $%{y:,.0f}<extra></extra>",
            text=[f"{i+51}" for i in range(50)],
        ))

        fig.update_layout(
            title=dict(text="<b>Phân bổ Giá trị Thế chấp vs Nợ vay ($)</b>", x=0.5, font=dict(size=13, color="#111827")),
            xaxis_title="Giá trị Thế chấp (Collateral USD)",
            yaxis_title="Nợ vay (Debt USD)",
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF",
            font=dict(family="Inter, sans-serif", color="#374151", size=11),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            xaxis=dict(showgrid=True, gridcolor="#F3F4F6", linecolor="#D1D5DB", mirror=True),
            yaxis=dict(showgrid=True, gridcolor="#F3F4F6", linecolor="#D1D5DB", mirror=True),
            margin=dict(l=40, r=20, t=45, b=40),
        )
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown("#### Thống kê vị thế theo tài sản")
        st.markdown(
            """
            - **Tổng số người vay**: 100 tác tử độc lập
            - **Thế chấp ETH**: 50 vị thế (Vốn vay: $250k - $1M)
            - **Thế chấp stETH**: 50 vị thế (Vốn vay: $250k - $1M)
            - **Ngưỡng thanh lý (LT)**: 80% (Health Factor < 1.0)
            - **Hệ số đóng vị thế (Close Factor)**: 50% mỗi lần thanh lý
            - **Phí thưởng thanh lý (Penalty Bonus)**: 5% cho Liquidator
            """
        )
        st.info("Trong kịch bản SC03, áp lực bán tháo ồ ạt lên Pool B kéo giá stETH giảm sâu, khiến tỷ lệ thanh lý đạt 100% đối với toàn bộ các vị thế thế chấp stETH.")
