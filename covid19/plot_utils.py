# -*- coding: utf-8 -*-
from matplotlib import rc, rcParams
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.offsetbox import AnchoredText
import matplotlib.patches as patches
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import numpy as np
from typing import Optional, Sequence, Tuple


text_locations = {
    "upper right": 1,
    "upper left": 2,
    "lower left": 3,
    "lower right": 4,
    "right": 5,
    "center left": 6,
    "center right": 7,
    "lower center": 8,
    "upper center": 9,
    "center": 10,
}


linestyle_dict = {
    "-": "solid",
    "--": "dashed",
    ":": "dotted",
    "-.": "dashdot",
    "solid": "solid",
    "dashed": "dashed",
    "dotted": "dotted",
    "dashdot": "dashdot",
    "loosely dotted": (0, (1, 10)),
    "densely dotted": (0, (1, 1)),
    "loosely dashed": (0, (5, 10)),
    "densely dashed": (0, (5, 1)),
    "loosely dashdotted": (0, (3, 10, 1, 10)),
    "dashdotted": (0, (3, 5, 1, 5)),
    "densely dashdotted": (0, (3, 1, 1, 1)),
    "dashdotdotted": (0, (3, 5, 1, 5, 1, 5)),
    "loosely dashdotdotted": (0, (3, 10, 1, 10, 1, 10)),
    "densely dashdotdotted": (0, (3, 1, 1, 1, 1, 1)),
}


