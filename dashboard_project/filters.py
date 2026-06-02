# filters.py
import pandas as pd
import os

# =========================================================================
# DYNAMIC RELATIVE PATH PATH RESOLUTION (Solves path error on other laptops)
# =========================================================================
# Yeh code automatically check karega ke 'filters.py' kis folder mein hai 
# aur wahan se auto-route karke 'data' folder ka rasta nikal lega.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "Traffic_Collision_Data_from_2010_to_Present (2).csv")


def load_and_clean_data():
    """
    Load data using dynamic relative path and handle basic cleaning.
    """
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(
            f"Dataset file nahi mili! Make sure your dataset is at: {DATA_PATH}"
        )
        
    df = pd.read_csv(DATA_PATH)
    df = df.drop_duplicates()
    df.columns = df.columns.str.strip()

    # Initial Date Conversion
    if "Date Occurred" in df.columns:
        df["Date Occurred"] = pd.to_datetime(df["Date Occurred"], errors="coerce")
        df = df[df["Date Occurred"].notna()]
        df["Year"] = df["Date Occurred"].dt.year
        df["Month"] = df["Date Occurred"].dt.month

    # Null Value Imputation
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].fillna("Unknown")
        else:
            df[col] = df[col].fillna(df[col].median())
            
    return df


# =========================================================================
# YOUR EXISTING FILTERS LOGIC (Kept exactly identical and untouched)
# =========================================================================

def apply_filters(
    df,
    start_date=None,
    end_date=None,
    selected_areas=None,
    max_age=None,
    search_text=None
):
    """
    Apply all dashboard filters and return filtered dataframe.
    """
    filtered_df = df.copy()

    # =========================
    # DATE FILTER
    # =========================
    if "Date Occurred" in filtered_df.columns:

        filtered_df["Date Occurred"] = pd.to_datetime(
            filtered_df["Date Occurred"],
            errors="coerce"
        )

        if start_date:
            filtered_df = filtered_df[
                filtered_df["Date Occurred"] >= pd.to_datetime(start_date)
            ]

        if end_date:
            filtered_df = filtered_df[
                filtered_df["Date Occurred"] <= pd.to_datetime(end_date)
            ]

    # =========================
    # AREA FILTER
    # =========================
    area_col = None

    for col in filtered_df.columns:
        if "AREA" in col.upper():
            area_col = col
            break

    if area_col and selected_areas:
        filtered_df = filtered_df[
            filtered_df[area_col].isin(selected_areas)
        ]

    # =========================
    # AGE FILTER
    # =========================
    if "Victim Age" in filtered_df.columns and max_age:

        filtered_df = filtered_df[
            filtered_df["Victim Age"] <= max_age
        ]

    # =========================
    # SEARCH FILTER
    # =========================
    if search_text:

        filtered_df = filtered_df[
            filtered_df.astype(str)
            .apply(
                lambda row: row.str.contains(
                    search_text,
                    case=False,
                    na=False
                )
            )
            .any(axis=1)
        ]

    return filtered_df


# =========================
# RESET FILTERS
# =========================

def reset_filters():
    return {
        "start_date": "",
        "end_date": "",
        "selected_areas": [],
        "max_age": 100,
        "search_text": ""
    }