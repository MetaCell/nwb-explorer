"""
netpyne_model_interpreter.py
Model interpreter for NWB. This class creates a geppetto type
"""
import logging
import model as pygeppetto
from model.services.model_interpreter import ModelInterpreter
from model.model_factory import GeppettoModelFactory
from model.values import Point, ArrayElement, ArrayValue
from model.model_serializer import GeppettoModelSerializer


class NWBModelInterpreter(ModelInterpreter):

    def __init__(self):
        self.factory = GeppettoModelFactory()

    def importType(self, url, typeName, library, commonLibraryAccess):
        logging.debug('Creating a Geppetto Model')

        factory = GeppettoModelFactory()
        geppetto_model = factory.createGeppettoModel('GepettoModel')
        nwb_geppetto_library = pygeppetto.GeppettoLibrary(
            name='nwblib')
        geppetto_model.libraries.append(nwb_geppetto_library)
        model = GeppettoModelSerializer().serialize(geppetto_model)

        return model

    def importValue(self, importValue):
        pass

    def getName(self):
        return "NWB Model Interpreter"

    def getDependentModels(self):
        return []

