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
from pynwb.image import ImageSeries
from pynwb.ophys import RoiResponseSeries
from pynwb import TimeSeries
import string

from .nwb_reader import NWBReader

SUPPORTED_TIME_SERIES_TYPES = (
    RoiResponseSeries, ImageSeries, TimeSeries)  # Assuming numerical or image time series only for now
MAX_SAMPLES = 1000


class NWBModelInterpreter(ModelInterpreter):

    def __init__(self):
        self.factory = GeppettoModelFactory()
        self.nwb_reader = None

    def get_nwbfile(self):
        return self.nwb_reader.nwbfile

    def importType(self, nwbfile_or_path, typeName, library, commonLibraryAccess):
        logging.debug('Creating a Geppetto Model')

        geppetto_model = self.factory.createGeppettoModel('GeppettoModel')
        nwb_geppetto_library = pygeppetto.GeppettoLibrary(name='nwblib', id='nwblib')
        geppetto_model.libraries.append(nwb_geppetto_library)

        nwbType = pygeppetto.CompositeType(id='nwb', name='nwb', abstract=False)
        nwb_geppetto_library.types.append(nwbType)

        # add top level variables
        nwb_variable = Variable(id='nwb')
        nwb_variable.types.append(nwbType)
        geppetto_model.variables.append(nwb_variable)
        # read data

        self.nwb_reader = NWBReader(nwbfile_or_path)

        time_series_list = self.nwb_reader.get_all_timeseries()
        variables = []

        for time_series in time_series_list:
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
            if isinstance(time_series, SUPPORTED_TIME_SERIES_TYPES):

                timeseries_path = self.nwb_reader.extract_time_series_path(
                    time_series)  # e.g. acquisition_[timeseriesname]
                group_name = '_'.join(timeseries_path) + '_{}'.format(time_series.name)
                group_name_clean = ''.join(c for c in group_name.replace(' ', '_') if c.isalnum() or c in '_')

                group_type = pygeppetto.CompositeType(id=group_name_clean, name=group_name_clean, abstract=False)
                nwb_geppetto_library.types.append(group_type)

                timeseries_variable = Variable(id=group_name_clean)
                timeseries_variable.types.append(group_type)
                variables.append(timeseries_variable)

                nwbType.variables.append(self.factory.createStateVariable(group_name_clean))


                try:

                    # TODO: add lazy fetching through importTypes

                    if isinstance(time_series, ImageSeries):
                        plottable_timeseries = NWBReader.get_timeseries_image_array(time_series)
                        md_time_series_variable = self.extract_image_variable('image', plottable_timeseries)
                        group_type.variables.append(self.factory.createStateVariable('image', md_time_series_variable))
                    else:



                        group_type.variables.append(self.factory.createStateVariable("time", self.factory.createImportValue()))

                        for index in range(NWBReader.get_timeseries_dimensions(time_series)):
                            name = 'data_' + str(index)


                            # Use ImportValue here instead than TimeSeries here for lazy loading
                            group_type.variables.append(self.factory.createStateVariable(name, self.factory.createImportValue()))

                except ValueError as e:
                    logging.error("Error loading timeseries: " + " -- ".join(e.args))
                    import traceback
                    traceback.print_exc()
                except NotImplementedError as e:
                    logging.error("Unsupported feature: " + " -- ".join(e.args))
                    import traceback
                    traceback.print_exc()

        # add type to nwb

        for variable in variables:
            geppetto_model.variables.append(variable)

        return geppetto_model

    def importValue(self, importValue):

        time_series = None # TODO retrieve the time series from the importValue path
        timestamps, plottable_timeseries = NWBReader.get_plottable_timeseries(time_series, MAX_SAMPLES)

        unit = time_series.unit
        timestamps_unit = time_series.timestamps_unit
        # time_series_time_variable = self.factory.createTimeSeries("time_" + time_series.name,
        #                                                           timestamps,
        #                                                           timestamps_unit)
        #
        # time_series_value = self.factory.createTimeSeries(name + "variable",
        #                                                   mono_dimensional_timeseries,
        #                                                   unit)


    def extract_image_variable(self, metatype, plottable_timeseries):
        img = Img.fromarray(plottable_timeseries, 'RGB')
        data_bytes = BytesIO()
        img.save(data_bytes, 'PNG')
        data_str = base64.b64encode(data_bytes.getvalue()).decode('utf8')
        values = [Image(data=data_str)]
        md_time_series_variable = self.factory.createMDTimeSeries(metatype + "variable", values)
        return md_time_series_variable



    def getName(self):
        return "NWB Model Interpreter"

    def getDependentModels(self):
        return []
