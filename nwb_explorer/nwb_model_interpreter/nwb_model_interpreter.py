"""
netpyne_model_interpreter.py
Model interpreter for NWB. This class creates a geppetto type
"""
import os
import logging

from pygeppetto.model import GeppettoLibrary
from pygeppetto.model.model_access import GeppettoModelAccess
from pygeppetto.model.model_factory import GeppettoModelFactory
from pygeppetto.services.model_interpreter import ModelInterpreter

from nwb_explorer.nwb_model_interpreter.nwb_geppetto_mappers import *
from .nwb_reader import NWBReader
from .settings import *
from ..utils import guess_units

from jupyter_geppetto import settings, PathService


def assign_name_to_type(pynwb_obj):
    ''' Use this function to assign custom names to geppetto compositeTypes '''
    return pynwb_obj.__class__.__name__


class NWBModelInterpreter(ModelInterpreter):

    def __init__(self, nwb_file_or_filename, source_url=None):
        if source_url == None:
            source_url = nwb_file_or_filename
        logging.info(f'Creating a Model Interpreter for {nwb_file_or_filename}')
        self.nwb_file_name = nwb_file_or_filename if isinstance(nwb_file_or_filename, str) else 'in-memory file'
        self.source_url = source_url
        self.nwb_reader = NWBReader(nwb_file_or_filename)
        self.library = GeppettoLibrary(name='nwbfile', id='nwbfile')

    @staticmethod
    def clean_name_to_variable(group_name):
        return ''.join(c for c in group_name.replace(' ', '_') if c.isalnum() or c in '_')

    def get_nwbfile(self):
        return self.nwb_reader.nwbfile

    def create_model(self):

        geppetto_model_access = GeppettoModelAccess('NWB File')
        geppetto_model = geppetto_model_access.geppetto_model

        geppetto_model.libraries.append(self.library)

        obj_type = ImportType(autoresolve=True, url=self.nwb_file_name, id="nwbfile", name='nwbfile')
        self.library.types.append(obj_type)
        obj_variable = Variable(id='nwbfile', name='nwbfile', types=(obj_type,))
        geppetto_model.variables.append(obj_variable)

        return geppetto_model

    def importType(self, url, type_name, library, geppetto_model_access: GeppettoModelAccess):
        logging.info(f"Importing type {type_name}, url: {url}")
        model_factory = GeppettoModelFactory(geppetto_model_access.geppetto_common_library)
        mapper = GenericCompositeMapper(model_factory, library)
        # build compositeTypes for pynwb objects
        root_type = mapper.create_type(self.get_nwbfile(), type_name=type_name, type_id=type_name)
        if isinstance(self.nwb_file_name, str) and type_name == 'nwbfile':

            root_type.variables.append(
                model_factory.create_url_variable(
                    id='source file',
                    url=self.source_url if 'http' in self.source_url else 'file://' + self.source_url
                )
            )
        return root_type

    def importValue(self, import_value: ImportValue):
        logging.info(f"Importing value {import_value.eContainer().eContainer().getPath()}")
        nwb_obj = ImportValueMapper.import_values[import_value]
        var_to_extract = import_value.eContainer().eContainer().id

        if isinstance(nwb_obj, TimeSeries):
            time_series = nwb_obj
            if var_to_extract in ['time', 'timestamps']:
                timestamps = NWBReader.get_timeseries_timestamps(time_series)
                if time_series.rate is not None:
                    for index, item in enumerate(timestamps):
                        timestamps[index] = ( timestamps[index] / time_series.rate / time_series.rate ) + time_series.starting_time
                timestamps_unit = guess_units(time_series.timestamps_unit) if hasattr(time_series,
                                                                                      'timestamps_unit') and time_series.timestamps_unit else 's'
                return GeppettoModelFactory.create_time_series(timestamps, timestamps_unit)
            else:

                plottable_timeseries = NWBReader.get_plottable_timeseries(time_series)

                unit = guess_units(time_series.unit)
                time_series_value = GeppettoModelFactory.create_time_series(plottable_timeseries[0], unit)
                if time_series.conversion is not None:
                    for index, item in enumerate(time_series_value.value):
                        time_series_value.value[index] = time_series_value.value[index] * time_series.conversion
                stringV = str(time_series_value)
                return time_series_value
        else:
            # TODO handle other possible ImportValue(s)
            pass

    def getName(self):
        return 'NWB Model Interpreter'

    # def extract_image_variable(self, metatype, plottable_timeseries): # pytest: no cover
    #     img = Img.fromarray(plottable_timeseries, 'RGB')
    #     data_bytes = BytesIO()
    #     img.save(data_bytes, 'PNG')
    #     data_str = base64.b64encode(data_bytes.getvalue()).decode('utf8')
    #     values = [Image(data=data_str)]
    #     md_time_series_variable = GeppettoModelFactory.createMDTimeSeries('', metatype + "variable", values)
    #     return md_time_series_variable

    def getDependentModels(self):
        return []

    def get_image(self, name, interface, index):
        return self.nwb_reader.get_image(name, interface, index)
