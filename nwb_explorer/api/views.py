from django.conf import settings
from pygeppetto.model.model_serializer import GeppettoModelSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from ..nwb_model_interpreter import NWBModelInterpreter
from ..plots_controller import PlotsController

geppetto_model = None
nwb_utils = None

# curl -X POST http://localhost:8000/api/load
@api_view(['GET','POST'])
@permission_classes((AllowAny, ))
def load(request):
    if request.method == 'GET':

        model_interpreter = NWBModelInterpreter()
        geppetto_model, nwbfile = model_interpreter.importType('./test_data/brain_observatory.nwb','','','')
        serialized_model = GeppettoModelSerializer().serialize(geppetto_model)

        # Todo: serialise and store geppetto model and nwb_file in session (temporary stored in settings)
        settings.GEPPETTO_MODEL = geppetto_model
        settings.NWB_FILE = nwbfile

        return Response(serialized_model)
    elif request.method == 'POST':
        return Response("Post model")

# Todo - Review: Both plot and plots_available assumes that load happens first. Should we do something to force that behaviour?

# curl -X POST http://localhost:8000/api/plot
@api_view(['GET','POST'])
@permission_classes((AllowAny, ))
def plot(request):
    if request.method == 'GET':
        plot_id = request.GET.get('plot')
        geppetto_model = settings.GEPPETTO_MODEL
        plot_controller = PlotsController(geppetto_model)
        return Response(plot_controller.plot(plot_id))
    elif request.method == 'POST':
        return Response("Post Response")

# curl -X POST http://localhost:8000/api/plots_available
@api_view(['GET','POST'])
@permission_classes((AllowAny, ))
def plots_available(request):
    if request.method == 'GET':
        geppetto_model = settings.GEPPETTO_MODEL
        nwbfile = settings.NWB_FILE
        plot_controller = PlotsController(geppetto_model)
        return Response(plot_controller.get_available_plots(nwbfile))
    elif request.method == 'POST':
        return Response("Post Response")


