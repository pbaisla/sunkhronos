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
            Synchroniser.synchronise(self.actions, self.data)

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
        ownRequiredFiles = self.synchroniser.getRequiredFiles(ownActions)
        theirRequiredFiles = self.synchroniser.getRequiredFiles(theirActions)
        theirRequiredData = FSManager.getFileContents(theirRequiredFiles)
        self.ownActions = ownActions
        response = {
            "type": "actions",
            "actions": theirActions,
            "files": ownRequiredFiles,
            "data": theirRequiredData,
        }
        return response

    def handleData(self, data):
        self.data = data

