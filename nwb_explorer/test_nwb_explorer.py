import unittest
import requests
import math
import os.path
import traceback
from datetime import datetime
from dateutil.tz import tzlocal
import pynwb
import os
from nwb_explorer.utils import get_file_from_url


TEST_DATA_DIR = '../test_data/'





def create_time_series_file():
    start_time = datetime(2019, 1, 1, 11, tzinfo=tzlocal())
    create_date = datetime.now(tz=tzlocal())

    nwbfile = pynwb.NWBFile('Example time series data',
                            'TSD',
                            start_time,
                            file_create_date=create_date,
                            notes='Example NWB file created with pynwb v%s' % pynwb.__version__,
                            experimenter='Padraig Gleeson',
                            experiment_description='Add example data',
                            institution='UCL')

    timestamps = [i / 1000.0 for i in range(2000)]
    data = [math.sin(t / 0.05) for t in timestamps]

    test_ts = pynwb.TimeSeries('test_sine_timeseries', data, 'SIunit', timestamps=timestamps)

    nwbfile.add_acquisition(test_ts)
    return nwbfile


def write_nwb_file(nwbfile, nwb_file_name):
    io = pynwb.NWBHDF5IO(nwb_file_name, mode='w')
    io.write(nwbfile)
    io.close()
    print("Written NWB file to %s" % nwb_file_name)


class TestModelInterpreter(unittest.TestCase):
    nwb_test_urls = {

        'time_series_data.nwb': 'https://github.com/OpenSourceBrain/NWBShowcase/blob/master/NWB/time_series_data.nwb?raw=true',
        'simple_example.nwb': 'https://github.com/OpenSourceBrain/NWBShowcase/raw/master/NWB/simple_example.nwb',
        'ferguson2015.nwb': 'https://github.com/OpenSourceBrain/NWBShowcase/raw/master/FergusonEtAl2015/FergusonEtAl2015.nwb',
        'brain_observatory.nwb': 'http://ec2-34-229-132-127.compute-1.amazonaws.com/api/v1/item/5ae9f7896664c640660400b5/download',
    }

    def setUp(self):
        from nwb_explorer.nwb_model_interpreter import NWBModelInterpreter
        self.uut = NWBModelInterpreter()

    def _test_samples(self):
        fails = []
        ok = []
        for name, url in self.nwb_test_urls.items():
            print('Testing file', name)
            file_path = get_file_from_url(url, name, TEST_DATA_DIR)
            try:
                geppetto_model = self.uut.importType(file_path, '', '', '')
                print('File read correctly:', name)
            except Exception as e:
                fails.append(name)
                print('Error', e.args)
                # traceback.print_exc()

        if fails:
            self.fail('Some file failed: {}'.format('; '.join(fails)))

    def _test_pynwb_files(self):
        import glob
        fails = []
        files = glob.glob('{}pynwb/*.nwb'.format(TEST_DATA_DIR))
        print('files found', files)
        for file_path in files:
            name = file_path.split('/')[-1]
            print('Testing file', name)
            try:
                geppetto_model = self.uut.importType(file_path, '', '', '')
                print('File read correctly:', name)
            except Exception as e:
                fails.append(name)
                print('Error', e.args)
                traceback.print_exc()

    def test_simple_timeseries(self):
        nwbfile = create_time_series_file()
        fname = TEST_DATA_DIR + 'timeseriestmp.nwb'
        write_nwb_file(nwbfile, fname)
        geppetto_model = self.uut.importType(fname, '', '', '')
        print('Geppetto model loaded')
        os.remove(fname)


if __name__ == '__main__':
    unittest.main()
