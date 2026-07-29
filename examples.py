import os

import matplotlib.pyplot as plt
import pandas as pd

from iec.peqi_metrics.loader import load_standard_csv
from iec.peqi_metrics.voltage_metrics import time_in_range
from iec.peqi_visuals.map_visuals import plot_voltage_range_map
from iec.peqi_visuals.ts_visuals import plot_weekly_voltage_profile

if __name__ == "__main__":
    # read each of the esmi processed files
    raw_dfs = []
    results = []
    for file in os.listdir("iec/datasets/esmi_processed"):
        if file.endswith(".csv"):
            df = load_standard_csv(os.path.join("iec/datasets/esmi_processed", file))
            raw_dfs.append(df)
            results.append(time_in_range(df))

    merged = pd.concat(results, ignore_index=True)
    # some locations appear in more than one file (e.g. multiple weeks) - combine those
    merged = merged.groupby(
        ["id", "phase", "voltage_range", "latitude", "longitude"], as_index=False
    )[["duration_in_range", "total_duration"]].sum()

    #fig, ax = plot_voltage_range_map(merged)
    #plt.show()
    #breakpoint()

    raw_merged = pd.concat(raw_dfs, ignore_index=True)
    fig, ax = plot_weekly_voltage_profile(raw_merged)
    plt.show()
    breakpoint()