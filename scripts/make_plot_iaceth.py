# -*- coding: utf-8 -*-
from covid19.monitor import MonitorComposite


fontsize = 14
figsize = (13, 7)


if __name__ == "__main__":
    from scripts.make_plot_iaceth_1 import main as get_monitor_1
    from scripts.make_plot_iaceth_2 import main as get_monitor_2

    slaves = [get_monitor_1(draw=False), get_monitor_2(draw=False)]

    figure_properties = {
        "fontsize": fontsize,
        "figsize": figsize,
        "tight_layout": True
    }
    monitor = MonitorComposite(slaves, nrows=1, ncols=2, figure_properties=figure_properties)

    monitor.run(show=True)
