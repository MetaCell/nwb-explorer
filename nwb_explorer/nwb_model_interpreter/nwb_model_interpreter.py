"""
netpyne_model_interpreter.py
Model interpreter for NWB. This class creates a geppetto type
"""
import base64
import logging
from io import BytesIO

import pygeppetto.model as pygeppetto
from PIL import Image as Img
from pygeppetto.model.types.types import TextType
from pygeppetto.model.model_factory import GeppettoModelFactory
from pygeppetto.model.values import Image, Text
from pygeppetto.model.variables import Variable, TypeToValueMap
from pygeppetto.services.model_interpreter import ModelInterpreter
from pygeppetto.utils import Singleton

from .nwb_reader import NWBReader
from .settings import *
from ..utils import guessUnits

from numpy import ndarray
from pynwb import TimeSeries
from pynwb.core import NWBBaseType
from pynwb.core import LabelledDict
from pynwb.file import Subject
from pynwb.core import DynamicTable
from pynwb.device import Device


class DefaultPyNWBToGeppettoMapper(object):
    ''' Extend this class to handle extra pynwb objects '''

    def __init__(self):
        self._supported_types = ( TimeSeries )

    @property
    def supported_types(self):
        ''' return the supported pynwb types '''
        return self._supported_types

    def assign_name_to_types(self, pynwb_obj):
        ''' Use this function to assign custom names to geppetto compositeTypes '''
        if isinstance(pynwb_obj, Subject):
            return 'map'

        elif isinstance(pynwb_obj, TimeSeries):
            return 'timeseries'

        elif isinstance(pynwb_obj, LabelledDict):
            if len(pynwb_obj) == 0:
                return None
            return pynwb_obj.label

        elif isinstance(pynwb_obj, ndarray):
            return None

        elif isinstance(pynwb_obj, set):
            return None

        elif isinstance(pynwb_obj, DynamicTable):
            return None

        elif isinstance(pynwb_obj, Device):
            return None

        else:
            return None

    def add_variables_to_type(self, pynwb_obj, geppetto_composite_type, geppetto_common_library_access):
        ''' Use this function to add variables to a geppetto compositeType '''
        
        if isinstance(pynwb_obj, TimeSeries):

            geppetto_composite_type.variables.append(
                geppetto_common_library_access.createStateVariable("time", geppetto_common_library_access.createImportValue()))
            
            geppetto_composite_type.variables.append(
                geppetto_common_library_access.createStateVariable('data', geppetto_common_library_access.createImportValue()))
            
            for key, value in pynwb_obj.fields.items():
                if isinstance(value, str):
                    geppetto_composite_type.variables.append(geppetto_common_library_access.createTextVariable(id=key, text=str(value)))

class Summary(object):
    ''' This is a custom Geppetto CompositeType that we want to have in the frontend.
        It collects information about the nwbfile '''
    def __init__(self, nwbfile):
        self._fields = self.build_fields(nwbfile)

    @property
    def fields(self):
        return self._fields

    def build_fields(self, nwbfile):
        ''' Use this function to add the fields you want to see in Geppetto model '''
        aqc = len(nwbfile.acquisition)
        stim = len(nwbfile.stimulus)
        summary = {}
        if aqc:
            summary['Num. of acquisitions'] = f"{aqc}"
        if stim:
            summary['Num. of stimulus'] = f"{stim}"
        
        return summary


class ExtendedPyNWBToGeppettoMapper(DefaultPyNWBToGeppettoMapper):
    ''' Add mappers for objects that are not present in pynwb but you want to have a compositeType 
        in geppetto for them. For example: aggregation data about number of acquisiton or stimulus'''

    def __init__(self):
        super(ExtendedPyNWBToGeppettoMapper, self).__init__()
        self._supported_types = ( self._supported_types, Summary )  # Add here your custom class

    def add_variables_to_type(self, pynwb_obj, geppetto_composite_type, geppetto_common_library_access):
        if isinstance(pynwb_obj, Summary):
            for key, value in pynwb_obj.fields.items():
                if isinstance(value, str):
                    geppetto_composite_type.variables.append(geppetto_common_library_access.createTextVariable(id=key, text=str(value)))
        else:
            super().add_variables_to_type(pynwb_obj, geppetto_composite_type, geppetto_common_library_access)


