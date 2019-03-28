import unittest
from nwb_explorer.nwb_model_interpreter.nwb_reader import NWBReader
from .utils import create_nwb_file
from nwb_explorer.nwb_model_interpreter import settings



class TestReader(unittest.TestCase):

    def setUp(self):
        self.nwbfile = create_nwb_file()
        self.uut = NWBReader(self.nwbfile)
        pass

    def _test_big_file(self):
        '''
        Testing a real file here for dev purposes
        :return:
        '''
        file_path = "/home/user/nwb-explorer-jupyter/test_data/pynwb/YutaMouse41-150903.nwb"
        uut = NWBReader(file_path)
        process_module = uut.nwbfile.modules['behavior']
        interface = process_module.get_data_interface('EightMazePosition_position')
        children = interface.fields['spatial_series']
        ts = children['EightMazePosition_linearized_spatial_series']
        path = uut.extract_time_series_path(ts)
        self.assertEqual(4, len(path))

    def test_extract_time_series_path(self):

        process_module = self.nwbfile.modules['mod']
        ts = process_module.get_data_interface('t3')
        path = self.uut.extract_time_series_path(ts)
        self.assertEqual(2, len(path))
        self.assertEqual('modules', path[0])
        self.assertEqual('mod', path[1])

        ts = self.nwbfile.get_acquisition('t1')
        path = self.uut.extract_time_series_path(ts)
        self.assertEqual(1, len(path))
        self.assertEqual('acquisition', path[0])

    def test_retrieve_from_path(self):
        ts = self.uut.retrieve_from_path(('acquisition', 't1'))
        self.assertTrue(ts != None)
        self.assertEqual(ts, self.nwbfile.acquisition['t1'])

        ts = self.uut.retrieve_from_path(('modules', 'mod', 't3'))
        self.assertTrue(ts != None)
        self.assertEqual(ts, self.nwbfile.modules['mod'].get_data_interface('t3'))

if __name__ == '__main__':
    unittest.main()
