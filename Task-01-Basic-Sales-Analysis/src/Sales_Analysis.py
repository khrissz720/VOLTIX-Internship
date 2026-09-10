# ============================================================
# VOLTIX INTERNSHIP - TASK 1
# BASIC SALES DATA ANALYSIS
# ============================================================

import pandas as pd
import matplotlib.pyplot as plt
import os

# ============================================================
# 1. CONFIGURACIÓN
# ============================================================

INPUT_FILE = "EzzSteel_Full_Dataset.xlsx"
SHEET_NAME = "Sales_Transactions"

CLEAN_FILE = "EzzSteel_Cleaned.xlsx"
ANALYSIS_FILE = "Sales_Analysis.xlsx"

# Carpeta donde se guardarán los gráficos
CHARTS_FOLDER = "Charts"

os.makedirs(CHARTS_FOLDER, exist_ok=True)


# ============================================================
# 2. CARGAR DATASET
# ============================================================

print("=" * 60)
print("1. CARGANDO DATASET")
print("=" * 60)

df = pd.read_excel(INPUT_FILE, sheet_name=SHEET_NAME)

print(f"Filas: {df.shape[0]}")
print(f"Columnas: {df.shape[1]}")
print("\nColumnas:")
print(df.columns.tolist())


# ============================================================
# 3. DATA CLEANING
# ============================================================

print("\n" + "=" * 60)
print("2. DATA CLEANING")
print("=" * 60)


# -------------------------
# Missing Values
# -------------------------

print("\n--- Missing Values ---")
print(df.isnull().sum())


# -------------------------
# Duplicates
# -------------------------

print("\n--- Duplicates ---")
print(f"Duplicated rows: {df.duplicated().sum()}")

df = df.drop_duplicates()


# -------------------------
# Data Types
# -------------------------

print("\n--- Data Types Before Cleaning ---")
print(df.dtypes)


# -------------------------
# Invoice Date
# -------------------------

df["Invoice_Date"] = pd.to_datetime(
    df["Invoice_Date"],
    format="mixed",
    dayfirst=True,
    errors="coerce"
)


# -------------------------
# Revenue
# -------------------------

df["Revenue_EGP"] = (
    df["Revenue_EGP"]
    .astype(str)
    .str.replace(r"[^\d.-]", "", regex=True)
)

df["Revenue_EGP"] = pd.to_numeric(
    df["Revenue_EGP"],
    errors="coerce"
)


# -------------------------
# Quantity
# -------------------------

df["Quantity_Tons"] = pd.to_numeric(
    df["Quantity_Tons"],
    errors="coerce"
)


# -------------------------
# Product Type
# -------------------------

df["Product_Type"] = (
    df["Product_Type"]
    .astype(str)
    .str.strip()
)


# -------------------------
# Governorate
# -------------------------

df["Governorate"] = (
    df["Governorate"]
    .astype(str)
    .str.strip()
)


# ============================================================
# 4. MISSING VALUES AFTER CLEANING
# ============================================================

print("\n--- Missing Values After Cleaning ---")
print(df.isnull().sum())


# ============================================================
# 5. GUARDAR DATASET LIMPIO
# ============================================================

df.to_excel(CLEAN_FILE, index=False)

print(f"\nClean dataset saved as: {CLEAN_FILE}")


# ============================================================
# 6. SALES ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("3. SALES ANALYSIS")
print("=" * 60)


# ------------------------------------------------------------
# Total Sales
# ------------------------------------------------------------

total_sales = df["Revenue_EGP"].sum()

print(f"\nTotal Sales: {total_sales:,.2f} EGP")


# ------------------------------------------------------------
# Total Profit
# ------------------------------------------------------------

# The dataset does not contain Profit or sufficient cost data.
print("\nTotal Profit: Cannot be calculated accurately.")
print("Reason: The dataset does not contain a Profit column or")
print("sufficient cost information to calculate profit.")


# ------------------------------------------------------------
# Best Product
# ------------------------------------------------------------

sales_by_product = (
    df.groupby("Product_Type")["Revenue_EGP"]
    .sum()
    .sort_values(ascending=False)
)

best_product = sales_by_product.index[0]
best_product_sales = sales_by_product.iloc[0]

print(f"\nBest Product: {best_product}")
print(f"Sales: {best_product_sales:,.2f} EGP")


# ------------------------------------------------------------
# Best Region
# ------------------------------------------------------------

sales_by_region = (
    df.groupby("Governorate")["Revenue_EGP"]
    .sum()
    .sort_values(ascending=False)
)

best_region = sales_by_region.index[0]
best_region_sales = sales_by_region.iloc[0]

