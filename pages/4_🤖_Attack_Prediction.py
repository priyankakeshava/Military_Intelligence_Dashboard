import streamlit as st
import joblib
import pandas as pd

from utils.data_loader import load_data
from utils.theme import inject_css, AMBER, RED, GREEN
from utils.components import classification_banner, page_header, section_label, kpi_card
from utils.state import get_settings

st.set_page_config(page_title="Attack Prediction", page_icon="🤖", layout="wide")
inject_css()

settings = get_settings()

page_header("🤖", "Attack Type Prediction", "ML classifier trained on historical GTD incident features")
classification_banner("ATTACK PREDICTION")

# -------------------------
# Load Model Artifacts
# -------------------------

try:
    model = joblib.load("models/attack_prediction_model.pkl")
    encoders = joblib.load("models/feature_encoders.pkl")
    target_encoder = joblib.load("models/target_encoder.pkl")
except FileNotFoundError:
    st.error(
        "Model files not found in `models/`. Run `train_attack_model.py` first to generate "
        "`attack_prediction_model.pkl`, `feature_encoders.pkl`, and `target_encoder.pkl`."
    )
    st.stop()

df = load_data()
df = df.dropna(subset=["country_txt", "region_txt", "weaptype1_txt", "targtype1_txt", "gname"])

section_label("Incident Parameters")

with st.form("prediction_form"):

    col1, col2 = st.columns(2)

    with col1:
        country = st.selectbox("🌍 Country", sorted(df["country_txt"].unique()))
        region = st.selectbox("🌎 Region", sorted(df["region_txt"].unique()))
        weapon = st.selectbox("🔫 Weapon Type", sorted(df["weaptype1_txt"].unique()))
        target = st.selectbox("🎯 Target Type", sorted(df["targtype1_txt"].unique()))

    with col2:
        group = st.selectbox("👥 Terrorist Group", sorted(df["gname"].unique()))
        success = st.selectbox("✅ Attack Successful?", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
        suicide = st.selectbox("💣 Suicide Attack?", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
        nkill = st.number_input("☠ Number of Fatalities", min_value=0, value=0, step=1)
        nwound = st.number_input("🏥 Number of Injured", min_value=0, value=0, step=1)

    submitted = st.form_submit_button("🚀 Predict Attack Type")

if submitted:

    country_enc = encoders["country_txt"].transform([country])[0]
    region_enc = encoders["region_txt"].transform([region])[0]
    weapon_enc = encoders["weaptype1_txt"].transform([weapon])[0]
    target_enc = encoders["targtype1_txt"].transform([target])[0]
    group_enc = encoders["gname"].transform([group])[0]

    input_df = pd.DataFrame({
        "country_txt": [country_enc], "region_txt": [region_enc],
        "weaptype1_txt": [weapon_enc], "targtype1_txt": [target_enc],
        "gname": [group_enc], "success": [success], "suicide": [suicide],
        "nkill": [nkill], "nwound": [nwound]
    })

    prediction = model.predict(input_df)
    attack_type = target_encoder.inverse_transform(prediction)[0]

    probabilities = model.predict_proba(input_df)
    confidence = probabilities.max() * 100

    section_label("Prediction Result")

    c1, c2 = st.columns(2)
    with c1:
        kpi_card("Predicted Attack Type", attack_type, accent=AMBER)
    with c2:
        accent = GREEN if confidence >= settings["min_confidence"] else RED
        kpi_card("Prediction Confidence", f"{confidence:.2f}%", accent=accent)

    if confidence < settings["min_confidence"]:
        st.warning(
            f"⚠ Confidence ({confidence:.2f}%) is below your configured minimum "
            f"threshold of {settings['min_confidence']}% (see Settings)."
        )

    if settings["show_probability"]:
        section_label("Full Probability Distribution")
        prob_df = pd.DataFrame({
            "Attack Type": target_encoder.inverse_transform(range(len(probabilities[0]))),
            "Probability": probabilities[0]
        }).sort_values("Probability", ascending=False)
        st.dataframe(prob_df, use_container_width=True, hide_index=True)

    if settings["show_feature_importance"]:
        section_label("Model Feature Importance")
        importance_df = pd.DataFrame({
            "Feature": input_df.columns,
            "Importance": model.feature_importances_
        }).sort_values("Importance", ascending=False)
        st.bar_chart(importance_df.set_index("Feature"))
