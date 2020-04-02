# -*- coding: utf-8 -*-
import functools

from covid19 import config
from covid19.drawers import TimeSeriesDrawer
from covid19.loader import Loader
from covid19.monitor import Monitor


fields = ["totale_casi", "tamponi"] * 3
regions = [None, None, "Lombardia", "Lombardia", "Veneto", "Veneto"]
provinces = [None] * 6

fontsize = 14
figsize = (6.5, 7)

colors = ["blue", "blue", "red", "red", "green", "green"]
labels = [
    "Italy - Confirmed cases",
    "Italy - Swabs",
    "Lombardy - Confirmed cases",
    "Lombardy - Swabs",
    "Veneto - Confirmed cases",
    "Veneto - Swabs"
]
linestyles = ["-", "--"] * 3
markers = [None] * 6

x_label = "Day"
x_ticklabels_rotation = 45
x_ticklabels_step = 5
y_label = None
y_lim = [1e1, 1e6]
y_scale = "log"

title = "$\\mathbf{(a)}$ Raw figures"

legend_loc = "best"


if __name__ == "__main__":
    # labels = []
    # for i in range(len(fields)):
    #     if regions[i] is None and provinces[i] is None:
    #         label = config.shorthands["Italy"]
    #     elif regions[i] is not None:
    #         label = config.shorthands.get(regions[i], regions[i])
    #     elif provinces[i] is not None:
    #         label = config.shorthands.get(provinces[i], provinces[i])
    #     else:
    #         assert False
    #     labels.append(label)
    #
    # labels = list(label + " " + field for label, field in zip(labels, fields))

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
    monitor.run(show=True)
