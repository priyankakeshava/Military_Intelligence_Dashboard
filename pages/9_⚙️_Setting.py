import streamlit as st

from utils.data_loader import load_data
from utils.theme import inject_css, AMBER, GREEN
from utils.components import classification_banner, page_header, section_label, kpi_card
from utils.state import init_state

st.set_page_config(page_title="Settings", page_icon="⚙️", layout="wide")
inject_css()

df = load_data()
init_state(df)

page_header("⚙️", "Dashboard Settings", "These values are read live by other modules — no restart needed")
classification_banner("SETTINGS")

st.info(
    "Settings on this page write directly to session state. "
    "**Default Country** pre-selects on Country Analysis & Forecasting. "
    "**Default Forecast Years** sets the initial Forecasting slider. "
    "**Minimum Confidence** flags low-confidence predictions on Attack Prediction."
)

section_label("Default Dashboard")

countries = sorted(df["country_txt"].dropna().unique())
current_default = st.session_state.get("settings_default_country", "India")
default_idx = countries.index(current_default) if current_default in countries else 0

country = st.selectbox("Default Country", countries, index=default_idx)
st.session_state["settings_default_country"] = country

forecast_years = st.slider(
    "Default Forecast Years", 1, 10,
    st.session_state.get("settings_forecast_years", 5)
)
st.session_state["settings_forecast_years"] = forecast_years

confidence = st.slider(
    "Minimum Prediction Confidence (%)", 50, 100,
    st.session_state.get("settings_min_confidence", 80)
)
st.session_state["settings_min_confidence"] = confidence

section_label("Attack Prediction Display")

show_probability = st.checkbox(
    "Show Full Probability Distribution",
    value=st.session_state.get("settings_show_probability", True)
)
st.session_state["settings_show_probability"] = show_probability

show_feature_importance = st.checkbox(
    "Show Model Feature Importance",
    value=st.session_state.get("settings_show_feature_importance", True)
)
st.session_state["settings_show_feature_importance"] = show_feature_importance

section_label("Dataset Information")

try:
    st.success("Dataset Loaded Successfully")

    c1, c2, c3 = st.columns(3)
    with c1:
        kpi_card("Rows", f"{df.shape[0]:,}", accent=AMBER)
    with c2:
        kpi_card("Columns", f"{df.shape[1]}", accent=AMBER)
    with c3:
        kpi_card("Countries", f"{df['country_txt'].nunique()}", accent=GREEN)

except FileNotFoundError:
    st.error("Dataset not found. Place `globalterrorism.csv` inside the `data/` folder.")

st.divider()

col1, col2 = st.columns(2)
with col1:
    if st.button("💾 Save Settings", use_container_width=True):
        st.success("Settings saved to session — active immediately on every module.")
        st.balloons()
with col2:
    if st.button("🔄 Reset to Defaults", use_container_width=True):
        for key in [
            "settings_default_country", "settings_forecast_years",
            "settings_min_confidence", "settings_show_probability",
            "settings_show_feature_importance", "global_year_range", "global_regions"
        ]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()
