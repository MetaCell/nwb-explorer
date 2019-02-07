from jupyter_geppetto.webapi import Route, JupyterGeppettoHandler

from nwb_explorer import handlers


routes = [
    Route('/api/load/', handlers.LoadNWBFileHandler),
    Route('/api/plot', handlers.PlotHandler),
    Route('/api/plots_available', handlers.PlotsAvailableHandler)
]





