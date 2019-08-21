import traceback
import pytest
import os
import pynwb
from pygeppetto.model import CompositeType, StateVariableType
from pygeppetto.model.types import ImportType
from pygeppetto.model.utils import pointer_utility
from pygeppetto.model.values import ImportValue

from nwb_explorer import nwb_model_interpreter
from nwb_explorer.nwb_data_manager import get_file_from_url, NWBDataManager
from nwb_explorer.nwb_model_interpreter import NWBModelInterpreter, GeppettoModelAccess
from .utils import create_nwb_file


from nwb_explorer.nwb_model_interpreter.nwb_reader import NWBReader

def write_nwb_file(nwbfile, nwb_file_name):
    io = pynwb.NWBHDF5IO(path=nwb_file_name, mode='w')
    io.write(nwbfile)
    io.close()
    print("Written NWB file to %s" % nwb_file_name)




@pytest.fixture
def nwbfile():
    return create_nwb_file()


@pytest.fixture
def nwb_data_manager():
    return NWBDataManager()

FILES = {
    'time_series_data.nwb': 'https://github.com/OpenSourceBrain/NWBShowcase/raw/master/NWB/time_series_data.nwb',
    'simple_example.nwb': 'https://github.com/OpenSourceBrain/NWBShowcase/raw/master/NWB/simple_example.nwb',
    'ferguson2015.nwb': 'https://github.com/OpenSourceBrain/NWBShowcase/raw/master/FergusonEtAl2015/FergusonEtAl2015.nwb',
    'brain_observatory.nwb': 'http://ec2-34-229-132-127.compute-1.amazonaws.com/api/v1/item/5ae9f7896664c640660400b5/download',
}


# def _test_samples():
#     '''
#     Here only for dev/debug purposed. Do not use as a standard unit test
#     :return:
#     '''
#     fails = []
#     for name, url in FILES.items():
#         print('Testing file', name)
#         file_path = get_file_from_url(url, name, '../../test_data')
#         try:
#             geppetto_model = nwb_interpreter.importType(file_path, '', '', '')
#             print('File read correctly:', name)
#         except Exception as e:
#             fails.append(name)
#             print('Error', e.args)
#             traceback.print_exc()

#     if fails:
#         pytest.fail('Some file failed: {}'.format('; '.join(fails)))


def _single_file_test(file_path, tmpdir):
    name = os.path.basename(file_path)

    print('Testing file', name)
    try:
        file_path = get_file_from_url(file_url=file_path, fname=name, cache_dir=tmpdir.dirname)
        nwb_interpreter = NWBModelInterpreter(file_path)
        nwb_interpreter.create_model()
        print('File read correctly:', name)

    except Exception as e:
        print('Error', e.args)
        pytest.fail(f"Error reading file: {name}. Message: {e.args}")


@pytest.mark.skip(reason="Only for dev")
def test_big_file(nwbfile, tmpdir):
    '''
            Here only for dev/debug purpose. Do not use as a standard unit test
            :return:
    '''
    nwb_model_interpreter.MAX_SAMPLES = 100000
    file_path = "/home/user/nwb-explorer-jupyter/test_data/pynwb/YutaMouse41-150903.nwb"
    _single_file_test(NWBModelInterpreter(file_path), file_path, tmpdir)


def test_ferguson(tmpdir):
    '''
            Here only for dev/debug purpose. Do not use as a standard unit test
            :return:
    '''
    _single_file_test(FILES['ferguson2015.nwb'], tmpdir)


def test_create_model(nwbfile):
    nwb_interpreter = NWBModelInterpreter(nwbfile)
    geppetto_model = nwb_interpreter.create_model()

    assert len(geppetto_model.variables) == 1
    variable = geppetto_model.variables[0]
    assert variable.name == 'nwbfile'
    itype = variable.types[0]
    assert type(itype) == ImportType
    assert itype.autoresolve == True
    assert itype.eContainer().name == 'nwblib'


