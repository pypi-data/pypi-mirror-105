import os
import sys
import copy

import numpy as np
import yaml
import mmap
from collections import OrderedDict

import ipywidgets as widgets
from IPython.display import display

from mcstasscript.interface import instr, functions, plotter

import matplotlib.pyplot as plt

class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout

class BaseInterface:
    def __init__(self, scan_overview):
        self.scan_overview = scan_overview

        self.guide_names = self.scan_overview.get_guide_names()
        self.guide_enable = {}
        for guide in self.guide_names:
            self.guide_enable[guide] = True

        n_pars = self.scan_overview.get_n_scanned_parameters()
        self.list_indicies = [0] * n_pars

        self.moderator = self.get_moderator_list()[0]
        self.run_name = self.get_run_name_list()[0]
        self.monitor = self.get_monitor_list()[0]

        self.moderator_scan_labels = None
        self.moderator_scan_sliders = None

        self.sample_scan_sliders = None
        self.sample_scan_labels = None

    def get_guide_names(self):
        return self.guide_names

    def enable_guide(self, guide):
        self.guide_enable[guide] = True

    def disable_guide(self, guide):
        self.guide_enable[guide] = False

    def enabled_guides(self):
        enabled_guides = []
        for guide in self.guide_enable:
            if self.guide_enable[guide]:
                enabled_guides.append(guide)
        return enabled_guides

    def get_monitor_list(self):
        shape = self.scan_overview.get_shape()
        indicies = tuple(self.list_indicies)
        guide = self.guide_names[0]
        moderator = self.get_moderator_list()[0]

        if self.scan_overview.data[guide][indicies][moderator] is not None:
            runs = self.scan_overview.data[guide][indicies][moderator].runs
            return runs[self.run_name].get_monitor_list()
        else:
            return []

    def set_monitor(self, monitor):
        if monitor not in self.get_monitor_list():
            raise KeyError("Monitor named " + monitor + " not available.")

        self.monitor = monitor

    def get_run_name_list(self):
        shape = self.scan_overview.get_shape()
        indicies = tuple(self.list_indicies)
        guide = self.guide_names[0]
        moderator = self.get_moderator_list()[0]

        if self.scan_overview.data[guide][indicies][moderator] is not None:
            runs = self.scan_overview.data[guide][indicies][moderator].runs
            return list(runs.keys())
        else:
            return []

    def set_run_name(self, run_name):
        if run_name not in self.get_run_name_list():
            raise KeyError("Run named " + str(run_name) + " not available.")

        self.run_name = run_name

    def get_moderator_list(self):
        return self.scan_overview.get_moderators()

    def set_moderator(self, moderator):
        if moderator not in self.get_moderator_list():
            raise KeyError("Moderator named " + str(moderator) + " not available.")

        self.moderator = moderator

    def get_scanned_parameters(self):
        return self.scan_overview.get_scanned_parameters()

    def get_scanned_sample_parameters(self):
        return self.scan_overview.get_scanned_sample_parameters()

    def get_scanned_sample_parameter_values(self, parameter):
        return self.scan_overview.get_scanned_sample_parameter_values(parameter)

    def get_scanned_sample_parameter_unit(self, parameter):
        return self.scan_overview.get_scanned_sample_unit(parameter)

    def get_scanned_moderator_parameters(self):
        return self.scan_overview.get_scanned_moderator_parameters()

    def get_scanned_moderator_parameter_values(self, parameter):
        return self.scan_overview.get_scanned_moderator_parameter_values(parameter)

    def get_scanned_moderator_parameter_unit(self, parameter):
        return self.scan_overview.get_scanned_moderator_unit(parameter)

    def get_par_index(self, parameter, type):
        if parameter not in self.get_scanned_parameters():
            raise KeyError("Parameter named" + str(parameter) + "not available.")

        if type == "sample":
            par_index = self.scan_overview.get_par_index_sample(parameter)
        elif type == "moderator":
            par_index = self.scan_overview.get_par_index_moderator(parameter)
        else:
            raise KeyError("type should be sample or moderator")

        return par_index

    def get_scan_from_index(self, index):
        return self.scan_overview.get_scan_values(index)

    def get_par_max_index(self, parameter, type):
        par_index = self.get_par_index(parameter, type)

        scan_shape = self.scan_overview.get_shape()
        return scan_shape[par_index] - 1

    def set_index(self, parameter, type, index):
        par_index = self.get_par_index(parameter, type)
        if index < 0 or index > self.get_par_max_index(parameter, type):
            raise IndexError("Given index outside of range of parameter")

        self.list_indicies[par_index] = index

    def make_dropdown_monitor(self):
        dropdown_monitor = widgets.Dropdown(
            value=self.monitor,
            options=self.get_monitor_list(),
            description='monitor'
        )

        dropdown_monitor.observe(self.update_monitor, "value")

        return dropdown_monitor

    def update_monitor(self, change):
        self.set_monitor(change.new)
        self.update_plot()

    def make_dropdown_run_name(self):
        dropdown_run_name = widgets.Dropdown(
            value=self.run_name,
            options=self.get_run_name_list(),
            description='run_name'
        )

        dropdown_run_name.observe(self.update_run_name, "value")

        return dropdown_run_name

    def update_run_name(self, change):
        self.set_run_name(change.new)
        self.update_plot()

    def make_dropdown_moderator(self):
        dropdown_moderator = widgets.Dropdown(
            value=self.moderator,
            options=self.get_moderator_list(),
            description='moderator'
        )

        dropdown_moderator.observe(self.update_moderator, "value")

        return dropdown_moderator

    def update_moderator(self, change):
        self.set_moderator(change.new)
        self.update_plot()

    def make_guide_checkboxes(self):
        guide_checkboxes = []
        for guide in self.get_guide_names():
            widget = widgets.Checkbox(value=True, description=guide, disabled=False, indent=True)
            guide_checkboxes.append(widget)

        for checkbox in guide_checkboxes:
            checkbox.observe(self.update_guide_selection, "value")

        return guide_checkboxes

    def update_guide_selection(self, change):
        if change.new:
            self.enable_guide(change["owner"].description)
        else:
            self.disable_guide(change["owner"].description)
        self.update_plot()

    def make_sample_scan_sliders(self):
        sample_sliders = []
        sample_labels = []
        full_sample_sliders = []
        self.sample_scan_sliders = {}
        self.sample_scan_labels = {}
        for sample_par in self.get_scanned_sample_parameters():
            max_index = self.get_par_max_index(sample_par, "sample")
            widget = widgets.IntSlider(value=0, min=0, max=max_index, step=1,
                                       description=sample_par, readout=False,
                                       layout=widgets.Layout(width="80%"))
            self.sample_scan_sliders[sample_par] = widget
            sample_sliders.append(widget)


            initial_value = self.get_scanned_sample_parameter_values(sample_par)[0]
            unit = self.get_scanned_sample_parameter_unit(sample_par)
            if unit is not None:
                value_string = str(initial_value) + " [" + str(unit) + "]"
            else:
                value_string = str(initial_value)

            widget_label = widgets.Label(value=value_string)
            sample_labels.append(widget_label)
            self.sample_scan_labels[sample_par] = widget_label

            full_sample_sliders.append(widgets.HBox([widget, widget_label]))

        for slider, label in zip(sample_sliders, sample_labels):
            slider.observe(self.update_scan_sample, "value")

        return full_sample_sliders

    def update_scan_sample(self, change):

        par_name = change.owner.description
        # Set the new index
        self.set_index(par_name, "sample", change.new)
        # Find new value of scan to show on label
        new_value = self.get_scanned_sample_parameter_values(par_name)[change.new]
        unit = self.get_scanned_sample_parameter_unit(par_name)
        if unit is not None:
            value_string = str(new_value) + " [" + str(unit) + "]"
        else:
            value_string = str(new_value)

        # Assign new value to the label
        self.sample_scan_labels[par_name].value = value_string
        # Update run names as this scanned variable may impact what runs are available
        current_run_name = self.dropdown_run_name.value
        new_options = tuple(self.get_run_name_list())

        self.dropdown_run_name.options = new_options
        if current_run_name in new_options:
            self.set_run_name(current_run_name)
            self.dropdown_run_name.value = current_run_name
        else:
            self.set_run_name(new_options[0])
            self.dropdown_run_name.value = new_options[0]

        self.update_plot()

    def make_moderator_scan_sliders(self):
        moderator_sliders = []
        moderator_labels = []
        full_moderator_sliders = []
        self.moderator_scan_sliders = {}
        self.moderator_scan_labels = {}
        for moderator_par in self.get_scanned_moderator_parameters():
            max_index = self.get_par_max_index(moderator_par, "moderator")
            widget = widgets.IntSlider(value=0, min=0, max=max_index, step=1,
                                       description=moderator_par, readout=False,
                                       layout=widgets.Layout(width="80%"))
            moderator_sliders.append(widget)
            self.moderator_scan_sliders[moderator_par] = widget

            initial_value = self.get_scanned_moderator_parameter_values(moderator_par)[0]
            unit = self.get_scanned_moderator_parameter_unit(moderator_par)
            if unit is not None:
                value_string = str(initial_value) + " [" + str(unit) + "]"
            else:
                value_string = str(initial_value)
            widget_label = widgets.Label(value=value_string)
            moderator_labels.append(widget_label)
            self.moderator_scan_labels[moderator_par] = widget_label

            full_moderator_sliders.append(widgets.HBox([widget, widget_label]))

        for slider, label in zip(moderator_sliders, moderator_labels):
            slider.observe(self.update_scan_moderator, "value")

        return full_moderator_sliders

    def update_scan_moderator(self, change):

        par_name = change.owner.description
        # Set the new index
        self.set_index(par_name, "moderator", change.new)
        # Find new value of scan to show on label
        new_value = self.get_scanned_moderator_parameter_values(par_name)[change.new]
        unit = self.get_scanned_moderator_parameter_unit(par_name)
        if unit is not None:
            value_string = str(new_value) + " [" + str(unit) + "]"
        else:
            value_string = str(new_value)

        # Assign new value to the label
        self.moderator_scan_labels[par_name].value = value_string
        # Update run names as this scanned variable may impact what runs are available
        self.dropdown_run_name.options = tuple(self.get_run_name_list())
        self.update_plot()


