# -*- coding: utf-8 -*-
from matplotlib import rcParams
import matplotlib.pyplot as plt
import os

from covid19 import plot_utils


class Monitor:
    def __init__(
        self,
        loader_functions,
        drawers,
        interactive=False,
        figure_properties=None,
        axes_properties=None,
    ):
        self.loader_fcts = loader_functions
        self.drawers = drawers
        self.interactive = interactive
        self.figure_properties = {} if figure_properties is None else figure_properties
        self.axes_properties = {} if axes_properties is None else axes_properties
        self._figure = None

    @property
    def figure(self) -> plt.Figure:
        self.set_figure()
        return self._figure

    def run(self, fig=None, ax=None, save_dest=None, show=False):
        # set the private _figure attribute
        self.set_figure(fig)

        # retrieve figure and axes
        out_fig, out_ax = plot_utils.get_figure_and_axes(
            fig,
            ax,
            default_fig=self._figure,
            **self.figure_properties,
            **{
                key: value
                for key, value in self.axes_properties.items()
                if key not in self.figure_properties
            }
        )

        # if needed, clean the canvas
        if ax is None:
            out_ax.cla()

        # load the data and draw
        for loader_fct, drawer in zip(self.loader_fcts, self.drawers):
            x, y = loader_fct()
            drawer.draw(x, y, out_ax)

        # set axes properties
        if self.axes_properties != {}:
            plot_utils.set_axes_properties(out_ax, **self.axes_properties)

        # if figure is not provided, set figure properties
        if fig is None and self.figure_properties != {}:
            plot_utils.set_figure_properties(out_fig, **self.figure_properties)

        # save
        if not (save_dest is None or save_dest == ""):
            _, ext = os.path.splitext(save_dest)
            plt.savefig(save_dest, format=ext[1:], dpi=1000)

        # show
        if fig is None:
            if self.interactive:
                out_fig.canvas.draw()
                plt.show(block=False)
            elif show:
                plt.show()

        return out_fig, out_ax

    def set_figure(self, fig=None):
        if fig is not None:
            self._figure = None
            return

        fontsize = self.figure_properties.get("fontsize", 12)
        figsize = self.figure_properties.get("figsize", (7, 7))

        if self.interactive:
            plt.ion()
            if self._figure is not None:
                rcParams["font.size"] = fontsize
                self._figure = plt.figure(figsize=figsize)
        else:
            plt.ioff()
            rcParams["font.size"] = fontsize
            self._figure = (
                plt.figure(figsize=figsize) if self._figure is None else self._figure
            )
