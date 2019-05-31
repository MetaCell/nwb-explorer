"""
hnn_geppetto.py
Initialise Geppetto, this class contains methods to connect the application with the Geppetto based UI
"""
import logging
import os
import sys
from contextlib import redirect_stdout

from jupyter_geppetto import synchronization

from . import nwb_data_manager
from .nwb_model_interpreter.nwb_reader import NWBReader


class NWBGeppetto():

    def __init__(self):
        # use to decide whether or not to update the canvas in the front end
    
        logging.debug("Initializing the original model")

        synchronization.context = { 'nwb_geppetto': self }

    def get_data(self):
        with redirect_stdout(sys.__stdout__):
            return {
                "metadata": {},
                "isDocker": os.path.isfile('/.dockerenv'),
                "currentFolder": os.getcwd()
            }

    def set_nwb_file(self, nwbfilename):
        main = __import__('__main__')
        import pynwb
        main.nwbfilename = nwb_data_manager.get_file_path(nwbfilename)
        main.pynwb = pynwb
        self.nwb_reader = NWBReader(main.nwbfilename)
        main.nwb_reader = self.nwb_reader
        main.nwbfile = self.nwb_reader.nwbfile


def main(nwbfilename):
    logging.info("Initialising NWB UI")
    geppetto = NWBGeppetto()
    geppetto.set_nwb_file(nwbfilename)

    main = __import__('__main__')

    from nwbwidgets import nwb2widget
    main.nwb2widget = nwb2widget
    main.show = lambda: nwb2widget(main.nwbfile)

    logging.info("NWB UI initialised")