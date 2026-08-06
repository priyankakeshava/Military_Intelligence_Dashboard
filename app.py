from pathlib import Path

import streamlit as st

from utils.components import classification_banner, kpi_card
from utils.data_loader import load_data
from utils.state import init_state
from utils.theme import AMBER, GREEN, RED, TEXT_MUTED, inject_css


def resolve_data_path() -> Path:
    """Return the GTD CSV path relative to this file, not the current working directory."""
    return (Path(__file__).resolve().parent / "data" / "globalterrorism.csv").resolve()


def main() -> None:
    st.set_page_config(
        page_title="AI Military Intelligence Dashboard",
        page_icon="🛡",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    inject_css()

    try:
        df = load_data()
    except FileNotFoundError:
        st.error(
            f"The GTD dataset was not found at {resolve_data_path()}. "
            "Place the CSV in the data folder and restart the app."
        )
        st.stop()

    init_state(df)

    st.markdown("# 🛡 AI-Based Military Intelligence Dashboard")
    st.markdown(
        f'<div style="color:{TEXT_MUTED};font-size:0.95rem;margin-top:-0.8rem;">'
        f'An intelligence-grade dashboard for analyzing global threat patterns using the Global Terrorism Database (GTD).'
        f'</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="ops-card" style="margin-bottom:1.2rem;">
            <div style="font-size:0.78rem;letter-spacing:0.13em;text-transform:uppercase;color:{AMBER};">Mission Focus</div>
            <div style="font-size:1.05rem;margin-top:0.35rem;">
                This platform combines data exploration, forecasting, and AI-assisted intelligence reporting into a single operational workspace for strategic analysis.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    classification_banner("COMMAND CONSOLE", record_count=len(df))

    # --------------------------------------------------------
    # Top-line KPIs
    # --------------------------------------------------------

    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        kpi_card("Total Incidents", f"{len(df):,}", accent=AMBER)
    with c2:
        kpi_card("Fatalities", f"{int(df['nkill'].sum()):,}", accent=RED)
    with c3:
        kpi_card("Injured", f"{int(df['nwound'].sum()):,}", accent=RED)
    with c4:
        kpi_card("Countries Affected", f"{df['country_txt'].nunique()}", accent=GREEN)
    with c5:
        kpi_card("Active Groups Tracked", f"{df['gname'].nunique():,}", accent=AMBER)

    st.markdown("<br>", unsafe_allow_html=True)

    # --------------------------------------------------------
    # Module navigation
    # --------------------------------------------------------

    st.markdown('<div class="section-label">Core Modules</div>', unsafe_allow_html=True)

    modules = [
        ("🏠", "Home", "Dashboard summary & trend overview", "pages/1_🏠_Home.py"),
        ("🌍", "Global Threat Map", "Geospatial incident view", "pages/2_🌍_Global_Threat_Map.py"),
        ("🌎", "Country Analysis", "Deep-dive intelligence report per country", "pages/3_🌎_Country_Analysis.py"),
        ("🤖", "Attack Prediction", "ML-based attack type classifier", "pages/4_🤖_Attack_Prediction.py"),
        ("🚨", "Threat Level", "Casualty-based risk scoring", "pages/5_🚨_Threat_Level.py"),
        ("📈", "Forecasting", "Attack volume projection", "pages/6_📈_Forecasting.py"),
        ("🧠", "AI Intelligence", "Auto-generated executive briefing", "pages/7_🧠_AI_Intelligence.py"),
        ("📊", "Data Explorer", "Filter, search, and export raw records", "pages/8_📊_Data_Explorer.py"),
        ("⚙️", "Settings", "Configure defaults used across all modules", "pages/9_⚙️_Setting.py"),
    ]

    cols = st.columns(3)
    for i, (icon, name, desc, path) in enumerate(modules):
        with cols[i % 3]:
            st.markdown(
                f"""
                <div class="ops-card" style="margin-bottom:1rem;min-height:110px;">
                    <div style="font-size:1.4rem;">{icon}</div>
                    <div style="font-family:'Orbitron',sans-serif;font-weight:700;
                                letter-spacing:0.04em;text-transform:uppercase;
                                margin-top:0.3rem;">{name}</div>
                    <div style="color:{TEXT_MUTED};font-size:0.78rem;margin-top:0.3rem;">{desc}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.page_link(path, label=f"Open {name} →")

    st.markdown("<br>", unsafe_allow_html=True)
    st.info(
        "👈 Use the sidebar to navigate directly. Global year/region filters set on any page persist across the whole session."
    )


if __name__ == "__main__":
    main()
