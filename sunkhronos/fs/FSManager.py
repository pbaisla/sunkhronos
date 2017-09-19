import os
import pickle

from os.path import abspath, join, relpath
from watchdog.utils.dirsnapshot import DirectorySnapshot, DirectorySnapshotDiff


class FSManager():
    def __init__(self, dir_path, snapshot_path):
        self.dir_path = dir_path
        self.snapshot_path = snapshot_path
        self.listdir = lambda path: [p for p in os.listdir(path) if p != abspath(snapshot_path)]

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
                diff_dict[key[1:]] = list(map(lambda p1, p2: (relpath(p1, self.dir_path), relpath(p2, self.dir_path)), value))
            else:
                diff_dict[key[1:]] = list(map(lambda p: relpath(p, self.dir_path), value))
        return diff_dict

    def getLastSyncSnapshot(self):
        try:
            with open(self.snapshot_path, 'rb') as snapshot_file:
                snapshot = pickle.load(snapshot_file)
        except FileNotFoundError:
            snapshot = DirectorySnapshot(self.dir_path, listdir=lambda _: [])
        return snapshot

    def writeSnapshot(self):
        snapshot = DirectorySnapshot(self.dir_path, listdir=self.listdir)
        with open(self.snapshot_path, 'wb') as snapshot_file:
            pickle.dump(snapshot, snapshot_file)

    def createDirectory(self, path):
        os.makedirs(relpath(path, self.dir_path), exist_ok=True)

    def deleteDirectory(self, path):
        os.rmdir(relpath(path, self.dir_path))

    def moveDirectory(self, src_path, dest_path):
        os.renames(relpath(src_path, self.dir_path), relpath(dest_path, self.dir_path))

    def deleteFile(self, path):
        os.remove(relpath(path, self.dir_path))

    def moveFile(self, src_path, dest_path):
        os.renames(relpath(src_path, self.dir_path), relpath(dest_path, self.dir_path))

    def readFile(self, path):
        with open(relpath(path, self.dir_path), 'r') as f:
            return f.read()

    def writeFile(self, path, contents):
        with open(relpath(path, self.dir_path), 'w') as f:
            f.write(contents)

    def getFileContents(self, files):
        data = {}
        for filename in files:
            data[filename] = self.readFile(filename)
        return data

