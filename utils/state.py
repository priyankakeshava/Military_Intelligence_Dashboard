"""
state.py — Cross-page state.

Two concerns live here:
1. Global command filters (year range + region) that apply on top of
   whatever a page filters locally — set them once in any page's sidebar,
   they follow you everywhere.
2. Dashboard settings (from the Settings page) that other pages actually
   read and act on, instead of being decorative toggles.
"""

import streamlit as st


DEFAULTS = {
    "global_year_range": None,       # set on first init from data min/max
    "global_regions": [],            # empty = all regions
    "settings_default_country": "India",
    "settings_forecast_years": 5,
    "settings_min_confidence": 80,
    "settings_show_probability": True,
    "settings_show_feature_importance": True,
}


def init_state(df):
    """Call once per page, before rendering filters. Idempotent."""
    if "global_year_range" not in st.session_state or st.session_state["global_year_range"] is None:
        st.session_state["global_year_range"] = (
            int(df["iyear"].min()), int(df["iyear"].max())
        )
    for key, val in DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = val


def render_global_filters(df):
    """Renders the Global Command Filters block in the sidebar and returns
    df filtered by year range + region. Every page calls this right after
    load_data() so filtering behavior is identical everywhere."""
    init_state(df)

    st.sidebar.markdown(
        '<div class="section-label">Global Command Filters</div>',
        unsafe_allow_html=True
    )

    year_min, year_max = int(df["iyear"].min()), int(df["iyear"].max())

    year_range = st.sidebar.slider(
        "Year Range",
        min_value=year_min,
        max_value=year_max,
        value=st.session_state["global_year_range"],
        key="global_year_range_widget"
    )
    st.session_state["global_year_range"] = year_range

    regions = sorted(df["region_txt"].dropna().unique())
    selected_regions = st.sidebar.multiselect(
        "Region (all if empty)",
        regions,
        default=st.session_state["global_regions"],
        key="global_regions_widget"
    )
    st.session_state["global_regions"] = selected_regions

    filtered = df[
        (df["iyear"] >= year_range[0]) & (df["iyear"] <= year_range[1])
    ]
    if selected_regions:
        filtered = filtered[filtered["region_txt"].isin(selected_regions)]

    if st.sidebar.button("↺ Reset Global Filters", use_container_width=True):
        st.session_state["global_year_range"] = (year_min, year_max)
        st.session_state["global_regions"] = []
        st.rerun()

    return filtered


def get_settings() -> dict:
    """Read-only accessor other pages use to pull Settings-page values."""
    return {
        "default_country": st.session_state.get("settings_default_country", "India"),
        "forecast_years": st.session_state.get("settings_forecast_years", 5),
        "min_confidence": st.session_state.get("settings_min_confidence", 80),
        "show_probability": st.session_state.get("settings_show_probability", True),
        "show_feature_importance": st.session_state.get("settings_show_feature_importance", True),
    }
