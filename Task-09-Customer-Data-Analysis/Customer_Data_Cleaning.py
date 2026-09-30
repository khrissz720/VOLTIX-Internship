import pandas as pd
from pathlib import Path

# ============================================================
# 1. File paths
# ============================================================

BASE = Path(__file__).resolve().parent

INPUT = BASE / "Customers_Fakedata.csv"
OUTPUT = BASE / "Customers_Fakedata_Cleaned.csv"


# ============================================================
# 2. Load dataset
# ============================================================

customers = pd.read_csv(INPUT)


# ============================================================
# 3. Clean column names
# ============================================================

# Remove unnecessary spaces from column names
customers.columns = customers.columns.str.strip()


# ============================================================
# 4. Remove empty / garbage columns
# ============================================================

# Remove columns whose names contain "Unnamed"
customers = customers.loc[
    :,
    ~customers.columns.str.contains(
        "^Unnamed",
        case=False,
        regex=True
    )
]



# ============================================================
# 5. Consolidate duplicated Gender columns
# ============================================================

# Find every column corresponding to Gender
gender_columns = [
    column
    for column in customers.columns
    if column.lower() == "gender"
]

if len(gender_columns) > 1:

    # Combine duplicated Gender columns.
    # The first non-null value is kept for each row.
    gender_data = customers[gender_columns].bfill(axis=1).iloc[:, 0]

    # Remove all duplicated Gender columns
    customers = customers.drop(columns=gender_columns)

    # Add one consolidated Gender column
    customers["Gender"] = gender_data

elif len(gender_columns) == 1:

    # Standardize the column name
    customers = customers.rename(
        columns={gender_columns[0]: "Gender"}
    )


# ============================================================
# 6. Handle invalid and missing numerical values
# ============================================================

# Age must be within a reasonable range.
# Values below 0 or above 100 are considered invalid.
customers.loc[
    (customers["Age"] < 0) | (customers["Age"] > 100),
    "Age"
] = pd.NA

# Replace missing and invalid Age values with the column mean
customers["Age"] = customers["Age"].fillna(
    customers["Age"].mean()
)


# Rating is expected to be between 1 and 5.
# Values above 5 are considered invalid.
customers.loc[
    (customers["Rating"] < 1) | (customers["Rating"] > 5),
    "Rating"
] = pd.NA

# Replace missing and invalid Rating values with the column mean
customers["Rating"] = customers["Rating"].fillna(
    customers["Rating"].mean()
)
# ============================================================
# 6.1 Standardize Gender values
# ============================================================

customers["Gender"] = (
    customers["Gender"]
    .astype("string")
    .str.strip()
    .str.lower()
    .replace({
        "f": "Female",
        "female": "Female",
        "m": "Male",
        "male": "Male",
        "no especificado": "No Especificado"
    })
)

# ============================================================
# 7. Convert PurchaseDate to datetime
# ============================================================

customers["PurchaseDate"] = pd.to_datetime(
    customers["PurchaseDate"],
    errors="coerce"
)


# ============================================================
# 8. Convert PurchaseAmount to numeric
# ============================================================

customers["PurchaseAmount"] = pd.to_numeric(
    customers["PurchaseAmount"],
    errors="coerce"
)


# ============================================================
# 9. Handle missing text values
# ============================================================

# Select only string columns.
# Using "str" avoids the Pandas 3/4 compatibility warning.
text_columns = customers.select_dtypes(
    include=["str"]
).columns

customers[text_columns] = customers[text_columns].fillna(
    "No Especificado"
)


# ============================================================
# 10. Save cleaned dataset
# ============================================================

customers.to_csv(
    OUTPUT,
    index=False
)


# ============================================================
# 11. Validation
# ============================================================

print("Cleaning completed successfully.")
print(f"Rows: {customers.shape[0]}")
print(f"Columns: {customers.shape[1]}")

print("\nFinal columns:")
print(customers.columns.tolist())

print("\nFinal data types:")
print(customers.dtypes)

print("\nRemaining null values:")
print(customers.isnull().sum())