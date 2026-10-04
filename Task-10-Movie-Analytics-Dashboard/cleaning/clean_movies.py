import pandas as pd
import ast
import os


# ============================================================
# TASK 10 - MOVIE ANALYTICS DASHBOARD
# Data Cleaning Script
# ============================================================

# ------------------------------------------------------------
# 1. Define paths
# ------------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INPUT_FILE = os.path.join(
    BASE_DIR,
    "data",
    "tmdb_5000_movies.csv"
)

OUTPUT_FILE = os.path.join(
    BASE_DIR,
    "data",
    "movies_cleaned.csv"
)

REPORT_FILE = os.path.join(
    BASE_DIR,
    "cleaning",
    "cleaning_report.txt"
)


# ------------------------------------------------------------
# 2. Load dataset
# ------------------------------------------------------------

print("=" * 60)
print("TASK 10 - MOVIE ANALYTICS DASHBOARD")
print("DATA CLEANING")
print("=" * 60)

print("\nLoading dataset...")

df = pd.read_csv(INPUT_FILE)

print(f"Original rows: {len(df)}")
print(f"Original columns: {len(df.columns)}")


# ------------------------------------------------------------
# 3. Initial inspection
# ------------------------------------------------------------

original_rows = len(df)
original_columns = len(df.columns)

duplicates = df.duplicated().sum()

nulls_before = df.isnull().sum()


# ------------------------------------------------------------
# 4. Convert release date to datetime
# ------------------------------------------------------------

print("\nConverting release_date...")

df["release_date"] = pd.to_datetime(
    df["release_date"],
    errors="coerce"
)

# Create release year

df["release_year"] = df["release_date"].dt.year


# ------------------------------------------------------------
# 5. Handle missing runtime
# ------------------------------------------------------------

print("Handling missing runtime...")

runtime_missing = df["runtime"].isna().sum()

# Missing runtime will be kept as NaN.
# We do not invent movie durations.


# ------------------------------------------------------------
# 6. Check numeric columns
# ------------------------------------------------------------

numeric_columns = [
    "budget",
    "revenue",
    "runtime",
    "popularity",
    "vote_average",
    "vote_count"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )


# ------------------------------------------------------------
# 7. Process genres
# ------------------------------------------------------------

print("Processing genres...")

def extract_genres(value):
    """
    Extract genre names from the JSON-like genres column.
    Example:
    [{"id": 28, "name": "Action"},
     {"id": 12, "name": "Adventure"}]

    Returns:
    Action | Adventure
    """

    try:
        genres = ast.literal_eval(value)

        if isinstance(genres, list):
            names = [
                genre.get("name")
                for genre in genres
                if isinstance(genre, dict)
                and genre.get("name")
            ]

            return " | ".join(names)

    except (ValueError, SyntaxError, TypeError):
        pass

    return "No Genre"


df["genres_clean"] = df["genres"].apply(extract_genres)


# ------------------------------------------------------------
# 8. Create primary genre
# ------------------------------------------------------------

def get_primary_genre(value):
    if pd.isna(value) or value == "":
        return "No Genre"

    return value.split(" | ")[0]


df["primary_genre"] = df["genres_clean"].apply(
    get_primary_genre
)


# ------------------------------------------------------------
# 9. Create useful financial metrics
# ------------------------------------------------------------

print("Creating financial metrics...")

# Profit

df["profit"] = df["revenue"] - df["budget"]


# Return on Investment (ROI)

df["roi"] = 0.0

valid_budget = df["budget"] > 0

df.loc[valid_budget, "roi"] = (
    df.loc[valid_budget, "revenue"]
    / df.loc[valid_budget, "budget"]
)


# ------------------------------------------------------------
# 10. Create runtime categories
# ------------------------------------------------------------

def runtime_category(runtime):

    if pd.isna(runtime):
        return "Unknown"

    if runtime < 90:
        return "Short (<90 min)"

    elif runtime < 120:
        return "Standard (90-119 min)"

    elif runtime < 150:
        return "Long (120-149 min)"

    else:
        return "Very Long (150+ min)"


