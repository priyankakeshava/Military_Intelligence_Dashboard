import pandas as pd

from utils.insights import summarize_dataset


def test_summarize_dataset_builds_key_intelligence_summary():
    df = pd.DataFrame(
        {
            "country_txt": ["India", "India", "Pakistan"],
            "gname": ["Group A", "Group B", "Group A"],
            "attacktype1_txt": ["Bombing", "Assassination", "Bombing"],
            "weaptype1_txt": ["Explosives", "Firearms", "Explosives"],
            "nkill": [5, 1, 2],
            "nwound": [10, 0, 5],
            "iyear": [2020, 2021, 2020],
        }
    )

    result = summarize_dataset(df)

    assert result["top_country"] == "India"
    assert result["top_group"] == "Group A"
    assert result["top_attack"] == "Bombing"
    assert result["top_weapon"] == "Explosives"
    assert result["total_incidents"] == 3
    assert result["total_fatalities"] == 8
    assert result["risk_signal"] in {"LOW", "MEDIUM", "HIGH"}
