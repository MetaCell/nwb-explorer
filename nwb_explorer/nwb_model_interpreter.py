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
        nwb_geppetto_library = pygeppetto.GeppettoLibrary(name='nwblib')
        geppetto_model.libraries.append(nwb_geppetto_library)
        model = GeppettoModelSerializer().serialize(geppetto_model)

        # read data 
        io = NWBHDF5IO(url, 'r')
        nwbfile = io.read()

        # get the processing module
        mod = nwbfile.get_processing_module('ophys')

        # get the RoiResponseSeries from the Fluorescence data interface
        # get the data...
        rrs = mod['DfOverF'].get_roi_response_series()
        rrs_data = rrs.data
        rrs_timestamps = rrs.timestamps

        nwbType = pygeppetto.CompositeType(id=str('nwb'), name=str('nwb'), abstract= False)
        ts_val1 = self.factory.createTimeSeries('myTimeSeriesValue', rrs_data[()][0].all())
        nwbType.variables.append(self.factory.createStateVariable('timeSeriesVariable', ts_val1))
        ts_val2 = self.factory.createTimeSeries('myTimeSeriesValue', rrs_data[()][1].all())
        nwbType.variables.append(self.factory.createStateVariable('timeSeriesVariable', ts_val2))
        time = self.factory.createTimeSeries('myTimeSeriesValue', rrs_timestamps[()].all())
        geppetto_model.variables.append(self.factory.createStateVariable('time', time))

        return model

    def importValue(self, importValue):
        pass

    def getName(self):
        return "NWB Model Interpreter"

    def getDependentModels(self):
        return []

