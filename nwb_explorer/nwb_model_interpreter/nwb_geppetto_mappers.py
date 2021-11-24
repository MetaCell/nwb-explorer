import logging
import sys
import numpy as np
from h5py.h5r import Reference
from pygeppetto.model import Pointer, GenericArray, PointerElement

from pynwb import TimeSeries
from hdmf.common import ElementIdentifiers, VectorData
from pynwb.core import LabelledDict
from pynwb.file import Subject
from pynwb.core import DynamicTable
from pynwb.device import Device
from pynwb.image import ImageSeries
from h5py import Dataset

from pygeppetto.model.types.types import TextType, ImportType, CompositeType

from pygeppetto.model.values import Image, Text, ImportValue, StringArray
from pygeppetto.model.variables import Variable, TypeToValueMap

nwb_geppetto_mappers = []


def is_metadata(value):
    return isinstance(value, (str, int, float, bool, bytes, np.number))


def is_collection(value):
    return isinstance(value, (list, tuple, set))


def is_array(value):
    return isinstance(value, (np.ndarray, Dataset))


def is_multidimensional_data(value):
    """ Use this function to decide whether to split up the data into multiple rows or not """
    image_types = ('ImageSeries', 'OpticalSeries', 'TwoPhotonSeries', 'ImageMaskSeries', 'VectorData')
    return hasattr(value, 'data') and  hasattr(value, 'neurodata_type') and value.data is not None and len(value.data.shape) > 1 and not(
            value.neurodata_type in image_types)


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
    created_variables = {}
    created_types = {}

    generic = False  # A generic mapper indicates that the type is not fully supported

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


class GenericCompositeMapper(NWBGeppettoMapper):
    generic = True
    excluded_types = (ElementIdentifiers, VectorData)

    def __init__(self, model_factory, nwb_geppetto_library):
        super().__init__(model_factory, nwb_geppetto_library)
        self.mappers = tuple(m(model_factory, nwb_geppetto_library) for m in nwb_geppetto_mappers)
        self.type_ids = {}

    def assign_name_to_type(self, pynwb_obj):
        ''' Use this function to assign custom names to geppetto compositeTypes '''
        return pynwb_obj.__class__.__name__

    def creates(self, pynwb_obj):
        ''' return the supported pynwb types '''
        return hasattr(pynwb_obj, 'fields') and type(pynwb_obj) and not any(
            mapper.creates(pynwb_obj) for mapper in self.mappers if mapper != self)

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
        if id(pynwb_obj) in self.created_types and not is_multidimensional_data(pynwb_obj):
            return self.created_types[id(pynwb_obj)]
        obj_type = CompositeType(id=type_id, name=type_name, abstract=False)

        self.nwb_geppetto_library.types.append(obj_type)
        self.created_types[id(pynwb_obj)] = obj_type

        for mapper in self.mappers:
            if mapper.modifies(pynwb_obj):
                try:
                    mapper.modify_type(pynwb_obj, obj_type)
                except Exception as e:
                    logging.error(e, exc_info=True)
                    UnsupportedMapper.handle_unsupported(obj_type, self.model_factory, 'unsupported')

        return obj_type

    def create_variable(self, name, pynwb_obj, parent_obj):
        if id(pynwb_obj) in self.created_variables:
            variable = self.created_variables[id(pynwb_obj)]
            return self.model_factory.create_pointer_variable(id=name,
                                                              initialValue=Pointer(elements=[
                                                                  PointerElement(variable=variable,
                                                                                 type=variable.types[0])])
                                                              )
        type_id = self.generate_obj_id(pynwb_obj)

        type_name = self.assign_name_to_type(pynwb_obj)

        obj_type = self.create_type(pynwb_obj, type_id, type_name, )

        return Variable(id=name, name=name, types=(obj_type,))

    def modify_type(self, pynwb_obj, obj_type):
        items = self.get_object_items(pynwb_obj)

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

            if is_multidimensional_data(value):
                for index in range(value.data.shape[1]):  # loop through data rows to make separate variables
                    name = f"{self.sanitize(key)}_row{index:02}"  # pad row name so ordered correctly in list view
                    variable = supportingmapper.create_variable(name, value, pynwb_obj)
                    self.created_variables[id(value.data[:, index])] = variable
                    obj_type.variables.append(variable)
            elif is_multidimensional_data(pynwb_obj) and key == 'data':
                continue  # create data variable in TimeSeriesMapper.modify_type instead
            else:
                variable = supportingmapper.create_variable(self.sanitize(key), value, pynwb_obj)
                self.created_variables[id(value)] = variable
                obj_type.variables.append(variable)

    def get_object_items(self, pynwb_obj):
        obj_dict = pynwb_obj.fields if hasattr(pynwb_obj, 'fields') else pynwb_obj
        if hasattr(obj_dict, 'items'):
            items = obj_dict.items()
        elif is_collection(obj_dict):
            items = tuple((obj_dict[k].name, obj_dict[k]) for k in range(len(obj_dict)) if hasattr(obj_dict[k], "name"))
        else:
            items = ()
        return items

    def sanitize(self, key):
        return ''.join(k if k.isalnum() else '_' for k in key)


