import logging

from ipywidgets import widgets
from jupyter_geppetto.webapi import get
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
from notebook.base.handlers import IPythonHandler

from nwb_explorer.nwb_model_interpreter import NWBModelInterpreter

from pygeppetto.managers import GeppettoManager

cache_model = False

from pygeppetto.services.data_manager import DataManagerHelper
from ipywidgets.embed import embed_snippet, html_template


from nwbwidgets import nwb2widget
import logging
import os

from pygeppetto.services.model_interpreter import get_model_interpreter_from_variable


def createNotebook(filename):
    import nbformat as nbf
    from nbformat.v4.nbbase import new_notebook
    from nbformat import sign
    import codecs
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


def get_model_interpreter(clientId, projectId) -> NWBModelInterpreter:
    data_manager = DataManagerHelper.getDataManager()
    geppetto_project = data_manager.getGeppettoProjectById(int(projectId))
    geppetto_manager = GeppettoManager.get_instance(int(clientId))
    runtime_project = geppetto_manager.get_runtime_project(geppetto_project)
    model_interpreter = get_model_interpreter_from_variable(runtime_project.model.variables[0])
    return model_interpreter


def nwb_object(nwbfile, path):
    obj = nwbfile
    for el in path.split('.')[1:]:
        if isinstance(obj, dict):
            if el in obj:
                obj = obj[el]
            else:
                logging.warning("%s not found in %s", el, obj)
        else:
            obj = getattr(obj, el)
    return obj


class NWBController:  # pytest: no cover

    @get('/api/image', {'Content-type': 'image/png', 'Cache-Control': 'max-age=600'})
    def image(handler: IPythonHandler, name: str, interface: str, projectId: str = '0', index: str = '0',
              clientId=None) -> str:
        if not any([name, interface, projectId]):
            return "Bad request"

        model_interpreter = get_model_interpreter(clientId, projectId)

        return model_interpreter.nwb_reader.get_image(name=name, interface=interface, index=index)

    @get('/notebook')
    def new_notebook(handler: IPythonHandler, path):
        if not os.path.exists(path):
            logging.info("Creating notebook {}".format(path))
            createNotebook(path)
        handler.redirect('notebooks/' + path)

    @get('/nwbwidget')
    def get_nwb_widget(handler: IPythonHandler, path='', projectId: str = '0', clientId=None):


        model_interpreter = get_model_interpreter(clientId, projectId)
        nwbfile = model_interpreter.get_nwbfile()

        widget = nwb2widget(nwb_object(nwbfile, path))

        snippet = embed_snippet([widget])

        values = {
            'title': '',
            'snippet': snippet,
        }

        template = html_template

        return template.format(**values)
