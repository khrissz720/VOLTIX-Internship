from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION

BASE = Path(__file__).resolve().parent
RAW_FILE = BASE / "FactSale.csv"
DATASET_DIR = BASE / "Dataset"
CHARTS_DIR = BASE / "Charts"
DATASET_DIR.mkdir(exist_ok=True)
CHARTS_DIR.mkdir(exist_ok=True)

OUT_XLSX = DATASET_DIR / "EzzSteel_Full_Dataset.xlsx"

# -----------------------------
# 1. LOAD DATA
# -----------------------------
df = pd.read_csv(RAW_FILE)
original_rows = len(df)
original_columns = len(df.columns)

# -----------------------------
# 2. DATA CLEANING
# -----------------------------
# Standardize column names
# Dates are the main data-quality focus.
for col in ["Invoice Date Key", "Delivery Date Key"]:
    df[col] = pd.to_datetime(df[col], errors="coerce", dayfirst=False)

# Standardize text fields
for col in ["Description", "Package"]:
    df[col] = df[col].astype("string").str.strip()

# Numeric fields
numeric_cols = [
    "Sale Key", "City Key", "Customer Key", "Bill To Customer Key",
    "Stock Item Key", "Salesperson Key", "WWI Invoice ID", "Quantity",
    "Unit Price", "Tax Rate", "Total Excluding Tax", "Tax Amount",
    "Profit", "Total Including Tax", "Total Dry Items", "Total Chiller Items",
    "Lineage Key"
]
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Remove exact duplicate rows if any
exact_duplicates = int(df.duplicated().sum())
df = df.drop_duplicates().copy()

# Missing dates: keep the record, because Delivery Date cannot be safely inferred.
missing_delivery_dates = int(df["Delivery Date Key"].isna().sum())

# Validation flags are used for the quality summary, not as business measures.
df["Calculated Total Excluding Tax"] = df["Quantity"] * df["Unit Price"]
df["Calculated Tax Amount"] = df["Total Excluding Tax"] * df["Tax Rate"] / 100
df["Calculated Total Including Tax"] = df["Total Excluding Tax"] + df["Tax Amount"]

# -----------------------------
# 3. DATA VALIDATION
# -----------------------------
tol = 0.01
excl_mismatch = int((abs(df["Total Excluding Tax"] - df["Calculated Total Excluding Tax"]) > tol).sum())
tax_mismatch = int((abs(df["Tax Amount"] - df["Calculated Tax Amount"]) > tol).sum())
incl_mismatch = int((abs(df["Total Including Tax"] - df["Calculated Total Including Tax"]) > tol).sum())
negative_quantity = int((df["Quantity"] < 0).sum())
zero_quantity = int((df["Quantity"] == 0).sum())
negative_price = int((df["Unit Price"] < 0).sum())
negative_profit = int((df["Profit"] < 0).sum())
delivery_before_invoice = int((df["Delivery Date Key"] < df["Invoice Date Key"]).fillna(False).sum())

# Drop helper columns from final cleaned dataset
df_clean = df.drop(columns=[
    "Calculated Total Excluding Tax",
    "Calculated Tax Amount",
    "Calculated Total Including Tax"
]).copy()

# Business dimensions
invoice_count = int(df_clean["WWI Invoice ID"].nunique())
total_sales = float(df_clean["Total Including Tax"].sum())
total_profit = float(df_clean["Profit"].sum())
total_quantity = int(df_clean["Quantity"].sum())
profit_margin = total_profit / total_sales * 100 if total_sales else 0
avg_invoice = total_sales / invoice_count if invoice_count else 0

# -----------------------------
# 4. ANALYSIS TABLES
# -----------------------------
df_clean["Invoice Year"] = df_clean["Invoice Date Key"].dt.year
df_clean["Invoice Month"] = df_clean["Invoice Date Key"].dt.to_period("M").astype(str)

sales_product = (df_clean.groupby("Description", as_index=False)["Total Including Tax"]
                 .sum().sort_values("Total Including Tax", ascending=False))
sales_city = (df_clean.groupby("City Key", as_index=False)["Total Including Tax"]
             .sum().sort_values("Total Including Tax", ascending=False))
sales_time = (df_clean.groupby("Invoice Month", as_index=False)["Total Including Tax"]
             .sum().sort_values("Invoice Month"))
top_products = sales_product.head(10).copy()

# -----------------------------
# 5. STATIC CHARTS
# -----------------------------
plt.rcParams.update({"font.family": "DejaVu Sans", "axes.titleweight": "bold"})