def test_importType(nwbfile):
    nwb_interpreter = NWBModelInterpreter(nwbfile)
    geppetto_model = nwb_interpreter.create_model()


    assert len(geppetto_model.variables) == 1
    variable_type = geppetto_model.variables[0].types[0]
    assert variable_type.eContainer() == nwb_interpreter.library

    typename = 'typename'
    geppetto_model_access = GeppettoModelAccess(geppetto_model)
    imported_type = nwb_interpreter.importType('DUMMY', typename, variable_type.eContainer(), geppetto_model_access)
    var_names = [var.name for var in imported_type.variables]
    assert imported_type.id
    assert imported_type.name
    assert 'acquisition' in var_names
    assert 'stimulus' in var_names
    assert len(imported_type.variables[0].types) == 1

    geppetto_model_access.swap_type(variable_type, imported_type)

    var = pointer_utility.find_variable_from_path(geppetto_model, 'nwbfile.acquisition')
    variable_type = var.types[0]
    assert isinstance(variable_type, CompositeType)
    assert var.name == 'acquisition'
    assert variable_type.name == 'acquisition'

    var = pointer_utility.find_variable_from_path(geppetto_model, 'nwbfile.acquisition.t1')
    variable_type = var.types[0]
    assert isinstance(variable_type, CompositeType)
    assert var.name == 't1'
    assert variable_type.name == 'TimeSeries'

    var = pointer_utility.find_variable_from_path(geppetto_model, 'nwbfile.acquisition.t1.data')
    variable_type = var.types[0]
    assert isinstance(variable_type, StateVariableType)
    assert var.id == 'data'

def test_importValue(nwbfile):
    nwb_interpreter = NWBModelInterpreter(nwbfile)
    # Create the model
    model = nwb_interpreter.create_model()

    # Import the main type
    variable_type = model.variables[0].types[0]
    assert variable_type.eContainer() == nwb_interpreter.library
    typename = 'typename'
    geppetto_model_access = GeppettoModelAccess(model)
    imported_type = nwb_interpreter.importType('DUMMY', typename, variable_type.eContainer(), geppetto_model_access)
    geppetto_model_access.swap_type(variable_type, imported_type)

    # Call import value
    var_to_import = pointer_utility.find_variable_from_path(model, 'nwbfile.acquisition.t1.data')
    value = var_to_import.initialValues[0].value
    assert type(value), ImportValue
    value = nwb_interpreter.importValue(value)

    #Test
    from pygeppetto.model.values import TimeSeries
    assert type(value) == TimeSeries
    assert len(value.value) == 100
    assert value.value[0] == 0.0

    var_to_import = pointer_utility.find_variable_from_path(model, 'nwbfile.acquisition.t1.timestamps')
    value = var_to_import.initialValues[0].value
    assert type(value), ImportValue
    value = nwb_interpreter.importValue(value)
    assert type(value) == TimeSeries
    assert len(value.value) == 100
    assert value.value[0] == 0.0
    assert value.value[1] == 1.0


def test_errors(nwbfile, tmpdir):
    nwb_interpreter = NWBModelInterpreter(nwbfile)
    nwb_interpreter.create_model()
    nwbfile = nwb_interpreter.nwb_reader.get_nwbfile()
    
    assert isinstance(nwbfile, pynwb.file.NWBFile)
    assert nwb_interpreter.getDependentModels() == []
    assert nwb_interpreter.getName() == 'NWB Model Interpreter'
    assert nwb_interpreter.nwb_reader.has_all_requirements(['acquisition.TimeSeries', 'acquisition.ImageSeries'])

    with pytest.raises(TypeError):
        assert _single_file_test('a_non_existent_file.pynwb')


def test_imageseries(nwbfile, tmpdir):
    nwb_interpreter = NWBModelInterpreter(nwbfile)
    nwb_interpreter.create_model()

    internal_images = [nwb_interpreter.get_image('internal_storaged_image', 'acquisition', i) for i in range(3)]
    external_images = [nwb_interpreter.get_image('external_storaged_image', 'acquisition', i) for i in range(3)]
    
    import imageio

    np_images = [imageio.imread(img) for img in internal_images + external_images]
    
    assert all([img.shape == (2, 2, 3) for img in np_images])