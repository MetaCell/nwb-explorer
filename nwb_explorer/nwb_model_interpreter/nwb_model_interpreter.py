"""
netpyne_model_interpreter.py
Model interpreter for NWB. This class creates a geppetto type
"""

import logging

import numpy


from pygeppetto.model import GeppettoLibrary, ArrayValue
from pygeppetto.model.model_access import GeppettoModelAccess
from pygeppetto.model.types.types import TextType, ImportType, CompositeType
from pygeppetto.model.model_factory import GeppettoModelFactory
from pygeppetto.model.values import Image, Text, ImportValue, StringArray
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
        self.type_ids = {}

    def generate_obj_id(self, pynwb_obj):
        if hasattr(pynwb_obj, 'name'):
            obj_id = str(pynwb_obj.name)
        elif hasattr(pynwb_obj, 'label'):
            obj_id = pynwb_obj.label
        else:
            obj_id = str(id(pynwb_obj))
        self.type_ids[obj_id] = 0 if obj_id not in self.type_ids else self.type_ids[obj_id] + 1
        return obj_id + (str(self.type_ids[obj_id]) if self.type_ids[obj_id] else '')

    @staticmethod
    def is_collection(value):
        return isinstance(value, (list, tuple, set))

    @staticmethod
    def is_array(value):
        return isinstance(value, (ndarray, Dataset))

    @staticmethod
    def is_metadata(value):
        return isinstance(value, (str, int, float, bool, numpy.number))

    @staticmethod
    def is_composite(pynwb_obj):
        return hasattr(pynwb_obj, 'fields') or hasattr(pynwb_obj, 'items')

    def build_geppetto_pynwb_type(self, pynwb_obj, type_name=None, type_id=None):
        if id(pynwb_obj) in self.created_types:
            return self.created_types[id(pynwb_obj)]

        if type_id is None:
            type_id = self.generate_obj_id(pynwb_obj)
        if type_name is None:
            type_name = assign_name_to_type(pynwb_obj)

        obj_type = CompositeType(
            id=type_id,
            name=type_name, abstract=False)

        self.nwb_geppetto_library.types.append(obj_type)
        self.created_types[id(pynwb_obj)] = obj_type

        return self.fill_composite_type(obj_type, pynwb_obj)

    def fill_composite_type(self, obj_type: CompositeType, pynwb_obj):
        obj_dict = pynwb_obj.fields if hasattr(pynwb_obj, 'fields') else pynwb_obj

        if hasattr(obj_dict, 'items'):
            items = obj_dict.items()
        elif self.is_collection(obj_dict):
            items = ((str(k), obj_dict[k]) for k in range(len(obj_dict)))
        else:
            items = ()


        for key, value in items:
            if value is None:
                continue

            if self.is_array(value):
                import_value = self.model_factory.createImportValueAndCache(pynwb_obj)
                obj_type.variables.append(
                    self.model_factory.create_state_variable(key, import_value))
            elif self.is_metadata(value):  # Meta data
                obj_type.variables.append(self.model_factory.create_text_variable(id=key, text=str(value)))
            elif self.is_collection(value) and len(value):
                an_element = value[0]
                if (self.is_composite(an_element)):
                    newtype = self.build_geppetto_pynwb_type(pynwb_obj=value,
                                                             type_id=self.generate_obj_id(pynwb_obj) + '.' + key)
                    obj_variable = Variable(id=key, name=key, types=(newtype,))
                    obj_type.variables.append(obj_variable)
                elif self.is_metadata(an_element):
                    value = StringArray(str(v) for v in value)
                    array_variable = self.model_factory.create_simple_array_variable(key, value)
                    obj_type.variables.append(array_variable)

                # obj_type.variables.append(self.model_factory.createTextVariable(id=key, name='json_array', text=json.dumps([v for v in value])))
            elif self.is_composite(pynwb_obj):
                newtype = self.build_geppetto_pynwb_type(pynwb_obj=value)
                obj_variable = Variable(id=key, name=key, types=(newtype,))
                obj_type.variables.append(obj_variable)
            else:
                logging.debug(f'Unsupported type found in nwb: {pynwb_obj.__class__.__name__}')

        for mapper in nwb_geppetto_mappers:
            if mapper.supports(pynwb_obj):
                mapper.add_variables_to_type(pynwb_obj, obj_type, self.model_factory)

        return obj_type


class NWBModelInterpreter(ModelInterpreter):

    def __init__(self, nwb_file_name):
        logging.info(f'Creating a Model Interpreter for {nwb_file_name}')
        self.nwb_reader = NWBReader(nwb_file_name)
        self.library = GeppettoLibrary(name='nwblib', id='nwblib')

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
                return GeppettoModelFactory.create_time_series(timestamps, timestamps_unit)
            else:

                plottable_timeseries = NWBReader.get_plottable_timeseries(time_series)

                unit = guess_units(time_series.unit)
                time_series_value = GeppettoModelFactory.create_time_series(plottable_timeseries[0], unit)
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
