import logging
import os

import pygeppetto
import requests
from pygeppetto.data_model import GeppettoProject
from pygeppetto.model import GeppettoLibrary
from pygeppetto.model.types import ImportType
from pygeppetto.services.data_manager import GeppettoDataManager
from pygeppetto.utils import Singleton
from pygeppetto.services.model_interpreter import add_model_interpreter
# TODO this path must be a shared storage inside the cluster
from nwb_explorer.nwb_model_interpreter import NWBModelInterpreter, GeppettoModelAccess, GeppettoModelFactory, Variable

CACHE_DEFAULT_DIR = 'nwb_files_cache/'


class NWBFileNotFound(FileNotFoundError): pass


def get_file_path(file_name_or_url):
    if file_name_or_url.startswith('http'):
        nwbfile = get_file_from_url(file_name_or_url)
        return nwbfile
    if not os.path.exists(file_name_or_url):
        raise NWBFileNotFound("NWB file not found", file_name_or_url)
    return file_name_or_url


def get_file_from_url(file_url, fname=None, cache_dir=CACHE_DEFAULT_DIR):
    file_name = os.path.join(cache_dir, (os.path.basename(file_url) if not fname else fname))
    if not os.path.exists(file_name):
        if not os.path.exists(os.path.dirname(file_name)):
            os.makedirs(os.path.dirname(file_name))
        logging.info('Downloading {} to {}...'.format(file_url, file_name))
        response = requests.get(file_url)
        with open(file_name, 'wb') as f:
            f.write(response.content)
        logging.info('Downloaded file to: {}'.format(file_name))
    return file_name


class NWBDataManager(GeppettoDataManager, metaclass=Singleton):
    last_id = 0

    def get_project_from_url(self, nwbfile):
        '''The url we expect here is a nwb file, potentially remote'''
        nwbfilename = get_file_path(nwbfile)
        model_interpreter = NWBModelInterpreter(nwbfilename)
        add_model_interpreter(model_interpreter.library.id, model_interpreter)
        try:

            geppetto_model = model_interpreter.create_model()
            project = GeppettoProject(id=self.last_id, name='NWB file {}'.format(os.path.basename(nwbfilename)),
                                      geppetto_model=geppetto_model, volatile=True, base_url=None, public=False,
                                      experiments=None, view=None)
            self.last_id += 1
            self.projects[project.id] = project
            return project
        except ValueError as e:
            raise Exception("File error", e)
