import pandas as pd
import gradio as gr
import matplotlib.pyplot as plt
import seaborn as sns
import os
import zipfile

sns.set_theme(style="whitegrid", palette="pastel")

# =========================================================================
# LOAD DATA WITH DYNAMIC RELATIVE PATH (Zip Compression Enabled)
# =========================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Data directory track karna jo har operating system par automatic resolve ho jaye
DATA_PATH = os.path.join(BASE_DIR, "data", "traffic_data.zip")

# Backup check agar data folder se bahar run ho rahi ho file
if not os.path.exists(DATA_PATH):
    DATA_PATH = "traffic_data.zip"

# Pandas direct zip archive ke andar se bagair extract kiye CSV read karega
df = pd.read_csv(DATA_PATH, compression='zip')
df = df.drop_duplicates()
df.columns = df.columns.str.strip()

# =========================
# DATE HANDLING
# =========================

if "Date Occurred" in df.columns:
    df["Date Occurred"] = pd.to_datetime(df["Date Occurred"], errors="coerce")
    df = df[df["Date Occurred"].notna()]
    df["Year"] = df["Date Occurred"].dt.year
    df["Month"] = df["Date Occurred"].dt.month

# =========================================================================
# CLEANING (Fixed for Python 3.14 + New Pandas TypeError Issue)
# =========================================================================

for col in df.columns:
    if df[col].dtype == "object":
        df[col] = df[col].fillna("Unknown")
    else:
        try:
            df[col] = df[col].fillna(df[col].median())
        except TypeError:
            df[col] = df[col].fillna("Unknown")

# =========================
# AREA COLUMN
# =========================

area_col = None
for c in df.columns:
    if "AREA" in c.upper():
        area_col = c
        break

areas = sorted(df[area_col].dropna().unique().tolist()) if area_col else []

# =========================================================================
# SAVE ZIP FUNCTION (Cross-Platform Path Fixed)
# =========================================================================
def save_zip(*figs):
    charts_dir = os.path.join(BASE_DIR, "charts")
    os.makedirs(charts_dir, exist_ok=True)

    paths = []
    for i, fig in enumerate(figs, start=1):
        path = os.path.join(charts_dir, f"chart_{i}.png")
        fig.savefig(path, bbox_inches="tight")
        paths.append(path)

    zip_path = os.path.join(charts_dir, "all_charts.zip")

    with zipfile.ZipFile(zip_path, "w") as z:
        for p in paths:
            z.write(p, os.path.basename(p))

    return zip_path

# =========================
# DASHBOARD FUNCTION
# =========================

