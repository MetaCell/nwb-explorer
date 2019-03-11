from datetime import datetime
from dateutil.tz import tzlocal
import pynwb
import math
import numpy as np


def create_nwb_file():
    start_time = datetime(2019, 1, 1, 11, tzinfo=tzlocal())
    create_date = datetime.now(tz=tzlocal())

    nwbfile = pynwb.NWBFile('Example structured data',
                            'TSD',
                            start_time,
                            file_create_date=create_date,
                            notes='Example NWB file',
                            experimenter='Filippo Ledda',
                            experiment_description='Add example data',
                            institution='UCL',
                            )
    sample_num = 100
    timestamps = np.arange(0, 1, 1 / sample_num)
    data = np.sin(timestamps)

    nwbfile.add_acquisition(pynwb.TimeSeries('t1', data, 'm', timestamps=timestamps))
    nwbfile.add_acquisition(pynwb.TimeSeries('t2', data, 'm', timestamps=timestamps))

    mod = nwbfile.create_processing_module('mod', 'Mod')
    interface = mod.add_data_interface(pynwb.TimeSeries('t3', data, 'm', timestamps=timestamps))
    mod.add_data_interface(pynwb.TimeSeries('t4', data, 'm', timestamps=timestamps))
    return nwbfile