df["runtime_category"] = df["runtime"].apply(
    runtime_category
)


# ------------------------------------------------------------
# 11. Create rating categories
# ------------------------------------------------------------

def rating_category(rating):

    if pd.isna(rating):
        return "Unknown"

    if rating < 5:
        return "Low (<5)"

    elif rating < 7:
        return "Medium (5-6.9)"

    elif rating < 8:
        return "Good (7-7.9)"

    else:
        return "Excellent (8+)"


df["rating_category"] = df["vote_average"].apply(
    rating_category
)


# ------------------------------------------------------------
# 12. Create vote-count categories
# ------------------------------------------------------------

def vote_count_category(votes):

    if pd.isna(votes):
        return "Unknown"

    if votes < 100:
        return "Low (<100)"

    elif votes < 1000:
        return "Medium (100-999)"

    elif votes < 5000:
        return "High (1K-4.9K)"

    else:
        return "Very High (5K+)"


df["vote_count_category"] = df["vote_count"].apply(
    vote_count_category
)


# ------------------------------------------------------------
# 13. Handle missing text values
# ------------------------------------------------------------

text_columns = [
    "homepage",
    "overview",
    "tagline"
]

for column in text_columns:
    df[column] = df[column].fillna("Not Available")


# ------------------------------------------------------------
# 14. Remove unnecessary columns
# ------------------------------------------------------------

columns_to_remove = [
    "homepage",
    "keywords",
    "production_companies",
    "production_countries",
    "spoken_languages",
    "tagline",
    "overview"
]

df = df.drop(
    columns=columns_to_remove,
    errors="ignore"
)


# ------------------------------------------------------------
# 15. Final column organization
# ------------------------------------------------------------

final_columns = [
    "id",
    "title",
    "original_title",
    "original_language",
    "release_date",
    "release_year",
    "genres_clean",
    "primary_genre",
    "budget",
    "revenue",
    "profit",
    "roi",
    "runtime",
    "runtime_category",
    "popularity",
    "vote_average",
    "rating_category",
    "vote_count",
    "vote_count_category",
    "status"
]

df = df[final_columns]


# ------------------------------------------------------------
# 16. Final validation
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("FINAL VALIDATION")
print("=" * 60)

print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")
print(f"Duplicates: {df.duplicated().sum()}")

print("\nMissing values:")

print(
    df.isnull().sum()[
        df.isnull().sum() > 0
    ]
)


# ------------------------------------------------------------
# 17. Save cleaned dataset
# ------------------------------------------------------------

df.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig"
)

print("\nCleaned dataset saved:")
print(OUTPUT_FILE)


# ------------------------------------------------------------
# 18. Generate cleaning report
# ------------------------------------------------------------

with open(
    REPORT_FILE,
    "w",
    encoding="utf-8"
) as report:

    report.write(
        "TASK 10 - MOVIE ANALYTICS DASHBOARD\n"
    )

    report.write(
        "DATA CLEANING REPORT\n"
    )

    report.write("=" * 60 + "\n\n")

    report.write(
        f"Original rows: {original_rows}\n"
    )

    report.write(
        f"Original columns: {original_columns}\n"
    )

    report.write(
        f"Duplicate rows: {duplicates}\n"
    )

    report.write(
        f"Missing release dates: "
        f"{df['release_date'].isna().sum()}\n"
    )

    report.write(
        f"Missing runtime values: "
        f"{df['runtime'].isna().sum()}\n"
    )

    report.write(
        f"Final rows: {len(df)}\n"
    )

    report.write(
        f"Final columns: {len(df.columns)}\n"
    )

    report.write("\nFinal columns:\n")

    for column in df.columns:
        report.write(f"- {column}\n")


print("\nCleaning report saved:")
print(REPORT_FILE)

print("\n" + "=" * 60)
print("CLEANING COMPLETED SUCCESSFULLY")
print("=" * 60)