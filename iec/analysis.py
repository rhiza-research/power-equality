import numpy as np
import pandas as pd

def daily_profile(df, rez="hour", value="voltage"):
    """Get average daily measurement profiles for each id.
    
    Resolution of daily curve is specified by rez parameter.
    """
    if rez == "hour":
        df["tidx"] = df["time"].dt.hour
    elif rez == "minute":
        df["tidx"] = df["time"].dt.minute
    df = df.groupby(["id", "tidx"]).agg(value=(value, "mean"))\
           .reset_index()
    df = df.rename(columns={"value" : value})
    return df

def avg_daily_time(df, value="undervoltage"):
    """Average daily time in given state by measurement point."""
    # Get daily values by id
    df["tidx"] = df["time"].dt.date
    df = df.groupby(["id", "tidx"]).agg(vtot=(value, "sum"))\
           .reset_index()
    # Get avg of daily values by id
    df = df.groupby(["id"]).agg(avg_daily=("vtot", "mean"))\
           .reset_index()
    
    return df

def get_agg_stats(df, value="voltage"):
    """Produces a set of aggregate statistics for a dataset.

    These can be visualized as summaries of overall supply quality
    where more granular visualizations are not possible. Value can
    be "voltage" or "frequency".
    """
    # Get daily values by id
    df["tidx"] = df["time"].dt.date
    df = df.groupby(["id", "tidx"]).agg(vmin=(value, "min"),
                                        vmax=(value, "max"),
                                        vmean=(value, "mean"))\
           .reset_index()
    # Get avg of daily values by id
    df = df.groupby(["id"]).agg(avg_daily_min=("vmin", "mean"),
                                avg_daily_max=("vmax", "mean"),
                                avg_daily=("vmean", "mean"))\
           .reset_index()
    
    return df

     
