"""
theme.py — Single source of truth for the dashboard's visual identity.

A cleaner, modern interface with subtle contrast, balanced spacing, and
a more polished presentation suitable for a submission-ready project.
"""

import streamlit as st

# ----------------------------------------------------------------
# Palette
# ----------------------------------------------------------------

BG_MAIN = "#030712"
BG_PANEL = "#111827"
BG_PANEL_ALT = "#1f2937"
BG_INPUT = "#111827"

BORDER = "#334155"
BORDER_STRONG = "#475569"

ACCENT = "#38bdf8"
ACCENT_SOFT = "#0ea5e9"
RED = "#f87171"
GREEN = "#22c55e"
AMBER = "#fbbf24"
CYAN = "#38bdf8"

TEXT_PRIMARY = "#f8fafc"
TEXT_MUTED = "#cbd5e1"
TEXT_DIM = "#94a3b8"

THREAT_COLORS = {
    "LOW": GREEN,
    "MEDIUM": AMBER,
    "HIGH": RED,
}

FONT_DISPLAY = "'Inter', 'Segoe UI', sans-serif"
FONT_MONO = "'Inter', 'Segoe UI', sans-serif"

PLOTLY_COLORWAY = [
    ACCENT, CYAN, RED, GREEN, "#8b5cf6", "#14b8a6", "#f97316", "#64748b"
]


def plotly_layout(title=None, height=None):
    """Shared plotly layout dict — spread into fig.update_layout(**this)."""
    layout = dict(
        paper_bgcolor=BG_PANEL_ALT,
        plot_bgcolor=BG_PANEL_ALT,
        font=dict(family=FONT_MONO, color=TEXT_PRIMARY, size=12),
        colorway=PLOTLY_COLORWAY,
        margin=dict(l=10, r=10, t=50 if title else 20, b=10),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(color=TEXT_MUTED, size=11)
        ),
        xaxis=dict(
            gridcolor="#e2e8f0",
            zerolinecolor="#e2e8f0",
            linecolor="#cbd5e1",
            tickfont=dict(color=TEXT_MUTED)
        ),
        yaxis=dict(
            gridcolor="#e2e8f0",
            zerolinecolor="#e2e8f0",
            linecolor="#cbd5e1",
            tickfont=dict(color=TEXT_MUTED)
        ),
    )
    if title:
        layout["title"] = dict(
            text=title,
            font=dict(family=FONT_DISPLAY, color=TEXT_PRIMARY, size=15)
        )
    if height:
        layout["height"] = height
    return layout


def style_fig(fig, title=None, height=None):
    """Apply the shared polished layout to any plotly figure in place, return it."""
    fig.update_layout(**plotly_layout(title=title, height=height))
    return fig


