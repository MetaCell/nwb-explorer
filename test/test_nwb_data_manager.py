import pytest
from pygeppetto.model.types import ImportType

from nwb_explorer.nwb_data_manager import NWBDataManager

from pygeppetto.services.model_interpreter import get_model_interpreter


@pytest.fixture
def nwb_data_manager():
    return NWBDataManager()


def test_get_project_from_url(nwb_data_manager):
    fname = 'nwb_files/time_series_data.nwb'
    project = nwb_data_manager.get_project_from_url(fname)
    assert project.geppettoModel
    library = project.geppettoModel.variables[0].types[0].eContainer()
    assert library
    assert library.id == fname
    model_interpreter = get_model_interpreter(library.id)
    assert model_interpreter
