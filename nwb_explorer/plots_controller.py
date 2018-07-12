"""
netpyne_model_interpreter.py
Model interpreter for NWB. This class creates a geppetto type
"""
import importlib
import json
from os import listdir, path

import holoviews as hv
import pygeppetto.ui
import seaborn as sns

from nwb_explorer.utils.nwb_utils import NWBUtils

hv.extension('bokeh')
sns.set_style('whitegrid')


class PlotsController:
    holoviews_plots_path = "static/org.geppetto.frontend/src/main/webapp/extensions/geppetto-nwbexplorer/holoviews_plots/"
    public_plots_path = "nwb_explorer/public/plots"
    public_plots_dict = {}

    def __init__(self, geppetto_model=None):
        self.geppetto_model = geppetto_model

    # def get_nearest_frame(self, timepoint, timestamps):
    #     return None  # int(np.nanargmin(abs(timestamps - timepoint)))
    #
    # def get_trace_around_timepoint(self, timepoint, trace, timestamps, window=1, frame_rate=30):
    #     frame_for_timepoint = self.get_nearest_frame(timepoint, timestamps)
    #     lower_frame = frame_for_timepoint - (window * frame_rate)
    #     upper_frame = frame_for_timepoint + (window * frame_rate)
    #     trace = trace[lower_frame:upper_frame]
    #     timepoints = timestamps[lower_frame:upper_frame]
    #     return trace, timepoints
    #
    # def get_xticks_xticklabels(self, trace, interval_sec=1):
    #     interval_frames = interval_sec * 30
    #     n_frames = len(trace)
    #     n_sec = n_frames / 30
    #     xticks = np.arange(0, n_frames + 1, interval_frames)
    #     xticklabels = np.arange(0, n_sec + 0.1, interval_sec)
    #     xticklabels = xticklabels - n_sec / 2
    #     return xticks, xticklabels
    #
    # def plot_mean_trace(self, traces, label=None, color='k', interval_sec=1, ax=None):
    #     if ax is None:
    #         fig, ax = plt.subplots()
    #     if len(traces) > 0:
    #         trace = np.mean(traces, axis=0)
    #         times = np.arange(0, len(trace), 1)
    #         sem = (traces.std()) / np.sqrt(float(len(traces)))
    #         ax.plot(trace, label=label, linewidth=3, color=color)
    #         ax.fill_between(times, trace + sem, trace - sem, alpha=0.5, color=color)
    #
    #         xticks, xticklabels = self.get_xticks_xticklabels(trace, interval_sec)
    #         ax.set_xticks([int(x) for x in xticks])
    #         ax.set_xticklabels([int(x) for x in xticklabels])
    #         ax.set_xlabel('time after change (s)')
    #         ax.set_ylabel('dF/F')
    #     sns.despine(ax=ax)
    #     return ax
    #
    # def plot_mean(self):
    #     cell = 17
    #     cell_trace = dataset.dff_traces[cell]
    #     timestamps = dataset.timestamps_2p
    #     flashes = dataset.flashes[:-1]  # avoid issues with truncated last flash
    #
    #     fig, ax = plt.subplots()
    #     colors = sns.color_palette('hls', 8)
    #     for i, image_name in enumerate(np.sort(flashes.image_name.unique())):
    #         flash_times = flashes[flashes.image_name == image_name].master_time
    #
    #         traces = []
    #         window = 1  # seconds around flash time to take trace snippet
    #         for flash_time in flash_times:
    #             trace, timepoints = self.get_trace_around_timepoint(flash_time, cell_trace, timestamps, window)
    #             traces.append(trace)
    #         traces = np.asarray(traces)
    #
    #         self.plot_mean_trace(traces, label=image_name, color=colors[i], interval_sec=1, ax=ax)
    #         ax.set_title('roi ' + str(cell))
    #
    #     plt.legend(bbox_to_anchor=(1., 1))
    #     return plt

    def plot(self, plot_id):
        """Given a valid plot_id dynamically imports the module and calls the method responsible for plotting """
        plot_path = self.public_plots_dict[plot_id]
        try:
            imported_module = importlib.import_module(plot_path)
            method_to_call = getattr(imported_module, plot_id)
            plot = method_to_call()  # Todo: Pass the requirements
        except ImportError:
            empty_data = {'url': ''}
            return json.dumps(empty_data)
        data = pygeppetto.ui.get_url(plot, self.holoviews_plots_path)
        return json.dumps(data)

    def get_available_plots(self, nwbfile):
        """Given a nwbfile looks under public_plots_path to verify which plots can be draw """
        try:
            nwb_utils = NWBUtils(nwbfile)
        except ValueError:
            return json.dumps([])
        plots = self._get_public_plots()
        available_plots = [{'name': plot['name'], 'id': plot['id']} for plot in plots if
                           nwb_utils.has_all_requirements(plot["requirements"])]
        return json.dumps(available_plots)

    def _get_public_plots(
            self):  # Todo - Review: We probably just need to call this once an save the result somewhere, what do you think?
        """Looks under public_plots_path and expects to find folders containing each one
        2 files with the same base name as the first; one a json file containing name, id and requirements as fields
        and other a python module where the method's name responsible to return the plot should be the same
        as the id in the json file """
        plots = []
        for folder in listdir(
                self.public_plots_path):
            json_filepath = self.public_plots_path + "/" + folder + "/" + folder + ".json"
            python_filepath = self.public_plots_path.replace('/', '.') + "." + folder + "." + folder
            if path.isfile(json_filepath):
                with open(json_filepath) as file:
                    data = json.load(file)
                    self.public_plots_dict[data["id"]] = python_filepath
                    plots.append(data)
        return plots
