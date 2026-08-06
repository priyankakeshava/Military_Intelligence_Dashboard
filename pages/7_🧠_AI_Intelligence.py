import streamlit as st
import plotly.express as px

from utils.data_loader import load_data
from utils.insights import summarize_dataset
from utils.theme import AMBER, RED, inject_css, style_fig
from utils.components import classification_banner, kpi_card, page_header, section_label, threat_badge
from utils.state import render_global_filters

st.set_page_config(page_title="AI Intelligence Report", page_icon="🧠", layout="wide")
inject_css()

df_raw = load_data()
df = render_global_filters(df_raw)

page_header("🧠", "AI Intelligence Report", "Executive-grade threat intelligence generated from the active dataset")
classification_banner("AI INTELLIGENCE", record_count=len(df))

if df.empty:
    st.warning("No records match the current Global Command Filters.")
    st.stop()

summary = summarize_dataset(df)

section_label("Key Intelligence Indicators")

c1, c2, c3, c4 = st.columns(4)
with c1:
    kpi_card("Incidents", f"{summary['total_incidents']:,}", accent=AMBER)
with c2:
    kpi_card("Fatalities", f"{summary['total_fatalities']:,}", accent=RED)
with c3:
    kpi_card("Injuries", f"{summary['total_injuries']:,}", accent=RED)
with c4:
    st.markdown(
        f'<div class="ops-card"><div style="color:#8a9599;font-size:0.7rem;text-transform:uppercase;letter-spacing:0.08em;">Risk Signal</div><div style="margin-top:0.5rem;">{threat_badge(summary["risk_signal"])}</div></div>',
        unsafe_allow_html=True,
    )

section_label("Executive Summary")

st.markdown(
    f"""
    <div class="ops-card">
        <strong>Operational assessment:</strong> the current dataset indicates <strong>{summary['total_incidents']:,}</strong> incidents across <strong>{summary['countries_affected']}</strong> countries, with <strong>{summary['total_fatalities']:,}</strong> fatalities and <strong>{summary['total_injuries']:,}</strong> injuries.
        <br><br>
        The most active region of concern is <strong>{summary['top_country']}</strong>, while <strong>{summary['top_group']}</strong> is the most frequently observed actor. The dominant pattern is <strong>{summary['top_attack'].lower()}</strong>-type activity using <strong>{summary['top_weapon'].lower()}</strong>.
        <br><br>
        Overall risk posture is <strong>{summary['risk_signal'].lower()}</strong> and the trend is <strong>{summary['trend_direction'].lower()}</strong>.
    </div>
    """,
    unsafe_allow_html=True,
)

section_label("Most Affected Countries")
top_countries = df["country_txt"].value_counts().head(10)
fig = px.bar(top_countries, x=top_countries.values, y=top_countries.index, orientation="h", labels={"x": "Incidents", "y": "Country"})
fig.update_traces(marker_color=AMBER)
style_fig(fig, height=380)
st.plotly_chart(fig, use_container_width=True)

section_label("Threat Actor Activity")
top_groups = df["gname"].value_counts().head(10)
fig2 = px.bar(top_groups, x=top_groups.values, y=top_groups.index, orientation="h", labels={"x": "Attacks", "y": "Group"})
fig2.update_traces(marker_color=RED)
style_fig(fig2, height=380)
st.plotly_chart(fig2, use_container_width=True)

section_label("Decision Support")
recommendation = (
    f"1. Prioritize surveillance in {summary['top_country']}\n\n"
    f"2. Monitor activity linked to {summary['top_group']}\n\n"
    f"3. Strengthen protection around high-frequency {summary['top_attack'].lower()} targets\n\n"
    f"4. Expand intelligence-sharing workflows for {summary['top_weapon'].lower()}-related incidents"
)
st.success(recommendation)

report = f"""==============================
AI INTELLIGENCE REPORT
==============================

Total Incidents : {summary['total_incidents']}
Fatalities : {summary['total_fatalities']}
Injuries : {summary['total_injuries']}
Risk Signal : {summary['risk_signal']}
Trend : {summary['trend_direction']}

Top Country : {summary['top_country']}
Top Group : {summary['top_group']}
Most Common Attack : {summary['top_attack']}
Most Common Weapon : {summary['top_weapon']}

Recommendations
{recommendation}
"""

st.download_button("📄 Download Intelligence Report", report, file_name="AI_Intelligence_Report.txt")
