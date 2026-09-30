import pandas as pd
from pathlib import Path

# ============================================================
# 1. File paths
# ============================================================

BASE = Path(__file__).resolve().parent
INPUT = BASE / "Customers_Fakedata_Cleaned.csv"


# ============================================================
# 2. Load cleaned dataset
# ============================================================

customers = pd.read_csv(INPUT)

# Convert date column to datetime
customers["PurchaseDate"] = pd.to_datetime(
    customers["PurchaseDate"],
    errors="coerce"
)


# ============================================================
# 3. Main KPIs
# ============================================================

total_customers = customers["CustomerID"].nunique()

valid_purchases = customers["PurchaseAmount"].dropna()

total_revenue = valid_purchases.sum()

average_purchase = valid_purchases.mean()

total_purchases = valid_purchases.count()

average_rating = customers["Rating"].mean()


# ============================================================
# 4. Sales by Product Category
# ============================================================

category_sales = (
    customers
    .dropna(subset=["PurchaseAmount"])
    .groupby("ProductCategory")["PurchaseAmount"]
    .sum()
    .sort_values(ascending=False)
)

top_category = category_sales.index[0]
top_category_value = category_sales.iloc[0]


# ============================================================
# 5. Purchase statistics
# ============================================================

highest_purchase = valid_purchases.max()
lowest_purchase = valid_purchases.min()


# ============================================================
# 6. Date range
# ============================================================

valid_dates = customers["PurchaseDate"].dropna()

first_purchase_date = valid_dates.min()
last_purchase_date = valid_dates.max()


# ============================================================
# 7. Monthly purchase analysis
# ============================================================

monthly_sales = (
    customers
    .dropna(subset=["PurchaseDate", "PurchaseAmount"])
    .set_index("PurchaseDate")["PurchaseAmount"]
    .resample("ME")
    .sum()
)

best_month = monthly_sales.idxmax()
best_month_value = monthly_sales.max()

lowest_month = monthly_sales.idxmin()
lowest_month_value = monthly_sales.min()


# ============================================================
# 8. Gender distribution
# ============================================================

gender_distribution = (
    customers["Gender"]
    .value_counts()
)


# ============================================================
# 9. Age statistics
# ============================================================

average_age = customers["Age"].mean()
minimum_age = customers["Age"].min()
maximum_age = customers["Age"].max()


# ============================================================
# 10. Display results
# ============================================================

print("=" * 60)
print("VOLTIX TASK 9 — CUSTOMER DATA ANALYSIS")
print("=" * 60)

print("\nMAIN KPIs")
print("-" * 60)

print(f"Total Customers: {total_customers:,}")
print(f"Total Purchases: {total_purchases:,}")
print(f"Total Revenue: ${total_revenue:,.2f}")
print(f"Average Purchase Amount: ${average_purchase:,.2f}")
print(f"Average Rating: {average_rating:.2f}")
print(f"Top Product Category: {top_category}")
print(f"Top Category Purchase Amount: ${top_category_value:,.2f}")

print("\nPURCHASE STATISTICS")
print("-" * 60)

print(f"Highest Purchase: ${highest_purchase:,.2f}")
print(f"Lowest Purchase: ${lowest_purchase:,.2f}")

print("\nDATE RANGE")
print("-" * 60)

print(f"First Purchase Date: {first_purchase_date}")
print(f"Last Purchase Date: {last_purchase_date}")

print("\nMONTHLY PURCHASE TREND")
print("-" * 60)

print(
    f"Highest Month: {best_month.strftime('%B %Y')} "
    f"(${best_month_value:,.2f})"
)

print(
    f"Lowest Month: {lowest_month.strftime('%B %Y')} "
    f"(${lowest_month_value:,.2f})"
)

print("\nSALES BY PRODUCT CATEGORY")
print("-" * 60)

print(category_sales)

print("\nGENDER DISTRIBUTION")
print("-" * 60)

print(gender_distribution)

print("\nAGE STATISTICS")
print("-" * 60)

print(f"Average Age: {average_age:.2f}")
print(f"Minimum Age: {minimum_age:.2f}")
print(f"Maximum Age: {maximum_age:.2f}")

print("\n" + "=" * 60)
print("Analysis completed successfully.")
print("=" * 60)