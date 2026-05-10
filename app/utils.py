import pandas as pd

def load_data(path: str = "data/careflow_dataset.csv") -> pd.DataFrame:
    df = pd.read_csv(path)
    df["Journey Date"] = pd.to_datetime(df["Journey Date"])
    return df

def patient_level(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("Patient ID").agg({
        "D1 Retained":"max", "D7 Retained":"max", "D30 Retained":"max",
        "Treatment Completed":"max", "Outcome Success":"max",
        "Treatment Cost":"sum", "Engagement Score":"mean"
    }).reset_index()
