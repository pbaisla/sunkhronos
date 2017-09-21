import json

from sunkhronos.sync.Synchroniser import Synchroniser
from twisted.internet.error import ConnectionDone
from twisted.internet import reactor
from twisted.internet.protocol import Protocol


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
            self.factory.fs_manager.updateLastSyncState()
            reactor.stop()

    def dataReceived(self, data):
        response = {
            "type": "error",
            "message": "Unknown error"
        }
        try:
            message = json.loads(data)
            if message["type"] == "actions":
                response = self.handleActions(message["actions"], message["files"])
            elif message["type"] == "data":
                response = self.handleData(message["data"])
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

    def handleActions(self, actions, files):
        self.actions = actions
        theirRequiredData = self.factory.fs_manager.getFileContents(files)
        response = {
            "type": "data",
            "data": theirRequiredData
        }
        return response

    def handleData(self, data):
        self.data = data
        response = {
            "type": "end"
        }
        return response
