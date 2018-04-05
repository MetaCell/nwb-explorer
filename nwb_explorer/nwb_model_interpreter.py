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
from pynwb import NWBHDF5IO


class NWBModelInterpreter(ModelInterpreter):

    def __init__(self):
        self.factory = GeppettoModelFactory()

    def importType(self, url, typeName, library, commonLibraryAccess):
        logging.debug('Creating a Geppetto Model')

        factory = GeppettoModelFactory()
        geppetto_model = factory.createGeppettoModel('GepettoModel')
        nwb_geppetto_library = pygeppetto.GeppettoLibrary(name='nwblib')
        geppetto_model.libraries.append(nwb_geppetto_library)
        

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

        stimulus = nwbfile.get_stimulus('natural_images_timeseries')
        stimulus_data = stimulus.data[()]
        stimulus_timestamps = stimulus.timestamps[()]

        nwbType = pygeppetto.CompositeType(id=str('nwb'), name=str('nwb'), abstract= False)
        dff_val1 = self.factory.createTimeSeries('myTimeSeriesValue', rrs_data[()][0].tolist())
        nwbType.variables.append(self.factory.createStateVariable('DfOverF_1', dff_val1))
        dff_val2 = self.factory.createTimeSeries('myTimeSeriesValue', rrs_data[()][1].tolist())
        nwbType.variables.append(self.factory.createStateVariable('DfOverF_2', dff_val2))
        time = self.factory.createTimeSeries('myTimeSeriesValue', rrs_timestamps[()].tolist())
        geppetto_model.variables.append(self.factory.createStateVariable('time', time))

        stimulus_value = self.factory.createTimeSeries('myTimeSeriesValue', stimulus_data.tolist())
        nwbType.variables.append(self.factory.createStateVariable('Stimulus', stimulus_value)) 
        stimulus_time = self.factory.createTimeSeries('myTimeSeriesValue', stimulus_timestamps.tolist())
        geppetto_model.variables.append(self.factory.createStateVariable('stimulus_time', stimulus_time))

        model = GeppettoModelSerializer().serialize(geppetto_model)
        return model

    def importValue(self, importValue):
        pass

    def getName(self):
        return "NWB Model Interpreter"

    def getDependentModels(self):
        return []

