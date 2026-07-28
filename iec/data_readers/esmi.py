import json
import pandas as pd

VALUE_NAME = "voltage_mag_A_v"


def process(input_path, output_path, location_metadata_path):
    """Converts a raw ESMI xlsx export into the standard format.
    """
    df = pd.read_excel(input_path, header=None)

    columns = ["Location name", "Date", "Hour"] + [f"Min {i}" for i in range(60)]
    has_header = str(df.iloc[0, 0]).startswith("Location")
    if has_header:
        df.columns = columns
        df = df.iloc[1:].reset_index(drop=True)
    else:
        df.columns = columns

    # load the location lookup in the metadata path
    location_lookup = pd.read_csv(location_metadata_path)

    # rename the columns to the standard format
    minute_cols = [c for c in df.columns if c.startswith("Min ")]
    cmap = {c: int(c.replace("Min ", "")) for c in minute_cols}
    cmap["Location name"] = "id"
    df = df.rename(columns=cmap)
    df = df.dropna(subset=["id", "Date", "Hour"])

    # melt the data into the standard format, turning each minute into a row
    df = df.melt(
        id_vars=["id", "Date", "Hour"],
        value_vars=list(cmap.values())[:-1],
        var_name="minute",
        value_name="value",
    )

    # convert the date and hour to a datetime
    date = pd.to_datetime(df["Date"]).dt.normalize()
    df["time"] = (
        date
        + pd.to_timedelta(df["Hour"].astype(int), unit="h")
        + pd.to_timedelta(df["minute"].astype(int), unit="m")
    )

    # add the value name and location
    df["value_name"] = VALUE_NAME
    coords = location_lookup.set_index("id")[["lat", "lon"]]
    df = df.merge(coords, how="left", left_on="id", right_index=True)
    df = df.rename(columns={"lat": "latitude", "lon": "longitude"})

    # sort the data and reset the index
    df = df[["id", "time", "value", "value_name", "latitude", "longitude"]]
    df = df.sort_values(["id", "time"]).reset_index(drop=True)

    # save to the output path
    df.to_csv(output_path, index=False)
    return df
