import streamlit as st
import plotly.express as px

from utils.data_loader import load_data
from utils.theme import inject_css, style_fig, AMBER, RED, GREEN
from utils.components import (
    classification_banner, page_header, section_label, kpi_card,
    threat_badge, threat_level_from_impact
)
from utils.state import render_global_filters, get_settings

st.set_page_config(page_title="Country Analysis", page_icon="🌎", layout="wide")
inject_css()

df_raw = load_data()
df = render_global_filters(df_raw)
settings = get_settings()

page_header("🌎", "Country Analysis", "Intelligence report scoped to a single country")
classification_banner("COUNTRY ANALYSIS", record_count=len(df))

countries = sorted(df["country_txt"].dropna().unique())

if not countries:
    st.warning("No countries in the current Global Command Filters.")
    st.stop()

default_idx = countries.index(settings["default_country"]) if settings["default_country"] in countries else 0

country = st.sidebar.selectbox("Select Country", countries, index=default_idx)

country_df = df[df["country_txt"] == country]

st.header(f"Intelligence Report : {country}")

impact = country_df["nkill"].sum() + country_df["nwound"].sum()
avg_impact = (country_df["nkill"] + country_df["nwound"]).mean() if len(country_df) else 0
threat = threat_level_from_impact(avg_impact)

st.markdown(
    f'Overall Threat Assessment: {threat_badge(threat)}',
    unsafe_allow_html=True
)

st.markdown("<br>", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)

with c1:
    kpi_card("Incidents", f"{len(country_df):,}", accent=AMBER)
with c2:
    kpi_card("Fatalities", f"{int(country_df['nkill'].sum()):,}", accent=RED)
with c3:
    kpi_card("Injured", f"{int(country_df['nwound'].sum()):,}", accent=RED)
with c4:
    kpi_card("Groups Active", f"{country_df['gname'].nunique()}", accent=GREEN)

if country_df.empty:
    st.warning(f"No incidents for {country} within the current Global Command Filters.")
    st.stop()

section_label("Attacks Over Time & Attack Types")

left, right = st.columns(2)

with left:
    yearly = country_df.groupby("iyear").size().reset_index(name="Attacks")
    fig = px.line(yearly, x="iyear", y="Attacks", markers=True)
    fig.update_traces(line_color=AMBER, marker=dict(color=AMBER))
    style_fig(fig, title="Attacks Over Years", height=380)
    st.plotly_chart(fig, use_container_width=True)

with right:
    attack = country_df.groupby("attacktype1_txt").size().reset_index(name="Count")
    fig = px.pie(attack, names="attacktype1_txt", values="Count", hole=0.45)
    style_fig(fig, title="Attack Types", height=380)
    st.plotly_chart(fig, use_container_width=True)

section_label("Organizations & Weapons")

left, right = st.columns(2)

with left:
    groups = (
        country_df.groupby("gname").size().reset_index(name="Attacks")
        .sort_values("Attacks", ascending=False).head(10)
    )
    fig = px.bar(groups, x="Attacks", y="gname", orientation="h")
    fig.update_traces(marker_color=RED)
    style_fig(fig, title="Top Terrorist Organizations", height=380)
    st.plotly_chart(fig, use_container_width=True)

with right:
    weapon = (
        country_df.groupby("weaptype1_txt").size().reset_index(name="Count")
        .sort_values("Count", ascending=False)
    )
    fig = px.bar(weapon, x="weaptype1_txt", y="Count")
    fig.update_traces(marker_color=AMBER)
    style_fig(fig, title="Weapon Types", height=380)
    st.plotly_chart(fig, use_container_width=True)

section_label("Incident Locations")

map_df = country_df.dropna(subset=["latitude", "longitude"])

if not map_df.empty:
    fig = px.scatter_geo(
        map_df,
        lat="latitude",
        lon="longitude",
        hover_name="city",
        hover_data={
            "country_txt": True, "iyear": True, "attacktype1_txt": True,
            "gname": True, "nkill": True, "latitude": False, "longitude": False
        },
        color="attacktype1_txt",
        projection="natural earth"
    )
    fig.update_geos(
        bgcolor="#12181a", landcolor="#1a2224", oceancolor="#0a0e0f",
        showocean=True, coastlinecolor="#243033", fitbounds="locations"
    )
    style_fig(fig, title=f"Terrorist Incidents in {country}", height=550)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No geolocated incidents available for this country/filter combination.")

section_label("Incident Details")

cols = [
    "iyear", "city", "attacktype1_txt", "targtype1_txt",
    "weaptype1_txt", "gname", "nkill", "nwound"
]

st.dataframe(country_df[cols], use_container_width=True)

csv = country_df.to_csv(index=False).encode()

st.download_button(
    "⬇ Download Country Data",
    csv,
    file_name=f"{country}.csv",
    mime="text/csv"
)
