import pytest

from nwb_explorer.nwb_model_interpreter.nwb_reader import NWBReader
from .utils import create_nwb_file

nwbfile = create_nwb_file()


@pytest.fixture
def uut():
    return NWBReader(nwbfile)


def _test_big_file(uut):
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
    assert 4 == len(path)


def test_extract_time_series_path(uut):
    process_module = uut.nwbfile.modules['mod']
    ts = process_module.get_data_interface('t3')
    path = uut.extract_time_series_path(ts)
    assert 2 == len(path)
    assert 'processing' == path[0]
    assert 'mod' == path[1]

    ts = uut.nwbfile.get_acquisition('t1')
    path = uut.extract_time_series_path(ts)
    assert 1 == len(path)
    assert 'acquisition' == path[0]


def test_retrieve_from_path(uut):
    ts = uut.retrieve_from_path(('acquisition', 't1'))
    assert ts != None
    assert ts == nwbfile.acquisition['t1']

    ts = uut.retrieve_from_path(('processing', 'mod', 't3'))
    assert ts != None
    assert ts == nwbfile.modules['mod'].get_data_interface('t3')
