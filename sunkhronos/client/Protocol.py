from sunkhronos.sync.Synchroniser import Synchroniser
from twisted.internet.error import ConnectionDone
from twisted.internet.protocol import Protocol

import json

class SyncProtocol(Protocol):
    def __init__(self, factory):
        self.factory = factory
        self.actions = []
        self.data = {}

    def connectionMade(self):
        changes = self.factory.fs_manager.getChangesSinceLastSync()
        message = {
            "type": "changes",
            "changes": changes,
        }
        self.transport.write(json.dumps(message).encode())

    def connectionLost(self, reason):
        if reason.check(ConnectionDone):
            Synchroniser.synchronise(self.actions, self.data, self.factory.fs_manager)

    def dataReceived(self, data):
        response = {
            "type": "error",
            "message": "Unknown error"
        }
        try:
            message = json.loads(data)
            if message["type"] == "actions":
                response = self.handleActions(message["actions"], message["data"], message["files"])
                self.transport.loseConnection()
            else:
                response = {
                    "type": "error",
                    "message": "Invalid message type"
                }
        except json.JSONDecodeError:
            response = {
                "type": "error",
                "message": "Invalid message format"
            }
        finally:
            self.transport.write(json.dumps(response).encode())

    def handleActions(self, actions, data, files):
        self.actions = actions
        self.data = data
        theirRequiredData = self.factory.fs_manager.getFileContents(files)
        response = {
            "type": "data",
            "data": theirRequiredData
        }
        return response
