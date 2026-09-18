from pathlib import Path
import pandas as pd

INPUT_FILE = Path("Dataset") / "File 3.csv"
OUTPUT_FILE = Path("Dataset") / "File_3_Cleaned.csv"


def clean_data(input_file: Path = INPUT_FILE) -> pd.DataFrame:
    df = pd.read_csv(input_file)

    # Standardize text fields.
    for col in ["Name", "Sex", "Ticket", "Embarked", "Cabin"]:
        df[col] = df[col].astype("string").str.strip()

    # Age: median by Sex and Pclass.
    df["Age"] = df.groupby(["Sex", "Pclass"])["Age"].transform(
        lambda s: s.fillna(s.median())
    )

    # Fare: median by Pclass.
    df["Fare"] = df["Fare"].fillna(
        df.groupby("Pclass")["Fare"].transform("median")
    )

    # Cabin: retain rows and explicitly label unknown cabin information.
    df["Cabin"] = df["Cabin"].fillna("Unknown")

    return df


if __name__ == "__main__":
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    cleaned = clean_data()
    cleaned.to_csv(OUTPUT_FILE, index=False)

    print(f"Rows: {len(cleaned)}")
    print(f"Columns: {len(cleaned.columns)}")
    print(f"Remaining missing values: {int(cleaned.isna().sum().sum())}")
    print(f"Saved to: {OUTPUT_FILE}")