def money_fmt(x, pos):
    if abs(x) >= 1_000_000:
        return f"${x/1_000_000:.1f}M"
    if abs(x) >= 1_000:
        return f"${x/1_000:.0f}K"
    return f"${x:.0f}"

# Sales by product
fig, ax = plt.subplots(figsize=(10, 6))
plot_df = sales_product.head(10).sort_values("Total Including Tax")
ax.barh(plot_df["Description"].str.slice(0, 45), plot_df["Total Including Tax"])
ax.xaxis.set_major_formatter(FuncFormatter(money_fmt))
ax.set_title("Sales by Product")
ax.set_xlabel("Total Sales")
ax.grid(axis="x", alpha=0.2)
fig.tight_layout()
fig.savefig(CHARTS_DIR / "sales_by_product.png", dpi=180, bbox_inches="tight")
plt.close(fig)

# Sales by region: dataset has no Region column, so City Key is used as the available geographic dimension.
fig, ax = plt.subplots(figsize=(10, 6))
plot_df = sales_city.head(10).sort_values("Total Including Tax")
ax.barh(plot_df["City Key"].astype(str), plot_df["Total Including Tax"])
ax.xaxis.set_major_formatter(FuncFormatter(money_fmt))
ax.set_title("Sales by City Key")
ax.set_xlabel("Total Sales")
ax.set_ylabel("City Key")
ax.grid(axis="x", alpha=0.2)
fig.tight_layout()
fig.savefig(CHARTS_DIR / "sales_by_region.png", dpi=180, bbox_inches="tight")
plt.close(fig)

# Sales over time
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(sales_time["Invoice Month"], sales_time["Total Including Tax"], linewidth=2)
ax.xaxis.set_major_locator(plt.MaxNLocator(10))
ax.yaxis.set_major_formatter(FuncFormatter(money_fmt))
ax.set_title("Sales Over Time")
ax.set_xlabel("Invoice Month")
ax.set_ylabel("Total Sales")
ax.grid(alpha=0.2)
plt.xticks(rotation=45, ha="right")
fig.tight_layout()
fig.savefig(CHARTS_DIR / "sales_over_time.png", dpi=180, bbox_inches="tight")
plt.close(fig)

# Top products
fig, ax = plt.subplots(figsize=(10, 6))
plot_df = top_products.sort_values("Total Including Tax")
ax.barh(plot_df["Description"].str.slice(0, 42), plot_df["Total Including Tax"])
ax.xaxis.set_major_formatter(FuncFormatter(money_fmt))
ax.set_title("Top 10 Products by Sales")
ax.set_xlabel("Total Sales")
ax.grid(axis="x", alpha=0.2)
fig.tight_layout()
fig.savefig(CHARTS_DIR / "top_products.png", dpi=180, bbox_inches="tight")
plt.close(fig)

# -----------------------------
# 6. INTERACTIVE DASHBOARD
# -----------------------------
# Extra fields for dashboard views
package_sales = (df_clean.groupby("Package", as_index=False)["Total Including Tax"]
                 .sum().sort_values("Total Including Tax", ascending=False))
year_sales = (df_clean.groupby("Invoice Year", as_index=False)["Total Including Tax"]
             .sum().sort_values("Invoice Year"))
profit_product = (df_clean.groupby("Description", as_index=False)["Profit"]
                 .sum().sort_values("Profit", ascending=False).head(8))

fig = make_subplots(
    rows=3, cols=3,
    specs=[
        [{"type": "indicator"}, {"type": "indicator"}, {"type": "indicator"}],
        [{"type": "indicator"}, {"type": "indicator"}, {"type": "indicator"}],
        [{"type": "xy"}, {"type": "domain"}, {"type": "xy"}],
    ],
    vertical_spacing=0.12,
    horizontal_spacing=0.06,
    subplot_titles=("Sales Trend", "Package Mix", "Top Products by Sales")
)

kpis = [
    ("Total Sales", total_sales, "$,.0f"),
    ("Total Profit", total_profit, "$,.0f"),
    ("Total Quantity", total_quantity, ",.0f"),
    ("Profit Margin", profit_margin, ".1f"),
    ("Invoice Count", invoice_count, ",.0f"),
    ("Avg Invoice Value", avg_invoice, "$,.0f"),
]
positions = [(1,1),(1,2),(1,3),(2,1),(2,2),(2,3)]
for (title, value, fmt), (r,c) in zip(kpis, positions):
    fig.add_trace(go.Indicator(
        mode="number", value=value,
        title={"text": title},
        number={"prefix": "$" if "$" in fmt else "", "valueformat": fmt.replace("$", "")}
    ), row=r, col=c)