print(f"\nBest Region: {best_region}")
print(f"Sales: {best_region_sales:,.2f} EGP")


# ------------------------------------------------------------
# Best Month
# ------------------------------------------------------------

df["YearMonth"] = df["Invoice_Date"].dt.to_period("M")

monthly_sales = (
    df.groupby("YearMonth")["Revenue_EGP"]
    .sum()
    .sort_index()
)

best_month = monthly_sales.idxmax()
best_month_sales = monthly_sales.max()

print(f"\nBest Month: {best_month}")
print(f"Sales: {best_month_sales:,.2f} EGP")


# ============================================================
# 7. CREATE CHARTS
# ============================================================

print("\n" + "=" * 60)
print("4. CREATING CHARTS")
print("=" * 60)


# ============================================================
# CHART 1 — SALES BY PRODUCT
# ============================================================

plt.figure(figsize=(10, 6))

sales_by_product.sort_values().plot(
    kind="barh"
)

plt.title("Sales by Product Type")
plt.xlabel("Sales (EGP)")
plt.ylabel("Product Type")
plt.tight_layout()

plt.savefig(
    os.path.join(CHARTS_FOLDER, "sales_by_product.png"),
    dpi=300
)

plt.close()

print("✓ sales_by_product.png")


# ============================================================
# CHART 2 — SALES OVER TIME
# ============================================================

plt.figure(figsize=(12, 6))

monthly_sales.index = monthly_sales.index.astype(str)

monthly_sales.plot(
    kind="line",
    marker="o"
)

plt.title("Sales Over Time")
plt.xlabel("Month")
plt.ylabel("Sales (EGP)")
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig(
    os.path.join(CHARTS_FOLDER, "sales_over_time.png"),
    dpi=300
)

plt.close()

print("✓ sales_over_time.png")


# ============================================================
# CHART 3 — TOP PRODUCTS
# ============================================================

top_products = sales_by_product.head(10).sort_values()

plt.figure(figsize=(10, 6))

top_products.plot(
    kind="barh"
)

plt.title("Top Products by Sales")
plt.xlabel("Sales (EGP)")
plt.ylabel("Product Type")
plt.tight_layout()

plt.savefig(
    os.path.join(CHARTS_FOLDER, "top_products.png"),
    dpi=300
)

plt.close()

print("✓ top_products.png")


# ============================================================
# CHART 4 — SALES BY REGION
# ============================================================

top_regions = sales_by_region.head(10).sort_values()

plt.figure(figsize=(10, 6))

top_regions.plot(
    kind="barh"
)

plt.title("Top 10 Regions by Sales")
plt.xlabel("Sales (EGP)")
plt.ylabel("Governorate")
plt.tight_layout()

plt.savefig(
    os.path.join(CHARTS_FOLDER, "sales_by_region.png"),
    dpi=300
)

plt.close()

print("✓ sales_by_region.png")


# ============================================================
# 8. EXPORT ANALYSIS RESULTS
# ============================================================

results = {
    "Metric": [
        "Total Sales",
        "Total Profit",
        "Best Product",
        "Best Product Sales",
        "Best Region",
        "Best Region Sales",
        "Best Month",
        "Best Month Sales"
    ],

    "Value": [
        total_sales,
        "Not available",
        best_product,
        best_product_sales,
        best_region,
        best_region_sales,
        str(best_month),
        best_month_sales
    ]
}

results_df = pd.DataFrame(results)

with pd.ExcelWriter(ANALYSIS_FILE, engine="openpyxl") as writer:

    results_df.to_excel(
        writer,
        sheet_name="Summary",
        index=False
    )

    sales_by_product.reset_index().to_excel(
        writer,
        sheet_name="Sales_by_Product",
        index=False
    )

    sales_by_region.reset_index().to_excel(
        writer,
        sheet_name="Sales_by_Region",
        index=False
    )

    monthly_sales.reset_index().to_excel(
        writer,
        sheet_name="Sales_by_Month",
        index=False
    )


print(f"\nAnalysis results saved as: {ANALYSIS_FILE}")


# ============================================================
# 9. FINAL SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("5. FINAL SUMMARY")
print("=" * 60)

print(f"""
Total Sales:
{total_sales:,.2f} EGP

Total Profit:
Not available in the dataset.

Best Product:
{best_product}
{best_product_sales:,.2f} EGP

Best Region:
{best_region}
{best_region_sales:,.2f} EGP

Best Month:
{best_month}
{best_month_sales:,.2f} EGP

Charts saved in:
{CHARTS_FOLDER}/

Files generated:
- {CLEAN_FILE}
- {ANALYSIS_FILE}
""")

print("=" * 60)
print("TASK 1 ANALYSIS COMPLETED")
print("=" * 60)
