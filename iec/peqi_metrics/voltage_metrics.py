import pandas as pd


def _infer_duration_minutes(df, group_cols=("id", "phase")):
    """Infers the reporting duration (in minutes): mean diff of sorted times within each
    group, then mean of those group means across all groups."""
    group_mean_diffs = df.groupby(list(group_cols))["time"].apply(
        lambda times: times.sort_values().diff().mean()
    )
    return group_mean_diffs.mean().total_seconds() / 60


def time_in_range(df, vnom=230):
    """Given a standard dataframe, for voltage magnitude reports, calculate times in different ranges."""
    df = df[df["value_name"].str.startswith("voltage_mag_")].copy()
    df["phase"] = df["value_name"].str.split("_").str[2]

    # infer the reporting duration and use it as every row's duration
    df["duration"] = _infer_duration_minutes(df)

    # bin each measurement into a voltage range
    low, high = 0.9 * vnom, 1.1 * vnom
    df["voltage_range"] = pd.cut(
        df["value"],
        bins=[-float("inf"), low, high, float("inf")],
        labels=["low", "good", "high"],
    )

    locations = df.groupby("id")[["latitude", "longitude"]].first()

    duration_in_range = (
        df.groupby(["id", "phase", "voltage_range"], observed=True)["duration"]
        .sum()
        .reset_index(name="duration_in_range")
    )
    total_duration = (
        df.groupby(["id", "phase"])["duration"]
        .sum()
        .reset_index(name="total_duration")
    )

    result = duration_in_range.merge(total_duration, on=["id", "phase"])
    result = result.merge(locations, on="id", how="left")
    return result
