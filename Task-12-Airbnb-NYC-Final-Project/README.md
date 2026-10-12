# Task 12 — Airbnb NYC Final Data Analysis Project

## Dataset restriction
This project uses **only the supplied `AB_NYC_2019.csv`** as analytical data. No external dataset was downloaded, merged, or substituted. `New_York_City_.png` was not used as analytical data.

## Project contents
- `data/AB_NYC_2019_original.csv` — copy of the supplied original
- `data/airbnb_nyc_cleaned.csv` — cleaned and enriched analysis dataset
- `notebooks/Airbnb_NYC_Analysis.ipynb` — reproducible analysis notebook
- `dashboard/Airbnb_NYC_Interactive_Dashboard.html` — interactive Plotly dashboard
- `report/Airbnb_NYC_Final_Report.docx` — final written report
- `report/Final_Insights_and_Recommendations.md` — concise findings/recommendations
- `analysis/Airbnb_NYC_Analysis_Summaries.xlsx` — KPIs and summary tables
- `analysis/*.csv` and `analysis/key_metrics.json` — exported analytical outputs
- `visualizations/*.png` — report-ready figures

## Dataset profile
- Original dimensions: 48,895 rows × 16 columns
- Prepared dimensions: 48,895 rows × 22 columns (derived fields added)
- Exact duplicate rows removed: 0
- Median listed price: $106
- Unique hosts: 37,457

## Run the notebook
Recommended environment: Python 3.10+ with pandas, numpy, matplotlib, jupyter, and openpyxl.

```bash
python -m pip install pandas numpy matplotlib jupyter openpyxl
jupyter notebook notebooks/Airbnb_NYC_Analysis.ipynb
```

The notebook first tries `../data/AB_NYC_2019_original.csv`, which works when launched from the `notebooks` directory. If launching from the project root, it also checks `data/AB_NYC_2019_original.csv`.

## Open the dashboard
Open `dashboard/Airbnb_NYC_Interactive_Dashboard.html` in a browser with internet access for Plotly's CDN. The charts support hover, zoom, pan, and export. They do not cross-filter each other.

## Cleaning choices
- Trim text and normalize blank-like strings.
- Coerce expected numeric fields and parse `last_review` as datetime.
- Remove exact duplicate rows only.
- Preserve missing values in source columns; use a separate derived `reviews_per_month_filled` field.
- Flag price outliers using the IQR upper fence rather than deleting them automatically.
- Add price and minimum-night bands for analysis.

## Important caveats
- The dataset is a 2019 snapshot and is not current market data.
- No guest rating, booking transactions, realized revenue, or occupancy is included.
- `number_of_reviews` is not a rating or direct occupancy measure.
- Correlation does not establish causation.
- Price outliers and zero-price rows require validation before operational use.

## Main findings
- Most listings are in **Manhattan**.
- Highest borough median price: **Manhattan** ($150).
- Lowest borough median price: **Bronx** ($65).
- Most common room type: **Entire home/apt**.
- Price/review-count correlation: **-0.048** (descriptive, not causal).

## Final checklist
- [x] Cleaned dataset / analysis file
- [x] Analysis notebook
- [x] Interactive dashboard
- [x] Final report
- [x] Insights and recommendations
- [x] Visualizations and summary workbook
