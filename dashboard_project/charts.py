# charts.py
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os
import zipfile

# Global professional styling
sns.set_theme(style="whitegrid", palette="pastel")

# =========================================================================
# DYNAMIC UTILITY: SAVE AND BUNDLE CHARTS ZIP (Path Issue Resolved)
# =========================================================================
def save_zip(*figs):
    """
    Saare generated charts ko platform-independent dynamic paths par 
    save karke single zip file bundle banane ka dynamic function.
    """
    # Current file ki directory dhoond kar 'charts' sub-folder ka cross-platform path banana
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    CHARTS_DIR = os.path.join(BASE_DIR, "charts")
    
    # Folder agar mojood nahi hai toh automatically context ke mutabik create karna
    os.makedirs(CHARTS_DIR, exist_ok=True)

    paths = []
    for i, fig in enumerate(figs, start=1):
        # Universal local path resolution for image assets
        path = os.path.join(CHARTS_DIR, f"chart_{i}.png")
        fig.savefig(path, bbox_inches="tight")
        paths.append(path)

    # Creating full explicit archive bundle track
    zip_path = os.path.join(CHARTS_DIR, "all_charts.zip")

    with zipfile.ZipFile(zip_path, "w") as z:
        for p in paths:
            # OS-independent compression parameters handling inside structural tree
            z.write(p, os.path.basename(p))

    return zip_path


# =========================
# 1. PIE CHART
# =========================
def pie_chart(df):
    fig, ax = plt.subplots()
    if "Victim Sex" in df.columns:
        data = df["Victim Sex"].replace("Unknown", pd.NA).dropna()
        if len(data) > 0:
            data.value_counts().plot.pie(
                autopct="%1.1f%%",
                ax=ax
            )
    ax.set_title("Gender Distribution")
    ax.set_ylabel("")
    return fig


# =========================
# 2. COUNT PLOT
# =========================
def count_plot(df):
    fig, ax = plt.subplots()
    if "Victim Sex" in df.columns:
        data = df["Victim Sex"].replace("Unknown", pd.NA).dropna()
        if len(data) > 0:
            order = data.value_counts().index
            sns.countplot(
                x=data,
                order=order,
                ax=ax
            )
    ax.set_title("Count Plot")
    return fig


# =========================
# 3. VIOLIN PLOT
# =========================
def violin_plot(df):
    fig, ax = plt.subplots()
    if "Victim Sex" in df.columns and "Victim Age" in df.columns:
        clean = df[["Victim Sex", "Victim Age"]].dropna()
        clean = clean[clean["Victim Sex"] != "Unknown"]
        if len(clean) > 0:
            sns.violinplot(
                x="Victim Sex",
                y="Victim Age",
                data=clean,
                ax=ax
            )
    ax.set_title("Age Distribution by Gender")
    return fig


# =========================
# 4. HISTOGRAM
# =========================
def histogram(df):
    fig, ax = plt.subplots()
    if "Victim Age" in df.columns:
        ax.hist(
            df["Victim Age"].dropna(),
            bins=25,
            color="orange"
        )
    ax.set_title("Victim Age Distribution")
    return fig


# =========================
# 5. BAR CHART
# =========================
def bar_chart(df, area_col):
    fig, ax = plt.subplots()
    if area_col:
        df[area_col].value_counts() \
            .head(10) \
            .plot(
                kind="bar",
                ax=ax
            )
    ax.set_title("Top 10 Areas")
    return fig


# =========================
# 6. LINE CHART
# =========================
def line_chart(df):
    fig, ax = plt.subplots()
    if "Year" in df.columns:
        df.groupby("Year") \
          .size() \
          .plot(ax=ax)
    ax.set_title("Yearly Collision Trend")
    return fig


# =========================
# 7. SCATTER PLOT
# =========================
def scatter_plot(df):
    fig, ax = plt.subplots()
    lat_col = None
    for c in df.columns:
        if "LAT" in c.upper():
            lat_col = c
            break

    if lat_col and "Victim Age" in df.columns:
        clean = df[[lat_col, "Victim Age"]].dropna()
        if len(clean) > 0:
            ax.scatter(
                clean["Victim Age"],
                clean[lat_col],
                alpha=0.5
            )
    ax.set_title("Victim Age vs Latitude")
    return fig


# =========================
# 8. BOX PLOT
# =========================
def box_plot(df):
    fig, ax = plt.subplots()
    if "Victim Age" in df.columns:
        sns.boxplot(
            x=df["Victim Age"].dropna(),
            ax=ax
        )
    ax.set_title("Box Plot")
    return fig


# =========================
# 9. HEATMAP
# =========================
def heatmap(df):
    fig, ax = plt.subplots()
    numeric = df.select_dtypes(include=["int64", "float64"])
    if not numeric.empty:
        sns.heatmap(
            numeric.corr(),
            cmap="coolwarm",
            ax=ax
        )
    ax.set_title("Correlation Heatmap")
    return fig


# =========================
# 10. AREA CHART
# =========================
def area_chart(df):
    fig, ax = plt.subplots()
    if "Month" in df.columns:
        df.groupby("Month") \
          .size() \
          .plot(
              kind="area",
              ax=ax,
              alpha=0.6
          )
    ax.set_title("Monthly Collision Trend")
    return fig