class CompositeListMapper(GenericCompositeMapper):
    """We are mapping lists of complex objects to CompositeType due to missing functionality in setting complex array values"""
    generic = True
    @classmethod
    def creates(cls, pynwb_obj):
        return is_collection(pynwb_obj) and pynwb_obj and not is_metadata(next(iter(pynwb_obj)))

    def assign_name_to_type(self, pynwb_obj):
        ''' Use this function to assign custom names to geppetto compositeTypes '''
        return "CompositeList"

    def generate_obj_id(self, pynwb_obj):
        return self.single_id(self.assign_name_to_type(pynwb_obj))


class LabelledDictMapper(GenericCompositeMapper):

    def creates(self, pynwb_obj):
        return isinstance(pynwb_obj, LabelledDict)

    def generate_obj_id(self, pynwb_obj):
        return self.single_id(pynwb_obj.label.replace(' ', '_'))


class DynamicTableMapper(GenericCompositeMapper):
    generic = True

    def creates(self, pynwb_obj):
        return isinstance(pynwb_obj, DynamicTable)

    # def modify_type(self, pynwb_obj: DynamicTable, obj_type):
    #     obj_dict = pynwb_obj.fields if hasattr(pynwb_obj, 'fields') else pynwb_obj
    #
    #     array_mapper = SimpleArrayMapper(self.model_factory, self.nwb_geppetto_library)
    #     obj_type.variables.append(array_mapper.create_variable(, value, pynwb_obj))
    #     for key, value in items:
    #         if value is None:
    #             continue
    #         try:
    #             supportingmapper = next(m for m in self.mappers if m.creates(value))
    #         except StopIteration:
    #             # TODO handle Unsupported
    #             # obj_type.variables.append(mapper.create_variable(key, value))
    #
    #             if value:
    #                 logging.debug(f'No mappers are defined for: {value}')
    #             continue


class SimpleArrayMapper(NWBGeppettoMapper):
    generic = True

    @classmethod
    def creates(cls, value):
        ''' return the supported pynwb types '''
        return is_collection(value) and value and is_metadata(next(iter(value)))

    def create_variable(self, name, pynwb_obj, parent_obj):
        if any(hasattr(pynwb_obj[k],'decode') for k in range(len(pynwb_obj))):
            obj = tuple(pynwb_obj[k].decode() for k in range(len(pynwb_obj)) if hasattr(pynwb_obj[k],'decode'))
        else:
            obj = pynwb_obj
        value = StringArray(tuple(str(v) for v in obj))
        array_variable = self.model_factory.create_simple_array_variable(name, value)
        return array_variable

