import json

import pytest
from jupyter_geppetto import TornadoGeppettoWebSocketHandler
from pygeppetto.api import outbound_messages as OutboundMessages, inbound_messages as InboundMessages
from pygeppetto.api.message_handler import GeppettoMessageHandler
from pygeppetto.utils import Singleton

import nwb_explorer  # With this import we are assigning the model interpreter and data manager

model_interpreter = nwb_explorer.model_interpreter  # This is just to say the idle the nwb_explorer import is not useless


class TestWebsocketHandler(TornadoGeppettoWebSocketHandler):
    sent_messages = {}

    def __init__(self, *args, **kwargs):
        GeppettoMessageHandler.__init__(self)

    def send_message(self, requestID, return_msg_type, msg_data):
        if not return_msg_type in self.sent_messages:
            self.sent_messages[return_msg_type] = []
        self.sent_messages[return_msg_type].append(msg_data)


@pytest.fixture
def websocket_handler():
    Singleton._instances = {}
    TestWebsocketHandler.sent_messages = {}
    return TestWebsocketHandler()

def test_init_websocket(websocket_handler):
    websocket_handler.open()
    assert len(websocket_handler.sent_messages) == 2
    assert len(websocket_handler.sent_messages[OutboundMessages.CLIENT_ID]) == 1
    assert len(websocket_handler.sent_messages[OutboundMessages.USER_PRIVILEGES]) == 1

def test_load_project(websocket_handler):

    msg = {'type': InboundMessages.LOAD_PROJECT_FROM_URL, 'data': 'https://github.com/OpenSourceBrain/NWBShowcase/raw/master/NWB/time_series_data.nwb', 'requestID': 0}
    websocket_handler.on_message(json.dumps(msg))
    assert len(websocket_handler.sent_messages) == 2
    assert len(websocket_handler.sent_messages[OutboundMessages.PROJECT_LOADED]) == 1
    assert len(websocket_handler.sent_messages[OutboundMessages.GEPPETTO_MODEL_LOADED]) == 1

    model = json.loads(websocket_handler.sent_messages[OutboundMessages.GEPPETTO_MODEL_LOADED][0])
    assert len(model['variables']) == 1
    assert 'eClass' in model['variables'][0]['types'][0]

    websocket_handler.on_message(json.dumps(msg))
    assert len(websocket_handler.sent_messages) == 2
    assert len(websocket_handler.sent_messages[OutboundMessages.PROJECT_LOADED]) == 2
    assert len(websocket_handler.sent_messages[OutboundMessages.GEPPETTO_MODEL_LOADED]) == 2

    model2 = json.loads(websocket_handler.sent_messages[OutboundMessages.GEPPETTO_MODEL_LOADED][1])
    assert model2 == model

def test_import_value(websocket_handler):
    msg = {'type': InboundMessages.LOAD_PROJECT_FROM_URL, 'data': 'https://github.com/OpenSourceBrain/NWBShowcase/raw/master/NWB/time_series_data.nwb', 'requestID': 0}
    websocket_handler.on_message(json.dumps(msg))
    opened_projects = websocket_handler.geppettoManager.opened_projects

    runtime_project = next(iter(opened_projects.values()))
    msg = {'type': InboundMessages.RESOLVE_IMPORT_VALUE, 'data': json.dumps(
        {'projectId': runtime_project.project.id, 'experimentId': -1,
            'path': 'nwbfile.acquisition.test_sine_1.data'}), 'requestID': 0}
    websocket_handler.on_message(json.dumps(msg))
    assert len(websocket_handler.sent_messages) == 3
    assert len(websocket_handler.sent_messages[OutboundMessages.PROJECT_LOADED]) == 1
    assert len(websocket_handler.sent_messages[OutboundMessages.GEPPETTO_MODEL_LOADED]) == 1
    assert len(websocket_handler.sent_messages[OutboundMessages.IMPORT_VALUE_RESOLVED]) == 1

    model = json.loads(websocket_handler.sent_messages[OutboundMessages.GEPPETTO_MODEL_LOADED][0])
    assert len(model['variables']) == 1
    assert 'eClass' in model['variables'][0]['types'][0]

def test_load_errors(websocket_handler):
    msg1 = {'type': InboundMessages.LOAD_PROJECT_FROM_URL, 'data': 'fake.nwb', 'requestID': 0}
    websocket_handler.on_message(json.dumps(msg1))
    
    assert "error_loading_project" in websocket_handler.sent_messages.keys()