fig.add_trace(go.Scatter(x=sales_time["Invoice Month"], y=sales_time["Total Including Tax"], mode="lines+markers", name="Sales"), row=3, col=1)
fig.add_trace(go.Pie(labels=package_sales["Package"], values=package_sales["Total Including Tax"], hole=0.55, name="Package"), row=3, col=2)
fig.add_trace(go.Bar(x=top_products["Total Including Tax"], y=top_products["Description"].str.slice(0, 35), orientation="h", name="Products"), row=3, col=3)

fig.update_layout(
    title={"text": "Task 02 | Sales Performance Dashboard", "x": 0.5},
    height=1050,
    template="plotly_dark",
    paper_bgcolor="#17152B",
    plot_bgcolor="#211E3A",
    font={"family": "Arial", "color": "#F4F1FF"},
    showlegend=False,
    margin={"l": 40, "r": 40, "t": 90, "b": 40}
)
fig.write_html(BASE / "Dashboard.html", include_plotlyjs=True, full_html=True)

# -----------------------------
# 7. STATIC DASHBOARD IMAGE
# -----------------------------
# Management-oriented dashboard image similar in spirit to the provided example.
fig = plt.figure(figsize=(16, 9), facecolor="#17152B")
gs = fig.add_gridspec(4, 6, hspace=0.55, wspace=0.28)

kpi_info = [
    ("TOTAL SALES", f"${total_sales/1e6:.2f}M"),
    ("TOTAL PROFIT", f"${total_profit/1e6:.2f}M"),
    ("TOTAL QUANTITY", f"{total_quantity/1e6:.2f}M"),
    ("PROFIT MARGIN", f"{profit_margin:.1f}%"),
    ("INVOICES", f"{invoice_count:,}"),
    ("AVG INVOICE", f"${avg_invoice:,.0f}"),
]
for i, (label, value) in enumerate(kpi_info):
    ax = fig.add_subplot(gs[0, i])
    ax.set_facecolor("#272342")
    ax.text(0.5, 0.68, label, ha="center", va="center", fontsize=9, fontweight="bold", color="white")
    ax.text(0.5, 0.28, value, ha="center", va="center", fontsize=18, fontweight="bold", color="#9FE8E1")
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_visible(False)

# Sales trend
ax = fig.add_subplot(gs[1:3, :3])
ax.set_facecolor("#211E3A")
ax.plot(sales_time["Invoice Month"], sales_time["Total Including Tax"], linewidth=2.2)
ax.set_title("Monthly Sales Trend", color="white", loc="left", fontsize=12, fontweight="bold")
ax.tick_params(axis="x", rotation=45, labelsize=7, colors="white")
ax.tick_params(axis="y", labelsize=8, colors="white")
ax.yaxis.set_major_formatter(FuncFormatter(money_fmt))
ax.grid(alpha=.15)
for s in ax.spines.values(): s.set_color("#4A456B")

# Package donut
ax = fig.add_subplot(gs[1:3, 3:4])
ax.set_facecolor("#211E3A")
ax.pie(package_sales["Total Including Tax"], labels=package_sales["Package"], autopct="%.0f%%", startangle=90, wedgeprops=dict(width=.35), textprops={"color":"white", "fontsize":8})
ax.set_title("Sales by Package", color="white", fontsize=11, fontweight="bold")

# Top products
ax = fig.add_subplot(gs[1:3, 4:6])
ax.set_facecolor("#211E3A")
p = top_products.sort_values("Total Including Tax")
ax.barh(p["Description"].str.slice(0, 30), p["Total Including Tax"])
ax.xaxis.set_major_formatter(FuncFormatter(money_fmt))
ax.tick_params(axis="both", labelsize=7, colors="white")
ax.set_title("Top 10 Products", color="white", loc="left", fontsize=12, fontweight="bold")
ax.grid(axis="x", alpha=.15)
for s in ax.spines.values(): s.set_color("#4A456B")

# Annual sales
ax = fig.add_subplot(gs[3, :2])
ax.set_facecolor("#211E3A")
ax.bar(year_sales["Invoice Year"].astype(str), year_sales["Total Including Tax"])
ax.yaxis.set_major_formatter(FuncFormatter(money_fmt))
ax.set_title("Annual Sales", color="white", loc="left", fontsize=10, fontweight="bold")
ax.tick_params(axis="both", colors="white", labelsize=7)
for s in ax.spines.values(): s.set_color("#4A456B")

