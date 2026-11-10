"""Charts & Visualizations component using Plotly.

Generates 4 interactive charts for DeFi liquidation cascade analysis
with clean, light-mode financial layout.

# Implements FR-08, FR-08-01..FR-08-06, SRS §11, §14.4
"""

from typing import List, Dict, Any
import plotly.graph_objects as go
from src.domain.block_result import BlockResult

# Color palette with clear distinction and high contrast
COLOR_SC01 = "#059669"  # Emerald green (Baseline / Stable)
COLOR_SC02 = "#D97706"  # Amber orange (Direct shock)
COLOR_SC03 = "#DC2626"  # Crimson red (Cascade contagion)
COLOR_ETH = "#2563EB"   # Royal blue
COLOR_STETH = "#7C3AED" # Violet purple


def _add_shock_line(fig: go.Figure) -> None:
    """Add a vertical dashed line and annotation at block 1 marking the price shock.

    # Implements FR-08-03
    """
    fig.add_vline(
        x=1,
        line_width=1.5,
        line_dash="dash",
        line_color="#D97706",
        annotation_text="Cú sốc giá (Block 1)",
        annotation_position="top right",
        annotation_font_size=11,
        annotation_font_color="#B45309",
    )


def _apply_chart_theme(fig: go.Figure, title: str, y_title: str, **kwargs: Any) -> None:
    """Apply clean light mode layout styling to a Plotly figure."""
    yaxis_dict = dict(showgrid=True, gridcolor="#F1F5F9", zerolinecolor="#E2E8F0")
    if "yaxis" in kwargs:
        yaxis_dict.update(kwargs.pop("yaxis"))

    fig.update_layout(
        title=dict(text=title, font=dict(size=13, color="#0F172A", family="Plus Jakarta Sans, sans-serif")),
        xaxis_title="Block",
        yaxis_title=y_title,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#FFFFFF",
        font=dict(family="Plus Jakarta Sans, sans-serif", color="#475569"),
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color="#334155", size=11),
        ),
        xaxis=dict(dtick=1, showgrid=True, gridcolor="#F1F5F9", zerolinecolor="#E2E8F0"),
        yaxis=yaxis_dict,
        margin=dict(l=50, r=30, t=65, b=45),
        **kwargs,
    )


# Alias for backward compatibility if needed
_apply_dark_theme = _apply_chart_theme


def create_eth_price_chart(
    sc01_blocks: List[BlockResult],
    sc02_blocks: List[BlockResult],
    sc03_blocks: List[BlockResult],
) -> go.Figure:
    """Create interactive line chart comparing ETH prices across 3 scenarios.

    # Implements FR-08-01, FR-08-02, SRS §14.4
    """
    fig = go.Figure()

    if sc01_blocks:
        fig.add_trace(go.Scatter(
            x=[b.block for b in sc01_blocks],
            y=[b.eth_price_usd for b in sc01_blocks],
            mode="lines+markers",
            name="SC01: Baseline",
            line=dict(color=COLOR_SC01, width=2.5),
            marker=dict(size=4),
            hovertemplate="Block %{x}: $%{y:,.2f}<extra>SC01</extra>",
        ))

    if sc02_blocks:
        fig.add_trace(go.Scatter(
            x=[b.block for b in sc02_blocks],
            y=[b.eth_price_usd for b in sc02_blocks],
            mode="lines+markers",
            name="SC02: Direct Shock",
            line=dict(color=COLOR_SC02, width=2.5),
            marker=dict(size=4),
            hovertemplate="Block %{x}: $%{y:,.2f}<extra>SC02</extra>",
        ))

    if sc03_blocks:
        fig.add_trace(go.Scatter(
            x=[b.block for b in sc03_blocks],
            y=[b.eth_price_usd for b in sc03_blocks],
            mode="lines+markers",
            name="SC03: Cascade Contagion",
            line=dict(color=COLOR_SC03, width=3),
            marker=dict(size=5),
            hovertemplate="Block %{x}: $%{y:,.2f}<extra>SC03</extra>",
        ))

    _add_shock_line(fig)
    _apply_chart_theme(
        fig=fig,
        title="Biến động giá ETH theo Block",
        y_title="ETH Price (USD)",
        yaxis=dict(tickprefix="$", showgrid=True, gridcolor="#F1F5F9"),
    )
    return fig


