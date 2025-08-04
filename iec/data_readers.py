import numpy as np
import pandas as pd
from geopy.geocoders import Nominatim
from tqdm import tqdm

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



