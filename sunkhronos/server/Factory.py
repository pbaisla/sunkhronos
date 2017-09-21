from sunkhronos.server.Protocol import SyncProtocol
from twisted.internet.protocol import Factory


class SyncFactory(Factory):

    def __init__(self, fs_manager):
        self.fs_manager = fs_manager

    def buildProtocol(self, addr):
        return SyncProtocol(self)
