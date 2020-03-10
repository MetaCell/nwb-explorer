import pytest
import os

from nwb_explorer.nwb_data_manager import NWBDataManager

from pygeppetto.services.model_interpreter import get_model_interpreter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

@pytest.fixture
def nwb_data_manager():
    return NWBDataManager()


def test_get_project_from_url(nwb_data_manager):
    fname = os.path.join(HERE, 'nwb_files/time_series_data.nwb')
    project = nwb_data_manager.get_project_from_url(fname)
    assert project.geppettoModel
    library = project.geppettoModel.variables[0].types[0].eContainer()
    assert library
    assert library.id == 'nwbfile'
    model_interpreter = get_model_interpreter(library.id)
    assert model_interpreter
