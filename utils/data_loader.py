from pathlib import Path

import pandas as pd
import streamlit as st


def resolve_data_path() -> Path:
    """Resolve the GTD CSV path from the project root."""
    return (Path(__file__).resolve().parents[1] / "data" / "globalterrorism.csv").resolve()


@st.cache_data
def load_data():
    """
    Loads the Global Terrorism Database CSV and does light cleaning
    that every page relies on (fills missing kill/wound counts with 0
    so .sum() and metrics don't break).
    """
    data_path = resolve_data_path()
    if not data_path.exists():
        raise FileNotFoundError(f"Could not find GTD data file at {data_path}")

    df = pd.read_csv(data_path, encoding="latin1", low_memory=False)

    df["nkill"] = df["nkill"].fillna(0)
    df["nwound"] = df["nwound"].fillna(0)

    return df
