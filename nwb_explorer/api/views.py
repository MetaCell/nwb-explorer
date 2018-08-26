from django.http import HttpResponseBadRequest, HttpResponseNotFound
from pygeppetto.model.model_serializer import GeppettoModelSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from ..nwb_model_interpreter import NWBModelInterpreter
from ..plots_controller import PlotsController

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
            try:
                geppetto_model = model_interpreter.importType(nwbfile, '', '', '')
            except ValueError:
                return HttpResponseNotFound("File not found")
            serialized_model = GeppettoModelSerializer().serialize(geppetto_model)
            request.session['geppetto_model'] = serialized_model
            request.session['nwbfile'] = nwbfile
            return Response(serialized_model)
        else:
            return HttpResponseBadRequest("File path missing")
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
            geppetto_model = GeppettoModelSerializer().deserialize(serialized_model)
        else:
            return HttpResponseBadRequest("Geppetto Model not in session")
        plot_controller = PlotsController(geppetto_model)
        nwbfile = request.session.get('nwbfile')
        if nwbfile is None:
            return HttpResponseBadRequest("Nwbfile not in session")
        try:
            return Response(plot_controller.plot(plot_id, nwbfile))
        except Exception as e:
            return HttpResponseBadRequest(e)
    elif request.method == 'POST':
        return Response("Post Response")


# curl -X POST http://localhost:8000/api/plots_available
@api_view(['GET', 'POST'])
@permission_classes((AllowAny,))
def plots_available(request):
    if request.method == 'GET':
        serialized_model = request.session.get('geppetto_model')
        if serialized_model is not None:
            geppetto_model = GeppettoModelSerializer().deserialize(serialized_model)
        else:
            return HttpResponseBadRequest("Geppetto Model not in session")
        plot_controller = PlotsController(geppetto_model)
        nwbfile = request.session.get('nwbfile')
        if nwbfile is None:
            return HttpResponseBadRequest("Nwbfile not in session")
        try:
            return Response(plot_controller.get_available_plots(nwbfile))
        except Exception as e:
            return HttpResponseBadRequest(e)
    elif request.method == 'POST':
        return Response("Post Response")
