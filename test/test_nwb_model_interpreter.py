import traceback
import pytest
import os
import pynwb

from nwb_explorer import nwb_model_interpreter
from nwb_explorer.nwb_data_manager import get_file_from_url
from nwb_explorer.nwb_model_interpreter import NWBModelInterpreter
from .utils import create_nwb_file

from nwb_explorer.nwb_model_interpreter.nwb_reader import NWBReader

def write_nwb_file(nwbfile, nwb_file_name):
    io = pynwb.NWBHDF5IO(path=nwb_file_name, mode='w')
    io.write(nwbfile)
    io.close()
    print("Written NWB file to %s" % nwb_file_name)


@pytest.fixture
def nwb_interpreter():
    return NWBModelInterpreter()

@pytest.fixture
def nwbfile():
    return create_nwb_file()

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



def _single_file_test(nwb_interpreter, file_path, tmpdir):
    name = os.path.basename(file_path)
    print('Testing file', name)
    try:
        file_path = get_file_from_url(file_url=file_path, fname=name, cache_dir=tmpdir.dirname)
        nwb_interpreter.createModel(file_path, 'test-model')
        print('File read correctly:', name)

    except Exception as e:
        print('Error', e.args)
        pytest.fail(f"Error reading file: {name}. Message: {e.args}")


@pytest.mark.skip(reason="To be implemented")
def test_big_file(nwb_interpreter, nwbfile, tmpdir):
    '''
            Here only for dev/debug purpose. Do not use as a standard unit test
            :return:
    '''
    nwb_model_interpreter.MAX_SAMPLES = 100000
    file_path = "/home/user/nwb-explorer-jupyter/test_data/pynwb/YutaMouse41-150903.nwb"
    _single_file_test(nwb_interpreter, file_path, tmpdir)


def test_ferguson(nwb_interpreter, tmpdir):
    '''
            Here only for dev/debug purpose. Do not use as a standard unit test
            :return:
    '''
    _single_file_test(nwb_interpreter, FILES['ferguson2015.nwb'], tmpdir)


def test_importType(nwb_interpreter, nwbfile):
    geppetto_model = nwb_interpreter.createModel(nwbfile, 'typename')

    assert len(geppetto_model.variables) == 1
    assert geppetto_model.variables[0].types[0].name == 'nwbfile'
    assert len(geppetto_model.variables[0].types[0].variables) == 10
    assert len(geppetto_model.variables[0].types[0].variables[0].types[0].variables) == 3


def test_importValue(nwb_interpreter, nwbfile):
    nwb_interpreter.createModel(nwbfile, 'typename')
    value = nwb_interpreter.importValue('typename.acquisition.t1.data')
    from pygeppetto.model.values import TimeSeries
    assert type(value) == TimeSeries
    assert len(value.value) == 100
    assert value.value[0] == 0.0

    value = nwb_interpreter.importValue('typename.acquisition.t1.time')
    assert type(value) == TimeSeries
    assert len(value.value) == 100
    assert value.value[0] == 0.0
    assert value.value[1] == 1.0

    assert nwb_interpreter.import_value_from_path('typename.acquisition.t1.data').value[0] == 0.0
    assert nwb_interpreter.import_value_from_path('typename.acquisition.t1.time').value[0] == 0.0

def test_errors(nwb_interpreter, nwbfile, tmpdir):
    nwb_interpreter.createModel(nwbfile, 'typename')
    nwbfile = nwb_interpreter.nwb_reader.get_nwbfile()
    
    assert isinstance(nwbfile, pynwb.file.NWBFile)
    assert nwb_interpreter.getDependentModels() == []
    assert nwb_interpreter.getName() == 'NWB Model Interpreter'
    assert nwb_interpreter.nwb_reader.has_all_requirements(['acquisition.TimeSeries', 'TimeSeries', 'ProcessingModule', 'TwoPhotonSeries'])
    
    with pytest.raises(KeyError):
        assert _single_file_test(nwb_interpreter, FILES['a_non_existent_file.pynwb'], tmpdir)

