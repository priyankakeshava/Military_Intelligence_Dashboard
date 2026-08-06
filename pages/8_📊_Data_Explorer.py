import streamlit as st
import plotly.express as px

from utils.data_loader import load_data
from utils.theme import inject_css, style_fig, AMBER, RED, GREEN
from utils.components import classification_banner, page_header, section_label, kpi_card
from utils.state import render_global_filters

st.set_page_config(page_title="Data Explorer", page_icon="📊", layout="wide")
inject_css()

df_raw = load_data()
df = render_global_filters(df_raw)

page_header("📊", "Global Terrorism Data Explorer", "Filter, search, visualize, and export the GTD dataset")
classification_banner("DATA EXPLORER", record_count=len(df))

st.sidebar.markdown('<div class="section-label">Additional Filters</div>', unsafe_allow_html=True)

countries = sorted(df["country_txt"].dropna().unique())
selected_country = st.sidebar.multiselect("Country", countries, default=[])

attack_types = sorted(df["attacktype1_txt"].dropna().unique())
selected_attack = st.sidebar.multiselect("Attack Type", attack_types, default=[])

weapons = sorted(df["weaptype1_txt"].dropna().unique())
selected_weapon = st.sidebar.multiselect("Weapon Type", weapons, default=[])

groups = sorted(df["gname"].dropna().unique())
selected_group = st.sidebar.multiselect("Terrorist Group", groups, default=[])

filtered_df = df.copy()

if selected_country:
    filtered_df = filtered_df[filtered_df["country_txt"].isin(selected_country)]
if selected_attack:
    filtered_df = filtered_df[filtered_df["attacktype1_txt"].isin(selected_attack)]
if selected_weapon:
    filtered_df = filtered_df[filtered_df["weaptype1_txt"].isin(selected_weapon)]
if selected_group:
    filtered_df = filtered_df[filtered_df["gname"].isin(selected_group)]

search = st.text_input("🔍 Search by City or Country")

if search:
    filtered_df = filtered_df[
        filtered_df["city"].fillna("").str.contains(search, case=False)
        | filtered_df["country_txt"].fillna("").str.contains(search, case=False)
    ]

section_label("Dataset Summary")

c1, c2, c3, c4 = st.columns(4)
with c1:
    kpi_card("Incidents", f"{len(filtered_df):,}", accent=AMBER)
with c2:
    kpi_card("Countries", f"{filtered_df['country_txt'].nunique()}", accent=GREEN)
with c3:
    kpi_card("Fatalities", f"{int(filtered_df['nkill'].sum()):,}", accent=RED)
with c4:
    kpi_card("Injuries", f"{int(filtered_df['nwound'].sum()):,}", accent=RED)

section_label("Filtered Dataset")

st.dataframe(filtered_df, use_container_width=True, height=420)

csv = filtered_df.to_csv(index=False)
st.download_button("📥 Download Filtered Data", csv, file_name="Filtered_GTD_Data.csv", mime="text/csv")

section_label("Visual Analytics")

tab1, tab2, tab3 = st.tabs(["Country", "Attack Type", "Weapon Type"])

with tab1:
    country_chart = filtered_df["country_txt"].value_counts().head(10).reset_index()
    country_chart.columns = ["Country", "Incidents"]
    fig = px.bar(country_chart, x="Country", y="Incidents", color="Incidents",
                 color_continuous_scale=["#3a2b00", AMBER])
    style_fig(fig, title="Top 10 Countries", height=380)
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    attack_chart = filtered_df["attacktype1_txt"].value_counts().reset_index()
    attack_chart.columns = ["Attack Type", "Count"]
    fig = px.pie(attack_chart, names="Attack Type", values="Count", hole=0.45)
    style_fig(fig, title="Attack Type Distribution", height=420)
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    weapon_chart = filtered_df["weaptype1_txt"].value_counts().reset_index()
    weapon_chart.columns = ["Weapon", "Count"]
    fig = px.bar(weapon_chart, x="Weapon", y="Count", color="Count",
                 color_continuous_scale=["#4a0f0c", RED])
    style_fig(fig, title="Weapon Type Distribution", height=420)
    st.plotly_chart(fig, use_container_width=True)

section_label("Missing Values")

missing = filtered_df.isnull().sum().sort_values(ascending=False).reset_index()
missing.columns = ["Column", "Missing Values"]
st.dataframe(missing, use_container_width=True, height=250)

section_label("Dataset Information")

i1, i2, i3 = st.columns(3)
with i1:
    kpi_card("Rows", f"{filtered_df.shape[0]:,}", accent=AMBER)
with i2:
    kpi_card("Columns", f"{filtered_df.shape[1]}", accent=AMBER)
with i3:
    kpi_card("Memory (MB)", f"{round(filtered_df.memory_usage(deep=True).sum()/1024**2, 2)}", accent=AMBER)

with st.expander("Column Names"):
    st.write(filtered_df.columns.tolist())
