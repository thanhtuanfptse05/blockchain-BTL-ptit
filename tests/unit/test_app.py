"""Unit tests verifying import and structure of Streamlit UI components.

# Implements FR-10, SRS §12
"""

import pytest
from src.interface.components import (
    sidebar,
    metrics,
    charts,
    data_tab,
    methodology_tab,
)
import src.interface.app as app


def test_ui_components_imported_successfully():
    assert hasattr(sidebar, "render_sidebar")
    assert hasattr(metrics, "calculate_kpi_summary")
    assert hasattr(metrics, "render_kpi_metrics")
    assert hasattr(metrics, "generate_comparison_table")
    assert hasattr(charts, "create_eth_price_chart")
    assert hasattr(charts, "create_steth_discount_chart")
    assert hasattr(charts, "create_liquidation_breakdown_chart")
    assert hasattr(charts, "create_cumulative_liquidated_agents_chart")
    assert hasattr(data_tab, "render_data_tab")
    assert hasattr(methodology_tab, "render_methodology_tab")
    assert hasattr(app, "main")


def test_sidebar_default_constants():
    assert sidebar.DEFAULT_SHOCK_PCT == 15.0
    assert sidebar.DEFAULT_POOL_A_TVL == 150_000_000.0
    assert sidebar.DEFAULT_POOL_B_TVL == 80_000_000.0
    assert sidebar.DEFAULT_NUM_BORROWERS == 100
    assert sidebar.DEFAULT_MAX_BLOCKS == 30
    assert sidebar.DEFAULT_SEED == 42


def test_clean_architecture_layer_isolation():
    # NFR-05: Ensure presentation layer does NOT import core swap or liquidation execution directly
    import inspect
    import src.interface.app as app_mod

    app_source = inspect.getsource(app_mod)
    assert "swap_exact_input" not in app_source
    assert "liquidate_borrower_position" not in app_source
    assert "execute_swap" not in app_source


