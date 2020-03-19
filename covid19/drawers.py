# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt

from covid19 import plot_utils
from covid19.loaders import LoaderItaly


class TimeSeriesDrawer:
    def __init__(self, properties):
        self.properties = properties

    def draw(self, time, data, ax):
        plot_utils.make_lineplot(x=time, y=data, ax=ax, **self.properties)
        return ax


if __name__ == "__main__":
    fig, ax = plot_utils.get_figure_and_axes()

    properties = {
        "linestyle": "-",
        "linewidth": 2.0,
        "linecolor": "blue",
        "marker": "o",
        "markersize": 8,
        "markercolor": "blue",
    }
    drawer = TimeSeriesDrawer(properties)

    ld = LoaderItaly()
    time, data = ld.load("totale_attualmente_positivi")
    drawer.draw(time, data, ax)

    plot_utils.set_axes_properties(
        ax, x_ticks=range(len(time)), x_ticklabels=time, x_ticklabels_rotation=90.0
    )
    plot_utils.set_figure_properties(fig, tight_layout=True)

    plt.show()
