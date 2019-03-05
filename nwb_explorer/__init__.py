from nwb_explorer import api
from jupyter_geppetto.webapi import RouteManager

RouteManager.add_controller(api.NWBController)




