"""
netpyne_model_interpreter.py
Model interpreter for NWB. This class creates a geppetto type
"""
import logging
import model as pygeppetto
from model.services.model_interpreter import ModelInterpreter
from model.model_factory import GeppettoModelFactory
from model.values import Point, ArrayElement, ArrayValue
from model.variables import Variable
import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')


class PlotsController():

    def __init__(self, geppetto_model):
        self.geppetto_model = geppetto_model

    def get_nearest_frame(self, timepoint, timestamps):
        return None#int(np.nanargmin(abs(timestamps - timepoint)))

    def get_trace_around_timepoint(self, timepoint, trace, timestamps, window=1, frame_rate=30):
        frame_for_timepoint = self.get_nearest_frame(timepoint, timestamps)
        lower_frame = frame_for_timepoint - (window*frame_rate)
        upper_frame = frame_for_timepoint + (window*frame_rate)
        trace = trace[lower_frame:upper_frame]
        timepoints = timestamps[lower_frame:upper_frame]
        return trace, timepoints

    def get_xticks_xticklabels(self, trace, interval_sec=1):
        interval_frames = interval_sec * 30
        n_frames = len(trace)
        n_sec = n_frames / 30
        xticks = np.arange(0, n_frames + 1, interval_frames)
        xticklabels = np.arange(0, n_sec + 0.1, interval_sec)
        xticklabels = xticklabels - n_sec / 2
        return xticks, xticklabels

    def plot_mean_trace(self, traces,label=None,color='k',interval_sec=1,ax=None):
        if ax is None:
            fig,ax = plt.subplots()
        if len(traces) > 0:
            trace = np.mean(traces,axis=0)
            times = np.arange(0, len(trace), 1)
            sem = (traces.std()) / np.sqrt(float(len(traces)))
            ax.plot(trace, label=label, linewidth=3, color=color)
            ax.fill_between(times, trace + sem, trace - sem, alpha=0.5, color=color)

            xticks, xticklabels = self.get_xticks_xticklabels(trace, interval_sec)
            ax.set_xticks([int(x) for x in xticks]);
            ax.set_xticklabels([int(x) for x in xticklabels]);
            ax.set_xlabel('time after change (s)')
            ax.set_ylabel('dF/F')
        sns.despine(ax=ax)
        return ax

    def plot_mean(self):
        cell = 17
        cell_trace = dataset.dff_traces[cell]
        timestamps = dataset.timestamps_2p
        flashes = dataset.flashes[:-1] #avoid issues with truncated last flash

        fig,ax = plt.subplots()
        colors = sns.color_palette('hls',8)
        for i,image_name in enumerate(np.sort(flashes.image_name.unique())):
            flash_times = flashes[flashes.image_name==image_name].master_time

            traces = []
            window = 1 #seconds around flash time to take trace snippet
            for flash_time in flash_times: 
                trace, timepoints = self.get_trace_around_timepoint(flash_time, cell_trace, timestamps, window)
                traces.append(trace)
            traces = np.asarray(traces)

            self.plot_mean_trace(traces,label=image_name,color=colors[i],interval_sec=1,ax=ax)
            ax.set_title('roi '+str(cell))
            
        plt.legend(bbox_to_anchor=(1.,1))
        return plt