"""
netpyne_model_interpreter.py
Model interpreter for NWB. This class creates a geppetto type
"""
import base64
import logging
from io import BytesIO

import pygeppetto.model as pygeppetto
from PIL import Image as Img
from pygeppetto.model.model_factory import GeppettoModelFactory
from pygeppetto.model.services.model_interpreter import ModelInterpreter
from pygeppetto.model.values import Image
from pygeppetto.model.variables import Variable
from pynwb import NWBHDF5IO
from pynwb.image import ImageSeries
from pynwb.ophys import RoiResponseSeries

import nwb_explorer.utils.nwb_utils as nwb_utils


class NWBModelInterpreter(ModelInterpreter):

    def __init__(self):
        self.factory = GeppettoModelFactory()
        self.nwb_utils = None

    def importType(self, nwbfile_path, typeName, library, commonLibraryAccess):
        logging.debug('Creating a Geppetto Model')

        geppetto_model = self.factory.createGeppettoModel('GepettoModel')
        nwb_geppetto_library = pygeppetto.GeppettoLibrary(name='nwblib', id='nwblib')
        geppetto_model.libraries.append(nwb_geppetto_library)

        # read data
        try:
            self.nwb_utils = nwb_utils.NWBUtils(nwbfile_path)
        except ValueError:
            return None

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
                          (RoiResponseSeries, ImageSeries)):  # Assuming numerical or image time series only for now
                group = "group" + str(i)
                group_variable = Variable(id=group)
                group_type = pygeppetto.CompositeType(id=group, name=group, abstract=False)

                unit = time_series.unit
                timestamps_unit = time_series.timestamps_unit
                metatype = time_series.name

                timestamps = [float(i) for i in time_series.timestamps[()]]
                time_series_time_variable = self.factory.createTimeSeries("time" + str(i), timestamps, timestamps_unit)
                group_type.variables.append(self.factory.createStateVariable("time", time_series_time_variable))

                plottable_timeseries = self.nwb_utils.get_plottable_timeseries(time_series)

                # Todo: add importTypes

                if isinstance(time_series, ImageSeries):
                    img = Img.fromarray(plottable_timeseries, 'RGB')
                    data_bytes = BytesIO()
                    img.save(data_bytes, 'PNG')
                    data_str = base64.b64encode(data_bytes.getvalue()).decode('utf8')
                    values = [Image(data=data_str)]
                    md_time_series_variable = self.factory.createMDTimeSeries(metatype + "variable", values)
                    group_type.variables.append(self.factory.createStateVariable(metatype, md_time_series_variable))
                else:
                    for index, mono_dimensional_timeseries in enumerate(plottable_timeseries[:3]): #Todo: [:3] for development purposes while importTypes not implemented
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

        return geppetto_model

    def importValue(self, importValue):
        pass

    def getName(self):
        return "NWB Model Interpreter"

    def getDependentModels(self):
        return []
