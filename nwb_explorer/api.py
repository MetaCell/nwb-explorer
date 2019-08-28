import logging

from jupyter_geppetto.webapi import get
from notebook.base.handlers import IPythonHandler
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
from pygeppetto.services.model_interpreter import get_model_interpreter_from_variable


def get_model_interpreter(runtime_project) -> NWBModelInterpreter:
    return get_model_interpreter_from_variable(runtime_project.model.variables[0])

class NWBController:  # pytest: no cover

    @get('/api/image', {'Content-type': 'image/png', 'Cache-Control': 'max-age=600'})
    def image(handler: IPythonHandler, name: str, interface: str, projectId: str = '0', index: str = '0') -> str:
        if not any([name, interface, projectId]):
            return "Bad request"

        manager = GeppettoManager()

        dataManager = DataManagerHelper.getDataManager()
        project = dataManager.getGeppettoProjectById(project_id=int(projectId))

        project = manager.get_runtime_project(project)
        model_interpreter = get_model_interpreter(project)
        nwb_reader = model_interpreter.nwb_reader

        return nwb_reader.get_image(name=name, interface=interface, index=index)

    @get('/notebook')
    def new_notebook(handler: IPythonHandler, path):
        if not os.path.exists(path):
            logging.info("Creating notebook {}".format(path))
            from jupyter_geppetto.utils import createNotebook
            createNotebook(path)
        return handler.render_template('notebook.html',
                                       notebook_path=path,
                                       notebook_name=path.split('/')[-1],
                                       kill_kernel=False,
                                       mathjax_url=handler.mathjax_url,
                                       mathjax_config=handler.mathjax_config,
                                       get_custom_frontend_exporters=get_custom_frontend_exporters
                                       )
