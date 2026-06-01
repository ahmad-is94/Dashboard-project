# Dashboard-project
Traffic Collision EDA dashboard for Sir Ali Hassan Sherazi's course. Features 10 linked charts (Pie, Violin, Area, Heatmap, Box, Line) with real-time interactive filters (Date, Area, Age Slider, Text Search) using Gradio &amp; Pandas. Fully modular project structure (app.py, filters.py, charts.py) with programmatic ZIP chart exporter.
# 🚦 Traffic Collision Exploratory Data Analysis (EDA) & Interactive Dashboard

A professional-grade, interactive data visualization dashboard developed for the **Exploratory Data Analysis** course (Instructed by **Sir Ali Hassan Sherazi**). This project applies rigorous preprocessing, data cleaning, and modular software design to discover trends, demographic impact, and structural insights from historical traffic collision records.

---

## 📊 Project Highlights
* **Modular Codebase:** Adheres strictly to institutional project guidelines by splitting business logic into `filters.py`, visual rendering into `charts.py`, and the layout into `app.py`.
* **10 Mandatory Visualizations:** Implements ten distinct, non-overlapping chart types (Pie, Count, Violin, Histogram, Bar, Line, Scatter, Heatmap, Box, and Area plots) with explicit formatting, standardized colors, and descriptive titles.
* **Bi-Directional Linked Filters:** Fully synchronized control sidebar enabling simultaneous real-time filtering across all charts based on Date Boundaries, Sectors/Areas, Victim Age Limits, and Global Text Searches.
* **On-Demand Report Export:** Built-in programmatic packaging that compiles, compresses, and downloads all state-filtered visualizations into a unified `.ZIP` archive instantly.

---

## 🛠️ Project Directory Structure
To maintain corporate-standard code hygiene, the repository is organized as follows:
```text
/dashboard_project/
│
├── data/
│   └── Traffic_Collision_Data_from_2010_to_Present (2).csv  <-- Unaltered Original Dataset
│
├── charts/                  <-- Auto-generated folder for exported figures
│   └── all_charts.zip       <-- Packaged visualization assets downloadable through UI
│
├── app.py                   <-- Main interface application module (Gradio Framework)
├── filters.py               <-- Backend dataset ingestion, imputation, and processing pipeline
├── charts.py                <-- Core visualization asset rendering architecture
├── requirements.txt         <-- Automated environmental deployment packages checklist
└── README.md                <-- Core documentation & setup roadmap
