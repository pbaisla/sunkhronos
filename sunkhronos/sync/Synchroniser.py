class Synchroniser():
    def __init__(self, ownChanges, theirChanges):
        self.ownChanges = ownChanges
        self.theirChanges = theirChanges
        self.preprocessChanges()

    def preprocessChanges(self):
        for moved_file_src, _ in self.ownChanges["files_moved"]:
            if moved_file_src in self.ownChanges["files_modified"]:
                self.ownChanges["files_modified"].remove(moved_file_src)

        for moved_file_src, _ in self.theirChanges["files_moved"]:
            if moved_file_src in self.theirChanges["files_modified"]:
                self.theirChanges["files_modified"].remove(moved_file_src)

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

        if len(self.theirChanges["files_moved"]):
            their_moved_src, their_moved_dest = map(list, zip(*self.theirChanges["files_moved"]))
        else:
            their_moved_src, their_moved_dest = [], []

        if len(self.ownChanges["files_moved"]):
            own_moved_src, own_moved_dest = map(list, zip(*self.ownChanges["files_moved"]))
        else:
            own_moved_src, own_moved_dest = [], []

        for deleted_file in self.ownChanges["files_deleted"]:
            if deleted_file not in (self.theirChanges["files_deleted"] + self.theirChanges["files_modified"] + self.theirChanges["files_created"] + their_moved_src + their_moved_dest):
                theirActions.append(('delete', deleted_file))

        for deleted_file in self.theirChanges["files_deleted"]:
            if deleted_file not in (self.ownChanges["files_deleted"] + self.ownChanges["files_modified"] + self.ownChanges["files_created"] + own_moved_src + own_moved_dest):
                ownActions.append(('delete', deleted_file))

        return (ownActions, theirActions)

    def getFileMoveActions(self):
        ownActions = []
        theirActions = []

        for moved_file in self.ownChanges["files_moved"]:
            if moved_file not in self.theirChanges["files_moved"] and moved_file[0] not in self.theirChanges["files_deleted"] and moved_file[1] not in self.theirChanges["files_created"]:
                theirActions.append(('move', moved_file))

        for moved_file in self.theirChanges["files_moved"]:
            if moved_file not in self.ownChanges["files_moved"] and moved_file[0] not in self.ownChanges["files_deleted"] and moved_file[1] not in self.ownChanges["files_created"]:
                ownActions.append(('move', moved_file))

        return (ownActions, theirActions)

    def getFileCreateActions(self):
        ownActions = []
        theirActions = []

        if len(self.theirChanges["files_moved"]):
            their_moved_src, their_moved_dest = map(list, zip(*self.theirChanges["files_moved"]))
        else:
            their_moved_src, their_moved_dest = [], []

        if len(self.ownChanges["files_moved"]):
            own_moved_src, own_moved_dest = map(list, zip(*self.ownChanges["files_moved"]))
        else:
            own_moved_src, own_moved_dest = [], []

        for created_file in self.ownChanges["files_created"]:
            if created_file not in their_moved_dest:
                theirActions.append(('create', created_file))

        for created_file in self.theirChanges["files_created"]:
            if created_file not in own_moved_dest:
                ownActions.append(('create', created_file))

        return (ownActions, theirActions)

    def getModifyActions(self):
        ownActions = []
        theirActions = []

        return (ownActions, theirActions)

    def getRequiredFiles(self, actions):
        files = []
        for action in actions:
            if action[0] == 'create':
                files.append(action[1])
            elif action[0] == 'move':
                files.append(action[1][0])
        return files

    @staticmethod
    def synchronise(actions, data, fsManager):
        for action in actions:
            if action[0] == 'create':
                fsManager.writeFile(action[1], data[action[1]])
            elif action[0] == 'delete':
                fsManager.deleteFile(action[1])
            elif action[0] == 'move':
                fsManager.moveFile(action[1][0], action[1][1])

