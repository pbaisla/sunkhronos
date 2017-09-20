from sunkhronos.server.Factory import SyncFactory
from twisted.internet import reactor

def main():
    reactor.listenTCP(8123, SyncFactory())
    reactor.run()

if __name__ == '__main__':
    main()
