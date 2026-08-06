import streamlit as st
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

from utils.data_loader import load_data
from utils.theme import inject_css, AMBER
from utils.components import (
    classification_banner, page_header, section_label,
    threat_badge, kpi_card
)

st.set_page_config(page_title="Threat Level Prediction", page_icon="🚨", layout="wide")
inject_css()

page_header("🚨", "AI Threat Level Prediction System", "Casualty-based RandomForest risk classifier")
classification_banner("THREAT LEVEL")


@st.cache_resource
def train_threat_model():
    df = load_data()

    df = df[[
        "country_txt", "region_txt", "attacktype1_txt",
        "weaptype1_txt", "targtype1_txt", "nkill", "nwound"
    ]].dropna()

    df["impact"] = df["nkill"] + df["nwound"]

    def classify_threat(x):
        if x <= 2:
            return "LOW"
        elif x <= 10:
            return "MEDIUM"
        return "HIGH"

    df["threat_level"] = df["impact"].apply(classify_threat)

    encoders = {}
    for col in ["country_txt", "region_txt", "attacktype1_txt", "weaptype1_txt", "targtype1_txt"]:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        encoders[col] = le

    target_encoder = LabelEncoder()
    df["threat_level"] = target_encoder.fit_transform(df["threat_level"])

    X = df.drop(columns=["threat_level", "impact"])
    y = df["threat_level"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=200, max_depth=16, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)

    raw_df = load_data()[[
        "country_txt", "region_txt", "attacktype1_txt", "weaptype1_txt", "targtype1_txt"
    ]].dropna()

    return model, encoders, target_encoder, raw_df


with st.spinner("Loading threat classification model..."):
    model, encoders, target_encoder, raw_df = train_threat_model()

section_label("Input Parameters")

col1, col2, col3 = st.columns(3)

with col1:
    country = st.selectbox("Country", sorted(raw_df["country_txt"].unique()))
    region = st.selectbox("Region", sorted(raw_df["region_txt"].unique()))
with col2:
    attack = st.selectbox("Attack Type", sorted(raw_df["attacktype1_txt"].unique()))
    weapon = st.selectbox("Weapon Type", sorted(raw_df["weaptype1_txt"].unique()))
with col3:
    target = st.selectbox("Target Type", sorted(raw_df["targtype1_txt"].unique()))
    nkill = st.number_input("Number Killed", 0, 1000, 0)
    nwound = st.number_input("Number Wounded", 0, 1000, 0)

if st.button("🚨 Predict Threat Level", use_container_width=True):

    input_data = np.array([[
        encoders["country_txt"].transform([country])[0],
        encoders["region_txt"].transform([region])[0],
        encoders["attacktype1_txt"].transform([attack])[0],
        encoders["weaptype1_txt"].transform([weapon])[0],
        encoders["targtype1_txt"].transform([target])[0],
        nkill,
        nwound
    ]])

    prediction = model.predict(input_data)
    probability = model.predict_proba(input_data)

    result = target_encoder.inverse_transform(prediction)[0]
    confidence = np.max(probability) * 100

    section_label("Prediction Result")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            f'<div class="ops-card"><div style="color:#8a9599;font-size:0.7rem;'
            f'text-transform:uppercase;letter-spacing:0.08em;">Threat Level</div>'
            f'<div style="margin-top:0.5rem;">{threat_badge(result)}</div></div>',
            unsafe_allow_html=True
        )
    with c2:
        kpi_card("Confidence Score", f"{confidence:.2f}%", accent=AMBER)

    section_label("Probability Distribution")
    st.bar_chart(dict(zip(target_encoder.classes_, probability[0])))
