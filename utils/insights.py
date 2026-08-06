from __future__ import annotations

from typing import Any, Dict

import pandas as pd


def summarize_dataset(df: pd.DataFrame) -> Dict[str, Any]:
    """Create a compact intelligence summary for the dashboard."""
    if df.empty:
        return {
            "total_incidents": 0,
            "total_fatalities": 0,
            "total_injuries": 0,
            "countries_affected": 0,
            "top_country": "N/A",
            "top_group": "N/A",
            "top_attack": "N/A",
            "top_weapon": "N/A",
            "risk_signal": "LOW",
            "trend_direction": "Stable",
        }

    total_incidents = int(len(df))
    total_fatalities = int(df["nkill"].sum())
    total_injuries = int(df["nwound"].sum())
    countries_affected = int(df["country_txt"].nunique())

    top_country = df["country_txt"].dropna().mode().iloc[0] if not df["country_txt"].dropna().empty else "N/A"
    top_group = df["gname"].dropna().mode().iloc[0] if not df["gname"].dropna().empty else "N/A"
    top_attack = df["attacktype1_txt"].dropna().mode().iloc[0] if not df["attacktype1_txt"].dropna().empty else "N/A"
    top_weapon = df["weaptype1_txt"].dropna().mode().iloc[0] if not df["weaptype1_txt"].dropna().empty else "N/A"

    impact_score = total_fatalities + total_injuries / 2
    if impact_score > 1000:
        risk_signal = "HIGH"
    elif impact_score > 250:
        risk_signal = "MEDIUM"
    else:
        risk_signal = "LOW"

    yearly_counts = df.groupby("iyear").size()
    if len(yearly_counts) >= 2:
        trend_direction = "Rising" if yearly_counts.iloc[-1] > yearly_counts.iloc[0] else "Declining"
    else:
        trend_direction = "Stable"

    return {
        "total_incidents": total_incidents,
        "total_fatalities": total_fatalities,
        "total_injuries": total_injuries,
        "countries_affected": countries_affected,
        "top_country": top_country,
        "top_group": top_group,
        "top_attack": top_attack,
        "top_weapon": top_weapon,
        "risk_signal": risk_signal,
        "trend_direction": trend_direction,
    }
