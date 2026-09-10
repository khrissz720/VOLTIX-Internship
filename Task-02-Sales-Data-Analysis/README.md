# Task 02 – Sales Data Analysis

## Objective
Complete data cleaning, data validation, dashboard creation and business insights using the supplied sales dataset.

## Files
- `FactSale.csv`: source dataset used by the Python script.
- `Dataset/EzzSteel_Full_Dataset.xlsx`: cleaned dataset.
- `Charts/`: four required static charts.
- `Dashboard.html`: interactive Plotly dashboard.
- `Dashboard.png`: static management dashboard preview.
- `Insights.docx`: data-quality issues, findings and recommendations.
- `Sales_Analysis.py`: complete reproducible analysis script.

## Data Quality Summary
- Original rows: 26,397
- Columns: 21
- Exact duplicates: 0
- Missing Delivery Date Key: 13
- Invalid Invoice Date Key: 0
- Calculation mismatches: 0 within $0.01 tolerance
- Negative profit rows: 566 (retained because they can be valid business records)

## Main KPIs
- Total Sales: $22,855,077.65
- Total Profit: $9,923,891.70
- Total Quantity: 1,028,670
- Profit Margin: 43.4%
- Invoice Count: 8,188
- Average Invoice Value: $2,791.29

## How to Run in VS Code
1. Put `FactSale.csv` in the same folder as `Sales_Analysis.py`.
2. Install dependencies:

```bash
pip install pandas numpy matplotlib openpyxl plotly python-docx
```

3. Run:

```bash
python Sales_Analysis.py
```

The script automatically creates the cleaned Excel file, four PNG charts, the interactive dashboard and the Insights report.

## Important Note
The dataset does not contain a `Region` column. The geographic chart therefore uses `City Key` as the available geographic dimension. No region values were invented.
