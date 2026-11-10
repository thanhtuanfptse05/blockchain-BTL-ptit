"""Charts & Visualizations component using Plotly.

Generates interactive charts matching the exact demo layout:
- Tab 1: 3 charts side-by-side (Giá ETH, Giá stETH, Discount stETH)
- Tab 2: 2 charts side-by-side (Số vị thế thanh lý, Số lượt thanh lý trong block)

# Implements FR-08, FR-08-01..FR-08-06, SRS §11, §14.4
"""

from typing import List, Any, Optional
import plotly.graph_objects as go
from src.domain.block_result import BlockResult

# Colors matching the demo UI
COLOR_SC01 = "#4B5563"  # Gray / Charcoal (Baseline)
COLOR_SC02 = "#1D70B8"  # Deep blue (Direct shock)
COLOR_SC03 = "#D9383A"  # Coral red (Contagion cascade)
COLOR_ETH = "#1D70B8"   # Blue
COLOR_STETH = "#D9383A" # Red


def _add_shock_line(fig: go.Figure) -> None:
    """Add a vertical dotted line marking the price shock at block 1."""
    fig.add_vline(
        x=1,
        line_width=1.2,
        line_dash="dot",
        line_color="#1F2937",
        annotation_text="Shock (Block 1)",
        annotation_position="top right",
        annotation_font_size=10,
        annotation_font_color="#6B7280",
    )


def _apply_demo_theme(fig: go.Figure, title: str, y_title: str, **kwargs: Any) -> None:
    """Apply clean academic demo layout styling with framed plot area."""
    yaxis_dict = dict(showgrid=True, gridcolor="#F3F4F6", linecolor="#D1D5DB", mirror=True, showline=True)
    if "yaxis" in kwargs:
        yaxis_dict.update(kwargs.pop("yaxis"))

    fig.update_layout(
        title=dict(text=f"<b>{title}</b>", x=0.5, xanchor="center", font=dict(size=13, color="#111827", family="Inter, sans-serif")),
        xaxis_title=kwargs.pop("xaxis_title", "Block"),
        yaxis_title=y_title,
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(family="Inter, sans-serif", color="#374151", size=11),
        hovermode="x unified",
        showlegend=kwargs.pop("showlegend", False),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=10)),
        xaxis=dict(showgrid=True, gridcolor="#F3F4F6", linecolor="#D1D5DB", mirror=True, showline=True),
        yaxis=yaxis_dict,
        margin=dict(l=40, r=20, t=45, b=40),
        **kwargs,
    )


# Backward compatibility aliases
_apply_chart_theme = _apply_demo_theme
_apply_dark_theme = _apply_demo_theme


def create_eth_price_chart(
    sc01_blocks: List[BlockResult],
    sc02_blocks: List[BlockResult],
    sc03_blocks: List[BlockResult],
) -> go.Figure:
    """Chart 1 of Tab 1: Giá ETH (USD) across SC01, SC02, SC03."""
    fig = go.Figure()
    if sc01_blocks:
        fig.add_trace(go.Scatter(
            x=[b.block for b in sc01_blocks], y=[b.eth_price_usd for b in sc01_blocks],
            mode="lines", name="SC01 Baseline", line=dict(color=COLOR_SC01, width=1.5, dash="dash"),
            hovertemplate="Block %{x}: $%{y:,.0f}<extra>SC01</extra>",
        ))
    if sc02_blocks:
        fig.add_trace(go.Scatter(
            x=[b.block for b in sc02_blocks], y=[b.eth_price_usd for b in sc02_blocks],
            mode="lines", name="SC02 Direct (không phản hồi)", line=dict(color=COLOR_SC02, width=2.2),
            hovertemplate="Block %{x}: $%{y:,.0f}<extra>SC02</extra>",
        ))
    if sc03_blocks:
        fig.add_trace(go.Scatter(
            x=[b.block for b in sc03_blocks], y=[b.eth_price_usd for b in sc03_blocks],
            mode="lines", name="SC03 Contagion (có phản hồi)", line=dict(color=COLOR_SC03, width=2.4),
            hovertemplate="Block %{x}: $%{y:,.0f}<extra>SC03</extra>",
        ))
    _add_shock_line(fig)
    _apply_demo_theme(fig, title="Giá ETH (USD)", y_title="USD", yaxis=dict(dtick=200))
    return fig


def create_steth_price_chart(
    sc01_blocks: List[BlockResult],
    sc02_blocks: List[BlockResult],
    sc03_blocks: List[BlockResult],
) -> go.Figure:
    """Chart 2 of Tab 1: Giá stETH (USD) across SC01, SC02, SC03."""
    fig = go.Figure()
    if sc01_blocks:
        fig.add_trace(go.Scatter(
            x=[b.block for b in sc01_blocks], y=[b.steth_price_usd for b in sc01_blocks],
            mode="lines", name="SC01 Baseline", line=dict(color=COLOR_SC01, width=1.5, dash="dash"),
            hovertemplate="Block %{x}: $%{y:,.0f}<extra>SC01</extra>",
        ))
    if sc02_blocks:
        fig.add_trace(go.Scatter(
            x=[b.block for b in sc02_blocks], y=[b.steth_price_usd for b in sc02_blocks],
            mode="lines", name="SC02 Direct (không phản hồi)", line=dict(color=COLOR_SC02, width=2.2),
            hovertemplate="Block %{x}: $%{y:,.0f}<extra>SC02</extra>",
        ))
    if sc03_blocks:
        fig.add_trace(go.Scatter(
            x=[b.block for b in sc03_blocks], y=[b.steth_price_usd for b in sc03_blocks],
            mode="lines", name="SC03 Contagion (có phản hồi)", line=dict(color=COLOR_SC03, width=2.4),
            hovertemplate="Block %{x}: $%{y:,.0f}<extra>SC03</extra>",
        ))
    _add_shock_line(fig)
    _apply_demo_theme(fig, title="Giá stETH (USD)", y_title="USD", yaxis=dict(dtick=200))
    return fig