def get_figure_and_axes(
    fig: Optional[plt.Figure] = None,
    ax: Optional[plt.Axes] = None,
    default_fig: Optional[plt.Figure] = None,
    nrows: int = 1,
    ncols: int = 1,
    index: int = 1,
    **kwargs
) -> Tuple[plt.Figure, plt.Axes]:
    """
    Get a :class:`matplotlib.figure.Figure` object and a :class:`matplotlib.axes.Axes`
    object, with the latter embedded in the former. The returned values are determined
    as follows:

        * If both `fig` and `ax` arguments are passed in:

            - if `ax` is embedded in `fig`, return `fig` and `ax`;
            - otherwise, return the figure which encloses `ax`, and `ax` itself;

        * If `fig` is provided but `ax` is not:

            - if `fig` contains some subplots, return `fig` and the axes of the
                subplot in position (`nrows`, `ncols`, `index`) it contains;
            - otherwise, add a subplot to `fig` in position (`nrows`, `ncols`, `index`)
                and return `fig` and the subplot axes;

        * If `ax` is provided but `fig` is not, return the figure which encloses `ax`,
            and `ax` itself;

        * If neither `fig` nor `ax` are passed in:

            - if `default_fig` is not given, instantiate a new pair of figure and axes;
            - if `default_fig` is provided and it contains some subplots, return
                `default_fig` and the axes of the subplot in position
                (`nrows`, `ncols`, `index`) it contains;
            - if `default_fig` is provided but is does not contain any subplot, add a
                subplot to `default_fig` in position (1,1,1) and return `default_fig`
                and the subplot axes.

    Parameters
    ----------
    fig : `matplotlib.figure.Figure`, optional
        The figure.
    ax : `matplotlib.axes.Axes`, optional
        The axes.
    default_fig : `matplotlib.figure.Figure`, optional
        The default figure.
    nrows : `int`, optional
        Number of rows of the subplot grid. Defaults to 1.
    ncols : `int`, optional
        Number of columns of the subplot grid. Defaults to 1.
    index : `int`, optional
        Axes' index in the subplot grid. Defaults to 1.

    Keyword arguments
    -----------------
    figsize : `tuple`, optional
        The size which the output figure should have. Defaults to (7, 7).
        This argument is effective only if the figure is created within the function.
    fontsize : `int`, optional
        Font size for the output figure and axes. Defaults to 12.
        This argument is effective only if the figure is created within the function.
    projection : `str`, optional
        The axes projection. Defaults to `None`.
        This argument is effective only if the figure is created within the function.

    Returns
    -------
    out_fig : matplotlib.figure.Figure
        The figure.
    out_ax : matplotlib.axes.Axes
        The axes.
    """
    figsize = kwargs.get("figsize", (7, 7))
    fontsize = kwargs.get("fontsize", 12)
    projection = kwargs.get("projection", None)

    rcParams["font.size"] = fontsize

    if (fig is not None) and (ax is not None):
        try:
            if ax not in fig.get_axes():
                import warnings

                warnings.warn(
                    "Input axes do not belong to the input figure, "
                    "so the figure which the axes belong to is considered.",
                    RuntimeWarning,
                )

                out_fig, out_ax = ax.get_figure(), ax
            else:
                out_fig, out_ax = fig, ax
        except AttributeError:
            import warnings

            warnings.warn(
                "Input argument ''fig'' does not seem to be a matplotlib.figure.Figure, "
                "so the figure the axes belong to are considered.",
                RuntimeWarning,
            )

            out_fig, out_ax = ax.get_figure(), ax
    elif (fig is not None) and (ax is None):
        try:
            out_fig = fig
            out_ax = out_fig.add_subplot(nrows, ncols, index, projection=projection)
        except AttributeError:
            import warnings

            warnings.warn(
                "Input argument ''fig'' does not seem to be a matplotlib.figure.Figure, "
                "hence a proper matplotlib.figure.Figure object is created.",
                RuntimeWarning,
            )

            out_fig = plt.figure(figsize=figsize)
            out_ax = out_fig.add_subplot(nrows, ncols, index, projection=projection)
    elif (fig is None) and (ax is not None):
        out_fig, out_ax = ax.get_figure(), ax
    else:  # (fig is None) and (ax is None)
        if default_fig is None:
            out_fig = plt.figure(figsize=figsize)
            out_ax = out_fig.add_subplot(nrows, ncols, index, projection=projection)
        else:
            try:
                out_fig = default_fig
                out_ax = out_fig.add_subplot(nrows, ncols, index, projection=projection)
            except AttributeError:
                import warnings

                warnings.warn(
                    "Input argument ''default_fig'' does not seem to be a "
                    "matplotlib.figure.Figure, hence a proper matplotlib.figure.Figure "
                    "object is created.",
                    RuntimeWarning,
                )

                out_fig = plt.figure(figsize=figsize)
                out_ax = out_fig.add_subplot(nrows, ncols, index, projection=projection)

    return out_fig, out_ax


