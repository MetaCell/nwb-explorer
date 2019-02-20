import unittest
import requests
import os.path
import traceback

TEST_DATA_DIR = 'test_data/'


def get_test_file(file_url, fname=None):
    file_name = TEST_DATA_DIR + file_url.split('/')[-1] if not fname else fname
    if not os.path.exists(file_name):
        print('Downloading', file_url, 'to', file_name, '...')
        response = requests.get(file_url)
        with open(file_name, 'wb') as f:
            f.write(response.content)
    return file_name


class TestModelInterpreter(unittest.TestCase):
    nwb_test_urls = {

        'time_series_data.nwb':'https://github.com/OpenSourceBrain/NWBShowcase/blob/master/NWB/time_series_data.nwb?raw=true',
        'simple_example.nwb': 'https://github.com/OpenSourceBrain/NWBShowcase/blob/master/NWB/simple_example.nwb?raw=true',
        'ferguson2015.nwb': 'https://github.com/OpenSourceBrain/NWBShowcase/blob/master/FergusonEtAl2015/FergusonEtAl2015.nwb?raw=true',
        'brain_observatory.nwb': 'http://ec2-34-229-132-127.compute-1.amazonaws.com/api/v1/item/5ae9f7896664c640660400b5/download',
    }

    def setUp(self):
        from nwb_explorer.nwb_model_interpreter import NWBModelInterpreter
        self.uut = NWBModelInterpreter()

    def test_samples(self):
        fails = []
        ok = []
        for name, url in self.nwb_test_urls.items():
            print('Testing file', name)
            file_path = get_test_file(url, name)
            try:
                geppetto_model = self.uut.importType(file_path, '', '', '')
                print('File read correctly:', name)
            except Exception as e:
                fails.append(name)
                print('Error', e.args)
                traceback.print_exc()

        if fails:
            self.fail('Some file failed: {}'.format('; '.join(fails)))

if __name__ == '__main__':
    unittest.main()