class VectorDataMapper(NWBGeppettoMapper):

    def creates(self, pynwb_obj):
        return isinstance(pynwb_obj, VectorData)

    def create_variable(self, name, pynwb_obj, parent_obj):
        return self.create_variable_base(name, tuple(self.get_value(v) for v in pynwb_obj.data[()]))

    def create_variable_base(self, name, pynwb_obj):
        value = GenericArray(v for v in pynwb_obj)
        array_variable = self.model_factory.create_simple_array_variable(name, value)
        return array_variable

    def get_value(self, v):
        if is_metadata(v):
            if hasattr(v, 'decode'):
                return Text(str(v.decode()))
            return Text(str(v))
        if id(v) in self.created_variables:
            return Pointer(path=self.created_variables[id(v)].getPath())
        if hasattr(v, 'name'):
            return Text(v.name)
        return Text(str(v))


class TimeseriesMapper(GenericCompositeMapper):
    ''' Extend this class to handle extra pynwb objects '''

    def creates(self, pynwb_obj):
        ''' return the supported pynwb types '''
        return isinstance(pynwb_obj, TimeSeries)

    def modifies(self, pynwb_obj):
        ''' return the supported pynwb types '''
        return isinstance(pynwb_obj, TimeSeries)

    def modify_type(self, pynwb_obj, geppetto_composite_type):
        super().modify_type(pynwb_obj, geppetto_composite_type)
        ''' Use this function to add variables to a geppetto compositeType '''
        if pynwb_obj.timestamps is None:
            geppetto_composite_type.variables.append(
                self.model_factory.create_state_variable(id="timestamps",
                                                         initialValue=ImportValueMapper.create_import_value(pynwb_obj)))

        if pynwb_obj.timestamp_link:  # A set with linked timestamps
            variable = self.model_factory.create_text_variable(id="timestamp_link",
                                                               text=next(iter(pynwb_obj.timestamp_link)).name)
            geppetto_composite_type.variables.append(variable)

        if is_multidimensional_data(pynwb_obj):  # if multidimensional data, select data from relevant row
            index = self.type_ids[pynwb_obj.name]
            timeseries_dict = {**pynwb_obj.fields, 'data': pynwb_obj.data[:, index]}
            import_val = ImportValueMapper.create_import_value(timeseries_dict)
            variable = self.model_factory.create_state_variable(id="data", initialValue=import_val)
            geppetto_composite_type.variables.append(variable)

            message = f"contains values from row {index} of {pynwb_obj.name}"
            UnsupportedMapper.handle_unsupported(geppetto_composite_type, self.model_factory, message)

    def get_object_items(self, pynwb_obj):
        return ((key, value) for key, value in super().get_object_items(pynwb_obj) if key != 'timestamp_link')


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
            summary['Num. of stimuli'] = f"{stim}"

        return summary

    def modify_type(self, pynwb_obj, geppetto_composite_type):
        for key, value in self.build_fields(pynwb_obj).items():
            if isinstance(value, str):
                geppetto_composite_type.variables.append(
                    self.model_factory.create_text_variable(id=key, text=str(value)))


class UnsupportedMapper(GenericCompositeMapper):

    def creates(self, pynwb_obj):
        return False

    def modifies(self, pynwb_obj):
        return False  # not any(mapper.creates(pynwb_obj) for mapper in self.mappers if not mapper.generic)

    @staticmethod
    def handle_unsupported(geppetto_composite_type, model_factory, message='partially supported'):
        try:
            description_variable = next(
                variable for variable in geppetto_composite_type.variables if variable.name == 'description')
            description_variable.initialValues[0].value.text += ' (' + message + ')'
        except StopIteration:
            geppetto_composite_type.variables.append(
                model_factory.create_text_variable(id='description', text=message))

    def modify_type(self, pynwb_obj, geppetto_composite_type):
        ''' Use this function to add variables to a geppetto compositeType '''
        self.handle_unsupported(geppetto_composite_type, self.model_factory)
