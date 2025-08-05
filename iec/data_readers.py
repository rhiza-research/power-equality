import numpy as np
import pandas as pd
from geopy.geocoders import Nominatim
from tqdm import tqdm

"""
All functions named xx_to_standard convert the data format of a specific xx source to
a standard format accepted by the analysis functions in this library. 

The standard format has the following columns:
1. id - measurement point identifier (location, uuid)
2. time - timestamp of sample
3. value - measured value
"""

## Data readers for ESMI
def get_coords(esmi):
    """Obtains lat, long estimates for ESMI data collection points.

    ESMI metadata specifies data collection locations with a location name,
    district, and state. However, no lat/long coordinates are provided. This
    function uses a geocoding service to obtain potential lat/long values for
    each of the ESMI collection points.
    """
    geolocator = Nominatim(user_agent="find_esmi_locs")
    nlocs = len(esmi)
    locs = esmi[["Location name"]].copy()
    locs["latitude"], locs["longitude"] = None, None
    with tqdm(total=nlocs, desc="Obtaining data locations") as pbar:
        for i in range(nlocs):
            row = esmi.iloc[i]
            name, district, state = row["Location name"], row["District"], row["State"]
            try:
                loc = geolocator(f"{location_name}, {district}, {state}")
                if loc:
                    lat, long = loc.latitude, loc.longitude
                else:
                    lat, long = None, None
            except:
                lat, long = None, None
            locs.loc[i, "latitude"] = lat
            locs.loc[i, "longitude"] = long
    return locs


def esmi_to_standard(df):
    cmap = {f"Min {i}" : i for i in range(60)}
    cmap["Location name"] = "id"
    df = df.rename(columns=cmap)
    df = df.melt(
        id_vars=["id", "Date", "Hour"],
        var_name="minute",
        value_name="voltage"
    )
    # Get timestamp
    df["time"] = pd.to_datetime(
        df["Date"] + ' ' + df["Hour"].astype(str) + ":" + df["minute"].astype(str).str.zfill(2),
        format="%d-%m-%Y %H:%M"
    )
    df = df[["id", "time", "voltage"]]
    return df


