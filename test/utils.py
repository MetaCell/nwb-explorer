from datetime import datetime

import numpy as np
import pynwb
from dateutil.tz import tzlocal

from pynwb import NWBHDF5IO

def create_nwb_file():
    '''
    acquisition.t1
    acquisition.t2
    modules.mod.t3
    modules.mod.t4
    :return:
    '''
    start_time = datetime(2019, 1, 1, 11, tzinfo=tzlocal())
    create_date = datetime.now(tz=tzlocal())
    
    # FIXME: this attr breaks nwb-explorer
    # date_of_birth=create_date 
    sub = pynwb.file.Subject(
        age='33',
        description='Nothing too personal.',
        genotype='AA',
        sex='M',
        species='Homo erectus',
        subject_id='001',
        weight="199 lb"
    )
    
    nwbfile = pynwb.NWBFile('Example structured data',
                            'TSD',
                            start_time,
                            file_create_date=create_date,
                            notes='Example NWB file',
                            experimenter='Filippo Ledda',
                            experiment_description='Add example data',
                            institution='UCL',
                            subject=sub
                            )
    sample_num = 100
    timestamps = np.arange(0, sample_num, 1)
    data = timestamps * 2

    nwbfile.add_acquisition(pynwb.TimeSeries('t1', data, 'm', timestamps=timestamps))
    nwbfile.add_acquisition(pynwb.TimeSeries('t2', data, 'm', timestamps=timestamps))

    mod = nwbfile.create_processing_module('mod', 'Mod')
    interface = mod.add_data_interface(pynwb.TimeSeries('t3', data, 'm', timestamps=timestamps))
    mod.add_data_interface(pynwb.TimeSeries('t4', data, 'm', timestamps=timestamps))
    return nwbfile