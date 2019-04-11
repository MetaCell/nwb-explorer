import logging

from jupyter_geppetto.webapi import get
from pygeppetto.model.model_serializer import GeppettoModelSerializer

from nwb_explorer.nwb_model_interpreter import NWBModelInterpreter
from nwb_explorer.plots_manager import PlotManager
from . import nwb_data_manager

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
    model_interpreter = NWBModelInterpreter()

    @classmethod
    def load_nwb_model(cls, nwbfilename):

        try:

            geppetto_model = cls.model_interpreter.createModel(nwbfilename)
        except ValueError as e:
            raise Exception("File error", e)
        serialized_model = GeppettoModelSerializer().serialize(geppetto_model)
        return geppetto_model, serialized_model

    @get('/api/load')
    def load_file(self, nwbfile):
        logging.info('Loading nwb file: {}'.format(nwbfile))
        if nwbfile:
            nwbfile = nwb_data_manager.get_file_path(nwbfile)
            geppetto_model, serialized_model = NWBController.load_nwb_model(nwbfile)

            RuntimeProject.set_geppetto_model(geppetto_model)
            RuntimeProject.set_file_name(nwbfile)

            return serialized_model
        else:
            raise Exception("File path missing")

    @get('/api/importvalue')
    def import_value(self, path):
        logging.info('Loading value: {}'.format(path))
        if path:
            value = NWBController.model_interpreter.importValue(path)
            model = ''  # TODO
            serialized_value = GeppettoModelSerializer().serialize(value)
            # TODO implement: this should return a full geppetto model
            return serialized_value
        else:
            raise Exception("Value path missing")

    @get('/api/resolvevalue')
    def resolve_value(self, path):
        logging.info('Loading value: {}'.format(path))
        if path:
            value = NWBController.model_interpreter.importValue(path)
            serialized_value = GeppettoModelSerializer().serialize(value)
            return serialized_value
        else:
            raise Exception("Value path missing")

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
