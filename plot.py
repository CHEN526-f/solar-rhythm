# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib"]
# ///

"""Turn one year of Hong Kong solar-radiation data into a radial artwork.

Run:
    uv run plot.py
"""

import csv
import math
from datetime import date
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, Normalize


FILE = "nasa-power-hong-kong-daily-solar-radiation-2025.csv"
PICTURE = "solar-rhythm.png"

HERE = Path(__file__).parent
DATA = HERE / "data" / FILE
OUT = HERE / "out"


def rows(path):
    """Read daily rows with year, month, day, and solar-radiation values."""
    kept = []

    with path.open(encoding="utf-8-sig", newline="") as handle:
        for line in csv.reader(handle):
            if len(line) >= 4 and line[0].isdigit():
                kept.append(line)

    return kept


def main():
    table = rows(DATA)
    print(f"{DATA.name}: {len(table)} rows. First row: {table[0]}")

    day_numbers = []
    values = []

    # One loop: one real calendar day becomes one ray in the artwork.
    for year, month, day, value in table:
        if value == "-999":
            continue

        current_day = date(int(year), int(month), int(day))
        first_day = date(int(year), 1, 1)
        day_numbers.append((current_day - first_day).days)
        values.append(float(value))

    low = min(values)
    high = max(values)
    print(f"{len(values)} values, from {low:.2f} to {high:.2f} kWh/m2/day")

    # Calendar date decides position; radiation decides ray length and colour.
    angles = [2 * math.pi * day / 365 for day in day_numbers]
    strengths = [(value - low) / (high - low) for value in values]
    inner_radius = 0.78
    outer_radii = [inner_radius + 2.85 * strength for strength in strengths]

    sunshine = LinearSegmentedColormap.from_list(
        "sunshine",
        ["#071a33", "#145a86", "#f08a24", "#ffe08a"],
    )
    colour_scale = Normalize(vmin=low, vmax=high)
    colours = [sunshine(colour_scale(value)) for value in values]

    fig = plt.figure(figsize=(11, 11), facecolor="#050b16")
    # Reserve a clean header zone so the title and subtitle never touch the chart.
    fig.subplots_adjust(top=0.84, bottom=0.16)
    ax = fig.add_subplot(111, projection="polar")
    ax.set_facecolor("#050b16")

    # January begins at the top; dates run clockwise around the circle.
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    year = int(table[0][0])
    month_positions = [
        2 * math.pi * (date(year, month, 1) - date(year, 1, 1)).days / 365
        for month in range(1, 13)
    ]

    # Fine rings and month dividers make the year feel like a calendar dial.
    circle_angles = [2 * math.pi * step / 360 for step in range(361)]
    for radius in [1.35, 2.05, 2.75, 3.45]:
        ax.plot(circle_angles, [radius] * len(circle_angles), color="#40617f",
                linewidth=0.6, alpha=0.28, zorder=1)
    for angle in month_positions:
        ax.plot([angle, angle], [0.6, 3.85], color="#8da2b8",
                linewidth=0.7, alpha=0.25, zorder=1)

    # A wide transparent stroke creates a glow; a fine round stroke is the day.
    for angle, outer, colour in zip(angles, outer_radii, colours):
        ax.plot([angle, angle], [inner_radius, outer], color=colour,
                linewidth=6, alpha=0.09, solid_capstyle="round", zorder=2)
    for angle, outer, colour, strength in zip(angles, outer_radii, colours, strengths):
        ax.plot([angle, angle], [inner_radius, outer], color=colour,
                linewidth=1.1 + 1.8 * strength, alpha=0.95,
                solid_capstyle="round", zorder=3)

    # The bright dots are the outer tips of each daily ray.
    ax.scatter(angles, outer_radii, s=[10 + 36 * strength for strength in strengths],
               c=colours, alpha=0.9, edgecolors="none", zorder=4)

    ax.set_xticks(month_positions)
    ax.set_xticklabels(
        ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
         "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        color="#b8c9da",
        fontsize=10,
    )
    ax.tick_params(pad=14)
    ax.set_yticks([])
    ax.grid(False)
    ax.spines["polar"].set_visible(False)
    ax.set_ylim(0, 4.18)

    # Layered central circles give the chart a soft, sun-like heart.
    for size, alpha in [(55000, 0.018), (27000, 0.04), (12000, 0.10), (5600, 0.98)]:
        ax.scatter([0], [0], s=size, color="#ffbe5c", alpha=alpha,
                   edgecolors="none", zorder=5)
    ax.text(
        0,
        0,
        "HONG KONG\nSUNLIGHT\n2025",
        ha="center",
        va="center",
        color="#152234",
        fontsize=11,
        fontweight="bold",
        linespacing=1.25,
        zorder=6,
    )
    fig.suptitle(
        "THE SOLAR YEAR",
        color="#f6f2e9",
        fontsize=24,
        fontweight="bold",
        y=0.985,
    )
    fig.text(0.5, 0.94, "365 daily measures of sunlight over Hong Kong",
             ha="center", color="#b8c9da", fontsize=11)

    mapper = plt.cm.ScalarMappable(cmap=sunshine, norm=colour_scale)
    mapper.set_array(values)
    colour_bar = fig.colorbar(mapper, ax=ax, orientation="horizontal",
                              fraction=0.035, pad=0.09, shrink=0.58, aspect=35)
    colour_bar.outline.set_visible(False)
    colour_bar.ax.tick_params(colors="#b8c9da", labelsize=9)
    colour_bar.set_label("Daily solar radiation (kWh/m²/day): low  ←  blue to gold  →  high",
                         color="#b8c9da", labelpad=8)
    fig.text(0.5, 0.035,
             "One ray = one day · length and colour both come from the recorded value",
             ha="center", color="#b8c9da", fontsize=10)

    OUT.mkdir(exist_ok=True)
    fig.savefig(OUT / PICTURE, dpi=200, facecolor=fig.get_facecolor())
    print(f"saved out/{PICTURE}")
    plt.show()


if __name__ == "__main__":
    main()
