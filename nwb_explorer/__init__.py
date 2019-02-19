from nwb_explorer import handlers
from jupyter_geppetto.webapi import RouteManager

RouteManager.add_controller(handlers.NWBController)




