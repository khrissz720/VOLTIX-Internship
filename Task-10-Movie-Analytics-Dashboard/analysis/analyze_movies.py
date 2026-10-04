import pandas as pd
import os


# ============================================================
# TASK 10 - MOVIE ANALYTICS DASHBOARD
# Movie Data Analysis
# ============================================================

# ------------------------------------------------------------
# 1. Define paths
# ------------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INPUT_FILE = os.path.join(
    BASE_DIR,
    "data",
    "movies_cleaned.csv"
)

RESULTS_DIR = os.path.join(
    BASE_DIR,
    "analysis",
    "results"
)

os.makedirs(RESULTS_DIR, exist_ok=True)


# ------------------------------------------------------------
# 2. Load cleaned dataset
# ------------------------------------------------------------

print("=" * 70)
print("TASK 10 - MOVIE ANALYTICS DASHBOARD")
print("MOVIE DATA ANALYSIS")
print("=" * 70)

print("\nLoading cleaned dataset...")

df = pd.read_csv(INPUT_FILE)

print(f"Rows loaded: {len(df)}")
print(f"Columns loaded: {len(df.columns)}")


# ------------------------------------------------------------
# 3. Prepare data types
# ------------------------------------------------------------

df["release_date"] = pd.to_datetime(
    df["release_date"],
    errors="coerce"
)

numeric_columns = [
    "budget",
    "revenue",
    "profit",
    "roi",
    "runtime",
    "popularity",
    "vote_average",
    "vote_count",
    "release_year"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )


# ============================================================
# ANALYSIS 1
# Number of movies released over the years
# ============================================================

print("\n1. Movies released by year...")

movies_by_year = (
    df.dropna(subset=["release_year"])
      .groupby("release_year")
      .agg(
          movie_count=("id", "count"),
          average_rating=("vote_average", "mean"),
          total_revenue=("revenue", "sum")
      )
      .reset_index()
      .sort_values("release_year")
)

movies_by_year["average_rating"] = (
    movies_by_year["average_rating"].round(2)
)

movies_by_year["total_revenue"] = (
    movies_by_year["total_revenue"].round(2)
)

movies_by_year.to_csv(
    os.path.join(
        RESULTS_DIR,
        "movies_by_year.csv"
    ),
    index=False
)


# ============================================================
# ANALYSIS 2
# Movies by Genre
# ============================================================

print("2. Movies by genre...")

genre_df = df[
    [
        "id",
        "title",
        "genres_clean",
        "vote_average",
        "vote_count",
        "budget",
        "revenue",
        "profit",
        "runtime"
    ]
].copy()

# Split multiple genres into separate rows

genre_df["genre"] = genre_df[
    "genres_clean"
].fillna("No Genre").str.split(" | ", regex=False)

genre_df = genre_df.explode("genre")

genre_df["genre"] = genre_df[
    "genre"
].str.strip()

genre_df = genre_df[
    genre_df["genre"] != ""
]

# Remove possible duplicated movie/genre combinations

genre_df = genre_df.drop_duplicates(
    subset=["id", "genre"]
)


# ------------------------------------------------------------
# Genre statistics
# ------------------------------------------------------------

genre_analysis = (
    genre_df
    .groupby("genre")
    .agg(
        movie_count=("id", "nunique"),
        average_rating=("vote_average", "mean"),
        average_vote_count=("vote_count", "mean"),
        total_budget=("budget", "sum"),
        total_revenue=("revenue", "sum"),
        average_revenue=("revenue", "mean"),
        average_runtime=("runtime", "mean")
    )
    .reset_index()
    .sort_values(
        "movie_count",
        ascending=False
    )
)

genre_analysis[
    [
        "average_rating",
        "average_vote_count",
        "total_budget",
        "total_revenue",
        "average_revenue",
        "average_runtime"
    ]
] = genre_analysis[
    [
        "average_rating",
        "average_vote_count",
        "total_budget",
        "total_revenue",
        "average_revenue",
        "average_runtime"
    ]
].round(2)

genre_analysis.to_csv(
    os.path.join(
        RESULTS_DIR,
        "genre_analysis.csv"
    ),
    index=False
)
# Save movie-genre relationship for Power BI
genre_df.to_csv(
    os.path.join(
        RESULTS_DIR,
        "movie_genres.csv"
    ),
    index=False
)


# ============================================================
# ANALYSIS 3
# Budget vs Revenue
# ============================================================

print("3. Budget vs revenue analysis...")

budget_revenue = df[
    [
        "id",
        "title",
        "budget",
        "revenue",
        "profit",
        "roi",
        "vote_average",
        "vote_count"
    ]
].copy()

budget_revenue = budget_revenue[
    (budget_revenue["budget"] > 0) &
    (budget_revenue["revenue"] > 0)
]

