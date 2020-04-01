import logging
import glob
import os
import pynwb
from pynwb import load_namespaces

from jupyter_geppetto.webapi import RouteManager
from pygeppetto.services import model_interpreter, data_manager

from nwb_explorer import api
from nwb_explorer.nwb_data_manager import NWBDataManager
from nwb_explorer.nwb_model_interpreter import NWBModelInterpreter

EXTENSION_PATH = 'nwb-extensions'

# Add REST API
RouteManager.add_controller(api.NWBController)
logging.info("Adding NWBModelInterpreter")
# Add model interpreter


logging.info("Adding NWBDataManager")
# Replace data manager
data_manager.set_data_manager(NWBDataManager())


# This should be temporary. Ideally namespaces should be cached in the NWB files
# See https://github.com/SilverLabUCL/PySilverLabNWB/issues/26
def init_extensions():

    for namespace_file in glob.glob(EXTENSION_PATH + '/**/*.namespace.*ml'):
        extension_path = os.path.dirname(namespace_file)
        extension_name = os.path.basename(extension_path)
        logging.info('Initializing extension ' + extension_name)
        load_namespaces(namespace_file)

        init_file = os.path.join(extension_path, 'init.py')
        if os.path.exists(init_file):
            try:
                with open(init_file) as f:
                    for line in f:
                        eval(line)
            except Exception as e:
                logging.error("Error evaluating extension init file " + init_file, exc_info=True)
init_extensions()