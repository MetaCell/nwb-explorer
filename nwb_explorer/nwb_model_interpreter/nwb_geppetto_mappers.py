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


class NWBGeppettoMapper:
    pass


class SubjectMapper(NWBGeppettoMapper):
    ''' Add mappers for objects that are not present in pynwb but you want to have a compositeType
        in Geppetto model for them. For example: aggregation data about number of acquisiton or stimulus'''

    def supports(self, pynwb_obj):
        ''' return the supported pynwb types '''
        return isinstance(pynwb_obj, Subject)

    def add_variables_to_type(self, pynwb_obj, geppetto_composite_type, model_factory):
        geppetto_composite_type.name = 'map'


class LabeledDictMapper(NWBGeppettoMapper):
    ''' Add mappers for objects that are not present in pynwb but you want to have a compositeType
        in Geppetto model for them. For example: aggregation data about number of acquisiton or stimulus'''

    def supports(self, pynwb_obj):
        ''' return the supported pynwb types '''
        return isinstance(pynwb_obj, LabelledDict)

    def add_variables_to_type(self, pynwb_obj, geppetto_composite_type, model_factory):
        if len(pynwb_obj) != 0:
            geppetto_composite_type.name = pynwb_obj.label


class TimeseriesMapper(NWBGeppettoMapper):
    ''' Extend this class to handle extra pynwb objects '''

    def supports(self, pynwb_obj):
        ''' return the supported pynwb types '''
        return isinstance(pynwb_obj, TimeSeries)

    def add_variables_to_type(self, pynwb_obj, geppetto_composite_type, model_factory):
        ''' Use this function to add variables to a geppetto compositeType '''

        geppetto_composite_type.variables.append(
            model_factory.createStateVariable("time", model_factory.createImportValueAndCache(pynwb_obj)))

        geppetto_composite_type.variables.append(
            model_factory.createStateVariable('data', model_factory.createImportValueAndCache(pynwb_obj)))


class ImageSeriesMapper(NWBGeppettoMapper):

    def supports(self, pynwb_obj):
        ''' return the supported pynwb types '''
        return isinstance(pynwb_obj, ImageSeries)

    def add_variables_to_type(self, pynwb_obj, geppetto_composite_type, model_factory):
        geppetto_composite_type.variables.append(
            model_factory.createStateVariable("time", model_factory.createImportValueAndCache(pynwb_obj)))


class SummaryMapper(NWBGeppettoMapper):
    ''' Add mappers for objects that are not present in pynwb but you want to have a compositeType
        in Geppetto model for them. For example: aggregation data about number of acquisiton or stimulus'''

    def supports(self, pynwb_obj):
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

    def add_variables_to_type(self, pynwb_obj, geppetto_composite_type, model_factory):
        for key, value in pynwb_obj.fields.items():
            if isinstance(value, str):
                geppetto_composite_type.variables.append(
                    model_factory.createTextVariable(id=key, text=str(value)))
