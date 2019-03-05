import collections

import numpy as np
from pynwb import TimeSeries, NWBHDF5IO
from pynwb.core import NWBDataInterface
from pynwb.image import ImageSeries



class NWBReader:
    nwb_map_id_api = {'acquisition': 'acquisition',
                      'analysis': 'analysis',
                      'epochs': 'epochs',
                      'processing': 'modules',  # this dictionary is needed mainly because of this
                      'stimulus': 'stimulus',
                      }

    def __init__(self, nwbfile_path):
        try:
            io = NWBHDF5IO(nwbfile_path, 'r')
            nwbfile = io.read()
        except Exception  as e:
            raise ValueError('Error reading the NWB file.', e.args)

        self.nwbfile = nwbfile
        self.nwb_data_interfaces_list = self._get_data_interfaces(self.nwbfile)
        self.time_series_list = self._get_timeseries()

    def _get_data_interfaces(self, node):
        """Given a NWBHDF5IO returns all the data_interfaces objects presents on it."""
        data_interfaces_list = []
        for child in node.children:
            if isinstance(child, NWBDataInterface):
                data_interfaces_list.append(child)
            data_interfaces_list += self._get_data_interfaces(child)
        return data_interfaces_list

    def _get_timeseries(self):
        """Given all the nwb_data_interfaces returns all of those that are timeseries objects."""
        time_series_list = []
        for data_interface in self.nwb_data_interfaces_list:
            if isinstance(data_interface, TimeSeries):
                time_series_list.append(data_interface)
        return time_series_list

    def get_timeseries(self):
        return self.time_series_list

    def get_nwbfile(self):
        return self.nwbfile

    def get_plottable_timeseries(self, time_series):
        if isinstance(time_series, ImageSeries):
            return self.get_raw_data(time_series.data)
        return self.get_mono_dimensional_timeseries_aux(time_series.data[()])

    def get_raw_data(self, image_series_data):
        """Given a image_series data object returns a NumPy array with the raw data."""
        arr = np.zeros(image_series_data.shape, dtype=image_series_data.dtype)
        image_series_data.read_direct(arr)
        return arr

    def get_mono_dimensional_timeseries_aux(self, values):
        """Given a timeseries data object returns all mono dimensional timeseries presents on it."""
        mono_time_series_list = []
        if isinstance(values, collections.Iterable):
            try:
                data = [float(i) for i in values]
                mono_time_series_list.append(data)
            except:
                for inner_list in values:
                    mono_time_series_list += self.get_mono_dimensional_timeseries_aux(inner_list)
        return mono_time_series_list

    # Assuming requirements are NWBDataInterfaces provided by the API and NWB specification
    # http://pynwb.readthedocs.io/en/latest/overview_nwbfile.html#processing-modules
    def has_all_requirements(self, requirements):
        """Given a list of requirements verifies if all are meet ."""
        return all(self._check_requirement(requirement) for requirement in requirements)

    def _check_requirement(self, requirement):
        list_string = requirement.split('.')
        return self._check_requirement_full_path(list_string) if len(
            list_string) > 1 else self._check_requirement_data_interfaces(requirement)

    def _check_requirement_full_path(self, path_list):
        """Given a full_path requirement gets the initial group and expands it blindly in search of the last path
        element """
        group = NWBReader.nwb_map_id_api.get(path_list[0])
        if group is not None:
            nodes = [getattr(self.nwbfile, group)]
            for index, remaining_path in enumerate(path_list[1:]):
                for node in nodes:
                    if index == len(path_list) - 2:
                        if isinstance(node, dict):
                            for value in list(node.values()):
                                if value.neurodata_type == remaining_path:
                                    return True
                        else:
                            for child in node.children:
                                if child.neurodata_type == remaining_path:
                                    return True
                    else:
                        nodes = list(node.values()) if isinstance(node, dict) else node.children
        return False

    def _check_requirement_data_interfaces(self, requirement):
        """Given a requirement looks for a match in all the nwb_data_interfaces of the nwb file """
        for data_interfaces in self.nwb_data_interfaces_list:
            if data_interfaces.neurodata_type == requirement:
                return True
        return False