def set_figure_properties(fig: plt.Figure, **kwargs) -> None:
    """
    Ease the configuration of a :class:`matplotlib.figure.Figure`.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure.

    Keyword arguments
    -----------------
    fontsize : int
        Font size to use for the plot titles, and axes ticks and labels.
        Defaults to 12.
    tight_layout : bool
        `True` to fit the whole subplots into the figure area,
        `False` otherwise. Defaults to `True`.
    tight_layout_rect : Sequence[float]
        A rectangle (left, bottom, right, top) in the normalized figure
        coordinate that the whole subplots area (including labels) will
        fit into. Defaults to (0, 0, 1, 1).
    suptitle : str
        The figure title. Defaults to an empty string.
    xlabel : str
        TODO
    ylabel : str
        TODO
    figlegend_on : bool
        TODO
    figlegend_ax : int
        TODO
    figlegend_loc : `str` or `Tuple[float, float]`
        TODO
    figlegend_framealpha : float
        TODO
    figlegend_ncol : int
        TODO
    subplots_adjust_hspace : float
        TODO
    subplots_adjust_vspace : float
        TODO
    """
    fontsize = kwargs.get("fontsize", 12)
    tight_layout = kwargs.get("tight_layout", True)
    tight_layout_rect = kwargs.get("tight_layout_rect", (0, 0, 1, 1))
    suptitle = kwargs.get("suptitle", "")
    x_label = kwargs.get("x_label", "")
    x_labelpad = kwargs.get("x_labelpad", 20)
    y_label = kwargs.get("y_label", "")
    y_labelpad = kwargs.get("y_labelpad", 20)
    figlegend_on = kwargs.get("figlegend_on", False)
    figlegend_ax = kwargs.get("figlegend_ax", 0)
    figlegend_loc = kwargs.get("figlegend_loc", "lower center")
    figlegend_framealpha = kwargs.get("figlegend_framealpha", 1.0)
    figlegend_ncol = kwargs.get("figlegend_ncol", 1)
    wspace = kwargs.get("subplots_adjust_wspace", None)
    hspace = kwargs.get("subplots_adjust_hspace", None)

    rcParams["font.size"] = fontsize

    if suptitle is not None and suptitle != "":
        fig.suptitle(suptitle, fontsize=fontsize + 1)

    if x_label != "" or y_label != "":
        ax = fig.add_subplot(111)
        ax.set_frame_on(False)
        ax.set_xticks([])
        ax.set_xticklabels([], visible=False)
        ax.set_yticks([])
        ax.set_yticklabels([], visible=False)

        if x_label != "":
            ax.set_xlabel(x_label, labelpad=x_labelpad)
        if y_label != "":
            ax.set_ylabel(y_label, labelpad=y_labelpad)

    if tight_layout:
        fig.tight_layout(rect=tight_layout_rect)

    if figlegend_on:
        handles, labels = fig.get_axes()[figlegend_ax].get_legend_handles_labels()
        fig.legend(
            handles,
            labels,
            loc=figlegend_loc,
            framealpha=figlegend_framealpha,
            ncol=figlegend_ncol,
        )

    if wspace is not None:
        fig.subplots_adjust(wspace=wspace)
    if hspace is not None:
        fig.subplots_adjust(hspace=hspace)


