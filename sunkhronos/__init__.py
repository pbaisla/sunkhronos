from sunkhronos.client.Factory import SyncFactory as ClientFactory
from sunkhronos.server.Factory import SyncFactory as ServerFactory
from sunkhronos.fs.FSManager import FSManager
from sunkhronos.sync.Synchroniser import Synchroniser
from twisted.internet import reactor

import argparse

def connect(args):
    fs_manager = FSManager(args.directory, args.backup_directory)
    reactor.connectTCP(args.host, args.port, ClientFactory(fs_manager))
    reactor.run()

def serve(args):
    fs_manager = FSManager(args.directory, args.backup_directory)
    reactor.listenTCP(args.port, ServerFactory(fs_manager))
    reactor.run()

def main():
    parser = argparse.ArgumentParser(description='Keep two folders on different devices in sync')
    subparsers = parser.add_subparsers(title='subcommands', dest='command', help='connect to or start a sunkhronos server')

    connect_parser = subparsers.add_parser('connect', help='connect to a sunkhronos server to sync a directory')
    connect_parser.add_argument('--host', type=str, required=True, help='hostname')
    connect_parser.add_argument('--port', type=int, required=True, help='port')
    connect_parser.add_argument('--directory', type=str, help='path to directory to sync', default='.')
    connect_parser.add_argument('--backup-directory', type=str, help='path to backup of directory to sync', default='./.sunkhronos-backup')

    serve_parser = subparsers.add_parser('serve', help='start a sunkhronos server to sync a directory')
    serve_parser.add_argument('--port', type=int, required=True, help='port')
    serve_parser.add_argument('--directory', type=str, help='path to directory to sync', default='.')
    serve_parser.add_argument('--backup-directory', type=str, help='path to backup of directory to sync', default='./.sunkhronos-backup')

    args = parser.parse_args()

    if args.command == 'connect':
        connect(args)
    elif args.command == 'serve':
        serve(args)
    else:
        parser.error('A subcommand (one of {connect, serve}) is required')

if __name__ == '__main__':
    main()

