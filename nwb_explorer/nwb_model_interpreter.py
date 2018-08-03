"""
netpyne_model_interpreter.py
Model interpreter for NWB. This class creates a geppetto type
"""
import logging

import pygeppetto.model as pygeppetto
from pygeppetto.model.model_factory import GeppettoModelFactory
from pygeppetto.model.services.model_interpreter import ModelInterpreter
from pygeppetto.model.variables import Variable
from pynwb import NWBHDF5IO
from pynwb.image import IndexSeries
from pynwb.ophys import RoiResponseSeries
import nwb_explorer.utils.nwb_utils as nwb_utils


class NWBModelInterpreter(ModelInterpreter):

    def __init__(self):
        self.factory = GeppettoModelFactory()
        self.nwb_utils = None

    def importType(self, url, typeName, library, commonLibraryAccess):
        logging.debug('Creating a Geppetto Model')

        geppetto_model = self.factory.createGeppettoModel('GepettoModel')
        nwb_geppetto_library = pygeppetto.GeppettoLibrary(name='nwblib', id='nwblib')
        geppetto_model.libraries.append(nwb_geppetto_library)

        # read data
        io = NWBHDF5IO(url, 'r')
        nwbfile = io.read()
        self.nwb_utils = nwb_utils.NWBUtils(nwbfile)

        time_series_list = self.nwb_utils.get_timeseries()
        variables = []

        nwbType = pygeppetto.CompositeType(id=str('nwb'), name=str('nwb'), abstract=False)

        for i, time_series in enumerate(time_series_list):
            """
            Creates a group structure such as
            nwb.group1
            nwb.group2
            
            group1.time
            group1.stimulus
            
            group2.time
            group2.stimulus
            
            where each group entry contains the corresponding data from the nwb file. 
            """
            if isinstance(time_series,
                          (RoiResponseSeries, IndexSeries)):  # Assuming numerical time series only (Todo: for now)
                group = "group" + str(i)
                group_variable = Variable(id=group)
                group_type = pygeppetto.CompositeType(id=group, name=group, abstract=False)

                unit = time_series.unit
                timestamps_unit = time_series.timestamps_unit
                metatype = time_series.name

                mono_dimensional_timeseries_list = self.nwb_utils.get_mono_dimensional_timeseries(time_series.data[()])
                timestamps = [float(i) for i in time_series.timestamps[()]]

                time_series_time_variable = self.factory.createTimeSeries("time" + str(i), timestamps, timestamps_unit)
                group_type.variables.append(self.factory.createStateVariable("time", time_series_time_variable))

                # Todo: add importTypes
                for index, mono_dimensional_timeseries in enumerate(mono_dimensional_timeseries_list[:3]):
                    name = metatype + str(index)
                    time_series_variable = self.factory.createTimeSeries(name + "variable", mono_dimensional_timeseries,
                                                                         unit)
                    group_type.variables.append(self.factory.createStateVariable(name, time_series_variable))

                group_variable.types.append(group_type)
                variables.append(group_variable)
                nwb_geppetto_library.types.append(group_type)

                nwbType.variables.append(self.factory.createStateVariable(group))

        # add type to nwb
        nwb_geppetto_library.types.append(nwbType)

        # add top level variables
        nwb_variable = Variable(id='nwb')
        nwb_variable.types.append(nwbType)
        geppetto_model.variables.append(nwb_variable)
        for variable in variables:
            geppetto_model.variables.append(variable)

        return geppetto_model, nwbfile
        # Todo - Review: The geppetto_model and the nwbfile are needed under similar circunstances, would it be acceptable/interesting to have the second inside the first?

    def importValue(self, importValue):
        pass

    def getName(self):
        return "NWB Model Interpreter"

    def getDependentModels(self):
        return []
