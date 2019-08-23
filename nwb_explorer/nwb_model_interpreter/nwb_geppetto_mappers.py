import logging
import sys
import numpy as np
from numpy import ndarray
from pynwb import TimeSeries
from pynwb.core import NWBBaseType
from pynwb.core import LabelledDict
from pynwb.file import Subject
from pynwb.core import DynamicTable
from pynwb.device import Device
from pynwb.image import ImageSeries
from h5py import Dataset

import numpy

from pygeppetto.model.types.types import TextType, ImportType, CompositeType

from pygeppetto.model.values import Image, Text, ImportValue, StringArray
from pygeppetto.model.variables import Variable, TypeToValueMap

nwb_geppetto_mappers = []


def is_metadata(value):
    return isinstance(value, (str, int, float, bool, numpy.number))


def is_collection(value):
    return isinstance(value, (list, tuple, set))


def is_array(value):
    return isinstance(value, (ndarray, Dataset))


def is_composite(pynwb_obj):
    return hasattr(pynwb_obj, 'fields')


class MapperType(type):
    """Metaclass for mappers: control instances and classes"""
    instances = {}

    def __init__(cls, name, bases, dct):
        super().__init__(name, bases, dct)
        if cls.__name__ != 'NWBGeppettoMapper':
            nwb_geppetto_mappers.append(cls)

            MapperType.instances[cls] = {}

    def __call__(cls, model_factory, nwb_geppetto_library):
        """Control instances. We want the same instance for the same library"""

        key = id(model_factory)
        if key not in MapperType.instances[cls]:
            obj = cls.__new__(cls, model_factory, nwb_geppetto_library)
            MapperType.instances[cls][key] = obj
            obj.__init__(model_factory, nwb_geppetto_library)

        return MapperType.instances[cls][key]


class NWBGeppettoMapper(metaclass=MapperType):

    def __init__(self, model_factory, nwb_geppetto_library):
        self.model_factory = model_factory
        self.nwb_geppetto_library = nwb_geppetto_library

    def creates(self, value):
        return False

    def modifies(self, value):
        return False


class MetadataMapper(NWBGeppettoMapper):

    def creates(self, value):
        ''' return the supported pynwb types '''
        return is_metadata(value)

    def create_variable(self, name, pynwb_obj, parent_obj):
        return self.model_factory.create_text_variable(id=name, text=str(pynwb_obj))


class ImportValueMapper(NWBGeppettoMapper):

    def creates(self, value):
        ''' return the supported pynwb types '''
        return is_array(value)

    import_values = {}

    @classmethod
    def create_import_value(cls, nwb_object):
        iv = ImportValue()
        cls.import_values[iv] = nwb_object
        return iv

    def create_variable(self, name, pynwb_obj, parent_obj):
        return self.model_factory.create_state_variable(id=name, initialValue=self.create_import_value(parent_obj))


class CompositeMapper(NWBGeppettoMapper):
    priority = 0

    created_types = {}

    def __init__(self, model_factory, nwb_geppetto_library):
        super().__init__(model_factory, nwb_geppetto_library)
        self.mappers = tuple(m(model_factory, nwb_geppetto_library) for m in nwb_geppetto_mappers)
        self.type_ids = {}

    def assign_name_to_type(self, pynwb_obj):
        ''' Use this function to assign custom names to geppetto compositeTypes '''
        return pynwb_obj.__class__.__name__

    @classmethod
    def creates(cls, pynwb_obj):
        ''' return the supported pynwb types '''
        return is_composite(pynwb_obj)

    def modifies(self, pynwb_obj):
        return self.creates(pynwb_obj)

    def single_id(self, obj_id):
        if obj_id in self.type_ids:
            self.type_ids[obj_id] += 1
            obj_id = obj_id + str(self.type_ids[obj_id])
        else:
            self.type_ids[obj_id] = 0
        return obj_id

    def generate_obj_id(self, pynwb_obj):
        if hasattr(pynwb_obj, 'name'):
            obj_id = str(pynwb_obj.name)
        else:
            obj_id = str(id(pynwb_obj))

        return self.single_id(obj_id)

    def create_type(self, pynwb_obj, type_id=None, type_name=None):
        if id(pynwb_obj) in self.created_types:
            return self.created_types[id(pynwb_obj)]
        obj_type = CompositeType(id=type_id, name=type_name, abstract=False)

        self.nwb_geppetto_library.types.append(obj_type)
        self.created_types[id(pynwb_obj)] = obj_type

        for mapper in self.mappers:
            if mapper.modifies(pynwb_obj):
                mapper.modify_type(pynwb_obj, obj_type)

        return obj_type

    def create_variable(self, name, pynwb_obj, parent_obj):

        type_id = self.generate_obj_id(pynwb_obj)

        type_name = self.assign_name_to_type(pynwb_obj)

        obj_type = self.create_type(pynwb_obj, type_id, type_name, )

        return Variable(id=name, name=name, types=(obj_type,))

    def modify_type(self, pynwb_obj, obj_type):
        obj_dict = pynwb_obj.fields if hasattr(pynwb_obj, 'fields') else pynwb_obj

        if hasattr(obj_dict, 'items'):
            items = obj_dict.items()
        elif is_collection(obj_dict):
            items = ((str(k), obj_dict[k]) for k in range(len(obj_dict)))
        else:
            items = ()

        for key, value in items:
            if value is None:
                continue
            try:
                supportingmapper = next(m for m in self.mappers if m.creates(value))
            except StopIteration:
                # TODO handle Unsupported
                # obj_type.variables.append(mapper.create_variable(key, value))
                if value:
                    logging.debug(f'No mappers are defined for: {value}')
                continue

            obj_type.variables.append(supportingmapper.create_variable(key, value, pynwb_obj))


