# \# VOLTIX Internship – Task 07: Hospital Analytics

# 

# \## Objective

# 

# Complete the workflow from raw hospital data to clean analytical data, KPIs, interactive dashboard, and decision-support insights.

# 

# \## Dataset

# 

# \- Source file: Hospital Analytics.xlsx

# \- Original rows: 248

# \- Original columns: 10

# \- Exact duplicate rows detected: 1

# \- Rows after cleaning: 247

# 

# \## Cleaning Performed

# 

# \- Checked all columns for missing values.

# \- Removed exact duplicate rows.

# \- Standardized column names to English.

# \- Trimmed text values.

# \- Corrected numeric and date data types.

# \- Checked age and bill ranges.

# \- Detected 29 records where discharge date preceded admission date.

# \- Corrected those records by swapping the two supplied dates so admission precedes discharge.

# \- Created analytical columns:

# &#x20; - Length\_of\_Stay\_Days

# &#x20; - Age\_Group

# &#x20; - Admission\_Month

# &#x20; - Admission\_Month\_Name

# &#x20; - Admission\_Quarter

# &#x20; - Admission\_Year

# \- Rechecked missing values, duplicates, negative length of stay, invalid ages, and negative bills.

# 

# \## Final Data Quality

# 

# \- Missing values after cleaning: 0

# \- Duplicate rows after cleaning: 0

# \- Negative length-of-stay records: 0

# \- Invalid age records: 0

# \- Negative bill records: 0

# 

# \## Power BI KPIs

# 

# \- Total Patients = COUNTROWS(Hospital\_Data\_Cleaned)

# \- Total Billing = SUM(Hospital\_Data\_Cleaned\[Bill\_Amount])

# \- Average Bill = AVERAGE(Hospital\_Data\_Cleaned\[Bill\_Amount])

# \- Average Length of Stay = AVERAGE(Hospital\_Data\_Cleaned\[Length\_of\_Stay\_Days])

# \- Average Age = AVERAGE(Hospital\_Data\_Cleaned\[Age])

# 

# \## Interactive Dashboard

# 

# The Power BI dashboard provides an interactive overview of hospital activity, patient characteristics, risk levels, billing, and physician workload.

# 

# \### KPI Cards

# 

# \- Total Patients

# \- Total Billing

# \- Average Bill

# \- Average Length of Stay

# \- Average Age

# 

# \### Visualizations

# 

# \- Monthly Admissions – Line chart

# \- Patients by Diagnosis – Bar chart

# \- Patients by Risk Level – Column/Bar chart

# \- Average Bill by Risk Level – Bar chart

# \- Patients by Insurance – Bar chart

# \- Patients by Attending Doctor – Bar chart

# 

# \### Interactive Filters

# 

# \- Admission Year

# \- Admission Quarter

# \- Admission Month

# \- Gender

# \- Insurance

# \- Risk Level

# \- Diagnosis

# \- Age Group

# 

# The dashboard allows users to filter the data dynamically and analyze hospital performance from different perspectives.

# 

# \## Insights

# 

# The analysis identifies patient volume patterns, diagnosis distribution, risk-level distribution, billing differences, insurance coverage, physician workload, and monthly admission trends.

# 

# These insights support hospital performance monitoring and data-driven decision-making.

# 

# \## Files

# 

# \- Hospital\_Data\_Cleaned.csv

# \- Hospital\_Data\_Cleaning.py

# \- Insights.docx

# \- charts/

