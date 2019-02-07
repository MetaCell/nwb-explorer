from jupyter_geppetto.webapi import JupyterGeppettoHandler
from pygeppetto.model.model_serializer import GeppettoModelSerializer


from nwb_explorer.nwb_model_interpreter import NWBModelInterpreter
from nwb_explorer.plots_manager import PlotManager


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


def load_nwb_model(nwbfile):
    import os
    cached_file = nwbfile + '.json'
    if os.path.exists(cached_file):
        with open(cached_file, 'rb') as f:
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

        with open(cached_file, 'wb') as f:
            f.write(serialized_model)

    return geppetto_model, serialized_model

# curl -X POST http://localhost:8000/api/load


class LoadNWBFileHandler(JupyterGeppettoHandler):

    def get(self):
        nwbfile = self.get_query_argument('nwbfile')

        if nwbfile:

            geppetto_model, serialized_model = load_nwb_model(nwbfile)

            RuntimeProject.set_geppetto_model(geppetto_model)
            RuntimeProject.set_file_name(nwbfile)

            self.write(serialized_model)
        else:
            raise Exception("File path missing")

    def post(self):
        self.write('Post model')


# curl -X POST http://localhost:8000/api/plot
class PlotHandler(JupyterGeppettoHandler):

    def get(self):
        plot_id = self.get_query_argument('plot')
        geppetto_model = RuntimeProject.get_geppetto_model()
        if not geppetto_model:
            raise Exception(
                "Geppetto Model not initialized. Load should be called first")
        plot_manager = PlotManager(geppetto_model)
        nwbfile = RuntimeProject.get_file_name()
        if nwbfile is None:
            raise Exception("Nwbfile not initialized")
        try:
            self.finish(plot_manager.plot(plot_id, nwbfile))
        except Exception as e:
            raise Exception(
                "Error creating plot for file {1}. Error is {0}".format(e, nwbfile))

    def post(self):
        self.finish("Post Response")


# curl -X POST http://localhost:8000/api/plots_available
class PlotsAvailableHandler(JupyterGeppettoHandler):

    def get(self):
        geppetto_model = RuntimeProject.get_geppetto_model()
        if not geppetto_model:
            raise Exception("Geppetto Model not in session")

        plot_manager = PlotManager(geppetto_model)

        nwbfile = RuntimeProject.get_file_name()
        if nwbfile is None:
            raise Exception("Nwbfile not in session")
        try:
            self.finish(plot_manager.get_available_plots(nwbfile))
        except Exception as e:
            raise Exception("Error creating plot" + e)

    def post(self):
        self.finish("Post Response")
