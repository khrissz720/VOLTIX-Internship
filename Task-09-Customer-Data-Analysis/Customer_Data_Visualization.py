import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# ============================================================
# 1. File paths
# ============================================================

BASE = Path(__file__).resolve().parent

INPUT = BASE / "Customers_Fakedata_Cleaned.csv"
CHARTS = BASE / "charts"

CHARTS.mkdir(exist_ok=True)


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
# 3. Corporate / minimalist style
# ============================================================

sns.set_theme(
    style="whitegrid",
    context="notebook"
)

plt.rcParams["figure.figsize"] = (10, 6)
plt.rcParams["axes.titlesize"] = 16
plt.rcParams["axes.labelsize"] = 11
plt.rcParams["xtick.labelsize"] = 10
plt.rcParams["ytick.labelsize"] = 10


# ============================================================
# 4. Demographics: Age and Gender
# ============================================================

# Keep valid ages for demographic visualization
demographics = customers[
    customers["Age"].between(0, 100)
].copy()

plt.figure()

for gender in demographics["Gender"].unique():
    data = demographics[
        demographics["Gender"] == gender
    ]["Age"]

    plt.hist(
        data,
        bins=20,
        alpha=0.6,
        label=gender
    )

plt.title("Customer Demographics: Age and Gender")
plt.xlabel("Age")
plt.ylabel("Number of Customers")
plt.legend(title="Gender")

plt.tight_layout()

plt.savefig(
    CHARTS / "customer_demographics.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# 5. Sales by Product Category
# ============================================================

category_sales = (
    customers
    .groupby("ProductCategory")["PurchaseAmount"]
    .sum()
    .sort_values(ascending=False)
)

plt.figure()

sns.barplot(
    x=category_sales.values,
    y=category_sales.index
)

plt.title("Total Purchase Amount by Product Category")
plt.xlabel("Total Purchase Amount")
plt.ylabel("Product Category")

plt.tight_layout()

plt.savefig(
    CHARTS / "sales_by_category.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# 6. Purchase trends over time
# ============================================================

monthly_sales = (
    customers
    .dropna(subset=["PurchaseDate"])
    .set_index("PurchaseDate")["PurchaseAmount"]
    .resample("ME")
    .sum()
)

plt.figure()

plt.plot(
    monthly_sales.index,
    monthly_sales.values,
    marker="o",
    linewidth=2
)

plt.title("Monthly Purchase Amount Trend")
plt.xlabel("Month")
plt.ylabel("Purchase Amount")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    CHARTS / "purchase_trend.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# 7. Customer satisfaction: Rating distribution
# ============================================================

plt.figure()

sns.histplot(
    data=customers,
    x="Rating",
    bins=10,
    kde=True
)

average_rating = customers["Rating"].mean()

plt.axvline(
    average_rating,
    linestyle="--",
    linewidth=2,
    label=f"Average: {average_rating:.2f}"
)

plt.title("Customer Rating Distribution")
plt.xlabel("Rating")
plt.ylabel("Number of Customers")

plt.legend()

plt.tight_layout()

plt.savefig(
    CHARTS / "rating_distribution.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# 8. Key insights
# ============================================================

print("\nKEY INSIGHTS")
print("=" * 50)


# ------------------------------------------------------------
# 8.1 Demographics
# ------------------------------------------------------------

print("\n1. Demographics")

print(
    "The demographic chart shows the distribution of customers "
    "across different age groups and genders."
)


# ------------------------------------------------------------
# 8.2 Sales by Category
# ------------------------------------------------------------

print("\n2. Sales by Category")

# Exclude "No Especificado" from identifying the top
# specified product category
specified_category_sales = category_sales[
    category_sales.index != "No Especificado"
]

top_category = specified_category_sales.index[0]
top_category_value = specified_category_sales.iloc[0]

print(
    f"{top_category} generated the highest total purchase amount "
    f"among the specified product categories, with "
    f"{top_category_value:,.2f} in purchases."
)


# ------------------------------------------------------------
# 8.3 Purchase Trends
# ------------------------------------------------------------

print("\n3. Purchase Trends")

if not monthly_sales.empty:

    max_month = monthly_sales.idxmax()
    max_value = monthly_sales.max()

    print(
        f"The highest monthly purchase amount occurred in "
        f"{max_month.strftime('%B %Y')}, with approximately "
        f"{max_value:,.2f} in purchases."
    )


# ------------------------------------------------------------
# 8.4 Customer Satisfaction
# ------------------------------------------------------------

print("\n4. Customer Satisfaction")

print(
    f"The overall average customer rating is approximately "
    f"{average_rating:.2f}."
)


# ============================================================
# 9. Completion message
# ============================================================

print(
    "\nCharts saved successfully in the 'charts' folder."
)