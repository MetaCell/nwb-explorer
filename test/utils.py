from datetime import datetime

import numpy as np
import pynwb
from dateutil.tz import tzlocal


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

    nwbfile.add_acquisition(pynwb.TimeSeries('t1', data, 'm', unit='UA', timestamps=timestamps))
    nwbfile.add_acquisition(pynwb.TimeSeries('t2', data, 'm', rate=1.0))

    mod = nwbfile.create_processing_module('mod', 'Mod')
    interface = mod.add_data_interface(pynwb.TimeSeries('t3', data, 'm', timestamps=timestamps))
    mod.add_data_interface(pynwb.TimeSeries('t4', data, 'm', timestamps=timestamps))

    
    nwbfile.add_acquisition(create_image('image', nwbfile))
    
    return nwbfile

def create_image(name, nwbfile):
    device = pynwb.device.Device('imaging_device_1')
    nwbfile.add_device(device)
    optical_channel = pynwb.ophys.OpticalChannel('my_optchan', 'description', 500.)
    imaging_plane = nwbfile.create_imaging_plane('my_imgpln', optical_channel, 'a very interesting part of the brain',
                                             device, 600., 300., 'GFP', 'my favorite brain location',
                                             np.ones((5, 5, 3)), 4.0, 'manifold unit', 'A frame to refer to')

    data = np.ones((5, 5, 5))
    return pynwb.ophys.TwoPhotonSeries(name='test_iS', data=data, dimension=[2], imaging_plane=imaging_plane,
                                starting_frame=[0], format='tiff', starting_time=0.0, rate=1.0)
    
create_nwb_file()