class GeppettoNwbCompositeTypeBuilder(object):
    def __init__(self, typename, nwb_reader, geppetto_model, commonLibraryAccess, nwb_geppetto_library,
                pynwb_to_geppetto_mapper=DefaultPyNWBToGeppettoMapper()):

        self.geppetto_model = geppetto_model
        self.nwb_geppetto_library = nwb_geppetto_library
        self.commonLibraryAccess = commonLibraryAccess
        self.nwb_reader = nwb_reader
        self.typename = typename
        self.pynwb_to_geppetto_mapper = pynwb_to_geppetto_mapper


    def build_geppetto_pynwb_type(self, id, obj, geppetto_type_name, parent_geppetto_type):
        ''' Scan pynwb object and create geppetto CompositeTypes and Variables with a recursive strategy '''
        obj_type = pygeppetto.CompositeType(id=((parent_geppetto_type.id + '.' if parent_geppetto_type and  parent_geppetto_type.id  else '') + id  ), name=geppetto_type_name, abstract=False)
        self.nwb_geppetto_library.types.append(obj_type)
        
        if isinstance(obj, self.pynwb_to_geppetto_mapper.supported_types):
            self.pynwb_to_geppetto_mapper.add_variables_to_type(obj, obj_type, self.commonLibraryAccess)

        else:
            if hasattr(obj, 'fields'):
                obj = obj.fields
            
            for key, value in obj.items():
                create_composite_type = self.pynwb_to_geppetto_mapper.assign_name_to_types(value)

                if isinstance(value, (str, int)):
                    obj_type.variables.append(self.commonLibraryAccess.createTextVariable(id=key, text=str(value)))
                                        
                if create_composite_type:
                    self.build_geppetto_pynwb_type(id=key,
                                                obj=value,
                                                geppetto_type_name=create_composite_type,
                                                parent_geppetto_type=obj_type)

        obj_variable = Variable(id=id, name=geppetto_type_name, types=(obj_type, ))
        parent_geppetto_type.variables.append(obj_variable)

    def build(self):
        self.build_geppetto_pynwb_type(id=self.typename,
                                    obj=self.nwb_reader.nwbfile, 
                                    geppetto_type_name=self.typename, 
                                    parent_geppetto_type=self.geppetto_model)

    # This is for custom compositeTypes that are not present in nwbfile object
    def extended_build(self):
        ''' Use this function to add objects to the Geppetto model that are not present in nwbfile '''
        parent_type = self.get_root_type()

        if parent_type:
            # This function will handle creation of compositeTypes in a recursive fashion.
            # Just make sure your mapper can handle the classes you define for obj.
            self.build_geppetto_pynwb_type(id='Summary', 
                                            obj=Summary(self.nwb_reader.nwbfile), 
                                            geppetto_type_name='map', 
                                            parent_geppetto_type=parent_type)

    def get_root_type(self):
        try:
            return self.geppetto_model.variables[0].types[0]
        except:
            return None


class NWBModelInterpreter(ModelInterpreter, metaclass=Singleton):

    def __init__(self):
        self.nwb_reader = None

    @staticmethod
    def clean_name_to_variable(group_name):
        return ''.join(c for c in group_name.replace(' ', '_') if c.isalnum() or c in '_')

    def get_nwbfile(self):
        return self.nwb_reader.nwbfile

    def createModel(self, nwbfile_or_path, typeName='nwb', library='nwblib'):
        logging.debug(f'Creating a Geppetto Model from {nwbfile_or_path}')


        geppetto_model = GeppettoModelFactory.createGeppettoModel('GeppettoModel')
        
        # FIXME the library should not be created here at every call
        nwb_geppetto_library = pygeppetto.GeppettoLibrary(name='nwblib', id='nwblib')
        
        geppetto_model.libraries.append(nwb_geppetto_library)
        commonLibraryAccess = GeppettoModelFactory(geppetto_model)
        self.nwb_reader = NWBReader(nwbfile_or_path)


        
        self.importType(typename='nwbfile',
                        nwb_reader=self.nwb_reader,
                        geppetto_model=geppetto_model,
                        commonLibraryAccess=commonLibraryAccess,
                        nwb_geppetto_library=nwb_geppetto_library,
                        pynwb_to_geppetto_mapper=ExtendedPyNWBToGeppettoMapper())

        return geppetto_model


    def importType(self, typename, nwb_reader, geppetto_model, commonLibraryAccess, nwb_geppetto_library, pynwb_to_geppetto_mapper):

        geppetto_types_builder = GeppettoNwbCompositeTypeBuilder(typename='nwbfile',
                                        nwb_reader=self.nwb_reader,
                                        geppetto_model=geppetto_model,
                                        commonLibraryAccess=commonLibraryAccess,             
                                        nwb_geppetto_library=nwb_geppetto_library,
                                        pynwb_to_geppetto_mapper=pynwb_to_geppetto_mapper)
        
        # build compositeTypes for pynwb objects
        geppetto_types_builder.build()

        # Build compositeTypes for custom objects that are not present in pynwb
        if hasattr(geppetto_types_builder, 'extended_build'):
            geppetto_types_builder.extended_build()


    def importValue(self, import_value_path):
        path_pieces = import_value_path.split(path_separator)
        var_to_extract = path_pieces[-1]
        time_series = self.nwb_reader.retrieve_from_path(path_pieces[1:-1])
        # Geppetto timeseries does not include the time axe; we are using the last path piece to determine whether we
        # are looking for time or data

        if var_to_extract == 'time':
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



    def extract_image_variable(self, metatype, plottable_timeseries):
        img = Img.fromarray(plottable_timeseries, 'RGB')
        data_bytes = BytesIO()
        img.save(data_bytes, 'PNG')
        data_str = base64.b64encode(data_bytes.getvalue()).decode('utf8')
        values = [Image(data=data_str)]
        md_time_series_variable = GeppettoModelFactory.createMDTimeSeries('', metatype + "variable", values)
        return md_time_series_variable

    def getName(self):
        return "NWB Model Interpreter"

    def getDependentModels(self):
        return []
