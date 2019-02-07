"""
hnn_geppetto.py
Initialise HNN Geppetto, this class contains methods to connect HNN with the Geppetto based UI
"""
import importlib
import json
import logging
import os
import sys
from contextlib import redirect_stdout

from jupyter_geppetto import jupyter_geppetto, synchronization, utils

from pygeppetto.model.model_serializer import GeppettoModelSerializer


class NWBGeppetto():

    def __init__(self):
        # use to decide wheter or not to update the canvas in the front end
    
        logging.debug("Initializing the original model")

        jupyter_geppetto.context = { 'nwb_geppetto': self }

    def getData(self):
        with redirect_stdout(sys.__stdout__):
            return {
                "metadata": {},
                "isDocker": os.path.isfile('/.dockerenv'),
                "currentFolder": os.getcwd()
            }


    
    def instantiateModelInGeppetto(self):
        try:
            with redirect_stdout(sys.__stdout__):
                netpyne_model = self.instantiateModel()
                self.geppetto_model = self.model_interpreter.getGeppettoModel(netpyne_model)
                
                return json.loads(GeppettoModelSerializer().serialize(self.geppetto_model))
        except:
            return utils.getJSONError("Error while instantiating the NetPyNE model", sys.exc_info())

    def instantiateModel(self):
        with redirect_stdout(sys.__stdout__):
            netParams_snapshot = set_netParams(self.cfg)
            netParams_snapshot.cellParams = set_cellParams(self.cfg)
            sim.create(simConfig=self.cfg, netParams=netParams_snapshot)
            sim.gatherData(gatherLFP=False)
            self.last_cfg_snapshot = self.cfg.__dict__.copy()

        return sim

    def getEvokedInputs(self):
        return list(self.cfg.evoked.keys())

    # waiting for evoked input model (this is tentative)
    def addEvokedInput(self, input_type):
        evoked_indices = [int(key[key.index("_")+1:]) for key in self.cfg.evoked.keys() if input_type in key]
        index = str(max(evoked_indices) + 1) if len(evoked_indices) > 0 else 1
        self.cfg.evoked[f"{input_type}_{index}"] = DISTAL if input_type=="distal" else PROXIMAL
        return { 'inputs': self.getEvokedInputs(), 'selected_input': f'{input_type}_{index}' }
    
    def removeEvokedInput(self, name):
        del self.cfg.evoked[name]
        return self.getEvokedInputs()

    def compare_cfg_to_last_snapshot(self):
        return {
            "canvasUpdateRequired": self._is_canvas_update_required(),
            "simulationUpdateRequired": self._have_params_changed()
        }

    def _is_canvas_update_required(self):
        for key in self.cfg.__dict__:
            for end in CANVAS_KEYS:
                if key.endswith(end) and getattr(self.cfg, key) != self.last_cfg_snapshot[key]:
                    return True
        return False

    def _have_params_changed(self):
        for key in self.cfg.__dict__:
            if getattr(self.cfg, key) != self.last_cfg_snapshot[key]:
                return True
        return False

    def getDirList(self, dir=None, onlyDirs=False, filterFiles=False):
        # Get Current dir
        if dir is None or dir == '':
            dir = os.getcwd()
        dir_list = []
        for f in sorted(os.listdir(str(dir)), key=str.lower):
            ff = os.path.join(dir, f)
            if os.path.isdir(ff):
                dir_list.insert(0, {'title': f, 'path': ff, 'load': False, 'children': [{'title': 'Loading...'}]})
            elif not onlyDirs:
                if not filterFiles or os.path.isfile(ff) and ff.endswith(filterFiles):
                    dir_list.append({'title': f, 'path': ff})
        return dir_list

def main():
    logging.info("Initialising NWB UI")
    hnn_geppetto = NWBGeppetto()
    logging.info("NWB UI initialised")