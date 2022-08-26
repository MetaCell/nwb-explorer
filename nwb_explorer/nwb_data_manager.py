import logging
import os
import shutil
import requests
import re

from pygeppetto.data_model import GeppettoProject
from pygeppetto.services.data_manager import GeppettoDataManager
from pygeppetto.utils import Singleton
from pygeppetto.services.model_interpreter import add_model_interpreter

from nwb_explorer.nwb_model_interpreter import NWBModelInterpreter

CACHE_DIRNAME = './workspace'
# TODO this path must be a shared storage inside the cluster
CACHE_DEFAULT_DIR = f"{CACHE_DIRNAME}/"


class NWBFileNotFound(FileNotFoundError):
    pass


def get_file_path(file_name_or_url):
    if file_name_or_url.startswith('http'):
        file_name = get_file_from_url(file_name_or_url)
        return file_name
    elif not os.path.exists(file_name_or_url):
        raise NWBFileNotFound("NWB file not found", file_name_or_url)
    else:
        file_name = file_name_or_url
        if not os.path.exists(file_name):
            file_name = get_cache_path(file_name_or_url)
            if not os.path.exists(os.path.dirname(file_name)):
                os.makedirs(os.path.dirname(file_name))
                shutil.copyfile(file_name_or_url, file_name)
        return file_name


def get_file_from_url(file_url, fname=None, cache_dir=CACHE_DEFAULT_DIR):
    file_name = get_cache_path(file_url, fname, cache_dir)
    if not os.path.exists(file_name):
        if not os.path.exists(os.path.dirname(file_name)):
            os.makedirs(os.path.dirname(file_name))
        logging.info('Downloading {}'.format(file_url))
        response = requests.get(file_url, allow_redirects=True)
        if response.status_code != 200:
            raise Exception(f"Error downloading file {file_url}")
        if not fname and 'content-disposition' in response.headers:
            fname = re.findall('filename="(.+)"',
                               response.headers['content-disposition'])[0]
        file_name = get_cache_path(response.url, fname, cache_dir)

        dirname = os.path.dirname(file_name)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        with open(file_name, 'wb') as f:
            f.write(response.content)
        logging.info('Downloaded file to: {}'.format(file_name))

    return file_name


def get_cache_path(file_url, fname=None, cache_dir=CACHE_DEFAULT_DIR):
    return os.path.join(cache_dir, file_url.strip('/').split('//')[1] if not fname else fname)


class NWBDataManager(GeppettoDataManager, metaclass=Singleton):
    last_id = 0

    def get_project_from_url(self, nwbfile):
        '''The url we expect here is a nwb file, potentially remote'''
        try:
            nwbfilename = get_file_path(nwbfile)
        except Exception as e:
            raise Exception("Error retrieving file" + nwbfile) from e
        try:
            model_interpreter = NWBModelInterpreter(
                nwbfilename, source_url=nwbfile)
            add_model_interpreter(
                model_interpreter.library.id, model_interpreter)

            geppetto_model = model_interpreter.create_model()
            project = GeppettoProject(id=self.last_id, name='NWB file {}'.format(os.path.basename(nwbfilename)),
                                      geppetto_model=geppetto_model, volatile=True, base_url=None, public=False,
                                      experiments=None, view=None)
            self.last_id += 1
            self.projects[project.id] = project
            return project

        except Exception as e:
            os.remove(nwbfilename)
            raise Exception("NWB file error") from e
