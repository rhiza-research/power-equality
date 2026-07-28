import contextily as ctx
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

RANGE_COLORS = {
    "low": "#8B0000",
    "good": "#2E8B57",
    "high": "#FF6347",
}
RANGE_ORDER = ["low", "good", "high"]


def plot_voltage_range_map(df, pie_size=1, figsize=(12, 10)):
    """Plots a pie chart of voltage time-in-range at each location's lat/lon.

    df must have columns: id, phase, voltage_range, duration_in_range,
    total_duration, latitude, longitude. Locations with more than one phase
    get side-by-side pies labeled by phase.
    """
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_aspect("equal")

    locations = df[["latitude", "longitude"]].drop_duplicates()
    lon_pad = max(pie_size * 2, (locations["longitude"].max() - locations["longitude"].min()) * 0.1 + pie_size)
    lat_pad = max(pie_size * 2, (locations["latitude"].max() - locations["latitude"].min()) * 0.1 + pie_size)
    ax.set_xlim(locations["longitude"].min() - lon_pad, locations["longitude"].max() + lon_pad)
    ax.set_ylim(locations["latitude"].min() - lat_pad, locations["latitude"].max() + lat_pad)

    # add a tile basemap; crs tells contextily our axes are in lon/lat (EPSG:4326)
    # so it reprojects the tiles to match, rather than us reprojecting our points
    ctx.add_basemap(ax, crs="EPSG:4326", source=ctx.providers.OpenStreetMap.Mapnik)

    for (loc_id, lat, lon), loc_group in df.groupby(["id", "latitude", "longitude"]):
        phases = sorted(loc_group["phase"].unique())
        offsets = _phase_offsets(len(phases), pie_size)

        for phase, dx in zip(phases, offsets):
            phase_df = loc_group[loc_group["phase"] == phase].set_index("voltage_range")
            sizes = [phase_df["duration_in_range"].get(r, 0) for r in RANGE_ORDER]
            colors = [RANGE_COLORS[r] for r in RANGE_ORDER]

            cx = lon + dx
            inset = ax.inset_axes(
                [cx - pie_size / 2, lat - pie_size / 2, pie_size, pie_size],
                transform=ax.transData,
            )
            inset.pie(sizes, colors=colors)
            if len(phases) > 1:
                inset.set_title(phase, fontsize=6, pad=1)

    legend_handles = [Patch(color=RANGE_COLORS[r], label=r) for r in RANGE_ORDER]
    ax.legend(handles=legend_handles, title="Voltage range", loc="upper right")

    ax.set_title("Voltage time-in-range by location")
    return fig, ax


def _phase_offsets(n, pie_size):
    """Returns horizontal offsets (data units) to lay out n pies side by side, centered on 0."""
    spacing = pie_size * 1.2
    start = -(n - 1) * spacing / 2
    return [start + i * spacing for i in range(n)]