class CompareMonitors(BaseInterface):
    def __init__(self, scan_overview):
        super().__init__(scan_overview)

        self.fig = None
        self.ax = None

        self.show_interface()

        self.dropdown_monitor = None
        self.dropdown_run_name = None
        self.dropdown_moderator = None

        self.sample_scan_labels = None
        self.moderator_scan_labels = None

    def get_monitor_list(self):
        # Overwrite get_monitor_list to only allow 1D monitors
        shape = self.scan_overview.get_shape()
        indicies = tuple(self.list_indicies)
        guide = self.guide_names[0]
        moderator = self.get_moderator_list()[0]

        runs = self.scan_overview.data[guide][indicies][moderator].runs

        return runs[self.run_name].get_1D_monitor_list()

    def get_plot_data(self):

        indices = tuple(self.list_indicies)
        moderator = self.moderator
        run_name = self.run_name
        monitor = self.monitor

        plot_data = {}
        for guide in self.enabled_guides():
            if self.scan_overview.data[guide][indices][moderator] is not None:
                plot_data[guide] = self.scan_overview.data[guide][indices][moderator].runs[run_name].get_data(monitor)

        return plot_data

    def new_plot(self):

        self.fig, self.ax = plt.subplots()

        self.update_plot()

    def update_plot(self):

        plot_data = self.get_plot_data()

        self.ax.cla()
        for label in plot_data:
            data = plot_data[label]

            xaxis = data.xaxis
            intensity = data.Intensity

            self.ax.plot(xaxis, intensity, label=label)
            self.ax.set_xlabel(data.metadata.xlabel)
            self.ax.set_ylabel(data.metadata.ylabel)

            self.ax.legend()

    def show_interface(self):
        output = widgets.Output()

        # default line color
        initial_color = '#FF00DD'

        with output:
            # fig, ax = plt.subplots(constrained_layout=True, figsize=(6, 4))
            self.new_plot()

        # move the toolbar to the bottom
        self.fig.canvas.toolbar_position = 'bottom'
        self.ax.grid(True)

        control_widgets = []
        # Place control widgets
        control_widgets += [widgets.Label(value="Data source")]

        self.dropdown_monitor = self.make_dropdown_monitor()
        control_widgets.append(self.dropdown_monitor)

        self.dropdown_run_name = self.make_dropdown_run_name()
        control_widgets.append(self.dropdown_run_name)

        self.dropdown_moderator = self.make_dropdown_moderator()
        control_widgets.append(self.dropdown_moderator)

        if len(self.get_scanned_sample_parameters()) > 0:
            control_widgets += [widgets.Label(value="Scanned sample parameters")]
            control_widgets += self.make_sample_scan_sliders()

        if len(self.get_scanned_moderator_parameters()) > 0:
            control_widgets += [widgets.Label(value="Scanned moderator parameters")]
            control_widgets += self.make_moderator_scan_sliders()

        control_widgets += [widgets.Label(value="Guide selection")]

        guide_checkboxes = self.make_guide_checkboxes()
        control_widgets += guide_checkboxes

        controls = widgets.VBox(control_widgets)
        return widgets.HBox([controls, output])


