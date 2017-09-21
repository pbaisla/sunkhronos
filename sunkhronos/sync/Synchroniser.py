from sunkhronos.sync.merge import merge

class Synchroniser():
    def __init__(self, ownChanges, theirChanges):
        self.ownChanges = ownChanges
        self.theirChanges = theirChanges
        self.own_moved_src = []
        self.own_moved_dest = []
        self.their_moved_src = []
        self.their_moved_dest = []

        self.preprocessChanges()
        if len(self.theirChanges["files_moved"]):
            self.their_moved_src, self.their_moved_dest = map(list, zip(*self.theirChanges["files_moved"]))
        if len(self.ownChanges["files_moved"]):
            self.own_moved_src, self.own_moved_dest = map(list, zip(*self.ownChanges["files_moved"]))

    def preprocessChanges(self):
        ownFilesMoved = []
        theirFilesMoved = []

        for moved_file_src, moved_file_dest in self.ownChanges["files_moved"]:
            if moved_file_src in self.ownChanges["files_modified"]:
                self.ownChanges["files_modified"].remove(moved_file_src)
                self.ownChanges["files_created"].append(moved_file_dest)
            else:
                ownFilesMoved.append((moved_file_src, moved_file_dest))

        for moved_file_src, moved_file_dest in self.theirChanges["files_moved"]:
            if moved_file_src in self.theirChanges["files_modified"]:
                self.theirChanges["files_modified"].remove(moved_file_src)
                self.theirChanges["files_created"].append(moved_file_dest)
            else:
                theirFilesMoved.append((moved_file_src, moved_file_dest))

        self.ownChanges["files_moved"] = ownFilesMoved
        self.theirChanges["files_moved"] = theirFilesMoved

    def getActions(self):
        actions = []
        actions.append(self.getFileDeleteActions())
        actions.append(self.getFileMoveActions())
        actions.append(self.getFileCreateActions())
        actions.append(self.getModifyActions())

        if len(actions):
            ownActions, theirActions = map(list, zip(*actions))
        else:
            ownActions, theirActions = [], []

        flattenedOwnActions = [action for ownActionList in ownActions for action in ownActionList]
        flattenedTheirActions = [action for theirActionList in theirActions for action in theirActionList]

        return (flattenedOwnActions, flattenedTheirActions)

    def getFileDeleteActions(self):
        ownActions = []
        theirActions = []

        for deleted_file in self.ownChanges["files_deleted"]:
            if deleted_file not in (self.theirChanges["files_deleted"] + self.theirChanges["files_modified"] + self.theirChanges["files_created"] + self.their_moved_src + self.their_moved_dest):
                theirActions.append(('delete', deleted_file))

        for deleted_file in self.theirChanges["files_deleted"]:
            if deleted_file not in (self.ownChanges["files_deleted"] + self.ownChanges["files_modified"] + self.ownChanges["files_created"] + self.own_moved_src + self.own_moved_dest):
                ownActions.append(('delete', deleted_file))

        return (ownActions, theirActions)

    def getFileMoveActions(self):
        ownActions = []
        theirActions = []

        for moved_file_src, moved_file_dest in self.ownChanges["files_moved"]:
            if moved_file_src in self.theirChanges["files_modified"] and moved_file_dest in self.theirChanges["files_created"]:
                theirActions.append(('create', moved_file_src))
                theirActions.append(('create', moved_file_dest))
            elif moved_file_dest in self.theirChanges["files_created"]:
                theirActions.append(('delete', moved_file_src))
                theirActions.append(('create', moved_file_dest))
            elif moved_file_src in self.theirChanges["files_deleted"]:
                theirActions.append(('create', moved_file_dest))
            elif moved_file_src in self.their_moved_src:
                if (moved_file_src, moved_file_dest) in self.theirChanges["files_moved"]:
                    pass # No action required
                else:
                    theirActions.append(('create', moved_file_dest))
            else:
                theirActions.append(('move', (moved_file_src, moved_file_dest)))

        for moved_file_src, moved_file_dest in self.theirChanges["files_moved"]:
            if moved_file_src in self.ownChanges["files_modified"] and moved_file_dest in self.ownChanges["files_created"]:
                ownActions.append(('create', moved_file_src))
                ownActions.append(('create', moved_file_dest))
            elif moved_file_dest in self.ownChanges["files_created"]:
                ownActions.append(('delete', moved_file_src))
                ownActions.append(('create', moved_file_dest))
            elif moved_file_src in self.ownChanges["files_deleted"]:
                ownActions.append(('create', moved_file_dest))
            elif moved_file_src in self.own_moved_src:
                if (moved_file_src, moved_file_dest) in self.ownChanges["files_moved"]:
                    pass # No action required
                else:
                    ownActions.append(('create', moved_file_dest))
            else:
                ownActions.append(('move', (moved_file_src, moved_file_dest)))

        return (ownActions, theirActions)

    def getFileCreateActions(self):
        ownActions = []
        theirActions = []

        for created_file in self.ownChanges["files_created"]:
            theirActions.append(('create', created_file))

        for created_file in self.theirChanges["files_created"]:
            ownActions.append(('create', created_file))

        return (ownActions, theirActions)

    def getModifyActions(self):
        ownActions = []
        theirActions = []

        for modified_file in self.ownChanges["files_modified"]:
            if modified_file in self.theirChanges["files_deleted"]:
                theirActions.append(('create', modified_file))
            elif modified_file in self.their_moved_src:
                theirActions.append(('create', modified_file))
            else:
                theirActions.append(('modify', modified_file))

        for modified_file in self.theirChanges["files_modified"]:
            if modified_file in self.ownChanges["files_deleted"]:
                ownActions.append(('create', modified_file))
            elif modified_file in self.own_moved_src:
                ownActions.append(('create', modified_file))
            else:
                ownActions.append(('modify', modified_file))

        return (ownActions, theirActions)

    def getData(self, theirFilesData, ownRequiredFiles, theirRequiredFiles, fsManager):
        ownData = theirFilesData
        theirData = {}

        commonFiles = list(set(ownRequiredFiles) & set(theirRequiredFiles))
        for filename in commonFiles:
            ownFileData = fsManager.readFile(filename)
            originalFileData = fsManager.readBackupFile(filename)
            theirFileData = theirFilesData[filename]
            mergedFile = merge(ownFileData, originalFileData, theirFileData)
            ownData[filename] = mergedFile
            theirData[filename] = mergedFile

        remainingFiles = list(set(theirRequiredFiles) - set(commonFiles))
        for filename in remainingFiles:
            contents = fsManager.readFile(filename)
            theirData[filename] = contents

        return (ownData, theirData)

    def getRequiredFiles(self, actions):
        files = []
        for action in actions:
            if action[0] == 'create':
                files.append(action[1])
            elif action[0] == 'modify':
                files.append(action[1])
            elif action[0] == 'move':
                files.append(action[1][1])
        return files

    @staticmethod
    def synchronise(actions, data, fsManager):
        for action in actions:
            if action[0] == 'create' or action[0] == 'modify':
                fsManager.writeFile(action[1], data[action[1]])
            elif action[0] == 'delete':
                fsManager.deleteFile(action[1])
            elif action[0] == 'move':
                fsManager.moveFile(action[1][0], action[1][1])