def set_axes_properties(ax: plt.Axes, **kwargs) -> None:
    """
    Ease the configuration of a :class:`matplotlib.axes.Axes` object.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        The axes.

    Keyword arguments
    -----------------
    fontsize : int
        Font size to use for the plot titles, and axes ticks and labels.
        Defaults to 12.
    title_center : str
        The center title. Defaults to an empty string.
    title_left : str
        The left title. Defaults to an empty string.
    title_right : str
        The right title. Defaults to an empty string.
    x_label : str
        The x-axis label. Defaults to an empty string.
    x_labelcolor : str
        Color of the x-axis label. Defaults to 'black'.
    x_lim : Sequence[int]
        Data limits for the x-axis. Defaults to `None`, i.e., the data limits
        will be left unchanged.
    invert_xaxis : bool
        `True` to make to invert the x-axis, `False` otherwise.
        Defaults to `False`.
    x_scale : str
        The x-axis scale. Defaults to 'linear'.
    x_ticks : sequence[float]
        Sequence of x-axis ticks location. Defaults to `None`.
    x_ticklabels : sequence[str]
        Sequence of x-axis ticks labels. Defaults to `None`.
    x_ticklabels_color : str
        Color for the x-axis ticks labels. Defaults to 'black'.
    x_ticklabels_rotation : float
        Rotation angle of the x-axis ticks labels. Defaults to 0.
    xaxis_minor_ticks_visible : bool
        `True` to show all ticks, either labelled or unlabelled,
        `False` to show only the labelled ticks. Defaults to `False`.
    xaxis_visible : bool
        `False` to make the x-axis invisible. Defaults to `True`.
    y_label : str
        The y-axis label. Defaults to an empty string.
    y_labelcolor : str
        Color of the y-axis label. Defaults to 'black'.
    y_lim : Sequence[int]
        Data limits for the y-axis. Defaults to `None`, i.e., the data limits
        will be left unchanged.
    invert_yaxis : bool
        `True` to make to invert the y-axis, `False` otherwise.
        Defaults to `False`.
    y_scale : str
        The y-axis scale. Defaults to 'linear'.
    y_ticks : sequence[float]
        Sequence of y-axis ticks location. Defaults to `None`.
    y_ticklabels : sequence[str]
        Sequence of y-axis ticks labels. Defaults to `None`.
    y_ticklabels_color : str
        Color for the y-axis ticks labels. Defaults to 'black'.
    y_ticklabels_rotation : float
        Rotation angle of the y-axis ticks labels. Defaults to 0.
    yaxis_minor_ticks_visible : bool
        `True` to show all ticks, either labelled or unlabelled,
        `False` to show only the labelled ticks. Defaults to :obj:`False`.
    yaxis_visible : bool
        :obj:`False` to make the y-axis invisible. Defaults to :obj:`True`.
    z_label : str
        The z-axis label. Defaults to an empty string.
    z_labelcolor : str
        Color of the z-axis label. Defaults to 'black'.
    z_lim : Sequence[int]
        Data limits for the z-axis. Defaults to :obj:`None`, i.e., the data limits
        will be left unchanged.
    invert_zaxis : bool
        :obj:`True` to make to invert the z-axis, :obj:`False` otherwise.
        Defaults to :obj:`False`.
    z_scale : str
        The z-axis scale. Defaults to 'linear'.
    z_ticks : sequence[float]
        Sequence of z-axis ticks location. Defaults to :obj:`None`.
    z_ticklabels : sequence[str]
        Sequence of z-axis ticks labels. Defaults to :obj:`None`.
    z_ticklabels_color : str
        Rotation angle of the z-axis ticks labels. Defaults to 0.
    z_ticklabels_rotation : float
        Color for the z-axis ticks labels. Defaults to 'black'.
    zaxis_minor_ticks_visible : bool
        :obj:`True` to show all ticks, either labelled or unlabelled,
        :obj:`False` to show only the labelled ticks. Defaults to :obj:`False`.
    zaxis_visible : bool
        :obj:`False` to make the z-axis invisible. Defaults to :obj:`True`.
    legend_on : bool
        :obj:`True` to show the legend, :obj:`False` otherwise. Defaults to :obj:`False`.
    legend_loc : str
        String specifying the location where the legend should be placed.
        Defaults to 'best'; please see :func:`matplotlib.pyplot.legend` for all
        the available options.
    legend_bbox_to_anchor : Sequence[float]
        4-items tuple defining the box used to place the legend. This is used in
        conjuction with `legend_loc` to allow arbitrary placement of the legend.
    legend_framealpha : float
        Legend transparency. It should be between 0 and 1; defaults to 0.5.
    legend_ncol : int
        Number of columns into which the legend labels should be arranged.
        Defaults to 1.
    text : str
        Text to be added to the figure as anchored text. Defaults to :obj:`None`,
        meaning that no text box is shown.
    text_loc : str
        String specifying the location where the text box should be placed.
        Defaults to 'upper right'; please see :class:`matplotlib.offsetbox.AnchoredText`
        for all the available options.
    grid_on : bool
        :obj:`True` to show the plot grid, :obj:`False` otherwise.
        Defaults to :obj:`False`.
    grid_properties : dict
        Keyword arguments specifying various settings of the plot grid.
    """
    fontsize = kwargs.get("fontsize", 12)
    # title
    title_center = kwargs.get("title_center", "")
    title_left = kwargs.get("title_left", "")
    title_right = kwargs.get("title_right", "")
    # x-axis
    x_label = kwargs.get("x_label", "")
    x_labelcolor = kwargs.get("x_labelcolor", "black")
    x_lim = kwargs.get("x_lim", None)
    invert_xaxis = kwargs.get("invert_xaxis", False)
    x_scale = kwargs.get("x_scale", "linear")
    x_ticks = kwargs.get("x_ticks", None)
    x_ticklabels = kwargs.get("x_ticklabels", None)
    x_ticklabels_color = kwargs.get("x_ticklabels_color", "black")
    x_ticklabels_rotation = kwargs.get("x_ticklabels_rotation", 0)
    x_tickformat = kwargs.get("x_tickformat", None)
    xaxis_minor_ticks_visible = kwargs.get("xaxis_minor_ticks_visible", False)
    xaxis_visible = kwargs.get("xaxis_visible", True)
    # y-axis
    y_label = kwargs.get("y_label", "")
    y_labelcolor = kwargs.get("y_labelcolor", "black")
    y_lim = kwargs.get("y_lim", None)
    invert_yaxis = kwargs.get("invert_yaxis", False)
    y_scale = kwargs.get("y_scale", "linear")
    y_ticks = kwargs.get("y_ticks", None)
    y_ticklabels = kwargs.get("y_ticklabels", None)
    y_ticklabels_color = kwargs.get("y_ticklabels_color", "black")
    y_ticklabels_rotation = kwargs.get("y_ticklabels_rotation", 0)
    y_tickformat = kwargs.get("y_tickformat", None)
    yaxis_minor_ticks_visible = kwargs.get("yaxis_minor_ticks_visible", False)
    yaxis_visible = kwargs.get("yaxis_visible", True)
    # legend
    legend_on = kwargs.get("legend_on", False)
    legend_loc = kwargs.get("legend_loc", "best")
    legend_bbox_to_anchor = kwargs.get("legend_bbox_to_anchor", None)
    legend_framealpha = kwargs.get("legend_framealpha", 0.5)
    legend_ncol = kwargs.get("legend_ncol", 1)
    legend_fontsize = kwargs.get("legend_fontsize", fontsize)
    # textbox
    text = kwargs.get("text", None)
    text_loc = kwargs.get("text_loc", "")
    # grid
    grid_on = kwargs.get("grid_on", False)
    grid_properties = kwargs.get("grid_properties", None)

    rcParams["font.size"] = fontsize
    # rcParams['text.usetex'] = True

    # plot titles
    if ax.get_title(loc="center") == "":
        ax.set_title(title_center, loc="center", fontsize=rcParams["font.size"] - 1)
    if ax.get_title(loc="left") == "":
        ax.set_title(title_left, loc="left", fontsize=rcParams["font.size"] - 1)
    if ax.get_title(loc="right") == "":
        ax.set_title(title_right, loc="right", fontsize=rcParams["font.size"] - 1)

    # axes labels
    if ax.get_xlabel() == "":
        ax.set(xlabel=x_label)
    if ax.get_ylabel() == "":
        ax.set(ylabel=y_label)

    # axes labelcolors
    if ax.get_xlabel() != "" and x_labelcolor != "":
        ax.xaxis.label.set_color(x_labelcolor)
    if ax.get_ylabel() != "" and y_labelcolor != "":
        ax.yaxis.label.set_color(y_labelcolor)

    # axes limits
    if x_lim is not None:
        ax.set_xlim(x_lim)
    if y_lim is not None:
        ax.set_ylim(y_lim)

    # invert the axes
    if invert_xaxis:
        ax.invert_xaxis()
    if invert_yaxis:
        ax.invert_yaxis()

    # axes scale
    if x_scale is not None:
        ax.set_xscale(x_scale)
    if y_scale is not None:
        ax.set_yscale(y_scale)

    # axes ticks
    if x_ticks is not None:
        ax.get_xaxis().set_ticks(x_ticks)
    if y_ticks is not None:
        ax.get_yaxis().set_ticks(y_ticks)

    # axes tick labels
    if x_ticklabels is not None:
        ax.get_xaxis().set_ticklabels(x_ticklabels)
    if y_ticklabels is not None:
        ax.get_yaxis().set_ticklabels(y_ticklabels)

    # axes tick labels color
    if x_ticklabels_color != "":
        ax.tick_params(axis="x", colors=x_ticklabels_color)
    if y_ticklabels_color != "":
        ax.tick_params(axis="y", colors=y_ticklabels_color)

    # axes tick format
    if x_tickformat is not None:
        ax.xaxis.set_major_formatter(FormatStrFormatter(x_tickformat))
    if y_tickformat is not None:
        ax.yaxis.set_major_formatter(FormatStrFormatter(y_tickformat))

    # axes tick labels rotation
    plt.xticks(rotation=x_ticklabels_rotation)
    plt.yticks(rotation=y_ticklabels_rotation)

    # unlabelled axes ticks
    if not xaxis_minor_ticks_visible:
        ax.get_xaxis().set_tick_params(which="minor", size=0)
        ax.get_xaxis().set_tick_params(which="minor", width=0)
    if not yaxis_minor_ticks_visible:
        ax.get_yaxis().set_tick_params(which="minor", size=0)
        ax.get_yaxis().set_tick_params(which="minor", width=0)

    # axes visibility
    if not xaxis_visible:
        ax.get_xaxis().set_visible(False)
    if not yaxis_visible:
        ax.get_yaxis().set_visible(False)

    # legend
    if legend_on:
        if legend_bbox_to_anchor is None:
            ax.legend(
                loc=legend_loc,
                framealpha=legend_framealpha,
                ncol=legend_ncol,
                fontsize=legend_fontsize,
            )
        else:
            ax.legend(
                loc=legend_loc,
                framealpha=legend_framealpha,
                ncol=legend_ncol,
                fontsize=legend_fontsize,
                bbox_to_anchor=legend_bbox_to_anchor,
            )

    # text box
    if text is not None:
        ax.add_artist(AnchoredText(text, loc=text_locations[text_loc]))

    # plot grid
    if grid_on:
        gps = grid_properties if grid_properties is not None else {}
        ax.grid(True, **gps)