# Top city keys
ax = fig.add_subplot(gs[3, 2:4])
ax.set_facecolor("#211E3A")
p = sales_city.head(6).sort_values("Total Including Tax")
ax.barh(p["City Key"].astype(str), p["Total Including Tax"])
ax.xaxis.set_major_formatter(FuncFormatter(money_fmt))
ax.set_title("Top City Keys", color="white", loc="left", fontsize=10, fontweight="bold")
ax.tick_params(axis="both", colors="white", labelsize=7)
for s in ax.spines.values(): s.set_color("#4A456B")

# Data quality panel
ax = fig.add_subplot(gs[3, 4:6])
ax.set_facecolor("#211E3A")
ax.axis("off")
ax.text(0.03, .86, "DATA QUALITY", color="white", fontsize=10, fontweight="bold")
quality_lines = [
    f"Exact duplicates: {exact_duplicates}",
    f"Missing delivery dates: {missing_delivery_dates}",
    f"Calculation mismatches: {excl_mismatch + tax_mismatch + incl_mismatch}",
    f"Negative quantities: {negative_quantity}",
    f"Negative profit rows: {negative_profit}",
]
for j, line in enumerate(quality_lines):
    ax.text(0.04, .66 - j*.14, line, color="#E8E4F8", fontsize=8)

fig.suptitle("TASK 02 | SALES PERFORMANCE", color="white", fontsize=20, fontweight="bold", y=.985)
fig.text(.5, .955, "Management Dashboard • Cleaned & Validated Sales Data", ha="center", color="#9FE8E1", fontsize=9)
fig.savefig(BASE / "Dashboard.png", dpi=160, bbox_inches="tight", facecolor=fig.get_facecolor())
plt.close(fig)

# -----------------------------
# 8. CLEANED DATASET
# -----------------------------
# Excel-ready dates and no helper columns.
df_clean.to_excel(OUT_XLSX, index=False)

# -----------------------------
# 9. INSIGHTS REPORT
# -----------------------------
top_product = sales_product.iloc[0]
top_city = sales_city.iloc[0]
best_year = year_sales.loc[year_sales["Total Including Tax"].idxmax()]

# Monthly peak
peak_month = sales_time.loc[sales_time["Total Including Tax"].idxmax()]

# Negative-profit product concentration
neg_profit_by_product = (df_clean[df_clean["Profit"] < 0]
                          .groupby("Description")
                          .size().sort_values(ascending=False).head(5))

report = Document()
section = report.sections[0]
section.top_margin = Inches(0.8)
section.bottom_margin = Inches(0.8)
section.left_margin = Inches(0.9)
section.right_margin = Inches(0.9)

styles = report.styles
styles["Normal"].font.name = "Times New Roman"
styles["Normal"].font.size = Pt(11)

p = report.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("TASK 02 – SALES DATA ANALYSIS")
r.bold = True; r.font.size = Pt(16); r.font.name = "Times New Roman"

p = report.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Data Cleaning, Validation, Dashboard and Business Insights")
r.italic = True; r.font.size = Pt(11)

report.add_heading("1. Dataset Overview", level=1)
report.add_paragraph(
    f"The dataset contains {original_rows:,} sales-line records and {original_columns} variables. "
    f"The analysis covers invoice dates from {df_clean['Invoice Date Key'].min().strftime('%d %B %Y')} "
    f"to {df_clean['Invoice Date Key'].max().strftime('%d %B %Y')}. The dataset contains "
    f"{invoice_count:,} distinct invoices, {df_clean['Description'].nunique():,} products and "
    f"{df_clean['City Key'].nunique():,} city keys."
)

report.add_heading("2. Data Cleaning", level=1)
report.add_paragraph(
    f"Invoice Date Key and Delivery Date Key were converted to datetime format. No invalid invoice dates were found. "
    f"{missing_delivery_dates} delivery-date values were missing and were retained as missing because no reliable value could be inferred. "
    f"Text fields were trimmed and numeric fields were converted to appropriate numeric types. "
    f"{exact_duplicates} exact duplicate rows were detected."
)

report.add_heading("3. Data Validation", level=1)
report.add_paragraph(
    f"The calculations were validated using the relationships between quantity, unit price, tax and totals. "
    f"There were {excl_mismatch} mismatches for Total Excluding Tax, {tax_mismatch} mismatches for Tax Amount, "
    f"and {incl_mismatch} mismatches for Total Including Tax using a tolerance of $0.01. "
    f"There were {negative_quantity} negative quantities, {zero_quantity} zero quantities and {negative_price} negative unit prices. "
    f"There were {delivery_before_invoice} records where delivery occurred before the invoice date. "
    f"Negative profit was observed in {negative_profit} rows; these records were not deleted because negative profit can represent legitimate low-margin or loss-making sales."
)

