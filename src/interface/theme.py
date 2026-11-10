"""Theme, CSS styling, and visual design system for the Streamlit Dashboard.

Clean, human-centered Light Mode design inspired by Stripe, Linear, and Notion.

# Implements NFR-06, SRS §12
"""

import streamlit as st

BG_LIGHT = "#FFFFFF"
BG_SURFACE = "#F8FAFC"
BORDER_COLOR = "#E2E8F0"
TEXT_PRIMARY = "#0F172A"
TEXT_SECONDARY = "#475569"
COLOR_PRIMARY = "#2563EB"
COLOR_SC01 = "#059669"
COLOR_SC02 = "#D97706"
COLOR_SC03 = "#DC2626"

CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    code, pre {
        font-family: 'JetBrains Mono', monospace !important;
    }
    
    /* Layout & Surface */
    .stApp {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
    }
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 3rem !important;
        max-width: 1360px !important;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #F8FAFC !important;
        border-right: 1px solid #E2E8F0 !important;
    }
    section[data-testid="stSidebar"] .block-container {
        padding-top: 1.5rem !important;
        padding-left: 1.25rem !important;
        padding-right: 1.25rem !important;
    }
    .sidebar-section-title {
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #64748B;
        margin-top: 1.15rem;
        margin-bottom: 0.35rem;
    }
    section[data-testid="stSidebar"] div.stButton > button {
        min-height: 38px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        white-space: nowrap !important;
    }

    /* Header Container */
    .header-container {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 1.4rem 1.8rem;
        margin-bottom: 1.25rem;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04);
    }
    .header-badge {
        display: inline-block;
        background: #EFF6FF;
        border: 1px solid #BFDBFE;
        color: #1D4ED8;
        padding: 0.2rem 0.65rem;
        border-radius: 6px;
        font-size: 0.72rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        margin-bottom: 0.5rem;
    }
    .header-title {
        font-size: 1.75rem;
        font-weight: 700;
        color: #0F172A;
        letter-spacing: -0.02em;
        margin: 0 0 0.35rem 0;
        line-height: 1.25;
    }
    .header-subtitle {
        color: #475569;
        font-size: 0.92rem;
        line-height: 1.5;
        margin: 0;
    }
    .header-disclaimer {
        display: inline-block;
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        color: #64748B;
        padding: 0.35rem 0.75rem;
        border-radius: 6px;
        font-size: 0.78rem;
        font-weight: 500;
        margin-top: 0.85rem;
    }

    /* Scenario Pills */
    .scenarios-strip {
        display: flex;
        flex-wrap: wrap;
        gap: 0.6rem;
        margin-top: 0.75rem;
        margin-bottom: 1.25rem;
    }
    .scenario-item {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        padding: 0.35rem 0.75rem;
        border-radius: 6px;
        font-size: 0.78rem;
        font-weight: 500;
    }
    .sc-01 { background: #ECFDF5; border: 1px solid #A7F3D0; color: #065F46; }
    .sc-02 { background: #FFFBEB; border: 1px solid #FDE68A; color: #92400E; }
    .sc-03 { background: #FEF2F2; border: 1px solid #FECACA; color: #991B1B; }

    /* KPI Cards */
    .metric-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 1rem 1.15rem;
        box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
        transition: border-color 0.15s ease, box-shadow 0.15s ease;
    }
    .metric-card:hover {
        border-color: #CBD5E1;
        box-shadow: 0 3px 8px rgba(15, 23, 42, 0.06);
    }
    .metric-label {
        font-size: 0.72rem;
        font-weight: 600;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        margin-bottom: 0.35rem;
    }
    .metric-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.5rem;
        font-weight: 700;
        color: #0F172A;
        letter-spacing: -0.02em;
        line-height: 1.2;
    }
    .metric-delta {
        margin-top: 0.4rem;
        font-size: 0.74rem;
        font-weight: 600;
        display: inline-block;
        padding: 0.12rem 0.45rem;
        border-radius: 4px;
    }
    .delta-down { background: #FEE2E2; color: #991B1B; }
    .delta-up { background: #D1FAE5; color: #065F46; }
    .delta-flat { background: #F1F5F9; color: #475569; }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background-color: #F1F5F9 !important;
        padding: 4px;
        border-radius: 8px;
        border: 1px solid #E2E8F0;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 7px 16px !important;
        border-radius: 6px !important;
        color: #64748B !important;
        font-weight: 500 !important;
        font-size: 0.88rem !important;
        border: none !important;
        background-color: transparent !important;
    }
    .stTabs [data-baseweb="tab"]:hover { color: #0F172A !important; }
    .stTabs [aria-selected="true"] {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        font-weight: 600 !important;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.08) !important;
    }

    /* Buttons */
    div.stButton > button {
        border-radius: 6px !important;
        font-weight: 500 !important;
        font-size: 0.88rem !important;
        padding: 0.5rem 1rem !important;
        border: 1px solid #CBD5E1 !important;
        background: #FFFFFF !important;
        color: #1E293B !important;
        transition: all 0.15s ease !important;
    }
    div.stButton > button:hover {
        background: #F8FAFC !important;
        border-color: #94A3B8 !important;
    }
    div.stButton > button[kind="primary"] {
        background: #2563EB !important;
        color: #FFFFFF !important;
        border: 1px solid #1D4ED8 !important;
        box-shadow: 0 1px 2px rgba(37, 99, 235, 0.15) !important;
    }
    div.stButton > button[kind="primary"]:hover {
        background: #1D4ED8 !important;
        box-shadow: 0 2px 4px rgba(37, 99, 235, 0.25) !important;
    }

    /* Methodology Flow & Formula Cards */
    .flow-container { display: flex; flex-direction: column; gap: 0.4rem; }
    .flow-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        box-shadow: 0 1px 2px rgba(15, 23, 42, 0.03);
    }
    .flow-card-highlight { background: #FEF2F2; border-color: #FECACA; }
    .flow-step { font-size: 0.68rem; font-weight: 700; color: #2563EB; letter-spacing: 0.04em; }
    .flow-title { font-size: 0.88rem; font-weight: 600; color: #0F172A; margin-top: 0.15rem; }
    .flow-desc { font-size: 0.78rem; color: #475569; margin-top: 0.25rem; line-height: 1.45; }
    .flow-arrow { text-align: center; color: #94A3B8; font-size: 0.95rem; line-height: 1; }

    .formula-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 0.9rem 1.15rem;
        margin-bottom: 0.85rem;
        box-shadow: 0 1px 2px rgba(15, 23, 42, 0.03);
    }
    .formula-badge { font-size: 0.68rem; font-weight: 700; color: #2563EB; letter-spacing: 0.05em; margin-bottom: 0.25rem; }
    .formula-title { font-size: 0.9rem; font-weight: 700; color: #0F172A; margin-bottom: 0.4rem; }
    .formula-desc { font-size: 0.78rem; color: #64748B; margin-top: 0.45rem; line-height: 1.4; }

    .scenario-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.85rem; }
    .scenario-box { border-radius: 8px; padding: 0.85rem 1rem; }
    .box-sc01 { background: #ECFDF5; border: 1px solid #A7F3D0; }
    .box-sc02 { background: #FFFBEB; border: 1px solid #FDE68A; }
    .box-sc03 { background: #FEF2F2; border: 1px solid #FECACA; }
    .scenario-tag { font-size: 0.7rem; font-weight: 700; letter-spacing: 0.04em; margin-bottom: 0.2rem; }
    .tag-sc01 { color: #065F46; }
    .tag-sc02 { color: #92400E; }
    .tag-sc03 { color: #991B1B; }
    .scenario-name { font-size: 0.88rem; font-weight: 700; color: #0F172A; margin-bottom: 0.25rem; }
    .scenario-body { font-size: 0.78rem; color: #475569; line-height: 1.4; }

    .limitations-container {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-left: 4px solid #2563EB;
        border-radius: 8px;
        padding: 0.9rem 1.2rem;
    }

    /* Sliders & Scrollbars */
    div[data-testid="stSlider"] label { font-size: 0.8rem !important; font-weight: 600 !important; color: #334155 !important; }
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: #F8FAFC; }
    ::-webkit-scrollbar-thumb { background: #CBD5E1; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #94A3B8; }
</style>
"""


def apply_theme() -> None:
    """Inject custom CSS theme into the active Streamlit app."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
