import pandas as pd
from pathlib import Path

BASE = Path(__file__).resolve().parent
INPUT = BASE / "Weather_Data.csv"
OUTPUT = BASE / "Weather_Data_Cleaned.csv"

# Load data
weather = pd.read_csv(INPUT)

# Clean column names
weather.columns = weather.columns.str.strip()

# Convert Date
weather["Date"] = pd.to_datetime(weather["Date"], errors="coerce")

# Remove exact duplicate rows
duplicates_removed = weather.duplicated().sum()
weather = weather.drop_duplicates().copy()

# Clean text fields
text_cols = weather.select_dtypes(include="object").columns

for col in text_cols:
    weather[col] = weather[col].astype(str).str.strip()

# Create date features
weather["Year"] = weather["Date"].dt.year
weather["Month"] = weather["Date"].dt.month
weather["MonthName"] = weather["Date"].dt.month_name()

# Create temperature indicators
weather["AvgTemp"] = (
    weather["MinTemp"] + weather["MaxTemp"]
) / 2

weather["TempRange"] = (
    weather["MaxTemp"] - weather["MinTemp"]
)

# Save cleaned data
weather.to_csv(OUTPUT, index=False)

# Basic analysis
summary = weather[
    [
        "MinTemp",
        "MaxTemp",
        "AvgTemp",
        "Rainfall",
        "Humidity3pm",
        "WindGustSpeed"
    ]
].describe().round(2)

print("Weather Data Analysis")
print("-" * 30)

print(f"Rows after cleaning: {len(weather)}")
print(f"Columns: {len(weather.columns)}")
print(
    f"Date range: "
    f"{weather['Date'].min().date()} "
    f"to "
    f"{weather['Date'].max().date()}"
)
print(f"Duplicates removed: {duplicates_removed}")
print(
    f"Missing values after cleaning: "
    f"{int(weather.isna().sum().sum())}"
)

print("\nSummary Statistics:")
print(summary)

print("\nYearly Temperature and Rainfall:")
annual = weather.groupby("Year").agg(
    AvgTemperature=("AvgTemp", "mean"),
    MaxTemperature=("MaxTemp", "max"),
    TotalRainfall=("Rainfall", "sum"),
    AvgHumidity=("Humidity3pm", "mean"),
    AvgWindGust=("WindGustSpeed", "mean")
).round(2)

print(annual)

print("\nMonthly Temperature and Rainfall:")
monthly = weather.groupby("Month").agg(
    AvgTemperature=("AvgTemp", "mean"),
    TotalRainfall=("Rainfall", "sum"),
    AvgHumidity=("Humidity3pm", "mean"),
    AvgWindGust=("WindGustSpeed", "mean")
).round(2)

print(monthly)