def make_lineplot(x: np.ndarray, y: np.ndarray, ax: plt.Axes, **kwargs) -> None:
    """ Plot a line.

    Parameters
    ----------
    x : numpy.ndarray
        1-D array gathering the x-coordinates of the points to plot.
    y : numpy.ndarray
        1-D array gathering the y-coordinates of the points to plot.
    ax : matplotlib.axes.Axes
        The axes embodying the plot.

    Keyword arguments
    -----------------
    fontsize : int
        The fontsize to be used. Defaults to 16.
    x_factor : float
        Scaling factor for the x-coordinates. Defaults to 1.
    y_factor : float
        Scaling factor for the y-coordinates. Defaults to 1.
    linestyle : str
        String specifying the line style. Defaults to 'solid'.
        Please see https://matplotlib.org/3.1.1/gallery/lines_bars_and_markers/linestyles.html
        for all available options.
    linewidth : float
        The line width. Defaults to 1.5.
    linecolor : str
        String specifying the line color. Defaults to 'blue'.
    marker : str
        The shape of the markers. If not given, no markers will be displayed.
    markersize : float
        Marker size. Defaults to 5.
    markeredgewidth : str
        Marker edge width. Defaults to 1.5.
    markerfacecolor : str
        Marker face color. Defaults to 'blue'.
    markeredgecolor : str
        Marker edge color. Defaults to 'blue'.
    legend_label : str
        The legend label for the line. Defaults to an empty string.
    """
    # get keyword arguments
    fontsize = kwargs.get("fontsize", 16)
    x_factor = kwargs.get("x_factor", 1.0)
    y_factor = kwargs.get("y_factor", 1.0)
    linestyle = kwargs.get("linestyle", "solid")
    linestyle = linestyle or "solid"
    linewidth = kwargs.get("linewidth", 1.5)
    linecolor = kwargs.get("linecolor", "blue")
    marker = kwargs.get("marker", None)
    markersize = kwargs.get("markersize", 5)
    markeredgewidth = kwargs.get("markeredgewidth", 1.5)
    markerfacecolor = kwargs.get("markerfacecolor", "blue")
    markeredgecolor = kwargs.get("markeredgecolor", "blue")
    legend_label = kwargs.get("legend_label", "")

    # global settings
    rcParams["font.size"] = fontsize

    # rescale the axes for visualization purposes
    # x *= x_factor
    # y *= y_factor

    # plot
    if legend_label == "" or legend_label is None:
        ax.plot(
            x,
            y,
            color=linecolor,
            linestyle=linestyle_dict[linestyle],
            linewidth=linewidth,
            marker=marker,
            markersize=markersize,
            markeredgewidth=markeredgewidth,
            markerfacecolor=markerfacecolor,
            markeredgecolor=markeredgecolor,
        )
    else:
        ax.plot(
            x,
            y,
            color=linecolor,
            linestyle=linestyle_dict[linestyle],
            linewidth=linewidth,
            marker=marker,
            markersize=markersize,
            markeredgewidth=markeredgewidth,
            markerfacecolor=markerfacecolor,
            markeredgecolor=markeredgecolor,
            label=legend_label,
        )

    # bring axes back to original units
    # x /= x_factor
    # y /= y_factor


