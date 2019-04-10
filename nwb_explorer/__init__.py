from jupyter_geppetto.webapi import RouteManager
from pygeppetto.services import model_interpreter, data_manager

from nwb_explorer import api
from nwb_explorer.nwb_data_manager import NWBDataManager
from nwb_explorer.nwb_model_interpreter import NWBModelInterpreter

# Add REST API
RouteManager.add_controller(api.NWBController)

# Add model interpreter
model_interpreter.add_model_interpreter('nwb', NWBModelInterpreter())

# Replace data manager
data_manager.set_data_manager(NWBDataManager())
