import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

from sklearn.linear_model import LinearRegression

from utils.data_loader import load_data
from utils.theme import inject_css, style_fig, AMBER, RED, GREEN, CYAN
from utils.components import classification_banner, page_header, section_label, kpi_card
from utils.state import get_settings

st.set_page_config(page_title="Forecasting", page_icon="📈", layout="wide")
inject_css()

settings = get_settings()

page_header("📈", "Terrorism Attack Forecasting", "Linear projection of future attack volume from historical GTD trends")
classification_banner("FORECASTING")

df = load_data()

countries = sorted(df["country_txt"].dropna().unique())
default_idx = countries.index(settings["default_country"]) if settings["default_country"] in countries else 0

st.sidebar.markdown('<div class="section-label">Forecast Settings</div>', unsafe_allow_html=True)
country = st.sidebar.selectbox("Select Country", countries, index=default_idx)
forecast_years = st.sidebar.slider("Forecast Years", 1, 10, settings["forecast_years"])

country_df = df[df["country_txt"] == country]

yearly = country_df.groupby("iyear").size().reset_index(name="Attacks").sort_values("iyear")

if len(yearly) < 5:
    st.warning("Not enough historical data for forecasting this country.")
    st.stop()

X = yearly[["iyear"]]
y = yearly["Attacks"]

model = LinearRegression()
model.fit(X, y)

last_year = yearly["iyear"].max()
future_years = np.arange(last_year + 1, last_year + forecast_years + 1)
future_df = pd.DataFrame({"iyear": future_years})

predictions = np.maximum(model.predict(future_df), 0)

forecast = pd.DataFrame({
    "Year": future_years,
    "Forecasted Attacks": predictions.astype(int)
})

section_label("Historical + Forecast")

fig = go.Figure()
fig.add_trace(go.Scatter(x=yearly["iyear"], y=yearly["Attacks"], mode="lines+markers",
                          name="Historical", line=dict(color=CYAN)))
fig.add_trace(go.Scatter(x=forecast["Year"], y=forecast["Forecasted Attacks"], mode="lines+markers",
                          name="Forecast", line=dict(color=AMBER, dash="dash")))
style_fig(fig, title=f"Attack Forecast for {country}", height=500)
st.plotly_chart(fig, use_container_width=True)

section_label("Forecast Results")

st.dataframe(forecast, use_container_width=True, hide_index=True)

historical_last = yearly.iloc[-1]["Attacks"]
forecast_last = forecast.iloc[-1]["Forecasted Attacks"]
growth = ((forecast_last - historical_last) / max(historical_last, 1)) * 100

section_label("Growth & Risk Assessment")

c1, c2, c3 = st.columns(3)
with c1:
    kpi_card("Current Attacks", f"{int(historical_last)}", accent=AMBER)
with c2:
    kpi_card(f"Forecast ({forecast_years}y)", f"{int(forecast_last)}", accent=AMBER)
with c3:
    accent = GREEN if growth < 0 else (AMBER if growth < 15 else RED)
    kpi_card("Growth %", f"{growth:.2f}%", accent=accent)

if growth < 0:
    st.success("🟢 Threat Trend: Decreasing")
elif growth < 15:
    st.warning("🟡 Threat Trend: Stable")
else:
    st.error("🔴 Threat Trend: Increasing")

csv = forecast.to_csv(index=False)

st.download_button(
    label="📥 Download Forecast CSV",
    data=csv,
    file_name=f"{country}_forecast.csv",
    mime="text/csv"
)