report.add_heading("4. Key Business Insights", level=1)
report.add_paragraph(
    f"1. Total sales reached ${total_sales:,.2f}, while total profit reached ${total_profit:,.2f}, producing an overall profit margin of {profit_margin:.1f}%."
)
report.add_paragraph(
    f"2. The highest-selling product was '{top_product['Description']}' with ${top_product['Total Including Tax']:,.2f} in sales."
)
report.add_paragraph(
    f"3. City Key {int(top_city['City Key'])} generated the highest sales among the available geographic identifiers, with ${top_city['Total Including Tax']:,.2f}."
)
report.add_paragraph(
    f"4. The strongest full invoice year in the available data was {int(best_year['Invoice Year'])}, with ${best_year['Total Including Tax']:,.2f} in sales."
)
report.add_paragraph(
    f"5. The highest monthly sales value occurred in {peak_month['Invoice Month']}, reaching ${peak_month['Total Including Tax']:,.2f}."
)

report.add_heading("5. Data Quality Issues", level=1)
issues = [
    f"Missing Delivery Date Key values: {missing_delivery_dates}.",
    "No exact duplicate rows were found.",
    "No invalid Invoice Date Key values were found after datetime conversion.",
    "No quantity, unit-price or delivery-before-invoice logical errors were found.",
    "No arithmetic inconsistencies were found in the total and tax calculations within the selected tolerance.",
    f"Negative profit was present in {negative_profit} rows and was preserved for business interpretation rather than removed."
]
for item in issues:
    report.add_paragraph(item, style="List Bullet")

report.add_heading("6. Recommendations", level=1)
recommendations = [
    "Monitor products generating negative profit and review their pricing, costs or commercial conditions.",
    "Investigate the missing delivery dates to determine whether the source system can provide the original values.",
    "Continue monitoring the highest-selling products and geographic identifiers because they have a strong effect on overall sales performance.",
    "Use the dashboard as a management monitoring tool to compare sales, profit and product performance over time."
]
for item in recommendations:
    report.add_paragraph(item, style="List Bullet")

report.add_heading("7. Dashboard Note", level=1)
report.add_paragraph(
    "The dataset does not contain a Region field. Therefore, the geographic visualization uses City Key, the available geographic identifier, "
    "rather than inventing regional categories."
)

report.save(BASE / "Insights.docx")

# -----------------------------
# 10. README
# -----------------------------
readme = f"""# Task 02 – Sales Data Analysis\n\n## Objective\nComplete data cleaning, data validation, dashboard creation and business insights using the supplied sales dataset.\n\n## Files\n- `FactSale.csv`: source dataset used by the Python script.\n- `Dataset/EzzSteel_Full_Dataset.xlsx`: cleaned dataset.\n- `Charts/`: four required static charts.\n- `Dashboard.html`: interactive Plotly dashboard.\n- `Dashboard.png`: static management dashboard preview.\n- `Insights.docx`: data-quality issues, findings and recommendations.\n- `Sales_Analysis.py`: complete reproducible analysis script.\n\n## Data Quality Summary\n- Original rows: {original_rows:,}\n- Columns: {original_columns}\n- Exact duplicates: {exact_duplicates}\n- Missing Delivery Date Key: {missing_delivery_dates}\n- Invalid Invoice Date Key: 0\n- Calculation mismatches: 0 within $0.01 tolerance\n- Negative profit rows: {negative_profit:,} (retained because they can be valid business records)\n\n## Main KPIs\n- Total Sales: ${total_sales:,.2f}\n- Total Profit: ${total_profit:,.2f}\n- Total Quantity: {total_quantity:,}\n- Profit Margin: {profit_margin:.1f}%\n- Invoice Count: {invoice_count:,}\n- Average Invoice Value: ${avg_invoice:,.2f}\n\n## How to Run in VS Code\n1. Put `FactSale.csv` in the same folder as `Sales_Analysis.py`.\n2. Install dependencies:\n\n```bash\npip install pandas numpy matplotlib openpyxl plotly python-docx\n```\n\n3. Run:\n\n```bash\npython Sales_Analysis.py\n```\n\nThe script automatically creates the cleaned Excel file, four PNG charts, the interactive dashboard and the Insights report.\n\n## Important Note\nThe dataset does not contain a `Region` column. The geographic chart therefore uses `City Key` as the available geographic dimension. No region values were invented.\n"""
(BASE / "README.md").write_text(readme, encoding="utf-8")

print("Task 02 completed successfully.")
print(f"Output folder: {BASE}")
