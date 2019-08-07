import logging

from jupyter_geppetto.webapi import get
from pygeppetto.model.model_serializer import GeppettoModelSerializer

from nwb_explorer.nwb_model_interpreter import NWBModelInterpreter
from nwb_explorer.plots_manager import PlotManager
from . import nwb_data_manager

from pygeppetto.managers import GeppettoManager
from pygeppetto.managers.geppetto_manager import RuntimeProject

cache_model = False

from pygeppetto.services.data_manager import DataManagerHelper
import logging
import os
from notebook.notebook.handlers import get_custom_frontend_exporters


class NWBController:  # pytest: no cover
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

    @get('/api/image', {'Content-type': 'image/png'})
    def image(self, name: str, interface: str, projectId: str = '0', index: str = '0') -> str:
        if not any([name, interface, projectId]):
            return "Bad request"

        manager = GeppettoManager()

        dataManager = DataManagerHelper.getDataManager()
        project = dataManager.getGeppettoProjectById(project_id=int(projectId))

        project = manager.get_runtime_project(project)
        nwb_reader = NWBController.model_interpreter.nwb_reader

        return nwb_reader.get_image(name=name, interface=interface, index=index)

    @get('/notebook')
    def new_notebook(self, path):
        if not os.path.exists(path):
            logging.info("Creating notebook {}".format(path))
            from jupyter_geppetto.utils import createNotebook
            createNotebook(path)
        return self.render_template('notebook.html',
                                    notebook_path=path,
                                    notebook_name=path.split('/')[-1],
                                    kill_kernel=False,
                                    mathjax_url=self.mathjax_url,
                                    mathjax_config=self.mathjax_config,
                                    get_custom_frontend_exporters=get_custom_frontend_exporters
                                    )
