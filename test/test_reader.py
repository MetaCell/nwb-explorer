import pytest

from nwb_explorer.nwb_model_interpreter.nwb_reader import NWBReader
from .utils import create_nwb_file

nwbfile = create_nwb_file()


@pytest.fixture
def uut():
    return NWBReader(nwbfile)





def test_retrieve_from_path(uut):
    ts = uut.retrieve_from_path(('acquisition', 't1'))
    assert ts != None
    assert ts == nwbfile.acquisition['t1']

    ts = uut.retrieve_from_path(('processing', 'mod', 't3'))
    assert ts != None
    assert ts == nwbfile.modules['mod'].get_data_interface('t3')
