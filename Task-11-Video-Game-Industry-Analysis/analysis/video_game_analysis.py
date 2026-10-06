
import pandas as pd
import numpy as np
from pathlib import Path


# ============================================================
# PATH CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"

print("Data directory:")
print(DATA_DIR)


# ============================================================
# FUNCTION TO LOAD CSV FILES
# ============================================================

def load_csv(file_path):
    """
    Load a CSV file using UTF-8.
    If UTF-8 fails, CP1252 is used as a fallback.
    """

    try:
        return pd.read_csv(file_path, encoding="utf-8")
    except UnicodeDecodeError:
        print(f"UTF-8 encoding failed for {file_path.name}")
        print("Trying CP1252 encoding...")
        return pd.read_csv(file_path, encoding="cp1252")


# ============================================================
# 1. MAIN VIDEO GAME SALES DATASET
# ============================================================

print("\n========================================")
print("1. MAIN VIDEO GAME SALES DATASET")
print("========================================")

main_file = DATA_DIR / "Video_Games_Sales_as_at_22_Dec_2016.csv"

df_main = load_csv(main_file)

print("Original shape:", df_main.shape)


# ------------------------------------------------------------
# Remove rows without essential information
# ------------------------------------------------------------

df_main = df_main.dropna(
    subset=["Name", "Genre"]
).copy()


# ------------------------------------------------------------
# Convert Year_of_Release
# ------------------------------------------------------------

df_main["Year_of_Release"] = pd.to_numeric(
    df_main["Year_of_Release"],
    errors="coerce"
)

# Keep only reasonable release years
df_main.loc[
    ~df_main["Year_of_Release"].between(1980, 2020),
    "Year_of_Release"
] = np.nan

df_main["Year_of_Release"] = (
    df_main["Year_of_Release"].astype("Int64")
)


# ------------------------------------------------------------
# Convert numerical columns
# ------------------------------------------------------------

main_numeric_columns = [
    "NA_Sales",
    "EU_Sales",
    "JP_Sales",
    "Other_Sales",
    "Global_Sales",
    "Critic_Score",
    "Critic_Count",
    "User_Score",
    "User_Count"
]

for column in main_numeric_columns:

    if column in df_main.columns:

        df_main[column] = pd.to_numeric(
            df_main[column],
            errors="coerce"
        )


# ------------------------------------------------------------
# Convert User_Score
# ------------------------------------------------------------

# Values such as "tbd" are converted to NaN.
# They are not treated as zero because "tbd" means
# that the score was not yet determined.

df_main["User_Score"] = pd.to_numeric(
    df_main["User_Score"],
    errors="coerce"
)


# ------------------------------------------------------------
# Remove negative sales values
# ------------------------------------------------------------

main_sales_columns = [
    "NA_Sales",
    "EU_Sales",
    "JP_Sales",
    "Other_Sales",
    "Global_Sales"
]

for column in main_sales_columns:

    df_main.loc[
        df_main[column] < 0,
        column
    ] = np.nan


# ------------------------------------------------------------
# Handle missing categorical values
# ------------------------------------------------------------

categorical_columns = [
    "Publisher",
    "Developer",
    "Rating"
]

for column in categorical_columns:

    if column in df_main.columns:

        df_main[column] = df_main[column].fillna(
            "Unknown"
        )


# ------------------------------------------------------------
# Remove exact duplicates
# ------------------------------------------------------------

duplicates_main = df_main.duplicated().sum()

print("Duplicate rows found:", duplicates_main)

df_main = df_main.drop_duplicates()


# ------------------------------------------------------------
# Save cleaned main dataset
# ------------------------------------------------------------

main_output = DATA_DIR / "video_games_sales_cleaned.csv"

df_main.to_csv(
    main_output,
    index=False,
    encoding="utf-8"
)

print("Cleaned shape:", df_main.shape)
print("Saved:", main_output)


# ============================================================
# 2. PS4 DATASET
# ============================================================

print("\n========================================")
print("2. PS4 DATASET")
print("========================================")

ps4_file = DATA_DIR / "PS4_GamesSales.csv"

df_ps4 = load_csv(ps4_file)

print("Original shape:", df_ps4.shape)


# ------------------------------------------------------------
# Convert Year
# ------------------------------------------------------------

df_ps4["Year"] = pd.to_numeric(
    df_ps4["Year"],
    errors="coerce"
)

df_ps4.loc[
    ~df_ps4["Year"].between(1980, 2020),
    "Year"
] = np.nan

