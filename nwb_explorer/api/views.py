from django.conf import settings
from pygeppetto.model.model_serializer import GeppettoModelSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from ..nwb_model_interpreter import NWBModelInterpreter
from ..plots_controller import PlotsController
import json

geppetto_model = None
nwb_utils = None


# curl -X POST http://localhost:8000/api/load
@api_view(['GET', 'POST'])
@permission_classes((AllowAny,))
def load(request):
    if request.method == 'GET':
        nwbfile = request.GET.get('nwbfile')
        if nwbfile is not None:
            model_interpreter = NWBModelInterpreter()
            geppetto_model = model_interpreter.importType(nwbfile, '', '', '')
            serialized_model = GeppettoModelSerializer().serialize(geppetto_model)
            request.session['geppetto_model'] = serialized_model
            request.session['nwbfile'] = nwbfile
        else:
            serialized_model = None
            print("nwbfile not found")
        return Response(serialized_model)
    elif request.method == 'POST':
        return Response("Post model")


# curl -X POST http://localhost:8000/api/plot
@api_view(['GET', 'POST'])
@permission_classes((AllowAny,))
def plot(request):
    if request.method == 'GET':
        plot_id = request.GET.get('plot')
        serialized_model = request.session.get('geppetto_model')
        if serialized_model is not None:
            geppetto_model = json.loads(serialized_model)  # Todo - Review: Is there a better way to deserialize?
        else:
            geppetto_model = None
            print("Geppetto Model not in session")
        nwbfile = request.session.get('nwbfile')
        plot_controller = PlotsController(geppetto_model)
        return Response(plot_controller.plot(plot_id, nwbfile))
    elif request.method == 'POST':
        return Response("Post Response")


# curl -X POST http://localhost:8000/api/plots_available
@api_view(['GET', 'POST'])
@permission_classes((AllowAny,))
def plots_available(request):
    if request.method == 'GET':
        serialized_model = request.session.get('geppetto_model')
        if serialized_model is not None:
            geppetto_model = json.loads(serialized_model)
        else:
            geppetto_model = None
            print("Geppetto Model not in session")
        nwbfile = request.session.get('nwbfile')
        plot_controller = PlotsController(geppetto_model)
        return Response(plot_controller.get_available_plots(nwbfile))
    elif request.method == 'POST':
        return Response("Post Response")
