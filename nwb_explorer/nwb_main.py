"""
hnn_geppetto.py
Initialise Geppetto, this class contains methods to connect the application with the Geppetto based UI
"""
import importlib
import json
import logging
import os
import sys
from contextlib import redirect_stdout

from jupyter_geppetto import synchronization, utils

from pygeppetto.model.model_serializer import GeppettoModelSerializer


class NWBGeppetto():

    def __init__(self):
        # use to decide whether or not to update the canvas in the front end
    
        logging.debug("Initializing the original model")

        synchronization.context = { 'nwb_geppetto': self }

    def getData(self):
        with redirect_stdout(sys.__stdout__):
            return {
                "metadata": {},
                "isDocker": os.path.isfile('/.dockerenv'),
                "currentFolder": os.getcwd()
            }



def main():
    logging.info("Initialising NWB UI")
    hnn_geppetto = NWBGeppetto()
    logging.info("NWB UI initialised")