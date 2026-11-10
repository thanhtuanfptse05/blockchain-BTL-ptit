"""Theme and styling matching the clean academic demo interface.

Clean light mode design with coral/crimson accents, airy typography,
and high-contrast charts.

# Implements NFR-06, SRS §12
"""

import streamlit as st

COLOR_PRIMARY = "#D9383A"  # Coral red accent
COLOR_SC01 = "#4B5563"     # Charcoal/slate gray
COLOR_SC02 = "#1D70B8"     # Deep blue
COLOR_SC03 = "#D9383A"     # Crimson/coral red
COLOR_ETH = "#1D70B8"      # Blue
COLOR_STETH = "#D9383A"    # Red

CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Global Page Layout */
    .stApp {
        background-color: #FFFFFF !important;
        color: #111827 !important;
    }
    .block-container {
        padding-top: 1.8rem !important;
        padding-bottom: 3.5rem !important;
        max-width: 1400px !important;
    }

    /* Sidebar Clean Styling */
    section[data-testid="stSidebar"] {
        background-color: #F9FAFB !important;
        border-right: 1px solid #E5E7EB !important;
    }
    section[data-testid="stSidebar"] .block-container {
        padding-top: 1.8rem !important;
        padding-left: 1.25rem !important;
        padding-right: 1.25rem !important;
    }
    .sidebar-title {
        font-size: 1.12rem;
        font-weight: 700;
        color: #111827;
        margin-bottom: 1.25rem;
    }
    .sidebar-fixed-note {
        font-size: 0.86rem;
        color: #374151;
        line-height: 1.55;
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid #E5E7EB;
    }

    /* Main Page Header */
    .demo-header-title {
        font-size: 2.15rem;
        font-weight: 800;
        color: #111827;
        letter-spacing: -0.025em;
        line-height: 1.2;
        margin-bottom: 0.5rem;
    }
    .demo-header-subtitle {
        font-size: 0.85rem;
        color: #6B7280;
        line-height: 1.5;
        margin-bottom: 1.8rem;
    }

    /* Typographic Metrics Grid */
    .metrics-row {
        display: grid;
        grid-template-columns: repeat(6, 1fr);
        gap: 1.25rem;
        margin-bottom: 1.8rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid #F3F4F6;
    }
    .metric-item {
        display: flex;
        flex-direction: column;
    }
    .metric-item-label {
        font-size: 0.82rem;
        color: #4B5563;
        margin-bottom: 0.25rem;
        white-space: nowrap;
    }
    .metric-item-value {
        font-size: 1.95rem;
        font-weight: 700;
        color: #111827;
        line-height: 1.15;
        letter-spacing: -0.02em;
    }
    .metric-item-delta {
        font-size: 0.78rem;
        color: #D9383A;
        margin-top: 0.35rem;
        font-weight: 500;
        display: flex;
        align-items: center;
        gap: 0.2rem;
    }

    /* Clean Underline Tabs (Matching Demo) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 22px;
        background-color: transparent !important;
        padding: 0 !important;
        border-bottom: 1px solid #E5E7EB !important;
        margin-bottom: 1.25rem !important;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 8px 2px 10px 2px !important;
        color: #4B5563 !important;
        font-weight: 500 !important;
        font-size: 0.92rem !important;
        border: none !important;
        background-color: transparent !important;
        border-bottom: 2px solid transparent !important;
        border-radius: 0 !important;
        transition: color 0.15s ease !important;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #111827 !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: transparent !important;
        color: #D9383A !important;
        font-weight: 600 !important;
        border-bottom: 2px solid #D9383A !important;
    }

    /* Slider Styling */
    div[data-testid="stSlider"] label {
        font-size: 0.82rem !important;
        color: #374151 !important;
        font-weight: 500 !important;
    }
    div[data-testid="stSlider"] div[data-baseweb="slider"] {
        margin-top: 0.15rem !important;
    }

    /* Action Buttons */
    div.stButton > button {
        border-radius: 6px !important;
        font-weight: 500 !important;
        font-size: 0.88rem !important;
        padding: 0.45rem 0.9rem !important;
        border: 1px solid #D1D5DB !important;
        background: #FFFFFF !important;
        color: #374151 !important;
    }
    div.stButton > button:hover {
        background: #F3F4F6 !important;
        border-color: #9CA3AF !important;
    }
    div.stButton > button[kind="primary"] {
        background: #D9383A !important;
        color: #FFFFFF !important;
        border: 1px solid #B91C1C !important;
    }
    div.stButton > button[kind="primary"]:hover {
        background: #B91C1C !important;
    }

    /* Legend and Notes under Charts */
    .chart-caption-note {
        font-size: 0.82rem;
        color: #6B7280;
        line-height: 1.5;
        margin-top: 0.75rem;
    }
</style>
"""


def apply_theme() -> None:
    """Inject custom CSS theme into the active Streamlit app."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
