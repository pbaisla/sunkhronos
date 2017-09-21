from sunkhronos.fs.FSManager import FSManager
from sunkhronos.sync.Synchroniser import Synchroniser
from twisted.internet.error import ConnectionDone
from twisted.internet.protocol import Protocol

import json

class SyncProtocol(Protocol):
    def __init__(self, factory):
        self.factory = factory
        self.actions = []
        self.data = {}

    def connectionLost(self, reason):
        if reason.check(ConnectionDone):
            Synchroniser.synchronise(self.actions, self.data, self.factory.fs_manager)
            self.factory.fs_manager.updateLastSyncState()

    def dataReceived(self, data):
        response = {
            "type": "error",
            "message": "Unknown error"
        }
        try:
            message = json.loads(data)
            if message["type"] == "changes":
                response = self.handleChanges(message["changes"])
            elif message["type"] == "data":
                response = self.handleData(message["data"])
            elif message["type"] == "end":
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

    def handleChanges(self, theirChanges):
        ownChanges = self.factory.fs_manager.getChangesSinceLastSync()
        self.synchroniser = Synchroniser(ownChanges, theirChanges)
        ownActions, theirActions = self.synchroniser.getActions()
        self.ownRequiredFiles = self.synchroniser.getRequiredFiles(ownActions)
        self.theirRequiredFiles = self.synchroniser.getRequiredFiles(theirActions)
        self.actions = ownActions
        response = {
            "type": "actions",
            "actions": theirActions,
            "files": self.ownRequiredFiles,
        }
        return response

    def handleData(self, data):
        ownData, theirData = self.synchroniser.getData(data, self.ownRequiredFiles, self.theirRequiredFiles, self.factory.fs_manager)
        self.data = ownData
        response = {
            "type": "data",
            "data": theirData,
        }
        return response

