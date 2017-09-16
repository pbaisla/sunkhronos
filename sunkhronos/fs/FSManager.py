import os
import pickle

from os.path import abspath
from watchdog.utils.dirsnapshot import DirectorySnapshotDiff, DirectorySnapshotDiff


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
        return DirectorySnapshot('.', listdir=self.listdir)

    def getDictFromDiff(self, diff):
        diff_dict = {}
        for key, value in diff.__dict__.items():
            diff_dict[key[1:]] = value
        return diff_dict

    def getLastSyncSnapshot(self):
        try:
            with open(snapshot_path, 'rb') as snapshot_file:
                snapshot = pickle.load(snapshot_file)
        except FileNotFoundError:
            snapshot = DirectorySnapshot('.', listdir=lambda _: [])
        return snapshot

    def writeSnapshot(self):
        snapshot = DirectorySnapshot('.', listdir=self.listdir)
        with open(self.snapshot_path, 'wb') as snapshot_file:
            pickle.dump(snapshot, snapshot_file)

    def createDirectory(self, path):
        os.makedirs(path, exist_ok=True)

    def deleteDirectory(self, path):
        os.rmdir(path)

    def moveDirectory(self, src_path, dest_path):
        os.renames(src_path, dest_path)

    def deleteFile(self, path):
        os.remove(path)

    def moveFile(self, src_path, dest_path):
        os.renames(src_path, dest_path)

    def readFile(self, path):
        with open(path, 'r') as f:
            return f.read()

    def writeFile(self, path, contents):
        with open(path, 'w') as f:
            f.write(contents)

