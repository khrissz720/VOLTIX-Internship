# Task 10 – Movie Analytics Dashboard

## Overview

This project analyzes the TMDB 5000 Movies dataset to identify patterns in movie revenue, ratings, genres, release years, runtime, and financial performance.

The project combines Python-based data cleaning and analysis with an interactive Power BI dashboard.

## Project Structure

```text
Task-10-Movie-Analytics-Dashboard/
│
├── data/
│   ├── tmdb_5000_movies.csv
│   ├── tmdb_5000_credits.csv
│   └── movies_cleaned.csv
│
├── cleaning/
│   ├── clean_movies.py
│   └── cleaning_report.txt
│
├── analysis/
│   ├── analyze_movies.py
│   └── results/
│       ├── analysis_summary.csv
│       ├── budget_vs_revenue.csv
│       ├── genre_analysis.csv
│       ├── kpis.csv
│       ├── movies_by_year.csv
│       ├── runtime_analysis.csv
│       ├── runtime_category_analysis.csv
│       ├── runtime_correlations.csv
│       ├── top_10_highest_grossing.csv
│       ├── top_10_highest_rated.csv
│       └── yearly_trends.csv
│
├── Movie-Analytics-Dashboard.pbix
├── Insights.docx
└── README.md
```

## Dataset

The project uses the following TMDB datasets:

- `tmdb_5000_movies.csv`
- `tmdb_5000_credits.csv`

After data cleaning, the processed dataset is stored as:

`data/movies_cleaned.csv`

## Data Cleaning

The data cleaning process is implemented in:

`cleaning/clean_movies.py`

The cleaning process prepares the movie data for analysis by handling data types, missing values, dates, text fields, genres, and other data inconsistencies.

The cleaning process is documented in:

`cleaning/cleaning_report.txt`

## Data Analysis

The main analysis script is:

`analysis/analyze_movies.py`

The analysis generates datasets covering:

- Budget vs. Revenue
- Revenue by Genre
- Key Performance Indicators
- Movies by Year
- Runtime Analysis
- Runtime Categories
- Runtime Correlations
- Top 10 Highest-Grossing Movies
- Top 10 Highest-Rated Movies
- Yearly Trends

The resulting CSV files are stored in:

`analysis/results/`

## Power BI Dashboard

The final interactive dashboard is:

`Movie-Analytics-Dashboard.pbix`

### Page 1 – Main Dashboard

The first page provides an overview of the movie dataset using key indicators and high-level financial and performance visualizations.

### Page 2 – Movie Analytics Details

The second page provides detailed analysis through the following visualizations:

- Revenue Over Years
- Ratings Over Years
- Number of Movies by Year
- Revenue by Genre
- Average Rating by Genre
- Top 10 Highest-Grossing Movies
- Top 10 Highest-Rated Movies
- Runtime vs Rating
- Average Revenue by Runtime Category
- Movies by Runtime Category

The dashboard also includes filters for:

- Release Year
- Genre

## Main Insights

The analysis indicates that:

1. Production budget and revenue generally show a positive relationship, although a higher budget does not guarantee higher revenue.
2. Revenue varies considerably across release years and genres.
3. Different genres show differences in both commercial performance and average audience ratings.
4. The highest-grossing movies and highest-rated movies represent different dimensions of movie success.
5. Runtime can be analyzed in relation to ratings and financial performance.
6. Combining revenue, ratings, genre, year, and runtime provides a more complete view of movie performance.

## Tools Used

- Python
- Pandas
- NumPy
- Power BI
- Microsoft Word
- CSV
- TMDB 5000 Movies Dataset

## Project Deliverables

The project contains the following main deliverables:

- Cleaned movie dataset.
- Python data cleaning script.
- Cleaning report.
- Python analysis script.
- Analytical CSV results.
- Power BI dashboard.
- Insights document.
- Project README documentation.