budget_revenue.to_csv(
    os.path.join(
        RESULTS_DIR,
        "budget_vs_revenue.csv"
    ),
    index=False
)


# ------------------------------------------------------------
# Budget vs revenue correlation
# ------------------------------------------------------------

budget_revenue_correlation = (
    budget_revenue[
        ["budget", "revenue"]
    ]
    .corr()
    .loc["budget", "revenue"]
)


# ============================================================
# ANALYSIS 4
# Highest-grossing movies
# ============================================================

print("4. Highest-grossing movies...")

highest_grossing = (
    df[
        [
            "id",
            "title",
            "release_year",
            "budget",
            "revenue",
            "profit",
            "vote_average",
            "vote_count"
        ]
    ]
    .sort_values(
        "revenue",
        ascending=False
    )
    .head(10)
)

highest_grossing.to_csv(
    os.path.join(
        RESULTS_DIR,
        "top_10_highest_grossing.csv"
    ),
    index=False
)


# ============================================================
# ANALYSIS 5
# Highest-rated movies considering Vote Count
# ============================================================

print("5. Highest-rated movies considering vote count...")

# Minimum number of votes to avoid rankings dominated
# by movies with very few votes.

MIN_VOTES = 1000

rated_movies = df[
    df["vote_count"] >= MIN_VOTES
].copy()


# ------------------------------------------------------------
# Weighted rating
# ------------------------------------------------------------

# C = average rating of all movies
# m = minimum votes required
# v = votes for the movie
# R = movie rating
#
# Weighted rating:
#
# (v / (v + m)) * R +
# (m / (v + m)) * C
#
# This prevents movies with very few votes from
# dominating the ranking.

C = df["vote_average"].mean()
m = MIN_VOTES

rated_movies["weighted_rating"] = (
    (
        rated_movies["vote_count"]
        /
        (
            rated_movies["vote_count"] + m
        )
    )
    * rated_movies["vote_average"]
    +
    (
        m
        /
        (
            rated_movies["vote_count"] + m
        )
    )
    * C
)

highest_rated = (
    rated_movies[
        [
            "id",
            "title",
            "release_year",
            "vote_average",
            "vote_count",
            "weighted_rating",
            "revenue",
            "runtime"
        ]
    ]
    .sort_values(
        "weighted_rating",
        ascending=False
    )
    .head(10)
)

highest_rated[
    "weighted_rating"
] = highest_rated[
    "weighted_rating"
].round(2)

highest_rated.to_csv(
    os.path.join(
        RESULTS_DIR,
        "top_10_highest_rated.csv"
    ),
    index=False
)


# ============================================================
# ANALYSIS 6
# Revenue and Ratings over the years
# ============================================================

print("6. Revenue and ratings over the years...")

yearly_trends = (
    df.dropna(subset=["release_year"])
      .groupby("release_year")
      .agg(
          movie_count=("id", "count"),
          total_revenue=("revenue", "sum"),
          average_revenue=("revenue", "mean"),
          average_rating=("vote_average", "mean"),
          average_vote_count=("vote_count", "mean"),
          average_budget=("budget", "mean")
      )
      .reset_index()
      .sort_values("release_year")
)

yearly_trends[
    [
        "total_revenue",
        "average_revenue",
        "average_rating",
        "average_vote_count",
        "average_budget"
    ]
] = yearly_trends[
    [
        "total_revenue",
        "average_revenue",
        "average_rating",
        "average_vote_count",
        "average_budget"
    ]
].round(2)

yearly_trends.to_csv(
    os.path.join(
        RESULTS_DIR,
        "yearly_trends.csv"
    ),
    index=False
)


# ============================================================
# ANALYSIS 7
# Runtime vs Rating and Revenue
# ============================================================

print("7. Runtime analysis...")

runtime_analysis = df[
    [
        "id",
        "title",
        "runtime",
        "runtime_category",
        "vote_average",
        "vote_count",
        "revenue",
        "budget",
        "profit"
    ]
].copy()

runtime_analysis = runtime_analysis[
    runtime_analysis["runtime"].notna()
]

runtime_analysis.to_csv(
    os.path.join(
        RESULTS_DIR,
        "runtime_analysis.csv"
    ),
    index=False
)


# ------------------------------------------------------------
# Runtime category analysis
# ------------------------------------------------------------

runtime_category_analysis = (
    df.dropna(subset=["runtime"])
      .groupby("runtime_category")
      .agg(
          movie_count=("id", "count"),
          average_rating=("vote_average", "mean"),
          average_revenue=("revenue", "mean"),
          average_budget=("budget", "mean"),
          average_profit=("profit", "mean")
      )
      .reset_index()
)

