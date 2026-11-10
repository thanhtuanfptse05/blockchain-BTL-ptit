"""Analytics & Summary KPIs component.

Extracts, aggregates, and renders core performance indicators and comparison metrics
for simulation scenarios.

# Implements FR-07, FR-11, BR-10, SRS §7.5, §11, §12.2
"""

from typing import List, Dict, Any, Optional
from src.domain.simulation_result import KPISummary, SimulationResult


def format_usd(val: float) -> str:
    """Format a float as USD currency string with commas and 2 decimals.

    # Implements FR-07-02
    """
    return f"${val:,.2f}"


def format_pct(val: float) -> str:
    """Format a float as percentage string with 2 decimals.

    # Implements FR-07-02
    """
    return f"{val:.2f}%"


def calculate_kpi_summary(
    sim_result: SimulationResult,
    total_agents: int = 100,
    ref_sc02: Optional[SimulationResult] = None,
) -> KPISummary:
    """Extract and calculate the 6 core KPIs for a simulation result.

    # Implements FR-07, FR-07-01, FR-07-03, SRS §7.5

    Args:
        sim_result: The completed SimulationResult.
        total_agents: Total count of borrower agents in the simulation.
        ref_sc02: Optional reference SC02 SimulationResult for delta comparison.

    Returns:
        KPISummary instance populated with final metrics and optional deltas.
    """
    final_block = sim_result.block_results[-1]
    final_eth = final_block.eth_price_usd
    final_steth = final_block.steth_price_usd
    final_discount = final_block.steth_discount_pct
    bad_debt = final_block.bad_debt_usd

    unique_liquidated = len({ev.agent_id for ev in sim_result.liquidation_events})
    total_events = len(sim_result.liquidation_events)
    total_repaid = sum(ev.debt_repaid_usd for ev in sim_result.liquidation_events)
    ratio_pct = (unique_liquidated / total_agents) * 100.0 if total_agents > 0 else 0.0

    delta_eth: Optional[float] = None
    delta_steth: Optional[float] = None
    delta_discount: Optional[float] = None
    delta_unique: Optional[int] = None
    delta_events: Optional[int] = None
    delta_bad_debt: Optional[float] = None

    if ref_sc02 is not None:
        ref_final = ref_sc02.block_results[-1]
        delta_eth = final_eth - ref_final.eth_price_usd
        delta_steth = final_steth - ref_final.steth_price_usd
        delta_discount = final_discount - ref_final.steth_discount_pct

        ref_unique = len({ev.agent_id for ev in ref_sc02.liquidation_events})
        ref_events = len(ref_sc02.liquidation_events)
        ref_bad_debt = ref_final.bad_debt_usd

        delta_unique = unique_liquidated - ref_unique
        delta_events = total_events - ref_events
        delta_bad_debt = bad_debt - ref_bad_debt

    return KPISummary(
        scenario_id=sim_result.scenario_id,
        final_eth_price_usd=final_eth,
        final_steth_price_usd=final_steth,
        final_steth_discount_pct=final_discount,
        liquidated_agents_unique=unique_liquidated,
        total_agents=total_agents,
        liquidated_agents_ratio_pct=ratio_pct,
        liquidation_events_total=total_events,
        total_debt_repaid_usd=total_repaid,
        bad_debt_usd=bad_debt,
        delta_eth_price_usd=delta_eth,
        delta_steth_price_usd=delta_steth,
        delta_steth_discount_pct=delta_discount,
        delta_liquidated_agents=delta_unique,
        delta_liquidation_events=delta_events,
        delta_bad_debt_usd=delta_bad_debt,
    )


def _calc_relative_change(val_base: float, val_target: float) -> str:
    """Calculate relative percentage change with zero-division guard.

    # Implements FR-07-04, FR-11
    """
    if val_base == 0.0:
        if val_target > 0.0:
            return "N/A"
        return "0.0%"
    pct = ((val_target - val_base) / val_base) * 100.0
    return f"{pct:+.2f}%"


