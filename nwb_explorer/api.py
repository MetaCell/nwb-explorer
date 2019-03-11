
from pygeppetto.model.model_serializer import GeppettoModelSerializer
from jupyter_geppetto.webapi import get, RouteManager

from nwb_explorer.nwb_model_interpreter import NWBModelInterpreter
from nwb_explorer.plots_manager import PlotManager
from nwb_explorer.utils import get_file_from_url
import logging

cache_model = False

# TODO this is still a really distant relative of the RuntimeProject in the Java backend. Remove when a sensible implementation of the flow is available on pygeppetto
class RuntimeProject:
    __geppetto_model = None
    __filename = None

    @classmethod
    def get_geppetto_model(cls):
        return cls.__geppetto_model

    @classmethod
    def set_geppetto_model(cls, model):
        cls.__geppetto_model = model

    @classmethod
    def get_file_name(cls):
        return cls.__filename

    @classmethod
    def set_file_name(cls, file_name):
        cls.__filename = file_name




# curl -X POST http://localhost:8000/api/load


class NWBController:

    @staticmethod
    def load_nwb_model(nwbfile):
        import os
        cached_model_file = nwbfile + '.json'
        if cache_model and os.path.exists(cached_model_file):
            with open(cached_model_file, 'rb') as f:
                serialized_model = f.read()
                geppetto_model = GeppettoModelSerializer().deserialize(serialized_model)

        else:
            model_interpreter = NWBModelInterpreter()

            try:
                geppetto_model = model_interpreter.importType(
                    nwbfile, '', '', '')
            except ValueError as e:
                raise Exception("File error", e)
            serialized_model = GeppettoModelSerializer().serialize(geppetto_model)

            with open(cached_model_file, 'wb') as f:
                f.write(serialized_model)

        return geppetto_model, serialized_model

    @get('/api/load')
    def loadFile(self, nwbfile):
        logging.info('Loading nwb file: {}'.format(nwbfile))
        if nwbfile:
            if 'http' in nwbfile:
                logging.info('Downloading nwb file: {}'.format(nwbfile))
                nwbfile = get_file_from_url(nwbfile)
                logging.info('Downloaded file to: {}'.format(nwbfile))
            geppetto_model, serialized_model = NWBController.load_nwb_model(nwbfile)

            RuntimeProject.set_geppetto_model(geppetto_model)
            RuntimeProject.set_file_name(nwbfile)

            return serialized_model
        else:
            raise Exception("File path missing")

    @get('/api/plot')
    def get_plot(self, plot):

        geppetto_model = RuntimeProject.get_geppetto_model()
        if not geppetto_model:
            raise Exception(
                "Geppetto Model not initialized. Load should be called first")
        plot_manager = PlotManager(geppetto_model)
        nwbfile = RuntimeProject.get_file_name()
        if nwbfile is None:
            raise Exception("Nwbfile not initialized")
        try:
            return plot_manager.plot(plot, nwbfile)
        except Exception as e:
            raise Exception(
                "Error creating plot for file {1}. Error is {0}".format(e, nwbfile))


    @get('/api/plots_available')
    def plots_available(self):
        geppetto_model = RuntimeProject.get_geppetto_model()
        if not geppetto_model:
            raise Exception("Geppetto Model not in session")

        plot_manager = PlotManager(geppetto_model)

        nwbfile = RuntimeProject.get_file_name()
        if nwbfile is None:
            raise Exception("Nwbfile not in session")
        try:
            return plot_manager.get_available_plots(nwbfile)
        except Exception as e:
            e.args += ["Error creating plot"]
            raise e






