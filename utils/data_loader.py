from pathlib import Path

import kagglehub
import pandas as pd
import streamlit as st


@st.cache_data
def load_data() -> pd.DataFrame:
    # Download the GTD dataset from Kaggle
    dataset_path = kagglehub.dataset_download("START-UMD/gtd")

    # Find the CSV inside the downloaded dataset
    csv_files = list(Path(dataset_path).rglob("*.csv"))

    if not csv_files:
        raise FileNotFoundError("No CSV file found in the Kaggle dataset.")

    # Load the dataset
    df = pd.read_csv(
        csv_files[0],
        encoding="latin1",
        low_memory=False
    )

    # Clean casualty columns
    if "nkill" in df.columns:
        df["nkill"] = df["nkill"].fillna(0)

    if "nwound" in df.columns:
        df["nwound"] = df["nwound"].fillna(0)

    return df
