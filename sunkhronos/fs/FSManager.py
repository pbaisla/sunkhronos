import os
import pickle
import shutil

from itertools import starmap
from os.path import basename, join, normpath, relpath
from watchdog.utils.dirsnapshot import DirectorySnapshot, DirectorySnapshotDiff


class FSManager():
    def __init__(self, dir_path, backup_path):
        self.dir_path = dir_path
        self.backup_path = backup_path
        self.listdir = lambda path: [p for p in os.listdir(path) if p != basename(normpath(backup_path))]

    def getChangesSinceLastSync(self):
        old = self.getLastSyncSnapshot()
        now = self.getCurrentSnapshot()
        diff = DirectorySnapshotDiff(old, now)
        return self.getDictFromDiff(diff)

    def getCurrentSnapshot(self):
        return DirectorySnapshot(self.dir_path, listdir=self.listdir)

    def getDictFromDiff(self, diff):
        diff_dict = {}
        for key, value in diff.__dict__.items():
            if key == '_dirs_moved' or key == '_files_moved':
                diff_dict[key[1:]] = list(starmap(lambda p1, p2: (relpath(p1, self.dir_path), relpath(p2, self.dir_path)), value))
            else:
                diff_dict[key[1:]] = list(map(lambda p: relpath(p, self.dir_path), value))
        return diff_dict

    def getLastSyncSnapshot(self):
        try:
            with open(join(self.backup_path, '.snapshot'), 'rb') as snapshot_file:
                snapshot = pickle.load(snapshot_file)
        except FileNotFoundError:
            snapshot = DirectorySnapshot(self.dir_path, listdir=lambda _: [])
        return snapshot

    def updateLastSyncState(self):
        snapshot = DirectorySnapshot(self.dir_path, listdir=self.listdir)
        try:
            self.deleteDirectory(self.backup_path)
        except FileNotFoundError:
            pass
        self.copyDirectory(self.dir_path, self.backup_path)
        with open(join(self.backup_path, '.snapshot'), 'wb') as snapshot_file:
            pickle.dump(snapshot, snapshot_file)

    def createDirectory(self, path):
        os.makedirs(relpath(path, self.dir_path), exist_ok=True)

    def deleteDirectory(self, path):
        shutil.rmtree(relpath(path, self.dir_path))

    def moveDirectory(self, src_path, dest_path):
        os.renames(relpath(src_path, self.dir_path), relpath(dest_path, self.dir_path))

    def copyDirectory(self, src_path, dest_path):
        shutil.copytree(relpath(src_path, self.dir_path), relpath(dest_path, self.dir_path), ignore=lambda *_: [basename(normpath(self.backup_path))])

    def deleteFile(self, path):
        os.remove(relpath(path, self.dir_path))

    def moveFile(self, src_path, dest_path):
        os.renames(relpath(src_path, self.dir_path), relpath(dest_path, self.dir_path))

    def readFile(self, path):
        with open(relpath(path, self.dir_path), 'r') as f:
            return f.readlines()

    def writeFile(self, path, contents):
        with open(relpath(path, self.dir_path), 'w') as f:
            f.writelines(contents)

    def readBackupFile(self, path):
        try:
            return self.readFile(join(self.backup_path, path))
        except FileNotFoundError:
            return []

    def getFileContents(self, files):
        data = {}
        for filename in files:
            data[filename] = self.readFile(filename)
        return data

