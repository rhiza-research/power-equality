import matplotlib.pyplot as plt

DAY_NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
MINUTES_PER_DAY = 24 * 60
MINUTES_PER_WEEK = 7 * MINUTES_PER_DAY


def plot_weekly_voltage_profile(df, vnom=230, figsize=(14, 6)):
    """Plots the average weekly (Mon-Sun) voltage magnitude profile at full time
    resolution, one line per location. The +/-10% nominal band is shaded green
    and nominal voltage is marked with a dashed red line.
    """
    df = df[df["value_name"].str.startswith("voltage_mag_")].copy()
    df["phase"] = df["value_name"].str.split("_").str[2]

    df["minute_of_week"] = (
        df["time"].dt.dayofweek * MINUTES_PER_DAY
        + df["time"].dt.hour * 60
        + df["time"].dt.minute
    )

    weekly = (
        df.groupby(["id", "phase", "minute_of_week"])["value"]
        .mean()
        .reset_index()
    )

    fig, ax = plt.subplots(figsize=figsize)

    # shade the +/-10% good range and mark nominal voltage
    ax.axhspan(
        vnom * 0.9, vnom * 1.1, color="#2E8B57", alpha=0.15, zorder=0,
        label="Good range (±10% nominal)",
    )
    ax.axhline(vnom, color="red", linestyle="--", linewidth=1, zorder=1, label=f"Nominal ({vnom}V)")

    for (loc_id, phase), group in weekly.groupby(["id", "phase"]):
        ax.plot(group["minute_of_week"], group["value"], color="grey", alpha=0.4, linewidth=1, zorder=2)

    day_ticks = [d * MINUTES_PER_DAY for d in range(8)]
    day_labels = DAY_NAMES + [DAY_NAMES[0]]
    ax.set_xticks(day_ticks)
    ax.set_xticklabels(day_labels)
    ax.set_xlim(0, MINUTES_PER_WEEK)
    for t in day_ticks:
        ax.axvline(t, color="grey", linewidth=0.5, alpha=0.3, zorder=0)

    ax.set_xlabel("Day of week")
    ax.set_ylabel("Voltage (V)")
    ax.set_title("Average weekly voltage profile")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.tight_layout()
    return fig, ax
