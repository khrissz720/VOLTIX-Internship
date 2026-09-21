# Task 06 - Weather Data Analysis

## Objective
Analyze historical weather data by cleaning the dataset, studying temperature, humidity, wind speed, and rainfall patterns over time, identifying unusual values or changes, and presenting the main findings in an interactive Power BI or Tableau dashboard.

## Files
- `Weather_Data.csv` - original dataset used for the task.
- `Weather_Data_Cleaned.csv` - cleaned and prepared dataset with date and analysis fields.
- `Weather_Analysis.py` - cleaning and exploratory analysis script.
- `Summary_Statistics.csv` - descriptive statistics for the main weather variables.
- `Annual_KPIs.csv` - yearly KPI summary.
- `Monthly_KPIs.csv` - monthly KPI summary.
- `Insights.md` - findings from the analysis.
- `charts/` - exploratory visualizations.

## Cleaning and preparation
- Parsed `Date` as a date field.
- Removed exact duplicate rows if present.
- Trimmed text fields.
- Checked missing values.
- Added `Year`, `Month`, and `MonthName` fields.
- Added `AvgTemp` and `TempRange` for temperature analysis.

## Dashboard KPIs
- Average Temperature
- Maximum Temperature
- Total Rainfall
- Average Humidity
- Average Wind Gust
- Rainy Days

## Dashboard visuals
Use the cleaned dataset to create an interactive dashboard with:
- KPI cards for the main weather measures.
- Average temperature by year.
- Total rainfall by year.
- Humidity and wind patterns by year.
- Rainfall distribution.
- Temperature range by month.
- Date/year filters for interactive exploration.

## Data limitation
The supplied dataset has no city or country fields, so geographic comparisons cannot be performed without adding another source of location data. No location values are invented in this project.