def create_steth_discount_chart(
    sc01_blocks: List[BlockResult],
    sc02_blocks: List[BlockResult],
    sc03_blocks: List[BlockResult],
) -> go.Figure:
    """Chart 3 of Tab 1: Discount stETH so với ETH (%)."""
    fig = go.Figure()
    if sc01_blocks:
        fig.add_trace(go.Scatter(
            x=[b.block for b in sc01_blocks], y=[b.steth_discount_pct for b in sc01_blocks],
            mode="lines", name="SC01 Baseline", line=dict(color=COLOR_SC01, width=1.5, dash="dash"),
            hovertemplate="Block %{x}: %{y:.1f}%<extra>SC01</extra>",
        ))
    if sc02_blocks:
        fig.add_trace(go.Scatter(
            x=[b.block for b in sc02_blocks], y=[b.steth_discount_pct for b in sc02_blocks],
            mode="lines", name="SC02 Direct (không phản hồi)", line=dict(color=COLOR_SC02, width=2.2),
            hovertemplate="Block %{x}: %{y:.1f}%<extra>SC02</extra>",
        ))
    if sc03_blocks:
        fig.add_trace(go.Scatter(
            x=[b.block for b in sc03_blocks], y=[b.steth_discount_pct for b in sc03_blocks],
            mode="lines", name="SC03 Contagion (có phản hồi)", line=dict(color=COLOR_SC03, width=2.4),
            hovertemplate="Block %{x}: %{y:.1f}%<extra>SC03</extra>",
        ))
    _add_shock_line(fig)
    _apply_demo_theme(fig, title="Discount stETH so với ETH (%)", y_title="Discount (%)", yaxis=dict(ticksuffix="%", dtick=5))
    return fig


def create_scenario_liquidations_bar_chart(
    sc01_blocks: List[BlockResult],
    sc02_blocks: List[BlockResult],
    sc03_blocks: List[BlockResult],
) -> go.Figure:
    """Chart 1 of Tab 2: Số vị thế bị thanh lý (trên 50 mỗi nhóm) across 3 scenarios."""
    fig = go.Figure()
    cats = ["SC01<br>baseline", "SC02<br>direct", "SC03<br>contagion"]
    eth_counts = [
        sc01_blocks[-1].liquidations_eth if sc01_blocks else 0,
        sc02_blocks[-1].liquidations_eth if sc02_blocks else 0,
        sc03_blocks[-1].liquidations_eth if sc03_blocks else 0,
    ]
    steth_counts = [
        sc01_blocks[-1].liquidations_steth if sc01_blocks else 0,
        sc02_blocks[-1].liquidations_steth if sc02_blocks else 0,
        sc03_blocks[-1].liquidations_steth if sc03_blocks else 0,
    ]

    fig.add_trace(go.Bar(
        x=cats, y=eth_counts, name="Vị thế ETH", marker_color=COLOR_ETH,
        text=eth_counts, textposition="outside",
    ))
    fig.add_trace(go.Bar(
        x=cats, y=steth_counts, name="Vị thế stETH", marker_color=COLOR_STETH,
        text=steth_counts, textposition="outside",
    ))
    _apply_demo_theme(
        fig, title="Số vị thế bị thanh lý (trên 50 mỗi nhóm)",
        y_title="Số vị thế bị thanh lý (trên 50 mỗi nhóm)",
        xaxis_title="", showlegend=True, barmode="group",
        yaxis=dict(range=[0, 58], dtick=10),
    )
    return fig


def create_liquidation_breakdown_chart(sc03_blocks: List[BlockResult]) -> go.Figure:
    """Chart 2 of Tab 2: Số lượt thanh lý trong block (SC03)."""
    fig = go.Figure()
    if sc03_blocks:
        blocks = [b.block for b in sc03_blocks]
        fig.add_trace(go.Bar(
            x=blocks, y=[b.liquidations_eth for b in sc03_blocks],
            name="ETH", marker_color=COLOR_ETH,
        ))
        fig.add_trace(go.Bar(
            x=blocks, y=[b.liquidations_steth for b in sc03_blocks],
            name="stETH", marker_color=COLOR_STETH,
        ))
    _apply_demo_theme(
        fig, title="Số lượt thanh lý trong block (SC03)",
        y_title="Số lượt thanh lý trong block (SC03)",
        showlegend=True, barmode="group",
        yaxis=dict(rangemode="tozero"),
    )
    return fig


def create_cumulative_liquidated_agents_chart(
    sc02_blocks: List[BlockResult],
    sc03_blocks: List[BlockResult],
) -> go.Figure:
    """Line chart comparing cumulative unique liquidated agents (SC02 vs SC03)."""
    fig = go.Figure()
    if sc02_blocks:
        fig.add_trace(go.Scatter(
            x=[b.block for b in sc02_blocks], y=[b.liquidated_agents_unique_cumulative for b in sc02_blocks],
            mode="lines", name="SC02 Direct", line=dict(color=COLOR_SC02, width=2.2, shape="hv"),
        ))
    if sc03_blocks:
        fig.add_trace(go.Scatter(
            x=[b.block for b in sc03_blocks], y=[b.liquidated_agents_unique_cumulative for b in sc03_blocks],
            mode="lines", name="SC03 Contagion", line=dict(color=COLOR_SC03, width=2.4, shape="hv"),
        ))
    _apply_demo_theme(fig, title="Số người vay bị thanh lý lũy kế", y_title="Số người vay", showlegend=True)
    return fig
