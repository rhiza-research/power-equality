import pandas as pd


def load_standard_csv(path):
    """Reads a CSV in the standard format and casts columns to their proper types."""
    df = pd.read_csv(path)
    df["id"] = df["id"].astype(str)
    df["time"] = pd.to_datetime(df["time"])
    df["value"] = df["value"].astype(float)
    df["value_name"] = df["value_name"].astype(str)
    df["latitude"] = df["latitude"].astype(float)
    df["longitude"] = df["longitude"].astype(float)
    return df
