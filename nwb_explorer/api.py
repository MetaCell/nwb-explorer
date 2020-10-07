from pygeppetto.services.model_interpreter import get_model_interpreter_from_variable
from pygeppetto.services.data_manager import DataManagerHelper
import logging
import logging
import os

import tornado
from notebook.base.handlers import IPythonHandler

from jupyter_geppetto.webapi import get
from pygeppetto.managers import GeppettoManager

from nwb_explorer.nwb_model_interpreter import NWBModelInterpreter

cache_model = False


def create_notebook(filename):
    import nbformat as nbf
    from nbformat.v4.nbbase import new_notebook
    from nbformat import sign
    import codecs

    directory = os.path.dirname(filename)
    if not os.path.exists(directory):
        os.makedirs(directory)
    nb0 = new_notebook(cells=[nbf.v4.new_markdown_cell("""Welcome to the NWB Explorer!
--

This interface allows you to interact with the data in your NWB file both graphically (click on the icons under the 'Controls' column on the list above) and programmatically.

With this Python console you can programmatically access the loaded data using the [PyNWB Python API](https://pynwb.readthedocs.io/en/stable/).

The loaded NWB:N 2 file can be accessed from the variable `nwbfile`. 
If you would like to inspect the content of the file using the [NWB Juypyter widgets](https://pypi.org/project/nwbwidgets/) you can use the `show()` function.

To execute a command type it and press `Shift+Enter`. To execute a command and create a new cell press `Alt+Enter`."""),
                              nbf.v4.new_code_cell('nwbfile')
                              ], metadata={"kernelspec": {
        "display_name": "Python 3",
        "language": "python",
        "name": "python3"
    }})

    f = codecs.open(filename, encoding='utf-8', mode='w')

    nbf.write(nb0, f, 4)
    f.close()


def get_model_interpreter(runtime_project) -> NWBModelInterpreter:
    return get_model_interpreter_from_variable(runtime_project.model.variables[0])


class NWBController:  # pytest: no cover

    @get('/api/image', {'Content-type': 'image/png', 'Cache-Control': 'max-age=600'})
    def image(handler: IPythonHandler, clientId: str, name: str, interface: str, projectId: str,
              index: str = '0', ) -> str:
        if not any([name, interface, projectId, clientId]):
            raise tornado.web.HTTPError(400)

        dataManager = DataManagerHelper.getDataManager()
        geppetto_project = dataManager.getGeppettoProjectById(
            project_id=int(projectId))

        if geppetto_project is None:
            raise tornado.web.HTTPError(400)
        geppetto_manager = GeppettoManager.get_instance(int(clientId))
        runtime_project = geppetto_manager.get_runtime_project(
            geppetto_project)

        model_interpreter = get_model_interpreter(runtime_project)
        nwb_reader = model_interpreter.nwb_reader

        return nwb_reader.get_image(name=name, interface=interface, index=index)

    @get('/notebook')
    def new_notebook(handler: IPythonHandler, path):
        if not os.path.exists(path):
            logging.info("Creating notebook {}".format(path))
            create_notebook(path)
        handler.redirect('notebooks/' + path)