def generate_comparison_table(
    sc01: SimulationResult,
    sc02: SimulationResult,
    sc03: SimulationResult,
) -> List[Dict[str, Any]]:
    """Generate side-by-side comparison rows for SC01, SC02, and SC03.

    # Implements FR-11, SRS §11, §12.2

    Args:
        sc01: Baseline simulation result.
        sc02: Direct shock simulation result.
        sc03: Cascade contagion simulation result.

    Returns:
        List of dictionaries with comparison metrics and deltas.
    """
    b1, b2, b3 = sc01.block_results[-1], sc02.block_results[-1], sc03.block_results[-1]
    u1 = len({ev.agent_id for ev in sc01.liquidation_events})
    u2 = len({ev.agent_id for ev in sc02.liquidation_events})
    u3 = len({ev.agent_id for ev in sc03.liquidation_events})

    e1 = len(sc01.liquidation_events)
    e2 = len(sc02.liquidation_events)
    e3 = len(sc03.liquidation_events)

    r1 = sum(ev.debt_repaid_usd for ev in sc01.liquidation_events)
    r2 = sum(ev.debt_repaid_usd for ev in sc02.liquidation_events)
    r3 = sum(ev.debt_repaid_usd for ev in sc03.liquidation_events)

    d_eth = b3.eth_price_usd - b2.eth_price_usd
    d_steth = b3.steth_price_usd - b2.steth_price_usd
    d_disc = b3.steth_discount_pct - b2.steth_discount_pct
    d_u = u3 - u2
    d_e = e3 - e2
    d_r = r3 - r2
    d_bd = b3.bad_debt_usd - b2.bad_debt_usd

    rows = [
        {
            "metric": "Final ETH Price ($)",
            "unit": "USD",
            "sc01_value": format_usd(b1.eth_price_usd),
            "sc02_value": format_usd(b2.eth_price_usd),
            "sc03_value": format_usd(b3.eth_price_usd),
            "delta_sc03_sc02": format_usd(d_eth),
            "relative_change": _calc_relative_change(b2.eth_price_usd, b3.eth_price_usd),
        },
        {
            "metric": "Final stETH Price ($)",
            "unit": "USD",
            "sc01_value": format_usd(b1.steth_price_usd),
            "sc02_value": format_usd(b2.steth_price_usd),
            "sc03_value": format_usd(b3.steth_price_usd),
            "delta_sc03_sc02": format_usd(d_steth),
            "relative_change": _calc_relative_change(b2.steth_price_usd, b3.steth_price_usd),
        },
        {
            "metric": "Final stETH Discount (%)",
            "unit": "%",
            "sc01_value": format_pct(b1.steth_discount_pct),
            "sc02_value": format_pct(b2.steth_discount_pct),
            "sc03_value": format_pct(b3.steth_discount_pct),
            "delta_sc03_sc02": f"{d_disc:+.2f}%",
            "relative_change": _calc_relative_change(b2.steth_discount_pct, b3.steth_discount_pct),
        },
        {
            "metric": "Liquidated Agents (unique)",
            "unit": "agents",
            "sc01_value": str(u1),
            "sc02_value": str(u2),
            "sc03_value": str(u3),
            "delta_sc03_sc02": f"{d_u:+d}",
            "relative_change": _calc_relative_change(float(u2), float(u3)),
        },
        {
            "metric": "Total Liquidation Events",
            "unit": "events",
            "sc01_value": str(e1),
            "sc02_value": str(e2),
            "sc03_value": str(e3),
            "delta_sc03_sc02": f"{d_e:+d}",
            "relative_change": _calc_relative_change(float(e2), float(e3)),
        },
        {
            "metric": "Total Debt Repaid ($)",
            "unit": "USD",
            "sc01_value": format_usd(r1),
            "sc02_value": format_usd(r2),
            "sc03_value": format_usd(r3),
            "delta_sc03_sc02": format_usd(d_r),
            "relative_change": _calc_relative_change(r2, r3),
        },
        {
            "metric": "Total Bad Debt ($)",
            "unit": "USD",
            "sc01_value": format_usd(b1.bad_debt_usd),
            "sc02_value": format_usd(b2.bad_debt_usd),
            "sc03_value": format_usd(b3.bad_debt_usd),
            "delta_sc03_sc02": format_usd(d_bd),
            "relative_change": _calc_relative_change(b2.bad_debt_usd, b3.bad_debt_usd),
        },
    ]
    return rows


def _render_card(col, label: str, value: str, delta: Optional[str], is_bad_metric: bool = False) -> None:
    """Helper to render a clean, human-designed KPI card in a Streamlit column."""
    delta_html = ""
    if delta is not None:
        if delta in ("$0.00", "+0", "+0.00%", "0.00%", "0"):
            cls = "delta-flat"
        elif is_bad_metric:
            cls = "delta-down" if (delta.startswith("+") or not delta.startswith("-")) else "delta-up"
        else:
            cls = "delta-down" if delta.startswith("-") else "delta-up"
        delta_html = f'<div class="metric-delta {cls}">{delta} vs SC02</div>'

    html = f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        {delta_html}
    </div>
    """
    col.markdown(html, unsafe_allow_html=True)


def render_kpi_metrics(summary: KPISummary) -> None:
    """Render the 6 core KPI metric cards with clean financial layout in Streamlit UI.

    # Implements FR-07, FR-07-06, NFR-06, SRS §11, §14.3

    Args:
        summary: Calculated KPISummary object.
    """
    import streamlit as st

    c1, c2, c3, c4, c5, c6 = st.columns(6)

    d_eth = format_usd(summary.delta_eth_price_usd) if summary.delta_eth_price_usd is not None else None
    _render_card(c1, "Giá ETH cuối", format_usd(summary.final_eth_price_usd), d_eth)

    d_steth = format_usd(summary.delta_steth_price_usd) if summary.delta_steth_price_usd is not None else None
    _render_card(c2, "Giá stETH cuối", format_usd(summary.final_steth_price_usd), d_steth)

    d_disc = f"{summary.delta_steth_discount_pct:+.2f}%" if summary.delta_steth_discount_pct is not None else None
    _render_card(c3, "Chiết khấu stETH", format_pct(summary.final_steth_discount_pct), d_disc, is_bad_metric=True)

    d_ag = f"{summary.delta_liquidated_agents:+d}" if summary.delta_liquidated_agents is not None else None
    val_ag = f"{summary.liquidated_agents_unique}/{summary.total_agents} ({summary.liquidated_agents_ratio_pct:.0f}%)"
    _render_card(c4, "Vị thế thanh lý", val_ag, d_ag, is_bad_metric=True)

    d_ev = f"{summary.delta_liquidation_events:+d}" if summary.delta_liquidation_events is not None else None
    _render_card(c5, "Số lần thanh lý", str(summary.liquidation_events_total), d_ev, is_bad_metric=True)

    d_bd = format_usd(summary.delta_bad_debt_usd) if summary.delta_bad_debt_usd is not None else None
    _render_card(c6, "Nợ xấu phát sinh", format_usd(summary.bad_debt_usd), d_bd, is_bad_metric=True)


