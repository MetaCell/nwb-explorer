import unittest
from nwb_explorer.nwb_model_interpreter.nwb_reader import NWBReader
from .utils import create_nwb_file




class TestReader(unittest.TestCase):

    def setUp(self):
        self.nwbfile = create_nwb_file()
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
        uut = NWBReader(self.nwbfile)
        process_module = self.nwbfile.modules['mod']
        ts = process_module.get_data_interface('t3')
        path = uut.extract_time_series_path(ts)
        self.assertEqual(2, len(path))
        self.assertEqual('modules', path[0])
        self.assertEqual('mod', path[1])

        ts = self.nwbfile.get_acquisition('t1')
        path = uut.extract_time_series_path(ts)
        self.assertEqual(1, len(path))
        self.assertEqual('acquisition', path[0])

if __name__ == '__main__':
    unittest.main()