runtime_category_analysis[
    [
        "average_rating",
        "average_revenue",
        "average_budget",
        "average_profit"
    ]
] = runtime_category_analysis[
    [
        "average_rating",
        "average_revenue",
        "average_budget",
        "average_profit"
    ]
].round(2)

runtime_category_analysis.to_csv(
    os.path.join(
        RESULTS_DIR,
        "runtime_category_analysis.csv"
    ),
    index=False
)


# ------------------------------------------------------------
# Runtime correlations
# ------------------------------------------------------------

runtime_correlations = pd.DataFrame({
    "variable": [
        "Runtime vs Rating",
        "Runtime vs Revenue"
    ],
    "correlation": [
        df[
            ["runtime", "vote_average"]
        ].corr().loc[
            "runtime",
            "vote_average"
        ],
        df[
            ["runtime", "revenue"]
        ].corr().loc[
            "runtime",
            "revenue"
        ]
    ]
})

runtime_correlations[
    "correlation"
] = runtime_correlations[
    "correlation"
].round(4)

runtime_correlations.to_csv(
    os.path.join(
        RESULTS_DIR,
        "runtime_correlations.csv"
    ),
    index=False
)


# ============================================================
# ANALYSIS 8
# KPIs
# ============================================================

print("8. Calculating KPIs...")

kpis = {
    "Total Movies": len(df),
    "Total Revenue": df["revenue"].sum(),
    "Average Revenue": df["revenue"].mean(),
    "Average Rating": df["vote_average"].mean(),
    "Average Vote Count": df["vote_count"].mean(),
    "Average Runtime": df["runtime"].mean(),
    "Total Budget": df["budget"].sum(),
    "Total Profit": df["profit"].sum(),
    "Average Budget": df["budget"].mean(),
    "Budget-Revenue Correlation": budget_revenue_correlation,
    "Highest Revenue": df["revenue"].max(),
    "Highest Rating": df["vote_average"].max(),
    "Highest Vote Count": df["vote_count"].max()
}

kpi_df = pd.DataFrame(
    list(kpis.items()),
    columns=["KPI", "Value"]
)

kpi_df["Value"] = kpi_df["Value"].round(2)

kpi_df.to_csv(
    os.path.join(
        RESULTS_DIR,
        "kpis.csv"
    ),
    index=False
)


# ============================================================
# ANALYSIS 9
# Overall summary
# ============================================================

print("9. Creating summary...")

summary = pd.DataFrame({
    "Metric": [
        "Total Movies",
        "Total Genres",
        "Average Rating",
        "Average Runtime",
        "Total Revenue",
        "Total Budget",
        "Total Profit",
        "Average Revenue",
        "Budget-Revenue Correlation"
    ],
    "Value": [
        len(df),
        genre_analysis["genre"].nunique(),
        df["vote_average"].mean(),
        df["runtime"].mean(),
        df["revenue"].sum(),
        df["budget"].sum(),
        df["profit"].sum(),
        df["revenue"].mean(),
        budget_revenue_correlation
    ]
})

summary["Value"] = summary["Value"].round(2)

summary.to_csv(
    os.path.join(
        RESULTS_DIR,
        "analysis_summary.csv"
    ),
    index=False
)


# ============================================================
# FINAL OUTPUT
# ============================================================

print("\n" + "=" * 70)
print("ANALYSIS COMPLETED")
print("=" * 70)

print(f"\nResults saved in:")
print(RESULTS_DIR)

print("\nGenerated files:")

for file in sorted(os.listdir(RESULTS_DIR)):
    print(f"- {file}")

print("\n" + "=" * 70)
print("KEY RESULTS")
print("=" * 70)

print(f"\nTotal movies: {len(df):,}")

print(
    f"Average rating: "
    f"{df['vote_average'].mean():.2f}"
)

print(
    f"Average runtime: "
    f"{df['runtime'].mean():.2f} minutes"
)

print(
    f"Total revenue: "
    f"${df['revenue'].sum():,.2f}"
)

print(
    f"Total profit: "
    f"${df['profit'].sum():,.2f}"
)

print(
    f"Budget-Revenue correlation: "
    f"{budget_revenue_correlation:.4f}"
)

print(
    f"\nMinimum votes for rating ranking: "
    f"{MIN_VOTES:,}"
)

print("\nTop 5 highest-grossing movies:")

for _, movie in highest_grossing.head(5).iterrows():
    print(
        f"- {movie['title']} "
        f"(${movie['revenue']:,.0f})"
    )

print("\nTop 5 highest-rated movies:")
    
for _, movie in highest_rated.head(5).iterrows():
    print(
        f"- {movie['title']} "
        f"(Rating: {movie['vote_average']:.1f}, "
        f"Votes: {movie['vote_count']:,}, "
        f"Weighted: {movie['weighted_rating']:.2f})"
    )

print("\n" + "=" * 70)
print("DONE")
print("=" * 70)