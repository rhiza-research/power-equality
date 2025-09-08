import numpy as np
import pandas as pd
import time
from geopy.geocoders import Nominatim
from tqdm import tqdm

"""
All functions named xx_to_standard convert the data format of a specific xx source to
a standard format accepted by the analysis functions in this library. 

The standard format has the following columns:
1. id - measurement point identifier (location, uuid)
2. time - timestamp of sample
3. value columns - measured value, in [voltage, frequency]
"""

## Data readers for ESMI
def get_coords(esmi, subset=None):
    """Obtains lat, long estimates for ESMI data collection points.

    ESMI metadata specifies data collection locations with a location name,
    district, and state. However, no lat/long coordinates are provided. This
    function uses a geocoding service to obtain potential lat/long values for
    each of the ESMI collection points.
    """
    if subset:
        esmi = esmi.iloc[subset[0]:subset[1]]

    geolocator = Nominatim(user_agent="find_esmi_locs")
    nlocs = len(esmi)
    locs = esmi[["Location name"]].copy()
    locs["latitude"], locs["longitude"] = None, None
    with tqdm(total=nlocs, desc="Obtaining data locations") as pbar:
        for i in range(nlocs):
            row = esmi.iloc[i]
            district, state = row["District"], row["State"]
            try:
                loc = geolocator.geocode(f"{district}, {state}")
                if loc:
                    lat, long = loc.latitude, loc.longitude
                else:
                    lat, long = None, None
            except:
                lat, long = None, None
            locs.loc[i, "latitude"] = lat
            locs.loc[i, "longitude"] = long
            # Respect rate limits
            time.sleep(1)
            pbar.update(1)
    return locs


def esmi_to_standard(df, outage=True):
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
    # Filter low voltages and add an outage time column
    df = _add_outage_time(df, add_out_col = True)
    return df

## Data readers for nLine

def nline_to_standard(df):
    df = df[["time", "respondent_id", "voltage", "frequency",
             "site_id"]]
    df["time"] = pd.to_datetime(df["time"], errors='coerce')
    df = _add_outage_time(df, add_out_col = True)
    return df

def _add_outage_time(df, out_thresh=5, vnom=230, add_out_col = False):
    """Identifies outage periods based on recorded voltage."""
    thresh = out_thresh*vnom / 100
    out_times = df["voltage"] < thresh
    df.loc[out_times, "voltage"] = np.nan
    # Add a new outage time column
    if add_out_col:
        df.loc[:, "outage"] = 0
        df.loc[out_times, "outage"] = 1
    return df
