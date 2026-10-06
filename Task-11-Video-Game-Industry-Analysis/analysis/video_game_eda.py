import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


# ============================================================
# PATH CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
VIS_DIR = BASE_DIR / "visualizations"

VIS_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# LOAD CLEANED DATASETS
# ============================================================

main_file = DATA_DIR / "video_games_sales_cleaned.csv"
ps4_file = DATA_DIR / "ps4_games_sales_cleaned.csv"
xbox_file = DATA_DIR / "xboxone_games_sales_cleaned.csv"


df = pd.read_csv(main_file)
df_ps4 = pd.read_csv(ps4_file)
df_xbox = pd.read_csv(xbox_file)


# ============================================================
# DATA TYPES
# ============================================================

df["Year_of_Release"] = pd.to_numeric(
    df["Year_of_Release"],
    errors="coerce"
)

df["Global_Sales"] = pd.to_numeric(
    df["Global_Sales"],
    errors="coerce"
)

df["Critic_Score"] = pd.to_numeric(
    df["Critic_Score"],
    errors="coerce"
)

df["User_Score"] = pd.to_numeric(
    df["User_Score"],
    errors="coerce"
)


# ============================================================
# CREATE OUTPUT DIRECTORY
# ============================================================

print("\n========================================")
print("TASK 11 - EXPLORATORY DATA ANALYSIS")
print("========================================")


# ============================================================
# 1. GENERAL DATASET OVERVIEW
# ============================================================

print("\n1. DATASET OVERVIEW")
print("----------------------------------------")

print("Rows:", len(df))
print("Columns:", len(df.columns))

print("\nColumns:")
for column in df.columns:
    print("-", column)


# ============================================================
# 2. MAIN KPIs
# ============================================================

total_games = df["Name"].nunique()

total_sales = df["Global_Sales"].sum()

average_sales = df["Global_Sales"].mean()

top_genre = (
    df["Genre"]
    .value_counts()
    .idxmax()
)

top_platform = (
    df.groupby("Platform")["Global_Sales"]
    .sum()
    .idxmax()
)

top_publisher = (
    df.groupby("Publisher")["Global_Sales"]
    .sum()
    .idxmax()
)


print("\n2. KEY PERFORMANCE INDICATORS")
print("----------------------------------------")

print(f"Total Games: {total_games:,}")
print(f"Total Global Sales: {total_sales:,.2f} million")
print(f"Average Sales per Game: {average_sales:,.2f} million")
print(f"Top Genre by Number of Games: {top_genre}")
print(f"Top Platform by Sales: {top_platform}")
print(f"Top Publisher by Sales: {top_publisher}")


# ============================================================
# 3. MOST COMMON GENRES
# ============================================================

genre_count = (
    df["Genre"]
    .value_counts()
    .reset_index()
)

genre_count.columns = [
    "Genre",
    "Game_Count"
]

genre_count.to_csv(
    VIS_DIR / "genre_game_count.csv",
    index=False
)


print("\n3. MOST COMMON GENRES")
print("----------------------------------------")
print(genre_count)


# ============================================================
# GENRE DISTRIBUTION CHART
# ============================================================

plt.figure(figsize=(10, 6))

plt.bar(
    genre_count["Genre"],
    genre_count["Game_Count"]
)

plt.title("Number of Games by Genre")
plt.xlabel("Genre")
plt.ylabel("Number of Games")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    VIS_DIR / "genre_distribution.png",
    dpi=300
)

plt.close()


# ============================================================
# 4. SALES BY GENRE
# ============================================================