df_ps4["Year"] = df_ps4["Year"].astype("Int64")


# ------------------------------------------------------------
# Convert sales columns
# ------------------------------------------------------------

ps4_sales_columns = [
    "North America",
    "Europe",
    "Japan",
    "Rest of World",
    "Global"
]

for column in ps4_sales_columns:

    df_ps4[column] = pd.to_numeric(
        df_ps4[column],
        errors="coerce"
    )

    df_ps4.loc[
        df_ps4[column] < 0,
        column
    ] = np.nan


# ------------------------------------------------------------
# Handle missing publisher
# ------------------------------------------------------------

df_ps4["Publisher"] = df_ps4[
    "Publisher"
].fillna("Unknown")


# ------------------------------------------------------------
# Remove duplicates
# ------------------------------------------------------------

duplicates_ps4 = df_ps4.duplicated().sum()

print("Duplicate rows found:", duplicates_ps4)

df_ps4 = df_ps4.drop_duplicates()


# ------------------------------------------------------------
# Save cleaned PS4 dataset
# ------------------------------------------------------------

ps4_output = DATA_DIR / "ps4_games_sales_cleaned.csv"

df_ps4.to_csv(
    ps4_output,
    index=False,
    encoding="utf-8"
)

print("Cleaned shape:", df_ps4.shape)
print("Saved:", ps4_output)


# ============================================================
# 3. XBOX ONE DATASET
# ============================================================

print("\n========================================")
print("3. XBOX ONE DATASET")
print("========================================")

xbox_file = DATA_DIR / "XboxOne_GameSales.csv"

df_xbox = load_csv(xbox_file)

print("Original shape:", df_xbox.shape)


# ------------------------------------------------------------
# Convert position
# ------------------------------------------------------------

df_xbox["Pos"] = pd.to_numeric(
    df_xbox["Pos"],
    errors="coerce"
)

df_xbox["Pos"] = df_xbox["Pos"].astype("Int64")


# ------------------------------------------------------------
# Convert Year
# ------------------------------------------------------------

df_xbox["Year"] = pd.to_numeric(
    df_xbox["Year"],
    errors="coerce"
)

df_xbox.loc[
    ~df_xbox["Year"].between(1980, 2020),
    "Year"
] = np.nan

df_xbox["Year"] = df_xbox["Year"].astype("Int64")


# ------------------------------------------------------------
# Convert sales columns
# ------------------------------------------------------------

xbox_sales_columns = [
    "North America",
    "Europe",
    "Japan",
    "Rest of World",
    "Global"
]

for column in xbox_sales_columns:

    df_xbox[column] = pd.to_numeric(
        df_xbox[column],
        errors="coerce"
    )

    df_xbox.loc[
        df_xbox[column] < 0,
        column
    ] = np.nan


# ------------------------------------------------------------
# Handle missing publisher
# ------------------------------------------------------------

df_xbox["Publisher"] = df_xbox[
    "Publisher"
].fillna("Unknown")


# ------------------------------------------------------------
# Remove duplicates
# ------------------------------------------------------------

duplicates_xbox = df_xbox.duplicated().sum()

print("Duplicate rows found:", duplicates_xbox)

df_xbox = df_xbox.drop_duplicates()


# ------------------------------------------------------------
# Save cleaned Xbox One dataset
# ------------------------------------------------------------

xbox_output = DATA_DIR / "xboxone_games_sales_cleaned.csv"

df_xbox.to_csv(
    xbox_output,
    index=False,
    encoding="utf-8"
)

print("Cleaned shape:", df_xbox.shape)
print("Saved:", xbox_output)


# ============================================================
# FINAL CLEANING SUMMARY
# ============================================================

print("\n========================================")
print("CLEANING COMPLETED")
print("========================================")

print(
    f"Main dataset: {df_main.shape[0]} rows, "
    f"{df_main.shape[1]} columns"
)

print(
    f"PS4 dataset: {df_ps4.shape[0]} rows, "
    f"{df_ps4.shape[1]} columns"
)

print(
    f"Xbox One dataset: {df_xbox.shape[0]} rows, "
    f"{df_xbox.shape[1]} columns"
)

print("\nCleaned files created:")

print(
    "1.",
    DATA_DIR / "video_games_sales_cleaned.csv"
)

print(
    "2.",
    DATA_DIR / "ps4_games_sales_cleaned.csv"
)

print(
    "3.",
    DATA_DIR / "xboxone_games_sales_cleaned.csv"
)

print("\nTask 11 cleaning process finished successfully.")