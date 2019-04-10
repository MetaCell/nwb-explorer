from pygeppetto.services import model_interpreter

from .nwb_model_interpreter import *

model_interpreter.add_model_interpreter('nwb', nwb_model_interpreter)