def inject_css():
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {{
        font-family: {FONT_MONO};
        color: {TEXT_PRIMARY};
        background: {BG_MAIN};
    }}

    .stApp {{
        background: #000000;
    }}

    .block-container {{
        padding-top: 1.4rem;
        padding-bottom: 2rem;
        background: {BG_MAIN};
    }}

    section[data-testid="stSidebar"] {{
        background: {BG_PANEL};
        border-right: 1px solid {BORDER};
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.35);
    }}

    section[data-testid="stSidebar"] * {{
        color: {TEXT_PRIMARY};
    }}

    h1, h2, h3 {{
        font-family: {FONT_DISPLAY} !important;
        color: {TEXT_PRIMARY} !important;
        letter-spacing: -0.01em;
        font-weight: 700;
        margin: 0;
    }}
    h1 {{
        color: {ACCENT} !important;
    }}

    .page-title-row {{
        display: flex;
        align-items: flex-end;
        gap: 0.75rem;
        margin-bottom: 1rem;
        padding-bottom: 0.25rem;
        border-bottom: 1px solid {BORDER};
    }}
    .page-title-text {{
        font-size: 2.1rem;
        font-weight: 800;
        color: {TEXT_PRIMARY};
        margin: 0;
    }}
    .page-title-subtitle {{
        color: {TEXT_MUTED};
        font-size: 0.95rem;
        line-height: 1.5;
        margin-top: 0.35rem;
        max-width: min(76ch, 100%);
    }}

    div[data-testid="stMetric"] {{
        background-color: {BG_PANEL};
        border: 1px solid {BORDER};
        border-radius: 14px;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.04);
        padding: 0.9rem 1rem 0.8rem 1rem;
    }}
    div[data-testid="stMetricLabel"] {{
        color: {TEXT_MUTED} !important;
        font-size: 0.72rem !important;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }}
    div[data-testid="stMetricValue"] {{
        color: {TEXT_PRIMARY} !important;
        font-family: {FONT_MONO} !important;
        font-weight: 700 !important;
    }}

    .stButton > button, .stDownloadButton > button, .stFormSubmitButton > button {{
        background-color: {ACCENT};
        color: white;
        border: none;
        border-radius: 999px;
        padding: 0.45rem 0.9rem;
        font-family: {FONT_MONO};
        font-size: 0.84rem;
        font-weight: 600;
        transition: all 0.2s ease;
    }}
    .stButton > button:hover, .stDownloadButton > button:hover, .stFormSubmitButton > button:hover {{
        background-color: #1d4ed8;
        color: white;
        box-shadow: 0 6px 16px rgba(37, 99, 235, 0.18);
    }}

    div[data-testid="stAlertContentSuccess"] {{ color: {GREEN} !important; }}
    div[data-testid="stAlertContentError"] {{ color: {RED} !important; }}
    div[data-testid="stAlertContentWarning"] {{ color: {AMBER} !important; }}
    div[data-testid="stAlertContentInfo"] {{ color: {CYAN} !important; }}

    .stAlert {{
        background-color: {BG_PANEL_ALT} !important;
        border: 1px solid {BORDER} !important;
        border-radius: 12px !important;
    }}

    button[data-baseweb="tab"] {{
        font-family: {FONT_MONO};
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-size: 0.8rem;
        color: {TEXT_MUTED};
    }}
    button[aria-selected="true"] {{
        color: {ACCENT} !important;
        border-bottom-color: {ACCENT} !important;
    }}

    div[data-testid="stDataFrame"] {{
        border: 1px solid {BORDER};
        border-radius: 12px;
        overflow: hidden;
    }}

    div[data-baseweb="select"] > div, .stTextInput input, .stNumberInput input {{
        background-color: {BG_INPUT} !important;
        border: 1px solid {BORDER} !important;
        color: {TEXT_PRIMARY} !important;
        border-radius: 10px;
        font-family: {FONT_MONO} !important;
    }}

    .ops-banner {{
        background: linear-gradient(90deg, {ACCENT_SOFT} 0%, #ffffff 100%);
        border: 1px solid {BORDER};
        border-left: 4px solid {ACCENT};
        border-radius: 14px;
        padding: 0.7rem 0.9rem;
        margin-bottom: 1rem;
        font-family: {FONT_MONO};
        font-size: 0.78rem;
        letter-spacing: 0.08em;
        color: {ACCENT};
        text-transform: uppercase;
        display: flex;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 0.5rem;
    }}
    .ops-banner span.dim {{ color: {TEXT_MUTED}; }}

    .ops-card {{
        background-color: {BG_PANEL};
        border: 1px solid {BORDER};
        border-radius: 16px;
        padding: 1rem 1.1rem;
        box-shadow: 0 10px 24px rgba(15, 23, 42, 0.05);
    }}

    .threat-pill {{
        display: inline-block;
        padding: 0.18rem 0.75rem;
        border-radius: 999px;
        font-family: {FONT_MONO};
        font-weight: 700;
        font-size: 0.78rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }}

    .section-label {{
        font-family: {FONT_MONO};
        color: {TEXT_MUTED};
        font-size: 0.75rem;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        border-bottom: 1px solid {BORDER};
        padding-bottom: 0.35rem;
        margin: 1.4rem 0 0.8rem 0;
    }}

    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header[data-testid="stHeader"] {{background-color: transparent;}}
    </style>
    """, unsafe_allow_html=True)
