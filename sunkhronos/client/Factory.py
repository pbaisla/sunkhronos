from sunkhronos.client.Protocol import SyncProtocol
from twisted.internet.protocol import ClientFactory

class SyncFactory(ClientFactory):

    def __init__(self, fs_manager):
        self.fs_manager = fs_manager

    def buildProtocol(self, addr):
        return SyncProtocol(self)

