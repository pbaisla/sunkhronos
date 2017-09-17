class Synchroniser():
    def __init__(self, ownChanges, theirChanges):
        self.ownChanges = ownChanges
        self.theirChanges = theirChanges

    def getActions(self):
        actions = []
        actions.append(self.getFileDeleteActions())
        actions.append(self.getDirectoryMoveActions())
        actions.append(self.getDirectoryCreateActions())
        actions.append(self.getFileMoveActions())
        actions.append(self.getDirectoryDeleteActions())
        actions.append(self.getFileCreateActions())
        actions.append(self.getModifyActions())
        if len(actions):
            ownActions, theirActions = zip(*actions)
        else:
            ownActions, theirActions = [], []
        flattenedOwnActions = [action for ownActionList in ownActions for action in ownActionList]
        flattenedTheirActions = [action for theirActionList in theirActions for action in theirActionList]
        return (flattenedOwnActions, flattenedTheirActions)

    def getFileDeleteActions(self):
        ownActions = []
        theirActions = []
        if len(self.theirChanges["files_moved"]):
            their_moved_src, their_moved_dest = zip(*self.theirChanges["files_moved"])
        else:
            their_moved_src, their_moved_dest = [], []
        if len(self.ownChanges["files_moved"]):
            own_moved_src, own_moved_dest = zip(*self.ownChanges["files_moved"])
        else:
            own_moved_src, own_moved_dest = [], []
        for deleted_file in self.ownChanges["files_deleted"]:
            if deleted_file not in (self.theirChanges["files_deleted"] + self.theirChanges["files_modified"] + self.theirChanges["files_created"] + their_moved_src + their_moved_dest):
                theirActions.append(('delete', deleted_file))
        for deleted_file in self.theirChanges["files_deleted"]:
            if deleted_file not in (self.ownChanges["files_deleted"] + self.ownChanges["files_modified"] + self.ownChanges["files_created"] + own_moved_src + own_moved_dest):
                ownActions.append(('delete', deleted_file))
        return (ownActions, theirActions)

    def getDirectoryMoveActions(self):
        ownActions = []
        theirActions = []
        for moved_dir in self.ownChanges["dirs_moved"]:
            if moved_dir not in self.theirChanges["dirs_moved"] and moved_dir[0] not in self.theirChanges["dirs_deleted"] and moved_dir[1] not in self.theirChanges["dirs_created"]:
                theirActions.append(('move_dir', moved_dir))
        for moved_dir in self.theirChanges["dirs_moved"]:
            if moved_dir not in self.ownChanges["dirs_moved"] and moved_dir[0] not in self.ownChanges["dirs_deleted"] and moved_dir[1] not in self.ownChanges["dirs_created"]:
                ownActions.append(('move_dir', moved_dir))
        return (ownActions, theirActions)

    def getDirectoryCreateActions(self):
        ownActions = []
        theirActions = []
        if len(self.theirChanges["dirs_moved"]):
            their_moved_src, their_moved_dest = zip(*self.theirChanges["dirs_moved"])
        else:
            their_moved_src, their_moved_dest = [], []
        if len(self.ownChanges["dirs_moved"]):
            own_moved_src, own_moved_dest = zip(*self.ownChanges["dirs_moved"])
        else:
            own_moved_src, own_moved_dest = [], []
        for created_dir in self.ownChanges["dirs_created"]:
            if created_dir not in (self.theirChanges["dirs_created"] + their_moved_dest):
                theirActions.append(('create_dir', created_dir))
        for created_dir in self.theirChanges["dirs_created"]:
            if created_dir not in (self.ownChanges["dirs_created"] + own_moved_dest):
                ownActions.append(('create_dir', created_dir))
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

    def getDirectoryDeleteActions(self):
        ownActions = []
        theirActions = []
        if len(self.theirChanges["dirs_moved"]):
            their_moved_src, their_moved_dest = zip(*self.theirChanges["dirs_moved"])
        else:
            their_moved_src, their_moved_dest = [], []
        if len(self.ownChanges["dirs_moved"]):
            own_moved_src, own_moved_dest = zip(*self.ownChanges["dirs_moved"])
        else:
            own_moved_src, own_moved_dest = [], []
        for deleted_dir in self.ownChanges["dirs_deleted"]:
            if deleted_dir not in (self.theirChanges["dirs_deleted"] + self.theirChanges["dirs_modified"] + self.theirChanges["dirs_created"] + their_moved_src + their_moved_dest):
                theirActions.append(('delete_dir', deleted_dir))
        for deleted_dir in self.theirChanges["dirs_deleted"]:
            if deleted_dir not in (self.ownChanges["dirs_deleted"] + self.ownChanges["dirs_modified"] + self.ownChanges["dirs_created"] + own_moved_src + own_moved_dest):
                ownActions.append(('delete_dir', deleted_dir))
        return (ownActions, theirActions)

    def getFileCreateActions(self):
        ownActions = []
        theirActions = []
        if len(self.theirChanges["files_moved"]):
            their_moved_src, their_moved_dest = zip(*self.theirChanges["files_moved"])
        else:
            their_moved_src, their_moved_dest = [], []
        if len(self.ownChanges["files_moved"]):
            own_moved_src, own_moved_dest = zip(*self.ownChanges["files_moved"])
        else:
            own_moved_src, own_moved_dest = [], []
        for created_file in self.ownChanges["files_created"]:
            if created_file not in (self.theirChanges["files_created"] + their_moved_dest):
                theirActions.append(('create', created_file))
        for created_file in self.theirChanges["files_created"]:
            if created_file not in (self.ownChanges["files_created"] + own_moved_dest):
                ownActions.append(('create', created_file))
        return (ownActions, theirActions)

    def getModifyActions(self):
        return ([], [])

    def getRequiredData(self, changes):
        pass

    def getRequiredFiles(self, changes):
        pass