class CompareMonitorsScan(BaseInterface):
    def __init__(self, scan_overview):
        super().__init__(scan_overview)

        self.fig = None
        self.ax = None

        #self.show_interface()

        self.dropdown_monitor = None
        self.dropdown_run_name = None
        self.dropdown_moderator = None

        self.sample_scan_labels = None
        self.moderator_scan_labels = None

        self.selected_guide = self.get_guide_names()[0]

        self.scan_par = None
        self.target = None

        sample_scan = self.get_scanned_sample_parameters()
        if len(sample_scan) > 0:
            self.target = "sample"
            self.scan_par = sample_scan[0]
            self.unit = self.get_scanned_sample_parameter_unit(self.scan_par)

        mod_scan = self.get_scanned_moderator_parameters()
        if len(mod_scan) > 0:
            self.target = "moderator"
            self.scan_par = mod_scan[0]
            self.unit = self.get_scanned_moderator_parameter_unit(self.scan_par)

    def set_guide(self, guide):
        if guide not in self.get_guide_names():
            raise KeyError("Need to select a guide available in the dataset!")

        self.selected_guide = guide

    def make_guide_selector(self):

        widget = widgets.RadioButtons(options=self.get_guide_names(),
                                      #description="guide choices",
                                      disabled=False, indent=True)

        widget.observe(self.update_guide_selector, "value")

        return widget

    def update_guide_selector(self, change):
        self.set_guide(change.new)
        self.update_plot()

    def set_scanned_par(self, par_name, target):

        if target not in ["sample", "moderator"]:
            raise KeyError("Target has to be either sample or moderator")

        self.target = target

        if target == "sample":
            if par_name not in self.get_scanned_sample_parameters():
                raise KeyError("Parameter not recognized in sample scan")
            self.scan_par = par_name
            self.unit = self.get_scanned_sample_parameter_unit(self.scan_par)

            if len(self.sample_scan_sliders) > 0:
                self.unlock_all_sliders()
                locked_slider = self.sample_scan_sliders[par_name]
                locked_slider.disabled = True

        elif target == "moderator":
            if par_name not in self.get_scanned_moderator_parameters():
                raise KeyError("Parameter not recognized in moderator scan")
            self.scan_par = par_name
            self.unit = self.get_scanned_moderator_parameter_unit(self.scan_par)

            if len(self.moderator_scan_sliders) > 0:
                self.unlock_all_sliders()
                locked_slider = self.moderator_scan_sliders[par_name]
                locked_slider.disabled = True

    def unlock_all_sliders(self):
        for key in self.sample_scan_sliders:
            self.sample_scan_sliders[key].disabled = False
        for key in self.moderator_scan_sliders:
            self.moderator_scan_sliders[key].disabled = False

    def make_dropdown_scan_par(self):

        sample_scan = self.get_scanned_sample_parameters()
        mod_scan = self.get_scanned_moderator_parameters()

        option_list = []
        self.option_to_par_and_target = {}
        for par_name in sample_scan:
            original_par_name = par_name
            par_name = "sample: " + par_name
            self.option_to_par_and_target[par_name] = (original_par_name, "sample")
            option_list.append(par_name)
            if self.target == "sample":
                if self.scan_par == original_par_name:
                    initial_value = par_name

        for par_name in mod_scan:
            original_par_name = par_name
            par_name = "moderator: " + par_name
            self.option_to_par_and_target[par_name] = (original_par_name, "moderator")
            option_list.append(par_name)
            if self.target == "moderator":
                if self.scan_par == original_par_name:
                    initial_value = par_name

        dropdown_scan_par = widgets.Dropdown(
            value=initial_value,
            options=option_list,
            description=''
        )

        dropdown_scan_par.observe(self.update_scan_par, "value")

        return dropdown_scan_par

    def update_scan_par(self, change):
        par_name, target = self.option_to_par_and_target[change.new]
        self.set_scanned_par(par_name, target)

        self.update_plot()

    def get_monitor_list(self):
        # Overwrite get_monitor_list to only allow 1D monitors
        shape = self.scan_overview.get_shape()
        indicies = tuple(self.list_indicies)
        guide = self.guide_names[0]
        moderator = self.get_moderator_list()[0]

        runs = self.scan_overview.data[guide][indicies][moderator].runs

        return runs[self.run_name].get_1D_monitor_list()

    def get_plot_data(self):

        par_index = self.get_par_index(self.scan_par, self.target)
        par_values = self.get_scan_from_index(par_index)

        base_indices = self.list_indicies
        moderator = self.moderator
        run_name = self.run_name
        monitor = self.monitor
        guide = self.selected_guide

        plot_data = OrderedDict()
        for scan_index, par_value in zip(range(len(par_values)), par_values):
            indices = copy.copy(base_indices)
            indices[par_index] = scan_index
            indices = tuple(indices)

            label = self.target + " " +  self.scan_par  + " = " + str(par_value) + " " + self.unit

            if self.scan_overview.data[guide][indices][moderator] is not None:
                plot_data[label] = self.scan_overview.data[guide][indices][moderator].runs[run_name].get_data(monitor)

        return plot_data

    def new_plot(self):

        self.fig, self.ax = plt.subplots()

        self.update_plot()

    def update_plot(self):

        plot_data = self.get_plot_data()

        self.ax.cla()
        for label in reversed(plot_data):
            data = plot_data[label]

            xaxis = data.xaxis
            intensity = data.Intensity

            self.ax.plot(xaxis, intensity, label=label)
            self.ax.set_xlabel(data.metadata.xlabel)
            self.ax.set_ylabel(data.metadata.ylabel)

            self.ax.legend()

    def show_interface(self):
        output = widgets.Output()

        # default line color
        initial_color = '#FF00DD'

        with output:
            # fig, ax = plt.subplots(constrained_layout=True, figsize=(6, 4))
            self.new_plot()

        # move the toolbar to the bottom
        self.fig.canvas.toolbar_position = 'bottom'
        self.ax.grid(True)

        control_widgets = []
        # Place control widgets
        control_widgets += [widgets.Label(value="Data source")]

        self.dropdown_monitor = self.make_dropdown_monitor()
        control_widgets.append(self.dropdown_monitor)

        self.dropdown_run_name = self.make_dropdown_run_name()
        control_widgets.append(self.dropdown_run_name)

        self.dropdown_moderator = self.make_dropdown_moderator()
        control_widgets.append(self.dropdown_moderator)

        control_widgets += [widgets.Label(value="Scan parameter to plot")]

        self.dropdown_scan_par = self.make_dropdown_scan_par()
        control_widgets.append(self.dropdown_scan_par)

        if len(self.get_scanned_sample_parameters()) > 0:
            control_widgets += [widgets.Label(value="Scanned sample parameters")]
            self.sample_sliders = self.make_sample_scan_sliders()
            control_widgets += self.sample_sliders

        if len(self.get_scanned_moderator_parameters()) > 0:
            control_widgets += [widgets.Label(value="Scanned moderator parameters")]
            self.moderator_sliders = self.make_moderator_scan_sliders()
            control_widgets += self.moderator_sliders

        self.set_scanned_par(self.scan_par, self.target)  # locks slider corresponding to plotted parameter

        control_widgets += [widgets.Label(value="Guide selection")]

        control_widgets.append(self.make_guide_selector())

        controls = widgets.VBox(control_widgets)
        return widgets.HBox([controls, output])


