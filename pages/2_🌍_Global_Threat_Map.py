import streamlit as st
import plotly.express as px

from utils.data_loader import load_data
from utils.theme import AMBER, BG_PANEL_ALT, CYAN, GREEN, RED, PLOTLY_COLORWAY, inject_css, style_fig
from utils.components import classification_banner, page_header, section_label, kpi_card
from utils.state import render_global_filters

st.set_page_config(page_title="Global Threat Map", page_icon="🌍", layout="wide")
inject_css()

df_raw = load_data()
df = render_global_filters(df_raw)

page_header("🌍", "Global Threat Map", "Geospatial distribution of incidents in the current filter")
classification_banner("GLOBAL THREAT MAP", record_count=len(df))

st.sidebar.markdown('<div class="section-label">Map Filters</div>', unsafe_allow_html=True)

attack_options = sorted(df["attacktype1_txt"].dropna().unique())
selected_attacks = st.sidebar.multiselect(
    "Attack Type (all if empty)", attack_options, default=[]
)

map_df = df.dropna(subset=["latitude", "longitude"])
if selected_attacks:
    map_df = map_df[map_df["attacktype1_txt"].isin(selected_attacks)]

if map_df.empty:
    st.warning("No geolocated incidents match the current filters.")
    st.stop()

c1, c2, c3 = st.columns(3)
with c1:
    kpi_card("Plotted Incidents", f"{len(map_df):,}", accent=AMBER)
with c2:
    kpi_card("Fatalities (in view)", f"{int(map_df['nkill'].sum()):,}", accent=RED)
with c3:
    kpi_card("Countries (in view)", f"{map_df['country_txt'].nunique()}", accent=GREEN)

section_label("Incident Map")

fig = px.scatter_geo(
    map_df,
    lat="latitude",
    lon="longitude",
    color="attacktype1_txt",
    hover_name="country_txt",
    hover_data=["city", "gname", "nkill"],
    projection="natural earth",
    color_discrete_sequence=PLOTLY_COLORWAY
)
fig.update_geos(
    bgcolor=BG_PANEL_ALT,
    landcolor="#f4f7fb",
    oceancolor="#eff6ff",
    lakecolor="#eff6ff",
    showland=True,
    showocean=True,
    showlakes=True,
    showcountries=True,
    showcoastlines=True,
    coastlinecolor="#cbd5e1",
    countrycolor="#cbd5e1",
    projection_type="natural earth"
)
fig.update_traces(marker=dict(line=dict(width=0.5, color="#ffffff"), opacity=0.85))
style_fig(fig, height=620)
st.plotly_chart(fig, use_container_width=True)

st.info("👈 Global year/region filters apply here too — narrow the Map Filters above for attack-type specifics.")
