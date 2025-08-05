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
    df = df.groupby(["id"]).agg(vmin=("avg_daily_min", "mean"),
                                vmax=("avg_daily_max", "mean"),
                                vmean=("avg_daily", "mean"))\
           .reset_index()
    
    return df

     
