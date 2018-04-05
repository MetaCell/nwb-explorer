from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
import logging
import model as pygeppetto
from ..nwb_model_interpreter import NWBModelInterpreter
from model.model_serializer import GeppettoModelSerializer

geppetto_model = None

#curl -X POST http://localhost:8000/api/load
@api_view(['GET','POST'])
@permission_classes((AllowAny, ))
def load(request):
    if request.method == 'GET':

        model_interpreter = NWBModelInterpreter()
        geppetto_model = model_interpreter.importType('./test_data/ophys_672584839.nwb','','','')
        serialized_model = GeppettoModelSerializer().serialize(geppetto_model)
        return Response(serialized_model)
    elif request.method == 'POST':
        return Response("Post model")

#curl -X POST http://localhost:8000/api/plot
@api_view(['GET','POST'])
@permission_classes((AllowAny, ))
def plot(request):
    if request.method == 'GET':
        return Response(plotMean(geppetto_model))
    elif request.method == 'POST':
        return Response("Post model")

def get_nearest_frame(timepoint, timestamps):
    return None#int(np.nanargmin(abs(timestamps - timepoint)))

def get_trace_around_timepoint(timepoint, trace, timestamps, window=1, frame_rate=30):
    frame_for_timepoint = get_nearest_frame(timepoint, timestamps)
    lower_frame = frame_for_timepoint - (window*frame_rate)
    upper_frame = frame_for_timepoint + (window*frame_rate)
    trace = trace[lower_frame:upper_frame]
    timepoints = timestamps[lower_frame:upper_frame]
    return trace, timepoints

def get_xticks_xticklabels(trace, interval_sec=1):
    interval_frames = interval_sec * 30
    n_frames = len(trace)
    n_sec = n_frames / 30
    xticks = np.arange(0, n_frames + 1, interval_frames)
    xticklabels = np.arange(0, n_sec + 0.1, interval_sec)
    xticklabels = xticklabels - n_sec / 2
    return xticks, xticklabels

def plot_mean_trace(traces,label=None,color='k',interval_sec=1,ax=None):
    if ax is None:
        fig,ax = plt.subplots()
    if len(traces) > 0:
        trace = np.mean(traces,axis=0)
        times = np.arange(0, len(trace), 1)
        sem = (traces.std()) / np.sqrt(float(len(traces)))
        ax.plot(trace, label=label, linewidth=3, color=color)
        ax.fill_between(times, trace + sem, trace - sem, alpha=0.5, color=color)

        xticks, xticklabels = get_xticks_xticklabels(trace, interval_sec)
        ax.set_xticks([int(x) for x in xticks]);
        ax.set_xticklabels([int(x) for x in xticklabels]);
        ax.set_xlabel('time after change (s)')
        ax.set_ylabel('dF/F')
    sns.despine(ax=ax)
    return ax

def plotMean():
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
            trace, timepoints = get_trace_around_timepoint(flash_time, cell_trace, timestamps, window)
            traces.append(trace)
        traces = np.asarray(traces)

        plot_mean_trace(traces,label=image_name,color=colors[i],interval_sec=1,ax=ax)
        ax.set_title('roi '+str(cell))
        
    plt.legend(bbox_to_anchor=(1.,1))
    return plt