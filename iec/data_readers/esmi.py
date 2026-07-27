import json

import pandas as pd

VALUE_NAME = "voltage_mag_A_v"


def process(xlsx_path, metadata_path):
    """Converts a raw ESMI xlsx export into the standard format.

    Standard format columns: id, time, value, value_name, location.
    `metadata_path` points to a JSON file mapping location name -> [lat, lon].
    """
    df = pd.read_excel(xlsx_path)

    with open(metadata_path) as f:
        location_lookup = json.load(f)

    minute_cols = [c for c in df.columns if c.startswith("Min ")]
    cmap = {c: int(c.replace("Min ", "")) for c in minute_cols}
    cmap["Location name"] = "id"
    df = df.rename(columns=cmap)

    df = df.dropna(subset=["id", "Date", "Hour"])

    df = df.melt(
        id_vars=["id", "Date", "Hour"],
        value_vars=list(cmap.values())[:-1],
        var_name="minute",
        value_name="value",
    )

    date = pd.to_datetime(df["Date"]).dt.normalize()
    df["time"] = (
        date
        + pd.to_timedelta(df["Hour"].astype(int), unit="h")
        + pd.to_timedelta(df["minute"].astype(int), unit="m")
    )

    df["value_name"] = VALUE_NAME
    df["location"] = df["id"].map(
        lambda name: tuple(location_lookup[name]) if name in location_lookup else None
    )

    df = df[["id", "time", "value", "value_name", "location"]]
    df = df.sort_values(["id", "time"]).reset_index(drop=True)
    return df
