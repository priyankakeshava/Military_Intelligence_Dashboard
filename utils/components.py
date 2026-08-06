"""
components.py — Reusable UI building blocks so every page renders with
the same structure instead of hand-rolling headers/cards/badges per page.
"""

import streamlit as st
from datetime import datetime

from utils.theme import THREAT_COLORS, TEXT_MUTED, AMBER


def classification_banner(page_name: str, record_count: int = None):
    """Top-of-page status strip — reinforces the ops-command identity
    and gives at-a-glance context on every single page."""
    count_html = f'<span>RECORDS IN VIEW: {record_count:,}</span>' if record_count is not None else ""
    st.markdown(f"""
    <div class="ops-banner">
        <span>MODULE: {page_name}</span>
        {count_html}
    </div>
    """, unsafe_allow_html=True)


def page_header(icon: str, title: str, subtitle: str = None):
    subtitle_html = (
        f'<div class="page-title-subtitle">{subtitle}</div>' if subtitle else ""
    )
    st.markdown(
        f"""
        <div class="page-title-row">
            <div style="font-size:2.2rem; line-height:1;">{icon}</div>
            <div>
                <div class="page-title-text">{title}</div>
                {subtitle_html}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_label(text: str):
    st.markdown(f'<div class="section-label">{text}</div>', unsafe_allow_html=True)


def threat_badge(level: str) -> str:
    """Returns HTML for an inline colored pill. Caller wraps in st.markdown(..., unsafe_allow_html=True)."""
    color = THREAT_COLORS.get(level.upper(), TEXT_MUTED)
    return (
        f'<span class="threat-pill" style="background-color:{color}22;'
        f'border:1px solid {color};color:{color};">{level.upper()}</span>'
    )


def threat_level_from_impact(impact: float) -> str:
    """Single shared definition of threat classification — used by
    Home, AI Intelligence, and Threat Level pages so the number
    doesn't quietly diverge between pages."""
    if impact <= 2:
        return "LOW"
    elif impact <= 10:
        return "MEDIUM"
    return "HIGH"


def kpi_card(label: str, value: str, accent: str = AMBER, sub: str = None):
    """Custom KPI card with a colored accent bar (used where st.metric's
    fixed amber top-border isn't semantically right, e.g. fatality counts
    that should read as red)."""
    sub_html = f'<div style="color:{TEXT_MUTED};font-size:0.7rem;margin-top:0.15rem;">{sub}</div>' if sub else ""
    st.markdown(f"""
    <div class="ops-card" style="border-top:3px solid {accent};">
        <div style="color:{TEXT_MUTED};font-size:0.7rem;letter-spacing:0.08em;
                    text-transform:uppercase;">{label}</div>
        <div style="font-size:1.6rem;font-weight:700;font-family:'JetBrains Mono',monospace;
                    margin-top:0.2rem;">{value}</div>
        {sub_html}
    </div>
    """, unsafe_allow_html=True)


def empty_state(message: str):
    st.markdown(f"""
    <div class="ops-card" style="text-align:center;color:{TEXT_MUTED};padding:2.5rem;">
        ⚠ {message}
    </div>
    """, unsafe_allow_html=True)
