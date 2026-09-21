import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE = Path(__file__).resolve().parent
INPUT = BASE / 'Weather_Data.csv'
OUTPUT = BASE / 'Weather_Data_Cleaned.csv'
CHARTS = BASE / 'charts'
CHARTS.mkdir(exist_ok=True)

# Load and clean
weather = pd.read_csv(INPUT)
weather.columns = weather.columns.str.strip()
weather['Date'] = pd.to_datetime(weather['Date'], errors='coerce')

# Remove exact duplicate rows and standardize text fields
weather = weather.drop_duplicates().copy()
text_cols = weather.select_dtypes(include='object').columns
for col in text_cols:
    weather[col] = weather[col].astype(str).str.strip()

# Date features for analysis/dashboard
weather['Year'] = weather['Date'].dt.year
weather['Month'] = weather['Date'].dt.month
weather['MonthName'] = weather['Date'].dt.month_name()
weather['AvgTemp'] = (weather['MinTemp'] + weather['MaxTemp']) / 2
weather['TempRange'] = weather['MaxTemp'] - weather['MinTemp']

# Save cleaned data
weather.to_csv(OUTPUT, index=False)

# Summary statistics
summary = weather[['MinTemp','MaxTemp','AvgTemp','Rainfall','Humidity3pm','WindGustSpeed']].describe().round(2)
summary.to_csv(BASE / 'Summary_Statistics.csv')

# Yearly KPIs
annual = weather.groupby('Year').agg(
    AvgTemperature=('AvgTemp','mean'),
    MaxTemperature=('MaxTemp','max'),
    TotalRainfall=('Rainfall','sum'),
    AvgHumidity=('Humidity3pm','mean'),
    AvgWindGust=('WindGustSpeed','mean'),
    RainyDays=('RainToday', lambda x: (x == 'Yes').sum())
).reset_index()
annual.to_csv(BASE / 'Annual_KPIs.csv', index=False)

# Monthly KPIs
monthly = weather.groupby('Month').agg(
    AvgTemperature=('AvgTemp','mean'),
    TotalRainfall=('Rainfall','sum'),
    AvgHumidity=('Humidity3pm','mean'),
    AvgWindGust=('WindGustSpeed','mean')
).reset_index()
monthly.to_csv(BASE / 'Monthly_KPIs.csv', index=False)

# 1. Average temperature by year
plt.figure(figsize=(10,5))
annual.plot(x='Year', y='AvgTemperature', marker='o', legend=False)
plt.title('Average Temperature by Year')
plt.xlabel('Year')
plt.ylabel('Average Temperature')
plt.tight_layout()
plt.savefig(CHARTS / 'average_temperature_by_year.png', dpi=150)
plt.close()

# 2. Total rainfall by year
plt.figure(figsize=(10,5))
annual.plot(x='Year', y='TotalRainfall', kind='bar', legend=False)
plt.title('Total Rainfall by Year')
plt.xlabel('Year')
plt.ylabel('Total Rainfall')
plt.tight_layout()
plt.savefig(CHARTS / 'total_rainfall_by_year.png', dpi=150)
plt.close()

# 3. Humidity and wind by year
fig, ax = plt.subplots(figsize=(10,5))
ax.plot(annual['Year'], annual['AvgHumidity'], marker='o', label='Avg Humidity')
ax2 = ax.twinx()
ax2.plot(annual['Year'], annual['AvgWindGust'], marker='s', label='Avg Wind Gust')
ax.set_xlabel('Year')
ax.set_ylabel('Average Humidity')
ax2.set_ylabel('Average Wind Gust')
ax.set_title('Humidity and Wind Patterns by Year')
fig.tight_layout()
fig.savefig(CHARTS / 'humidity_wind_by_year.png', dpi=150)
plt.close(fig)

# 4. Rainfall distribution
plt.figure(figsize=(10,5))
plt.hist(weather['Rainfall'], bins=30)
plt.title('Rainfall Distribution')
plt.xlabel('Rainfall')
plt.ylabel('Number of Days')
plt.tight_layout()
plt.savefig(CHARTS / 'rainfall_distribution.png', dpi=150)
plt.close()

# 5. Temperature range by month
plt.figure(figsize=(10,5))
monthly_range = weather.groupby('Month')['TempRange'].mean().reset_index() if 'TempRange' in weather else None
if monthly_range is not None:
    plt.plot(monthly_range['Month'], monthly_range['TempRange'], marker='o')
plt.title('Average Daily Temperature Range by Month')
plt.xlabel('Month')
plt.ylabel('Average Temperature Range')
plt.tight_layout()
plt.savefig(CHARTS / 'temperature_range_by_month.png', dpi=150)
plt.close()

print(f'Rows after cleaning: {len(weather)}')
print(f'Date range: {weather["Date"].min().date()} to {weather["Date"].max().date()}')
print(f'Duplicates removed: {pd.read_csv(INPUT).duplicated().sum()}')
print(f'Missing values after cleaning: {int(weather.isna().sum().sum())}')
