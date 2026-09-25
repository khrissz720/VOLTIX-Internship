import pandas as pd
from pathlib import Path

BASE = Path(__file__).resolve().parent
INPUT = BASE / "Hospital Analytics.xlsx"
OUTPUT = BASE / "Hospital_Data_Cleaned.csv"

df = pd.read_excel(INPUT, sheet_name="Data Before Cleaning")

df.columns = [
    "Patient_Name", "Age", "Gender", "Diagnosis", "Attending_Doctor",
    "Admission_Date", "Discharge_Date", "Bill_Amount", "Insurance", "Risk_Level"
]

text_cols = ["Patient_Name", "Gender", "Diagnosis", "Attending_Doctor", "Insurance", "Risk_Level"]
for c in text_cols:
    df[c] = df[c].astype("string").str.strip()

df["Age"] = pd.to_numeric(df["Age"], errors="coerce").astype("Int64")
df["Bill_Amount"] = pd.to_numeric(df["Bill_Amount"], errors="coerce")
df["Admission_Date"] = pd.to_datetime(df["Admission_Date"], errors="coerce")
df["Discharge_Date"] = pd.to_datetime(df["Discharge_Date"], errors="coerce")

df = df.drop_duplicates().reset_index(drop=True)

invalid = df["Discharge_Date"] < df["Admission_Date"]
df.loc[invalid, ["Admission_Date", "Discharge_Date"]] = (
    df.loc[invalid, ["Discharge_Date", "Admission_Date"]].to_numpy()
)

df["Length_of_Stay_Days"] = (df["Discharge_Date"] - df["Admission_Date"]).dt.days
df["Age_Group"] = pd.cut(
    df["Age"].astype(float),
    bins=[0, 17, 39, 59, 200],
    labels=["0-17", "18-39", "40-59", "60+"],
    include_lowest=True
)
df["Admission_Month"] = df["Admission_Date"].dt.month
df["Admission_Month_Name"] = df["Admission_Date"].dt.strftime("%B")
df["Admission_Quarter"] = "Q" + df["Admission_Date"].dt.quarter.astype(str)
df["Admission_Year"] = df["Admission_Date"].dt.year

df.to_csv(OUTPUT, index=False, encoding="utf-8-sig")
print(f"Saved {len(df)} cleaned records to {OUTPUT}")
