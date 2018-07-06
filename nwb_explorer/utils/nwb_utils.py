import collections

from pynwb import TimeSeries
from pynwb.core import NWBDataInterface


class NWBUtils:

    def __init__(self, nwbfile):
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

    def get_mono_dimensional_timeseries(self, values):
        """Given a timeseries object returns all mono dimensional timeseries presents on it."""
        mono_time_series_list = []
        if isinstance(values, collections.Iterable):
            try:
                data = [float(i) for i in values]
                mono_time_series_list.append(data)
            except:
                for inner_list in values:
                    mono_time_series_list += self.get_mono_dimensional_timeseries(inner_list)
        return mono_time_series_list

    # Assuming requirements are NWBDataInterfaces provided by the API and NWB specification
    # TODO: Make sure this approach makes sense
    def has_all_requirements(self, requirements):
        return all(self._check_requirement(requirement) for requirement in requirements)

    def _check_requirement(self, requirement):
        for data_interfaces in self.nwb_data_interfaces_list:
            if data_interfaces.neurodata_type == requirement:
                return True
        return False

