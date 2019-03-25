from pygeppetto.model.model_serializer import GeppettoModelSerializer
from jupyter_geppetto.webapi import get
from nwb_explorer.nwb_model_interpreter import NWBModelInterpreter
from nwb_explorer.plots_manager import PlotManager
import logging
from . import service

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
    def get_model_interpreter(cls):
        return cls.model_interpreter

    @classmethod
    def load_nwb_model(cls, nwbfilename):

        try:

            geppetto_model = cls.get_model_interpreter().importType(nwbfilename, '', '', '')
        except ValueError as e:
            raise Exception("File error", e)
        serialized_model = GeppettoModelSerializer().serialize(geppetto_model)
        return geppetto_model, serialized_model

    @get('/api/load')
    def load_file(self, nwbfile):
        logging.info('Loading nwb file: {}'.format(nwbfile))
        if nwbfile:
            nwbfile = service.get_file_path(nwbfile)
            geppetto_model, serialized_model = NWBController.load_nwb_model(nwbfile)

            RuntimeProject.set_geppetto_model(geppetto_model)
            RuntimeProject.set_file_name(nwbfile)

            return serialized_model
        else:
            raise Exception("File path missing")

    @get('/api/lazyloading')
    def load_file(self, path):
        logging.info('Loading value: {}'.format(path))
        if path:
            value = self.get_model_interpreter().importValue(path)

            return GeppettoModelSerializer().serialize(geppetto_model)
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
