import json
import unittest

from jupyter_geppetto import GeppettoWebSocketHandler
from jupyter_geppetto.websocket import outbound_messages as OutboundMessages, inbound_messages as InboundMessages
from jupyter_geppetto.websocket.connection_handler import ConnectionHandler

import nwb_explorer  # With this import we are assigning the model interpreter and data manager

model_interpreter = nwb_explorer.model_interpreter  # This is just to say the idle the nwb_explorer import is not useless

class TestWebsocketHandler(GeppettoWebSocketHandler):
    sent_messages = {}

    def __init__(self, *args, **kwargs):
        self.geppettoHandler = ConnectionHandler(self)

    def send_message(self, requestID, return_msg_type, msg_data):
        if not return_msg_type in self.sent_messages:
            self.sent_messages[return_msg_type] = []
        self.sent_messages[return_msg_type].append(msg_data)


class NWBExplorerIntegrationTest(unittest.TestCase):

    @classmethod
    def setup_class(cls):
        cls.websocket_handler = TestWebsocketHandler()

    def test_init_websocket(self):
        self.websocket_handler.open()
        assert len(self.websocket_handler.sent_messages) == 2
        assert len(self.websocket_handler.sent_messages[OutboundMessages.CLIENT_ID]) == 1
        assert len(self.websocket_handler.sent_messages[OutboundMessages.USER_PRIVILEGES]) == 1

    def test_load_project(self):
        msg = {'type': InboundMessages.LOAD_PROJECT_FROM_URL, 'data': 'nwb_files/time_series_data.nwb', 'requestID': 0}
        self.websocket_handler.on_message(json.dumps(msg))
        assert len(self.websocket_handler.sent_messages) == 2
        assert len(self.websocket_handler.sent_messages[OutboundMessages.PROJECT_LOADED]) == 1
        assert len(self.websocket_handler.sent_messages[OutboundMessages.GEPPETTO_MODEL_LOADED]) == 1

        model = json.loads(self.websocket_handler.sent_messages[OutboundMessages.GEPPETTO_MODEL_LOADED][0])
        assert len(model['variables']) == 1
        assert 'eClass' in model['variables'][0]['types'][0]

        self.websocket_handler.on_message(json.dumps(msg))
        assert len(self.websocket_handler.sent_messages) == 2
        assert len(self.websocket_handler.sent_messages[OutboundMessages.PROJECT_LOADED]) == 2
        assert len(self.websocket_handler.sent_messages[OutboundMessages.GEPPETTO_MODEL_LOADED]) == 2

        model2 = json.loads(self.websocket_handler.sent_messages[OutboundMessages.GEPPETTO_MODEL_LOADED][1])
        assert model2 == model

    def test_import_value(self):
        self.test_load_project()
        opened_projects = self.websocket_handler.geppettoHandler.geppettoManager.opened_projects

        runtime_project = next(iter(opened_projects.values()))
        msg = {'type': InboundMessages.RESOLVE_IMPORT_VALUE, 'data': json.dumps(
            {'projectId': runtime_project.project.id, 'experimentId': -1,
             'path': 'nwbfile.acquisition.test_sine_timeseries.data'}), 'requestID': 0}
        self.websocket_handler.on_message(json.dumps(msg))
        assert len(self.websocket_handler.sent_messages) == 3
        assert len(self.websocket_handler.sent_messages[OutboundMessages.PROJECT_LOADED]) == 1
        assert len(self.websocket_handler.sent_messages[OutboundMessages.GEPPETTO_MODEL_LOADED]) == 1
        assert len(self.websocket_handler.sent_messages[OutboundMessages.IMPORT_VALUE_RESOLVED]) == 1

        model = json.loads(self.websocket_handler.sent_messages[OutboundMessages.GEPPETTO_MODEL_LOADED][0])
        assert len(model['variables']) == 1
        assert 'eClass' in model['variables'][0]['types'][0]