genre_sales = (
    df.groupby("Genre")["Global_Sales"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

genre_sales.columns = [
    "Genre",
    "Global_Sales"
]

genre_sales.to_csv(
    VIS_DIR / "sales_by_genre.csv",
    index=False
)


print("\n4. SALES BY GENRE")
print("----------------------------------------")
print(genre_sales)


# ============================================================
# SALES BY GENRE CHART
# ============================================================

plt.figure(figsize=(10, 6))

plt.bar(
    genre_sales["Genre"],
    genre_sales["Global_Sales"]
)

plt.title("Global Sales by Genre")
plt.xlabel("Genre")
plt.ylabel("Global Sales (Millions)")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    VIS_DIR / "sales_by_genre.png",
    dpi=300
)

plt.close()


# ============================================================
# 5. SALES BY PLATFORM
# ============================================================

platform_sales = (
    df.groupby("Platform")["Global_Sales"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

platform_sales.columns = [
    "Platform",
    "Global_Sales"
]

platform_sales.to_csv(
    VIS_DIR / "sales_by_platform.csv",
    index=False
)


print("\n5. TOP PLATFORMS BY SALES")
print("----------------------------------------")
print(platform_sales.head(15))


# ============================================================
# PLATFORM SALES CHART
# ============================================================

top_platforms = platform_sales.head(15)

plt.figure(figsize=(11, 6))

plt.bar(
    top_platforms["Platform"],
    top_platforms["Global_Sales"]
)

plt.title("Top 15 Platforms by Global Sales")
plt.xlabel("Platform")
plt.ylabel("Global Sales (Millions)")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    VIS_DIR / "sales_by_platform.png",
    dpi=300
)

plt.close()


# ============================================================
# 6. TOP PUBLISHERS
# ============================================================

publisher_sales = (
    df.groupby("Publisher")["Global_Sales"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

publisher_sales.columns = [
    "Publisher",
    "Global_Sales"
]

publisher_sales.to_csv(
    VIS_DIR / "sales_by_publisher.csv",
    index=False
)


print("\n6. TOP PUBLISHERS")
print("----------------------------------------")
print(publisher_sales.head(15))


# ============================================================
# PUBLISHER CHART
# ============================================================

top_publishers = publisher_sales.head(15)

plt.figure(figsize=(11, 7))

plt.barh(
    top_publishers["Publisher"].iloc[::-1],
    top_publishers["Global_Sales"].iloc[::-1]
)

plt.title("Top 15 Publishers by Global Sales")
plt.xlabel("Global Sales (Millions)")
plt.ylabel("Publisher")

plt.tight_layout()

plt.savefig(
    VIS_DIR / "sales_by_publisher.png",
    dpi=300
)

plt.close()


# ============================================================
# 7. BEST-SELLING GAMES
# ============================================================

top_games = (
    df[
        [
            "Name",
            "Platform",
            "Genre",
            "Publisher",
            "Global_Sales"
        ]
    ]
    .sort_values(
        "Global_Sales",
        ascending=False
    )
    .head(20)
)

top_games.to_csv(
    VIS_DIR / "top_20_games.csv",
    index=False
)


print("\n7. TOP 20 BEST-SELLING GAMES")
print("----------------------------------------")
print(top_games.to_string(index=False))


# ============================================================
# BEST-SELLING GAMES CHART
# ============================================================

top_games_chart = top_games.head(10).sort_values(
    "Global_Sales"
)

plt.figure(figsize=(11, 7))

plt.barh(
    top_games_chart["Name"],
    top_games_chart["Global_Sales"]
)

plt.title("Top 10 Best-Selling Video Games")
plt.xlabel("Global Sales (Millions)")
plt.ylabel("Game")

plt.tight_layout()

plt.savefig(
    VIS_DIR / "top_10_games.png",
    dpi=300
)

plt.close()


# ============================================================
# 8. SALES TREND BY YEAR
# ============================================================

# The original dataset is a December 2016 snapshot.
# Therefore, the historical trend uses releases from 1980-2016.

year_sales = (
    df[
        (df["Year_of_Release"] >= 1980) &
        (df["Year_of_Release"] <= 2016)
    ]
    .groupby("Year_of_Release")["Global_Sales"]
    .sum()
    .reset_index()
)

year_sales.columns = [
    "Year",
    "Global_Sales"
]

year_sales.to_csv(
    VIS_DIR / "sales_by_year.csv",
    index=False
)


print("\n8. SALES BY YEAR")
print("----------------------------------------")
print(year_sales)


# ============================================================
# SALES TREND CHART
# ============================================================

plt.figure(figsize=(12, 6))

plt.plot(
    year_sales["Year"],
    year_sales["Global_Sales"],
    marker="o"
)

plt.title("Global Video Game Sales by Year")
plt.xlabel("Year")
plt.ylabel("Global Sales (Millions)")

plt.grid(True, alpha=0.3)

plt.tight_layout()

plt.savefig(
    VIS_DIR / "sales_trend.png",
    dpi=300
)

plt.close()


# ============================================================
# 9. REGIONAL SALES
# ============================================================

regional_sales = pd.DataFrame({
    "Region": [
        "North America",
        "Europe",
        "Japan",
        "Other Regions"
    ],
    "Sales": [
        df["NA_Sales"].sum(),
        df["EU_Sales"].sum(),
        df["JP_Sales"].sum(),
        df["Other_Sales"].sum()
    ]
})

regional_sales = regional_sales.sort_values(
    "Sales",
    ascending=False
)

regional_sales.to_csv(
    VIS_DIR / "regional_sales.csv",
    index=False
)


print("\n9. REGIONAL SALES")
print("----------------------------------------")
print(regional_sales)


# ============================================================
# REGIONAL SALES CHART
# ============================================================

plt.figure(figsize=(8, 6))

plt.bar(
    regional_sales["Region"],
    regional_sales["Sales"]
)

plt.title("Video Game Sales by Region")
plt.xlabel("Region")
plt.ylabel("Sales (Millions)")

plt.xticks(rotation=30)

plt.tight_layout()

plt.savefig(
    VIS_DIR / "regional_sales.png",
    dpi=300
)

plt.close()


# ============================================================
# 10. RATING VS SALES
# ============================================================

rating_sales = df[
    [
        "Name",
        "Critic_Score",
        "User_Score",
        "Global_Sales"
    ]
].dropna(
    subset=[
        "Critic_Score",
        "Global_Sales"
    ]
)


print("\n10. RATING VS SALES")
print("----------------------------------------")

critic_correlation = rating_sales[
    "Critic_Score"
].corr(
    rating_sales["Global_Sales"]
)

print(
    f"Critic Score vs Global Sales correlation: "
    f"{critic_correlation:.4f}"
)


# ============================================================
# RATING VS SALES SCATTER PLOT
# ============================================================

plt.figure(figsize=(9, 6))

plt.scatter(
    rating_sales["Critic_Score"],
    rating_sales["Global_Sales"],
    alpha=0.4
)

plt.title("Critic Score vs Global Sales")
plt.xlabel("Critic Score")
plt.ylabel("Global Sales (Millions)")

plt.grid(True, alpha=0.3)

plt.tight_layout()

plt.savefig(
    VIS_DIR / "rating_vs_sales.png",
    dpi=300
)

plt.close()


# ============================================================
# 11. PS4 ANALYSIS
# ============================================================

print("\n11. PS4 ANALYSIS")
print("----------------------------------------")

ps4_top_genres = (
    df_ps4.groupby("Genre")["Global"]
    .sum()
    .sort_values(ascending=False)
)

ps4_top_publishers = (
    df_ps4.groupby("Publisher")["Global"]
    .sum()
    .sort_values(ascending=False)
)

print("Top PS4 Genres:")
print(ps4_top_genres.head(10))

print("\nTop PS4 Publishers:")
print(ps4_top_publishers.head(10))


# ============================================================
# 12. XBOX ONE ANALYSIS
# ============================================================

print("\n12. XBOX ONE ANALYSIS")
print("----------------------------------------")

xbox_top_genres = (
    df_xbox.groupby("Genre")["Global"]
    .sum()
    .sort_values(ascending=False)
)

xbox_top_publishers = (
    df_xbox.groupby("Publisher")["Global"]
    .sum()
    .sort_values(ascending=False)
)

print("Top Xbox One Genres:")
print(xbox_top_genres.head(10))

print("\nTop Xbox One Publishers:")
print(xbox_top_publishers.head(10))


# ============================================================
# 13. PS4 VS XBOX ONE
# ============================================================

comparison = pd.DataFrame({
    "Platform": [
        "PS4",
        "Xbox One"
    ],
    "Games": [
        len(df_ps4),
        len(df_xbox)
    ],
    "Global_Sales": [
        df_ps4["Global"].sum(),
        df_xbox["Global"].sum()
    ]
})

comparison.to_csv(
    VIS_DIR / "ps4_vs_xbox_one.csv",
    index=False
)


print("\n13. PS4 VS XBOX ONE")
print("----------------------------------------")
print(comparison)


# ============================================================
# 14. FINAL SUMMARY
# ============================================================

summary = pd.DataFrame({
    "Metric": [
        "Total Games",
        "Total Global Sales (Millions)",
        "Average Sales per Game (Millions)",
        "Top Genre",
        "Top Platform",
        "Top Publisher",
        "Critic Score vs Sales Correlation"
    ],
    "Value": [
        total_games,
        total_sales,
        average_sales,
        top_genre,
        top_platform,
        top_publisher,
        critic_correlation
    ]
})

summary.to_csv(
    VIS_DIR / "kpi_summary.csv",
    index=False
)


# ============================================================
# COMPLETION MESSAGE
# ============================================================

print("\n========================================")
print("EDA COMPLETED SUCCESSFULLY")
print("========================================")

print("\nVisualizations saved in:")
print(VIS_DIR)

print("\nGenerated analysis files:")
print("- genre_game_count.csv")
print("- sales_by_genre.csv")
print("- sales_by_platform.csv")
print("- sales_by_publisher.csv")
print("- top_20_games.csv")
print("- sales_by_year.csv")
print("- regional_sales.csv")
print("- ps4_vs_xbox_one.csv")
print("- kpi_summary.csv")

print("\nGenerated visualizations:")
print("- genre_distribution.png")
print("- sales_by_genre.png")
print("- sales_by_platform.png")
print("- sales_by_publisher.png")
print("- top_10_games.png")
print("- sales_trend.png")
print("- regional_sales.png")
print("- rating_vs_sales.png")