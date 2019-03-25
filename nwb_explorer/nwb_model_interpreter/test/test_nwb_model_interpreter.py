import unittest
import requests
import math
import os.path
import traceback
from datetime import datetime
from dateutil.tz import tzlocal
import pynwb
import os
from nwb_explorer.service import get_file_from_url
from nwb_explorer.nwb_model_interpreter import NWBModelInterpreter
from nwb_explorer import nwb_model_interpreter
from .utils import create_nwb_file



def write_nwb_file(nwbfile, nwb_file_name):
    io = pynwb.NWBHDF5IO(nwb_file_name, mode='w')
    io.write(nwbfile)
    io.close()
    print("Written NWB file to %s" % nwb_file_name)


class TestModelInterpreter(unittest.TestCase):
    nwb_test_urls = {

        'time_series_data.nwb': 'https://github.com/OpenSourceBrain/NWBShowcase/raw/master/NWB/time_series_data.nwb',
        'simple_example.nwb': 'https://github.com/OpenSourceBrain/NWBShowcase/raw/master/NWB/simple_example.nwb',
        'ferguson2015.nwb': 'https://github.com/OpenSourceBrain/NWBShowcase/raw/master/FergusonEtAl2015/FergusonEtAl2015.nwb',
        'brain_observatory.nwb': 'http://ec2-34-229-132-127.compute-1.amazonaws.com/api/v1/item/5ae9f7896664c640660400b5/download',
    }

    def setUp(self):

        self.uut = NWBModelInterpreter()
        self.nwbfile = create_nwb_file()

    def _test_samples(self):
        '''
        Here only for dev/debug purposed. Do not use as a standard unit test
        :return:
        '''
        fails = []
        for name, url in self.nwb_test_urls.items():
            print('Testing file', name)
            file_path = get_file_from_url(url, name, '../../test_data')
            try:
                geppetto_model = self.uut.importType(file_path, '', '', '')
                print('File read correctly:', name)
            except Exception as e:
                fails.append(name)
                print('Error', e.args)
                traceback.print_exc()

        if fails:
            self.fail('Some file failed: {}'.format('; '.join(fails)))

    def test_big_file(self):
        '''
               Here only for dev/debug purpose. Do not use as a standard unit test
               :return:
        '''
        nwb_model_interpreter.MAX_SAMPLES = 100000
        file_path = "/home/user/nwb-explorer-jupyter/test_data/pynwb/YutaMouse41-150903.nwb"
        self._single_file_test(file_path)

    def test_ferguson(self):
        '''
               Here only for dev/debug purpose. Do not use as a standard unit test
               :return:
               '''
        file_path = "/home/user/NWBShowcase/FergusonEtAl2015/FergusonEtAl2015.nwb"
        self._single_file_test(file_path)

    def _single_file_test(self, file_path):
        name = file_path.split('/')[-1]
        print('Testing file', name)
        try:
            geppetto_model = self.uut.importType(file_path, '', '', '')
            print('File read correctly:', name)

        except Exception as e:
            print('Error', e.args)
            traceback.print_exc()

    def test_importType(self):
        geppetto_model = self.uut.importType(self.nwbfile, '', '', '')
        # TODO let's write the test on the new object structure directly




if __name__ == '__main__':
    unittest.main()
