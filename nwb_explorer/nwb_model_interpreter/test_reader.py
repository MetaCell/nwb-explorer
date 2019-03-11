import unittest
from nwb_explorer.nwb_model_interpreter.nwb_reader import NWBReader

TEST_DATA_DIR = '../../test_data/'


class TestReader(unittest.TestCase):

    def setUp(self):
        pass

    def test_big_file(self):
        file_path = "/home/user/nwb-explorer-jupyter/test_data/pynwb/YutaMouse41-150903.nwb"
        uut = NWBReader(file_path)
        process_module = uut.nwbfile.modules['behavior']
        interface = process_module.get_data_interface('EightMazePosition_position')
        children = interface.fields['spatial_series']
        ts = children['EightMazePosition_linearized_spatial_series']
        path = uut.extract_time_series_path(ts)
        self.assertEquals(6, len(path))


if __name__ == '__main__':
    unittest.main()