def create_steth_discount_chart(
    sc01_blocks: List[BlockResult],
    sc02_blocks: List[BlockResult],
    sc03_blocks: List[BlockResult],
) -> go.Figure:
    """Create interactive line chart of stETH discount/depeg percentage.

    # Implements FR-08-01, FR-08-02, SRS §14.4
    """
    fig = go.Figure()

    if sc01_blocks:
        fig.add_trace(go.Scatter(
            x=[b.block for b in sc01_blocks],
            y=[b.steth_discount_pct for b in sc01_blocks],
            mode="lines+markers",
            name="SC01: Baseline",
            line=dict(color=COLOR_SC01, width=2),
            marker=dict(size=4),
            hovertemplate="Block %{x}: %{y:.2f}%<extra>SC01</extra>",
        ))

    if sc02_blocks:
        fig.add_trace(go.Scatter(
            x=[b.block for b in sc02_blocks],
            y=[b.steth_discount_pct for b in sc02_blocks],
            mode="lines+markers",
            name="SC02: Direct Shock",
            line=dict(color=COLOR_SC02, width=2),
            marker=dict(size=4),
            hovertemplate="Block %{x}: %{y:.2f}%<extra>SC02</extra>",
        ))

    if sc03_blocks:
        fig.add_trace(go.Scatter(
            x=[b.block for b in sc03_blocks],
            y=[b.steth_discount_pct for b in sc03_blocks],
            mode="lines+markers",
            name="SC03: Cascade Contagion",
            line=dict(color=COLOR_SC03, width=3),
            marker=dict(size=5),
            hovertemplate="Block %{x}: %{y:.2f}%<extra>SC03</extra>",
        ))

    _add_shock_line(fig)
    _apply_chart_theme(
        fig=fig,
        title="Tỉ lệ chiết khấu stETH so với ETH",
        y_title="stETH Discount vs ETH (%)",
        yaxis=dict(ticksuffix="%", showgrid=True, gridcolor="#F1F5F9"),
    )
    return fig


def create_liquidation_breakdown_chart(sc03_blocks: List[BlockResult]) -> go.Figure:
    """Create stacked bar chart showing liquidation events by asset type in SC03.

    # Implements FR-08-01, FR-08-02, SRS §14.4
    """
    fig = go.Figure()

    if sc03_blocks:
        blocks = [b.block for b in sc03_blocks]
        eth_liqs = [b.liquidations_eth for b in sc03_blocks]
        steth_liqs = [b.liquidations_steth for b in sc03_blocks]

        fig.add_trace(go.Bar(
            x=blocks,
            y=eth_liqs,
            name="ETH Liquidations",
            marker_color=COLOR_ETH,
            hovertemplate="Block %{x}: %{y} ETH events<extra></extra>",
        ))
        fig.add_trace(go.Bar(
            x=blocks,
            y=steth_liqs,
            name="stETH Liquidations",
            marker_color=COLOR_STETH,
            hovertemplate="Block %{x}: %{y} stETH events<extra></extra>",
        ))

    _apply_chart_theme(
        fig=fig,
        title="Phân bổ sự kiện thanh lý theo tài sản (SC03)",
        y_title="Số sự kiện thanh lý",
        barmode="stack",
        yaxis=dict(rangemode="tozero", dtick=1, showgrid=True, gridcolor="#F1F5F9"),
    )
    return fig


def create_cumulative_liquidated_agents_chart(
    sc02_blocks: List[BlockResult],
    sc03_blocks: List[BlockResult],
) -> go.Figure:
    """Create line chart comparing cumulative unique liquidated agents (SC02 vs SC03).

    # Implements FR-08-01, FR-08-02, SRS §14.4
    """
    fig = go.Figure()

    if sc02_blocks:
        fig.add_trace(go.Scatter(
            x=[b.block for b in sc02_blocks],
            y=[b.liquidated_agents_unique_cumulative for b in sc02_blocks],
            mode="lines+markers",
            name="SC02: Direct Shock",
            line=dict(color=COLOR_SC02, width=2.5, shape="hv"),
            marker=dict(size=4),
            hovertemplate="Block %{x}: %{y} agents<extra>SC02</extra>",
        ))

    if sc03_blocks:
        fig.add_trace(go.Scatter(
            x=[b.block for b in sc03_blocks],
            y=[b.liquidated_agents_unique_cumulative for b in sc03_blocks],
            mode="lines+markers",
            name="SC03: Cascade Contagion",
            line=dict(color=COLOR_SC03, width=3, shape="hv"),
            marker=dict(size=5),
            hovertemplate="Block %{x}: %{y} agents<extra>SC03</extra>",
        ))

    _apply_chart_theme(
        fig=fig,
        title="Số lượng người vay bị thanh lý lũy kế",
        y_title="Số người vay bị thanh lý lũy kế",
        yaxis=dict(rangemode="tozero", showgrid=True, gridcolor="#F1F5F9"),
    )
    return fig
