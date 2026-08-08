import streamlit as st
import plotly.express as px
import math

try:
    import pydeck as pdk
    _PYDECK_AVAILABLE = True
except Exception:
    pdk = None
    _PYDECK_AVAILABLE = False

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

# Performance controls
# Lower downsample limit to keep serialized payloads small
DOWNSAMPLE_LIMIT = 20000
auto_downsample = st.sidebar.checkbox("Auto-downsample large maps", value=True)
use_pydeck = st.sidebar.checkbox("Use WebGL map (pydeck) when available", value=True)
show_full_on_map = st.sidebar.checkbox("Show full dataset on map (may be slow)", value=False)

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
# Determine whether to downsample for plotting
map_df_display = map_df
was_downsampled = False
if auto_downsample and not show_full_on_map and len(map_df) > DOWNSAMPLE_LIMIT:
    map_df_display = map_df.sample(DOWNSAMPLE_LIMIT, random_state=42)
    was_downsampled = True

# Reduce hover payload to speed up serialization
hover_fields = ["city", "nkill"]

# If user selected pydeck and pydeck is available, render a WebGL map
if use_pydeck and _PYDECK_AVAILABLE:
    # helper: convert hex color to [r,g,b]
    def hex_to_rgb(h):
        h = h.lstrip("#")
        return [int(h[i:i+2], 16) for i in (0, 2, 4)]

    attack_types = list(map_df["attacktype1_txt"].dropna().unique())
    color_palette = [hex_to_rgb(c) for c in PLOTLY_COLORWAY]
    color_map = {t: color_palette[i % len(color_palette)] for i, t in enumerate(attack_types)}

    display_df = map_df_display.copy()
    display_df["color"] = display_df["attacktype1_txt"].map(lambda x: color_map.get(x, [120, 120, 120]))

    # Ensure positions for pydeck
    display_df = display_df.dropna(subset=["latitude", "longitude"]).reset_index(drop=True)

    initial_lat = float(display_df["latitude"].mean()) if not display_df["latitude"].isnull().all() else 0.0
    initial_lon = float(display_df["longitude"].mean()) if not display_df["longitude"].isnull().all() else 0.0

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=display_df,
        get_position=["longitude", "latitude"],
        get_radius=20000,
        get_fill_color="color",
        pickable=True,
        opacity=0.8,
    )

    view_state = pdk.ViewState(latitude=initial_lat, longitude=initial_lon, zoom=1)
    deck = pdk.Deck(layers=[layer], initial_view_state=view_state)
    if was_downsampled:
        st.info(f"Map downsampled to {len(display_df):,} points for performance.")
    st.pydeck_chart(deck)
else:
    # Fallback to Plotly (SVG/Canvas). Use downsampled display and lighter hover payload.
    if was_downsampled:
        st.info(f"Map downsampled to {len(map_df_display):,} points for performance.")

    fig = px.scatter_geo(
        map_df_display,
        lat="latitude",
        lon="longitude",
        color="attacktype1_txt",
        hover_name="country_txt",
        hover_data=hover_fields,
        projection="natural earth",
        color_discrete_sequence=PLOTLY_COLORWAY,
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