def make_cdf(data: np.ndarray, ax: plt.Axes, **kwargs) -> None:
    """
    Plot the cumulative distribution function (CDF) for an array of points.

    Parameters
    ----------
    data : numpy.ndarray
        1-D array gathering the sample points.
    ax : matplotlib.axes.Axes
        The axes embodying the plot.

    Keyword arguments
    -----------------
    fontsize : int
        The fontsize to be used. Defaults to 16.
    data_on_xaxis : bool
        :obj:`True` to place the data values on the x-axis,
        :obj:`False` to place the data values on the y-axis.
        Defaults to :obj:`False`.
    number_of_bins : int
        Number of bins to be used to compute the CDF. Defaults to 1000.
    threshold : float
        Consider only the grid values greater than this threshold.
        If not specified, all grid values will be considered.
    **kwargs:
        Any keyword argument accepted by :
        func:`tasmania.python.plot.plot_utils.make_lineplot`.
    """
    # get keyword arguments
    fontsize = kwargs.get("fontsize", 16)
    data_on_xaxis = kwargs.get("data_on_xaxis", False)
    number_of_bins = kwargs.get("number_of_bins", 1000)
    threshold = kwargs.get("threshold", None)

    # global settings
    rcParams["font.size"] = fontsize

    # filter data
    if threshold is not None:
        rdata = data[data > threshold]
    else:
        rdata = data

    # compute the cdf
    rdata_min, rdata_max = rdata.min(), rdata.max()
    bins = np.linspace(0, 1, number_of_bins + 1)
    values = rdata_min + bins * (rdata_max - rdata_min)
    cdf = np.zeros(number_of_bins + 1)
    for k in range(number_of_bins + 1):
        cdf[k] = np.sum(rdata <= values[k]) / rdata.size

    # plot
    if data_on_xaxis:
        make_lineplot(values, cdf, ax, **kwargs)
    else:
        make_lineplot(cdf, values, ax, **kwargs)


def add_annotation(ax: plt.Axes, **kwargs) -> None:
    """ Add a text annotation to a plot. """
    # get keyword arguments
    fontsize = kwargs.get("fontsize", 16)
    text = kwargs.get("text", "")
    location = kwargs.get("location", (0, 0))
    horizontal_alignment = kwargs.get("horizontal_alignment", "left")
    vertical_alignment = kwargs.get("vertical_alignment", "center")

    # add annotation
    ax.annotate(
        text,
        location,
        horizontalalignment=horizontal_alignment,
        verticalalignment=vertical_alignment,
        fontsize=fontsize,
    )
