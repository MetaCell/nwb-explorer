"""
netpyne_model_interpreter.py
Model interpreter for NWB. This class creates a geppetto type
"""
import base64
import logging
from io import BytesIO

import pygeppetto.model as pygeppetto
from PIL import Image as Img
from pygeppetto.model.model_access import GeppettoModelAccess
from pygeppetto.model.types.types import TextType
from pygeppetto.model.model_factory import GeppettoModelFactory
from pygeppetto.model.values import Image, Text
from pygeppetto.model.variables import Variable, TypeToValueMap
from pygeppetto.services.model_interpreter import ModelInterpreter
from pygeppetto.utils import Singleton

from nwb_explorer.nwb_model_interpreter.nwb_geppetto_mappers import *
from .nwb_reader import NWBReader
from .settings import *
from ..utils import guessUnits

nwb_geppetto_mappers = [SubjectMapper, LabeledDictMapper, ImageSeriesMapper, TimeseriesMapper, SummaryNWBGeppettoMapper]


class GeppettoNwbCompositeTypeBuilder(object):

    def __init__(self, nwbfile_or_path, nwb_geppetto_library, model_access: GeppettoModelAccess):

        self.nwb_reader = NWBReader(nwbfile_or_path)
        self.model_factory = GeppettoModelFactory(model_access.geppetto_common_library)
        self.nwb_geppetto_library = nwb_geppetto_library
        self.geppetto_model = model_access.geppetto_model

    def build_geppetto_pynwb_type(self, variable_id, nwb_obj, parent_geppetto_type):
        ''' Scan pynwb object and create geppetto CompositeTypes and Variables with a recursive strategy '''
        obj_type = pygeppetto.CompositeType(
            id=((
                    parent_geppetto_type.id + '.' if parent_geppetto_type and parent_geppetto_type.id else '') + variable_id),
            name=None, abstract=False)
        self.nwb_geppetto_library.types.append(obj_type)

        for mapper in nwb_geppetto_mappers:
            if mapper.supports(nwb_obj):
                mapper.add_variables_to_type(nwb_obj, obj_type, self.model_factory)

        else:
            if hasattr(nwb_obj, 'fields'):
                nwb_obj = nwb_obj.fields

            for key, value in nwb_obj.items():


                if isinstance(value, (str, int)):
                    obj_type.variables.append(self.model_factory.createTextVariable(id=key, text=str(value)))

                else:
                    self.build_geppetto_pynwb_type(variable_id=key,
                                                   nwb_obj=value,
                                                   parent_geppetto_type=obj_type)

        if parent_geppetto_type is not None:
            obj_variable = Variable(id=variable_id, name=variable_id, types=(obj_type,))
            parent_geppetto_type.variables.append(obj_variable)
        return obj_type

    def build(self):
        type_name = 'nwbfile'

        return self.build_geppetto_pynwb_type(variable_id=type_name,
                                              nwb_obj=self.nwb_reader.nwbfile,
                                              geppetto_type_name=type_name,
                                              parent_geppetto_type=None)

    # builder for compositeTypes created from classes that are not present in pynwb (custom objects)
    def extended_build(self):
        ''' Use this method to add objects to the Geppetto model that are not present in nwbfile '''
        parent_type = self.get_root_type()

        if parent_type:
            # This function will handle creation of compositeTypes in a recursive fashion.
            # Just make sure your mapper can handle the classes you define for obj.
            self.build_geppetto_pynwb_type(variable_id='Summary',
                                           nwb_obj=Summary(self.nwb_reader.nwbfile),
                                           geppetto_type_name='map',
                                           parent_geppetto_type=parent_type)

    def get_root_type(self):
        try:
            return self.geppetto_model.variables[0].types[0]
        except:
            return None


class NWBModelInterpreter(ModelInterpreter):
    builders = {}

    def __init__(self, nwbfile_or_path):
        self.nwbfile_or_path = nwbfile_or_path
        self.nwb_reader = NWBReader(self.nwbfile_or_path)

    @staticmethod
    def clean_name_to_variable(group_name):
        return ''.join(c for c in group_name.replace(' ', '_') if c.isalnum() or c in '_')

    def get_nwbfile(self):
        return self.nwb_reader.nwbfile

    def importType(self, url, typeName, library, geppetto_model_access: GeppettoModelAccess):
        geppetto_model_builder = GeppettoNwbCompositeTypeBuilder(nwbfile_or_path=url, nwb_geppetto_library=library,
                                                                 model_access=geppetto_model_access)

        self.builders[library.id] = geppetto_model_builder

        # build compositeTypes for pynwb objects
        geppetto_model_builder.build()

    def importValue(self, import_value_path, model_access: GeppettoModelAccess):
        path_pieces = import_value_path.split(path_separator)
        var_to_extract = path_pieces[-1]
        time_series = self.nwb_reader.retrieve_from_path(path_pieces[1:-1])
        # Geppetto timeseries does not include the time axe; we are using the last path piece to determine whether we
        # are looking for time or data

        if var_to_extract in ['time', 'timestamps']:
            timestamps = NWBReader.get_timeseries_timestamps(time_series, MAX_SAMPLES)
            timestamps_unit = guessUnits(time_series.timestamps_unit) if hasattr(time_series,
                                                                                 'timestamps_unit') and time_series.timestamps_unit else 's'
            return GeppettoModelFactory.createTimeSeries("time_" + time_series.name,
                                                         timestamps,
                                                         timestamps_unit)
        else:

            plottable_timeseries = NWBReader.get_plottable_timeseries(time_series, MAX_SAMPLES)

            unit = guessUnits(time_series.unit)
            time_series_value = GeppettoModelFactory.createTimeSeries("data_" + time_series.name,
                                                                      plottable_timeseries[0],
                                                                      unit)
            return time_series_value

    # def extract_image_variable(self, metatype, plottable_timeseries): # pytest: no cover
    #     img = Img.fromarray(plottable_timeseries, 'RGB')
    #     data_bytes = BytesIO()
    #     img.save(data_bytes, 'PNG')
    #     data_str = base64.b64encode(data_bytes.getvalue()).decode('utf8')
    #     values = [Image(data=data_str)]
    #     md_time_series_variable = GeppettoModelFactory.createMDTimeSeries('', metatype + "variable", values)
    #     return md_time_series_variable

    def getName(self):
        return "NWB Model Interpreter"

    def getDependentModels(self):
        return []

    def get_image(self, name, interface, index):
        return self.nwb_reader.get_image(name, interface, index)
