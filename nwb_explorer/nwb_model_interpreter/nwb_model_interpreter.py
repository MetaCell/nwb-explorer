"""
netpyne_model_interpreter.py
Model interpreter for NWB. This class creates a geppetto type
"""
import base64
import json
import logging
from io import BytesIO

import pygeppetto.model as pygeppetto
from PIL import Image as Img
from pygeppetto.model import GeppettoLibrary, ArrayValue
from pygeppetto.model.model_access import GeppettoModelAccess
from pygeppetto.model.types.types import TextType, ImportType
from pygeppetto.model.model_factory import GeppettoModelFactory
from pygeppetto.model.values import Image, Text, ImportValue
from pygeppetto.model.variables import Variable, TypeToValueMap
from pygeppetto.services.model_interpreter import ModelInterpreter
from pygeppetto.utils import Singleton
from pynwb import NWBContainer

from nwb_explorer.nwb_model_interpreter.nwb_geppetto_mappers import *
from .nwb_reader import NWBReader
from .settings import *
from ..utils import guess_units

nwb_geppetto_mappers = [SubjectMapper(), LabeledDictMapper(), ImageSeriesMapper(), TimeseriesMapper(), SummaryMapper()]


def assign_name_to_type(pynwb_obj):
    ''' Use this function to assign custom names to geppetto compositeTypes '''
    return pynwb_obj.__class__.__name__


class NWBModelFactory(GeppettoModelFactory):
    import_values = {}

    @classmethod
    def createImportValueAndCache(cls, nwb_object):
        iv = ImportValue()
        cls.import_values[iv] = nwb_object
        return iv


class GeppettoNwbCompositeTypeBuilder(object):
    created_types = {}
    def __init__(self, nwb_geppetto_library, model_access: GeppettoModelAccess):
        self.model_factory = NWBModelFactory(model_access.geppetto_common_library)
        self.nwb_geppetto_library = nwb_geppetto_library
        self.names = {}

    def get_obj_id(self, pynwb_obj):
        name = str(pynwb_obj.name if hasattr(pynwb_obj, 'name') else pynwb_obj.label)
        if not name:
            name = id(pynwb_obj)
        self.names[name] = 0 if name not in self.names else self.names[name] + 1
        return name + (str(self.names[name]) if self.names[name] else '')

    def build_geppetto_pynwb_type(self, pynwb_obj):
        if id(pynwb_obj) in self.created_types:
            return self.created_types[id(pynwb_obj)]
        obj_dict = pynwb_obj.fields if hasattr(pynwb_obj, 'fields') else pynwb_obj
        items = obj_dict.items()

        type_id = self.get_obj_id(pynwb_obj)


        obj_type = pygeppetto.CompositeType(
            id=type_id,
            name=assign_name_to_type(pynwb_obj), abstract=False)
        self.nwb_geppetto_library.types.append(obj_type)
        self.created_types[id(pynwb_obj)] = obj_type

        for key, value in items:
            if value is None:
                continue

            if isinstance(value, (ndarray, Dataset)):
                import_value = self.model_factory.createImportValueAndCache(pynwb_obj)
                obj_type.variables.append(
                    self.model_factory.createStateVariable(key, import_value))
            elif isinstance(value, (str, int, float, bool)):  # Meta data
                obj_type.variables.append(self.model_factory.createTextVariable(id=key, text=str(value)))
            elif isinstance(value, (list, tuple, set)):
                pass
                # obj_type.variables.append(self.model_factory.createTextVariable(id=key, name='json_array', text=json.dumps([v for v in value])))
            elif hasattr(pynwb_obj, 'fields') or hasattr(pynwb_obj, 'items'):
                newtype = self.build_geppetto_pynwb_type(pynwb_obj=value)
                obj_variable = Variable(id=key, name=key, types=(newtype,))
                obj_type.variables.append(obj_variable)

        for mapper in nwb_geppetto_mappers:
            if mapper.supports(pynwb_obj):
                mapper.add_variables_to_type(pynwb_obj, obj_type, self.model_factory)

        return obj_type


class NWBModelInterpreter(ModelInterpreter):

    def __init__(self, nwb_file_name):
        logging.info(f'Creating a Model Interpreter for {nwb_file_name}')
        self.nwb_reader = NWBReader(nwb_file_name)
        self.library = GeppettoLibrary(name=str(nwb_file_name), id=str(nwb_file_name))

    @staticmethod
    def clean_name_to_variable(group_name):
        return ''.join(c for c in group_name.replace(' ', '_') if c.isalnum() or c in '_')

    def get_nwbfile(self):
        return self.nwb_reader.nwbfile

    def create_model(self):

        geppetto_model_access = GeppettoModelAccess('NWB File')
        geppetto_model = geppetto_model_access.geppetto_model

        geppetto_model.libraries.append(self.library)

        obj_type = ImportType(autoresolve=True)
        self.library.types.append(obj_type)
        obj_variable = Variable(id='nwbfile', name='nwbfile', types=(obj_type,))
        geppetto_model.variables.append(obj_variable)

        return geppetto_model

    def importType(self, url, typeName, library, geppetto_model_access: GeppettoModelAccess):

        geppetto_model_builder = GeppettoNwbCompositeTypeBuilder(nwb_geppetto_library=library,
                                                                 model_access=geppetto_model_access)

        # build compositeTypes for pynwb objects
        return geppetto_model_builder.build_geppetto_pynwb_type(self.get_nwbfile())

    def importValue(self, import_value: ImportValue):

        nwb_obj = NWBModelFactory.import_values[import_value]
        var_to_extract = import_value.eContainer().eContainer().id

        if isinstance(nwb_obj, TimeSeries):
            time_series = nwb_obj
            if var_to_extract in ['time', 'timestamps']:
                timestamps = NWBReader.get_timeseries_timestamps(time_series)
                timestamps_unit = guess_units(time_series.timestamps_unit) if hasattr(time_series,
                                                                                      'timestamps_unit') and time_series.timestamps_unit else 's'
                return GeppettoModelFactory.createTimeSeries("time_" + time_series.name,
                                                             timestamps,
                                                             timestamps_unit)
            else:

                plottable_timeseries = NWBReader.get_plottable_timeseries(time_series)

                unit = guess_units(time_series.unit)
                time_series_value = GeppettoModelFactory.createTimeSeries("data_" + time_series.name,
                                                                          plottable_timeseries[0],
                                                                          unit)
                return time_series_value

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