def dashboard(start_date, end_date, categories, max_age, search_text):

    temp = df.copy()

    # DATE FILTER
    if "Date Occurred" in temp.columns:
        temp["Date Occurred"] = pd.to_datetime(temp["Date Occurred"], errors="coerce")

        if start_date:
            temp = temp[temp["Date Occurred"] >= pd.to_datetime(start_date, errors="coerce")]

        if end_date:
            temp = temp[temp["Date Occurred"] <= pd.to_datetime(end_date, errors="coerce")]

    # CATEGORY FILTER
    if area_col and categories:
        temp = temp[temp[area_col].isin(categories)]

    # AGE FILTER
    if "Victim Age" in temp.columns:
        temp = temp[temp["Victim Age"].notna()]
        temp = temp[temp["Victim Age"] <= max_age]

    # SEARCH FILTER
    if search_text:
        temp = temp[
            temp.astype(str).apply(
                lambda x: x.str.contains(search_text, case=False, na=False)
            ).any(axis=1)
        ]

    # =========================
    # KPI
    # =========================

    total = len(temp)
    avg_age = round(temp["Victim Age"].mean(), 2) if "Victim Age" in temp.columns else 0

    # =====================================================================
    # ALL 10 CHARTS RESTORED
    # =====================================================================

    # 1 PIE CHART
    fig1, ax1 = plt.subplots()
    if "Victim Sex" in temp.columns:
        pie_data = temp["Victim Sex"].replace("Unknown", pd.NA).dropna()
        if len(pie_data) > 0:
            pie_data.value_counts().plot.pie(autopct="%1.1f%%", ax=ax1)
    ax1.set_title("Gender Distribution")

    # 2 COUNT PLOT
    fig2, ax2 = plt.subplots()
    if "Victim Sex" in temp.columns:
        count_data = temp["Victim Sex"].replace("Unknown", pd.NA).dropna()
        if len(count_data) > 0:
            order = count_data.value_counts().index
            sns.countplot(x=count_data, order=order, ax=ax2)
    ax2.set_title("Count Plot")

    # 3 VIOLIN PLOT
    fig3, ax3 = plt.subplots()
    if "Victim Sex" in temp.columns and "Victim Age" in temp.columns:
        clean = temp[["Victim Sex", "Victim Age"]].dropna()
        clean = clean[clean["Victim Sex"] != "Unknown"]
        if len(clean) > 0:
            sns.violinplot(x="Victim Sex", y="Victim Age", data=clean, ax=ax3)
    ax3.set_title("Violin Plot")

    # 4 HISTOGRAM
    fig4, ax4 = plt.subplots()
    if "Victim Age" in temp.columns:
        ax4.hist(temp["Victim Age"].dropna(), bins=25)
    ax4.set_title("Age Distribution")

    # 5 BAR CHART
    fig5, ax5 = plt.subplots()
    if area_col:
        temp[area_col].value_counts().head(10).plot(kind="bar", ax=ax5)
    ax5.set_title("Top Areas")

    # 6 LINE CHART
    fig6, ax6 = plt.subplots()
    if "Year" in temp.columns:
        temp.groupby("Year").size().plot(ax=ax6)
    ax6.set_title("Year Trend")

    # 7 SCATTER
    fig7, ax7 = plt.subplots()
    lat_col = None
    for c in temp.columns:
        if "LAT" in c.upper():
            lat_col = c
            break

    if "Victim Age" in temp.columns and lat_col:
        clean = temp[[lat_col, "Victim Age"]].dropna()
        if len(clean) > 0:
            ax7.scatter(clean["Victim Age"], clean[lat_col])
    ax7.set_title("Scatter Plot")

    # 8 HEATMAP
    fig8, ax8 = plt.subplots()
    numeric = temp.select_dtypes(include=["int64", "float64"])
    if not numeric.empty:
        sns.heatmap(numeric.corr(), cmap="coolwarm", ax=ax8)
    ax8.set_title("Heatmap")

    # 9 BOX PLOT 
    fig9, ax9 = plt.subplots()
    if "Victim Age" in temp.columns:
        sns.boxplot(x=temp["Victim Age"].dropna(), ax=ax9)
    ax9.set_title("Box Plot")

    # 10 AREA CHART
    fig10, ax10 = plt.subplots()
    if "Month" in temp.columns:
        temp.groupby("Month").size().plot(kind="area", ax=ax10, alpha=0.6)
    ax10.set_title("Monthly Collision Trend")

    # Layout adjustment
    for f in [fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8, fig9, fig10]:
        f.tight_layout()

    # ZIP FILE
    zip_file = save_zip(fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8, fig9, fig10)

    return total, avg_age, temp.head(20), fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8, fig9, fig10, zip_file

# =========================
# UI
# =========================

with gr.Blocks(theme=gr.themes.Soft()) as app:

    gr.Markdown("# 🚦 CLEAN FIXED TRAFFIC DASHBOARD")

    with gr.Row():

        with gr.Column(scale=1):
            start_date = gr.Textbox(label="Start Date")
            end_date = gr.Textbox(label="End Date")

            category = gr.CheckboxGroup(choices=areas, label="Area")

            age_slider = gr.Slider(0, 100, value=50, label="Max Age")

            search = gr.Textbox(label="Search")

            btn = gr.Button("Apply")

            download = gr.File(label="Download Charts ZIP")

        with gr.Column(scale=3):

            kpi1 = gr.Number(label="Total Records")
            kpi2 = gr.Number(label="Average Age")

            table = gr.Dataframe()

            with gr.Row():
                c1 = gr.Plot()
                c2 = gr.Plot()
                c3 = gr.Plot()
                c4 = gr.Plot()

            with gr.Row():
                c5 = gr.Plot()
                c6 = gr.Plot()
                c7 = gr.Plot()
                c8 = gr.Plot()

            with gr.Row():
                c9 = gr.Plot()
                c10 = gr.Plot()

    btn.click(
        dashboard,
        inputs=[start_date, end_date, category, age_slider, search],
        outputs=[kpi1, kpi2, table, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, download]
    )

app.launch(share=True)