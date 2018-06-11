"""
netpyne_model_interpreter.py
Model interpreter for NWB. This class creates a geppetto type
"""
import logging
import pygeppetto.model as pygeppetto
from pygeppetto.model.services.model_interpreter import ModelInterpreter
from pygeppetto.model.model_factory import GeppettoModelFactory
from pygeppetto.model.values import Point, ArrayElement, ArrayValue
from pygeppetto.model.variables import Variable
from pynwb import NWBHDF5IO


class NWBModelInterpreter(ModelInterpreter):

    def __init__(self):
        self.factory = GeppettoModelFactory()

    def importType(self, url, typeName, library, commonLibraryAccess):
        logging.debug('Creating a Geppetto Model')

        geppetto_model = self.factory.createGeppettoModel('GepettoModel')
        nwb_geppetto_library = pygeppetto.GeppettoLibrary(name='nwblib', id='nwblib')
        geppetto_model.libraries.append(nwb_geppetto_library)
        
        # read data 
        io = NWBHDF5IO(url, 'r')
        nwbfile = io.read()

        # get the processing module
        mod = nwbfile.get_processing_module('ophys_module')

        # get the RoiResponseSeries from the Fluorescence data interface
        # get the data...
        rrs = mod['dff_interface'].get_roi_response_series()
        rrs_data = rrs.data
        rrs_timestamps = rrs.timestamps

        stimulus = nwbfile.get_stimulus('locally_sparse_noise_4deg')
        stimulus_data = [float(i) for i in stimulus.data]
        stimulus_timestamps = stimulus.timestamps[()]

        nwbType = pygeppetto.CompositeType(id=str('nwb'), name=str('nwb'), abstract= False)
        dff_val1 = self.factory.createTimeSeries('myTimeSeriesValue', rrs_data[()][0].tolist(), 'V')
        nwbType.variables.append(self.factory.createStateVariable('DfOverF_1', dff_val1))
        dff_val2 = self.factory.createTimeSeries('myTimeSeriesValue', rrs_data[()][1].tolist(), 'V')
        nwbType.variables.append(self.factory.createStateVariable('DfOverF_2', dff_val2))
        time = self.factory.createTimeSeries('myTimeSeriesValue', rrs_timestamps[()].tolist(), 's')
        geppetto_model.variables.append(self.factory.createStateVariable('time', time))

        stimulus_value = self.factory.createTimeSeries('myTimeSeriesValue', stimulus_data, 'V')
        nwbType.variables.append(self.factory.createStateVariable('Stimulus', stimulus_value)) 
        stimulus_time = self.factory.createTimeSeries('myTimeSeriesValue', stimulus_timestamps.tolist(), 's')
        geppetto_model.variables.append(self.factory.createStateVariable('stimulus_time', stimulus_time))
        
        # add type to nwb
        nwb_geppetto_library.types.append(nwbType)

        # add top level variables
        nwb_variable = Variable(id='nwb')
        nwb_variable.types.append(nwbType)
        geppetto_model.variables.append(nwb_variable)

        
        return geppetto_model

    def importValue(self, importValue):
        pass

    def getName(self):
        return "NWB Model Interpreter"

    def getDependentModels(self):
        return []

