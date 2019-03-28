from pynwb.ophys import RoiResponseSeries
from pynwb import TimeSeries
from pynwb.image import ImageSeries

SUPPORTED_TIME_SERIES_TYPES = (
    RoiResponseSeries, ImageSeries, TimeSeries)
# Assuming numerical or image time series only for now
MAX_SAMPLES = 1000
path_separator = '.'