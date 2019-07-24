from datetime import datetime

import numpy as np
import pynwb
from dateutil.tz import tzlocal

from pynwb import NWBFile
from pynwb.ophys import TwoPhotonSeries, OpticalChannel, ImageSegmentation, Fluorescence
from pynwb.device import Device
from pynwb.image import ImageSeries

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

    nwbfile.add_acquisition(pynwb.TimeSeries(name='t1', data=data, unit='UA', timestamps=timestamps))
    nwbfile.add_acquisition(pynwb.TimeSeries(name='t2', data=data, unit='pA',rate=1.0))

    mod = nwbfile.create_processing_module('mod', 'Mod')
    interface = mod.add_data_interface(pynwb.TimeSeries(name='t3', data=data, unit='pA', timestamps=timestamps))
    mod.add_data_interface(pynwb.TimeSeries(name='t4', data=data, unit='UA', timestamps=timestamps))

    nwbfile.add_acquisition(create_image('internal_storaged_image', nwbfile, False))
    nwbfile.add_acquisition(create_image('external_storaged_image', nwbfile, True))
    
    return nwbfile

def create_image(name, nwbfile, external_storage):
    import imageio
    formats = ['png', 'jpg', 'tiff']
    
    n = len(formats)
    
    if  external_storage:
        base_uri = "https://raw.githubusercontent.com/MetaCell/nwb-explorer/feature/60/test/images/"
    else:
        base_uri = "test/images/"
    
    images_uri = [f"{base_uri}{i}.{i}" for i in formats]  
    
    timestamp = datetime.now().timestamp()
    timestamps = np.arange(n) + timestamp

    if  external_storage:
        return ImageSeries(name=name,
                               external_file=images_uri,
                               timestamps=timestamps,
                               starting_frame=[0], 
                               format='external', 
                               description='Series of images from a simulation of the cerebellum via neuroConstruct')
    else:
        return ImageSeries(name=name,
                               data=np.array([imageio.imread(image_uri) for image_uri in images_uri]),
                               timestamps=timestamps,
                               starting_frame=[0], 
                               format='png,tiff,png', 
                               description='Series of images from a simulation of the cerebellum via neuroConstruct')


def generate_images():
    import imageio
    import numpy as np
    from PIL import Image as Img

    np_image = np.array(
        [[[0,0,0],[84,84,84]], 
        [[168, 168, 168], [255, 255, 255]]
    ], dtype=np.uint8)

    image = Img.fromarray(np_image, 'RGB')

    image.save('png.png', format='PNG')
    image.save('jpg.jpg', format='JPEG')
    image.save('tiff.tiff', format='TIFF')


if __name__ == "__main__":
    from pynwb import NWBHDF5IO
    with NWBHDF5IO('time_series_data.nwb', 'w') as io:
        io.write(create_nwb_file())