class PlotAnyMonitor(BaseInterface):
    def __init__(self, scan_overview):
        super().__init__(scan_overview)

        self.fig = None
        self.ax = None
        self.colorbar_ax = None

        self.dropdown_monitor = None
        self.dropdown_run_name = None
        self.dropdown_moderator = None

        self.sample_scan_labels = None
        self.moderator_scan_labels = None

        self.selected_guide = self.get_guide_names()[0]


    def set_guide(self, guide):

        if guide not in self.get_guide_names():
            raise KeyError("Need to select a guide available in the dataset!")

        self.selected_guide = guide

    def make_guide_selector(self):

        widget = widgets.RadioButtons(options=self.get_guide_names(),
                                      #description="guide choices",
                                      disabled=False, indent=True)

        widget.observe(self.update_guide_selector, "value")

        return widget

    def update_guide_selector(self, change):
        self.set_guide(change.new)
        self.update_plot()

    def get_plot_data(self):

        guide = self.selected_guide
        indices = tuple(self.list_indicies)
        moderator = self.moderator
        run_name = self.run_name
        monitor = self.monitor

        if self.scan_overview.data[guide][indices][moderator] is not None:
            return self.scan_overview.data[guide][indices][moderator].runs[run_name].get_data(monitor)
        else:
            return None

    def new_plot(self):

        self.fig, (self.ax, self.colorbar_ax) = plt.subplots(ncols=2, gridspec_kw={'width_ratios': [4, 1]})

        self.update_plot()

    def update_plot(self):

        plot_data = self.get_plot_data()

        self.ax.cla()
        # self.ax.xaxis.set_ticks([])
        # self.ax.yaxis.set_ticks([])
        self.colorbar_ax.cla()
        self.colorbar_ax.xaxis.set_ticks([])
        self.colorbar_ax.yaxis.set_ticks([])
        self.colorbar_ax.axis("off")

        if plot_data is None:
            self.ax.text(0.4,0.5, "No data available")
            return

        #print(self.ax.get_position())
        #print(self.original_ax_position)
        #self.ax.set_position(list(self.original_ax_position))

        plot_data.set_plot_options(show_colorbar=True)
        with HiddenPrints():
            plotter._plot_fig_ax(plot_data, self.fig, self.ax, colorbar_axes=self.colorbar_ax)

        if self.colorbar_ax.has_data():
            self.colorbar_ax.axis("on")
            self.ax.grid(False)
        else:
            self.ax.grid(True)

        self.colorbar_ax.set_aspect(20)

        plt.tight_layout()

    def show_interface(self):
        output = widgets.Output()

        # default line color
        initial_color = '#FF00DD'

        with output:
            # fig, ax = plt.subplots(constrained_layout=True, figsize=(6, 4))
            self.new_plot()

        # move the toolbar to the bottom
        self.fig.canvas.toolbar_position = 'bottom'
        #self.ax.grid(True)

        control_widgets = []
        # Place control widgets
        control_widgets += [widgets.Label(value="Data source")]

        self.dropdown_monitor = self.make_dropdown_monitor()
        control_widgets.append(self.dropdown_monitor)

        self.dropdown_run_name = self.make_dropdown_run_name()
        control_widgets.append(self.dropdown_run_name)

        self.dropdown_moderator = self.make_dropdown_moderator()
        control_widgets.append(self.dropdown_moderator)

        if len(self.get_scanned_sample_parameters()) > 0:
            control_widgets += [widgets.Label(value="Scanned sample parameters")]
            control_widgets += self.make_sample_scan_sliders()

        if len(self.get_scanned_moderator_parameters()) > 0:
            control_widgets += [widgets.Label(value="Scanned moderator parameters")]
            control_widgets += self.make_moderator_scan_sliders()

        control_widgets += [widgets.Label(value="Guide selection")]

        control_widgets.append(self.make_guide_selector())

        controls = widgets.VBox(control_widgets)
        return widgets.HBox([controls, output])


