import collections

from pynwb import TimeSeries


class NWBUtils:

    def __init__(self, nwbfile):
        self.nwbfile = nwbfile
        self.time_series_list = self._get_timeseries(self.nwbfile)

    def _get_timeseries(self, node):
        """Given a NWBHDF5IO returns all the timeseries objects presents on it."""
        time_series_list = []
        for child in node.children:
            if isinstance(child, TimeSeries):
                time_series_list.append(child)
            else:
                time_series_list += self._get_timeseries(child)
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

    # Assuming requirements are timeseries only
    def has_all_requirements(self, requirements):
        return all(self._check_requirement(requirement) for requirement in requirements)

    def _check_requirement(self, requirment):
        for time_series in self.time_series_list:
            time_series