class CompositeListMapper(CompositeMapper):
    """We are mapping lists od complex objects to CompositeType due to missing functionality in setting complex array values"""

    @classmethod
    def creates(cls, pynwb_obj):
        return is_collection(pynwb_obj) and pynwb_obj and not is_metadata(next(iter(pynwb_obj)))

    def assign_name_to_type(self, pynwb_obj):
        ''' Use this function to assign custom names to geppetto compositeTypes '''
        return "CompositeList"

    def generate_obj_id(self, pynwb_obj):
        return self.single_id(self.assign_name_to_type(pynwb_obj))


class LabelledDictMapper(CompositeMapper):

    @classmethod
    def creates(cls, pynwb_obj):
        return isinstance(pynwb_obj, LabelledDict)

    def assign_name_to_type(self, pynwb_obj):
        ''' Use this function to assign custom names to geppetto compositeTypes '''
        return pynwb_obj.label

    def generate_obj_id(self, pynwb_obj):
        return self.single_id(pynwb_obj.label)


class SimpleArrayMapper(NWBGeppettoMapper):

    @classmethod
    def creates(cls, value):
        ''' return the supported pynwb types '''
        return is_collection(value) and value and is_metadata(next(iter(value)))

    def create_variable(self, name, pynwb_obj, parent_obj):
        value = StringArray(str(v) for v in pynwb_obj)
        array_variable = self.model_factory.create_simple_array_variable(name, value)
        return array_variable


class SubjectMapper(NWBGeppettoMapper):
    ''' Add mappers for objects that are not present in pynwb but you want to have a compositeType
        in Geppetto model for them. For example: aggregation data about number of acquisiton or stimulus'''

    def modifies(self, pynwb_obj):
        ''' return the supported pynwb types '''
        return isinstance(pynwb_obj, Subject)

    def modify_type(self, pynwb_obj, geppetto_composite_type):
        geppetto_composite_type.name = 'map'


class TimeseriesMapper(NWBGeppettoMapper):
    ''' Extend this class to handle extra pynwb objects '''

    def modifies(self, pynwb_obj):
        ''' return the supported pynwb types '''
        return isinstance(pynwb_obj, TimeSeries)

    def modify_type(self, pynwb_obj, geppetto_composite_type):
        ''' Use this function to add variables to a geppetto compositeType '''
        if pynwb_obj.timestamps is None:
            geppetto_composite_type.variables.append(
                self.model_factory.create_state_variable(id="timestamps",
                                                         initialValue=ImportValueMapper.create_import_value(pynwb_obj)))




class ImageSeriesMapper(NWBGeppettoMapper):

    def modifies(self, pynwb_obj):
        ''' return the supported pynwb types '''
        return isinstance(pynwb_obj, ImageSeries)

    def modify_type(self, pynwb_obj, geppetto_composite_type):
        ''' Use this function to add variables to a geppetto compositeType '''

        geppetto_composite_type.variables.append(
            self.model_factory.create_text_variable(id='num_samples', text=str(len(pynwb_obj.timestamps))))

class SummaryMapper(NWBGeppettoMapper):
    ''' Add mappers for objects that are not present in pynwb but you want to have a compositeType
        in Geppetto model for them. For example: aggregation data about number of acquisiton or stimulus'''

    def modifies(self, pynwb_obj):
        ''' return the supported pynwb types '''
        return hasattr(pynwb_obj, 'acquisition')

    def build_fields(self, nwbfile):
        ''' Use this function to add the fields you want to see in the Geppetto model '''
        aqc = len(nwbfile.acquisition)
        stim = len(nwbfile.stimulus)
        summary = {}
        if aqc:
            summary['Num. of acquisitions'] = f"{aqc}"
        if stim:
            summary['Num. of stimulus'] = f"{stim}"

        return summary

    def modify_type(self, pynwb_obj, geppetto_composite_type):
        for key, value in self.build_fields(pynwb_obj).items():
            if isinstance(value, str):
                geppetto_composite_type.variables.append(
                    self.model_factory.create_text_variable(id=key, text=str(value)))
