# -*- coding: utf-8 -*-
import functools

from covid19 import config
from covid19.drawers import TimeSeriesDrawer
from covid19.loader import Loader
from covid19.monitor import Monitor


fields = ["Confirmed"] * 6
provinces = [None, None, None, None, None, None]
countries = ["China", "Germany", "Italy", "Spain", "Switzerland", "US"]

fontsize = 16
figsize = (13, 7)

colors = ["purple", "blue", "cyan", "green", "orange", "red"]
markers = [None] * 6
labels = countries

x_label = "Day"
x_ticklabels_step = 3

y_label = "Confirmed cases"
y_scale = "log"


if __name__ == "__main__":
    # labels = []
    # for i in range(len(fields)):
    #     label = provinces[i] if provinces[i] else countries[i]
    #     labels.append(label + " " + fields[i])

    loader = Loader.factory("world")
    time, _ = loader.run("Confirmed", country="Italy")
    loader_fcts = list(
        functools.partial(loader.run, field, province=province, country=country)
        for field, province, country in zip(fields, provinces, countries)
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
        "x_ticks": time[::x_ticklabels_step],
        "x_ticklabels": time[::x_ticklabels_step],
        "x_ticklabels_rotation": 90.0,
        "y_label": y_label,
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
    monitor.run(show=True)
