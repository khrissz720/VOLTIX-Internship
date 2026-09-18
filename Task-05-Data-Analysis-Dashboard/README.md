# Task 05 — Data Analysis & Dashboard Using Python

## Deliverables
- `data_cleaning.py` — data cleaning and missing-value treatment.
- `Dataset/File_3_Cleaned.csv` — cleaned dataset.
- `Dashboard/app.py` — interactive dashboard built with Python.
- `Insights.md` — key insights extracted from the dataset.

## Data cleaning
The dataset was checked for:
- Duplicate rows.
- Missing values.
- Invalid values in categorical fields.
- Invalid values in numeric fields.
- Basic text consistency.

Missing values were handled as follows:
- `Age`: median by `Sex` and `Pclass`.
- `Fare`: median by `Pclass`.
- `Cabin`: `Unknown`.

No duplicate rows or invalid values were found in the checked fields.

## Dashboard
The dashboard uses:
- Pandas
- Plotly
- Dash
- Dash Bootstrap Components

Interactive filters:
- Sex
- Passenger Class
- Embarked

Dashboard sections:
1. Key Performance Indicators (KPIs)
2. Comparisons
3. Detailed Analysis

The dashboard was adapted to the actual columns available in the provided CSV. No date, region, product, or other fields that are not present in the dataset were invented.

## Run
From the task folder:

```bash
pip install pandas plotly dash dash-bootstrap-components
python data_cleaning.py
python Dashboard/app.py
```

The dashboard then runs locally through Dash.
