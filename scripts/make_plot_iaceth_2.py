# -*- coding: utf-8 -*-
import functools

from covid19 import config
from covid19.drawers import TimeSeriesDrawer
from covid19.loader import Loader
from covid19.monitor import Monitor


fields = ["percentuale_tamponi_positivi"] * 3
regions = [None, "Lombardia", "Veneto"]
provinces = [None] * 3

fontsize = 14
figsize = (6.5, 7)

colors = ["blue", "red", "green"]
labels = [
    "Italy",
    "Lombardy",
    "Veneto",
]
linestyles = ["-"] * 3
markers = [None] * 3

x_label = "Date"
x_ticklabels_rotation = 45
x_ticklabels_step = 5
y_label = None
y_lim = None
y_scale = None

title = "$\\mathbf{(b)}$ Percentage of total swabs performed positive"

legend_loc = "best"


def main(draw=False):
    loader = Loader.factory("italy", update_data=True, apply_patches=False)
    time, _ = loader.run("data")
    loader_fcts = list(
        functools.partial(loader.run, field, region=region, province=province)
        for field, region, province in zip(fields, regions, provinces)
    )

    drawers = []
    for color, label, linestyle, marker in zip(colors, labels, linestyles, markers):
        drawer_properties = {
            "linestyle": linestyle,
            "linewidth": 2.0,
            "linecolor": color,
            "marker": marker,
            "markersize": 8,
            "markerfacecolor": color,
            "markeredgecolor": color,
            "legend_label": label,
        }
        drawers.append(TimeSeriesDrawer(drawer_properties))

    figure_properties = {"figsize": figsize, "fontsize": fontsize, "tight_layout": True}
    axes_properties = {
        "fontsize": fontsize,
        "title_center": title,
        "x_label": x_label,
        "x_ticks": time[::x_ticklabels_step],
        "x_ticklabels": time[::x_ticklabels_step],
        "x_ticklabels_rotation": x_ticklabels_rotation,
        "y_lim": y_lim,
        "y_scale": y_scale,
        "legend_on": True,
        "legend_loc": legend_loc,
        "legend_framealpha": 1.0,
        # "legend_bbox_to_anchor": (1.0, 1.0),
        "grid_on": True,
    }

    monitor = Monitor(
        loader_fcts,
        drawers,
        figure_properties=figure_properties,
        axes_properties=axes_properties,
    )

    if draw:
        monitor.run(show=True)

    return monitor


if __name__ == "__main__":
    main(draw=True)
