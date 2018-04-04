from django.test import TestCase
from datetime import datetime

import numpy as np

from pynwb import NWBFile, TimeSeries, NWBHDF5IO
from pynwb.ophys import TwoPhotonSeries, OpticalChannel, ImageSegmentation, Fluorescence

class PyNWBTestCase(TestCase):

    nwbfile = None

    def setUp(self):
        start_time = datetime(2017, 4, 3, 11, 0, 0)
        create_date = datetime(2017, 4, 15, 12, 0, 0)

        self.nwbfile = NWBFile('PyNWB tutorial', 'demonstrate NWBFile basics', 'NWB123', start_time,
                        file_create_date=create_date)

    def test_add_NWB_time_series(self):
        data = list(range(100, 200, 10))
        timestamps = list(range(10))
        test_ts_1 = TimeSeries('test_timeseries_1', 'PyNWB tutorial', data, 'SIunit', timestamps=timestamps)
        test_ts_2 = TimeSeries('test_timeseries_2', 'PyNWB tutorial', data, 'SIunit', starting_time=0.0, rate=1.0)

        self.nwbfile.add_acquisition(test_ts_1)
        self.nwbfile.add_acquisition(test_ts_2)

        self.assertIsNotNone(self.nwbfile.get_acquisition('test_timeseries_1'))
        self.assertIsNotNone(self.nwbfile.get_acquisition('test_timeseries_2'))

class PyNWBAnotherTestCase(TestCase):

    nwbfile = None

    def setUp(self):
        start_time = datetime(2017, 4, 3, 11, 0, 0)
        create_date = datetime(2017, 4, 15, 12, 0, 0)

        # create your NWBFile object
        self.nwbfile = NWBFile('PyNWB Sample File', 'A simple NWB file', 'NWB_test', start_time,
                        file_create_date=create_date)


    def test_create_complicated_NWB_file(self):
        # create acquisition metadata
        optical_channel = OpticalChannel('test_optical_channel', 'optical channel source',
                                        'optical channel description', '3.14')
        imaging_plane = self.nwbfile.create_imaging_plane('test_imaging_plane',
                                                    'ophys integration tests',
                                                    optical_channel,
                                                    'imaging plane description',
                                                    'imaging_device_1',
                                                    '6.28', '2.718', 'GFP', 'somewhere in the brain',
                                                    (1, 2, 1, 2, 3), 4.0, 'manifold unit', 'A frame to refer to')

        # create acquisition data
        image_series = TwoPhotonSeries(name='test_iS', source='a hypothetical source', dimension=[2],
                                    external_file=['images.tiff'], imaging_plane=imaging_plane,
                                    starting_frame=[1, 2, 3], format='tiff', timestamps=list())
        self.nwbfile.add_acquisition(image_series)


        mod = self.nwbfile.create_processing_module('img_seg_example', 'ophys demo', 'an example of writing Ca2+ imaging data')
        img_seg = ImageSegmentation('a toy image segmentation container')
        mod.add_data_interface(img_seg)
        ps = img_seg.create_plane_segmentation('integration test PlaneSegmentation', 'plane segmentation description',
                                            imaging_plane, 'test_plane_seg_name', image_series)
        # add two ROIs
        # - first argument is the pixel mask i.e. a list of pixels and their weights
        # - second argument is the image mask
        w, h = 3, 3
        pix_mask1 = [(0, 0, 1.1), (1, 1, 1.2), (2, 2, 1.3)]
        img_mask1 = [[0.0 for x in range(w)] for y in range(h)]
        img_mask1[0][0] = 1.1
        img_mask1[1][1] = 1.2
        img_mask1[2][2] = 1.3
        ps.add_roi(pix_mask1, img_mask1)

        pix_mask2 = [(0, 0, 2.1), (1, 1, 2.2)]
        img_mask2 = [[0.0 for x in range(w)] for y in range(h)]
        img_mask2[0][0] = 2.1
        img_mask2[1][1] = 2.2
        ps.add_roi(pix_mask2, img_mask2)

        # add a Fluorescence container
        fl = Fluorescence('a toy fluorescence container')
        mod.add_data_interface(fl)
        # get an ROI table region i.e. a subset of ROIs to create a RoiResponseSeries from
        rt_region = ps.create_roi_table_region([0], 'the first of two ROIs')
        # make some fake timeseries data
        data = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        timestamps = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
        rrs = fl.create_roi_response_series('test_roi_response_series', 'RoiResponseSeries integration test',
                                            data, 'lumens', rt_region, timestamps=timestamps)
        # write data
        nwb_path = './test_data/nwb_test_file.nwb'
        with NWBHDF5IO(nwb_path, 'w') as io:
            io.write(self.nwbfile)

        # read data back in
        io = NWBHDF5IO(nwb_path, 'r')
        self.nwbfile = io.read()

        # get the processing module
        mod = self.nwbfile.get_processing_module('img_seg_example')

        # get the PlaneSegmentation from the ImageSegmentation data interface
        ps = mod['ImageSegmentation'].get_plane_segmentation()
        img_mask1 = ps.get_image_mask(0)
        pix_mask1 = ps.get_pixel_mask(0)
        img_mask2 = ps.get_image_mask(1)
        pix_mask2 = ps.get_pixel_mask(1)

        # get the RoiResponseSeries from the Fluorescence data interface
        rrs = mod['Fluorescence'].get_roi_response_series()
        # get the data...
        rrs_data = rrs.data
        rrs_timestamps = rrs.timestamps
        # and now do something cool!

    def test_open_NWB_file_and_inspect_data(self):
        nwb_path = './test_data/nwb_test_file.nwb'
        # read data back in
        io = NWBHDF5IO(nwb_path, 'r')
        self.nwbfile = io.read()

        # get the processing module
        mod = self.nwbfile.get_processing_module('img_seg_example')

        # get the RoiResponseSeries from the Fluorescence data interface
        rrs = mod['Fluorescence'].get_roi_response_series()
        # get the data...
        rrs_data = rrs.data
        rrs_timestamps = rrs.timestamps

        self.assertTrue(np.array_equal(rrs_data[()], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]))
        self.assertTrue(np.array_equal(rrs_timestamps[()], [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]))