class PlotSum(BaseInterface):
    def __init__(self, scan_overview):
        super().__init__(scan_overview)

        self.fig = None
        self.ax = None

        self.dropdown_monitor = None
        self.dropdown_run_name = None
        self.dropdown_moderator = None

        self.sample_scan_labels = None
        self.moderator_scan_labels = None

        self.option_to_par_and_target = None
        self.dropdown_scan_par = None

        self.sample_sliders = None
        self.moderator_sliders = None

        self.scan_par = None
        self.target = None

        sample_scan = self.get_scanned_sample_parameters()
        if len(sample_scan) > 0:
            self.target = "sample"
            self.scan_par = sample_scan[0]
            self.unit = self.get_scanned_sample_parameter_unit(self.scan_par)

        mod_scan = self.get_scanned_moderator_parameters()
        if len(mod_scan) > 0:
            self.target = "moderator"
            self.scan_par = mod_scan[0]
            self.unit = self.get_scanned_moderator_parameter_unit(self.scan_par)

    def get_plot_data(self):

        par_index = self.get_par_index(self.scan_par, self.target)
        par_values = self.get_scan_from_index(par_index)

        base_indices = self.list_indicies
        moderator = self.moderator
        run_name = self.run_name
        monitor = self.monitor

        plot_data = {}
        for guide in self.enabled_guides():

            data = []
            scan_values = []
            for scan_index, par_value in zip(range(len(par_values)), par_values):
                indices = copy.copy(base_indices)
                indices[par_index] = scan_index
                indices = tuple(indices)

                if self.scan_overview.data[guide][indices][moderator] is not None:
                    #intensity = self.scan_overview.data[guide][indices][moderator].runs[run_name].get_sum_data(monitor)
                    intensity = self.scan_overview.data[guide][indices][moderator].runs[run_name].get_average_data(monitor)
                else:
                    intensity = None

                if intensity is not None:
                    scan_values.append(par_value)
                    data.append(intensity)


            plot_data[guide] = (scan_values, data)

        return plot_data

    def new_plot(self):

        self.fig, self.ax = plt.subplots()

        self.update_plot()

    def update_plot(self):
        plot_data = self.get_plot_data()

        self.ax.cla()
        for label in plot_data:
            scan_values, data = plot_data[label]

            self.ax.plot(scan_values, data, "-o", label=label)
            xlabel = self.scan_par
            if self.unit is not None:
                xlabel += " [" + str(self.unit) + "]"
            self.ax.set_xlabel(xlabel)
            self.ax.set_ylabel("average intensity")

            self.ax.legend()

        self.ax.grid(True)
        plt.tight_layout()

    def set_scanned_par(self, par_name, target):

        if target not in ["sample", "moderator"]:
            raise KeyError("Target has to be either sample or moderator")

        self.target = target

        if target == "sample":
            if par_name not in self.get_scanned_sample_parameters():
                raise KeyError("Parameter not recognized in sample scan")
            self.scan_par = par_name
            self.unit = self.get_scanned_sample_parameter_unit(self.scan_par)

            if len(self.sample_scan_sliders) > 0:
                self.unlock_all_sliders()
                locked_slider = self.sample_scan_sliders[par_name]
                locked_slider.disabled = True

        elif target == "moderator":
            if par_name not in self.get_scanned_moderator_parameters():
                raise KeyError("Parameter not recognized in moderator scan")
            self.scan_par = par_name
            self.unit = self.get_scanned_moderator_parameter_unit(self.scan_par)

            if len(self.moderator_scan_sliders) > 0:
                self.unlock_all_sliders()
                locked_slider = self.moderator_scan_sliders[par_name]
                locked_slider.disabled = True

    def unlock_all_sliders(self):
        for key in self.sample_scan_sliders:
            self.sample_scan_sliders[key].disabled = False
        for key in self.moderator_scan_sliders:
            self.moderator_scan_sliders[key].disabled = False

    def make_dropdown_scan_par(self):

        sample_scan = self.get_scanned_sample_parameters()
        mod_scan = self.get_scanned_moderator_parameters()

        option_list = []
        self.option_to_par_and_target = {}
        for par_name in sample_scan:
            original_par_name = par_name
            par_name = "sample: " + par_name
            self.option_to_par_and_target[par_name] = (original_par_name, "sample")
            option_list.append(par_name)
            if self.target == "sample":
                if self.scan_par == original_par_name:
                    initial_value = par_name

        for par_name in mod_scan:
            original_par_name = par_name
            par_name = "moderator: " + par_name
            self.option_to_par_and_target[par_name] = (original_par_name, "moderator")
            option_list.append(par_name)
            if self.target == "moderator":
                if self.scan_par == original_par_name:
                    initial_value = par_name

        dropdown_scan_par = widgets.Dropdown(
            value=initial_value,
            options=option_list,
            description=''
        )

        dropdown_scan_par.observe(self.update_scan_par, "value")

        return dropdown_scan_par

    def update_scan_par(self, change):
        par_name, target = self.option_to_par_and_target[change.new]
        self.set_scanned_par(par_name, target)

        self.update_plot()

    def show_interface(self):
        output = widgets.Output()

        # default line color
        initial_color = '#FF00DD'

        with output:
            # fig, ax = plt.subplots(constrained_layout=True, figsize=(6, 4))
            self.new_plot()

        # move the toolbar to the bottom
        self.fig.canvas.toolbar_position = 'bottom'
        self.ax.grid(True)

        control_widgets = []
        # Place control widgets
        control_widgets += [widgets.Label(value="Data source")]

        self.dropdown_monitor = self.make_dropdown_monitor()
        control_widgets.append(self.dropdown_monitor)

        self.dropdown_run_name = self.make_dropdown_run_name()
        control_widgets.append(self.dropdown_run_name)

        self.dropdown_moderator = self.make_dropdown_moderator()
        control_widgets.append(self.dropdown_moderator)

        control_widgets += [widgets.Label(value="Scan parameter to plot")]

        self.dropdown_scan_par = self.make_dropdown_scan_par()
        control_widgets.append(self.dropdown_scan_par)

        if len(self.get_scanned_sample_parameters()) > 0:
            control_widgets += [widgets.Label(value="Scanned sample parameters")]
            self.sample_sliders = self.make_sample_scan_sliders()
            control_widgets += self.sample_sliders

        if len(self.get_scanned_moderator_parameters()) > 0:
            control_widgets += [widgets.Label(value="Scanned moderator parameters")]
            self.moderator_sliders = self.make_moderator_scan_sliders()
            control_widgets += self.moderator_sliders

        self.set_scanned_par(self.scan_par, self.target) # locks slider corresponding to plotted parameter

        control_widgets += [widgets.Label(value="Guide selection")]

        guide_checkboxes = self.make_guide_checkboxes()
        control_widgets += guide_checkboxes

        controls = widgets.VBox(control_widgets)
        return widgets.HBox([controls, output])