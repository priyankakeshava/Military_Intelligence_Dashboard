import streamlit as st
import plotly.express as px

from utils.data_loader import load_data
from utils.insights import summarize_dataset
from utils.theme import AMBER, GREEN, RED, inject_css, style_fig
from utils.components import classification_banner, kpi_card, page_header, section_label
from utils.state import render_global_filters

st.set_page_config(page_title="Home", page_icon="🏠", layout="wide")
inject_css()

df_raw = load_data()
df = render_global_filters(df_raw)

page_header("🏠", "Strategic Threat Overview", "A polished executive view of the current threat landscape")
classification_banner("HOME", record_count=len(df))

if df.empty:
    st.warning("No records match the current Global Command Filters. Adjust the year range or region in the sidebar.")
    st.stop()

summary = summarize_dataset(df)

st.markdown(
    f"""
    <div class="ops-card" style="margin-bottom:1rem;">
        <div style="font-size:0.78rem;letter-spacing:0.13em;text-transform:uppercase;color:{RED};">Executive brief</div>
        <div style="font-size:1.15rem;margin-top:0.35rem;">
            Between <strong>{summary['top_country']}</strong> and <strong>{summary['top_group']}</strong>, the dataset suggests a <strong>{summary['trend_direction'].lower()}</strong> pattern in <strong>{summary['top_attack'].lower()}</strong>-type incidents, with a <strong>{summary['risk_signal'].lower()}</strong> overall risk signal.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

c1, c2, c3, c4 = st.columns(4)
with c1:
    kpi_card("Incidents", f"{summary['total_incidents']:,}", accent=AMBER)
with c2:
    kpi_card("Fatalities", f"{summary['total_fatalities']:,}", accent=RED)
with c3:
    kpi_card("Injuries", f"{summary['total_injuries']:,}", accent=RED)
with c4:
    kpi_card("Countries", f"{summary['countries_affected']:,}", accent=GREEN)

section_label("Trend and Activity Pattern")

yearly = df.groupby("iyear").size().reset_index(name="Attacks")
fig = px.line(yearly, x="iyear", y="Attacks", markers=True)
fig.update_traces(line_color=AMBER, marker=dict(color=AMBER, size=6))
style_fig(fig, height=360)
st.plotly_chart(fig, use_container_width=True)

section_label("Operational Breakdown")
col1, col2 = st.columns(2)

with col1:
    region_counts = df["region_txt"].value_counts().head(10).reset_index()
    region_counts.columns = ["Region", "Incidents"]
    fig2 = px.bar(region_counts, x="Incidents", y="Region", orientation="h")
    fig2.update_traces(marker_color=AMBER)
    style_fig(fig2, title="Top Regions by Incidents", height=360)
    st.plotly_chart(fig2, use_container_width=True)

with col2:
    attack_counts = df["attacktype1_txt"].value_counts().head(10).reset_index()
    attack_counts.columns = ["Attack Type", "Incidents"]
    fig3 = px.bar(attack_counts, x="Incidents", y="Attack Type", orientation="h")
    fig3.update_traces(marker_color=RED)
    style_fig(fig3, title="Top Attack Types", height=360)
    st.plotly_chart(fig3, use_container_width=True)

st.success("👉 Explore the geospatial and forecasting modules next for a deeper threat picture.")
