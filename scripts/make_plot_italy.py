# -*- coding: utf-8 -*-
import functools

from covid19 import config
from covid19.drawers import TimeSeriesDrawer
from covid19.loaders import LoaderItaly
from covid19.monitor import Monitor


fields = ["totale_casi"] * 5
regions = [None, None, "P.A. Trento", "P.A. Bolzano", None]
provinces = ["Bergamo", "Brescia", None, None, "Napoli"]

fontsize = 16
figsize = (13, 7)

colors = ["blue", "pink", "green", "red", "cyan"]
markers = ["o"] * 5

x_label = "Giorno"
y_scale = "log"


if __name__ == "__main__":
    labels = []
    for i in range(len(fields)):
        if regions[i] is None and provinces[i] is None:
            label = config.shorthands["Italy"]
        elif regions[i] is not None:
            label = config.shorthands.get(regions[i], regions[i])
        elif provinces[i] is not None:
            label = config.shorthands.get(provinces[i], provinces[i])
        else:
            assert False
        labels.append(label)

    labels = list(label + " " + field for label, field in zip(labels, fields))

    loader = LoaderItaly()
    time, _ = loader.load("data")
    loader_fcts = list(
        functools.partial(loader.load, field, region, province)
        for field, region, province in zip(fields, regions, provinces)
    )

    drawers = []
    for color, marker, label in zip(colors, markers, labels):
        drawer_properties = {
            "linestyle": "-",
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
        "x_label": x_label,
        "x_ticks": time,
        "x_ticklabels": time,
        "x_ticklabels_rotation": 90.0,
        "y_scale": y_scale,
        "legend_on": True,
        "legend_loc": "upper left",
        "legend_framealpha": 1.0,
        "legend_bbox_to_anchor": (1.0, 1.0),
        "grid_on": True,
    }

    monitor = Monitor(
        loader_fcts,
        drawers,
        figure_properties=figure_properties,
        axes_properties=axes_properties,
    )
    monitor.plot(show=True)
