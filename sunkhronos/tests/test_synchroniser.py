from unittest import TestCase
from sunkhronos.sync.Synchroniser import Synchroniser

class SynchroniserTestCase(TestCase):

    def test_file_deleted_on_own_device(self):
        ownChanges = {
            "dirs_created": [],
            "dirs_deleted": [],
            "dirs_modified": [],
            "dirs_moved": [],
            "files_created": [],
            "files_deleted": ["deleted_file"],
            "files_modified": [],
            "files_moved": [],
        }
        theirChanges = {
            "dirs_created": [],
            "dirs_deleted": [],
            "dirs_modified": [],
            "dirs_moved": [],
            "files_created": [],
            "files_deleted": [],
            "files_modified": [],
            "files_moved": [],
        }
        synchroniser = Synchroniser(ownChanges, theirChanges)
        ownActions, theirActions = synchroniser.getActions()
        expectedOwnActions = []
        expectedTheirActions = [("delete", "deleted_file")]
        self.assertCountEqual(ownActions, expectedOwnActions)
        self.assertCountEqual(theirActions, expectedTheirActions)

    def test_file_deleted_on_their_device(self):
        ownChanges = {
            "dirs_created": [],
            "dirs_deleted": [],
            "dirs_modified": [],
            "dirs_moved": [],
            "files_created": [],
            "files_deleted": [],
            "files_modified": [],
            "files_moved": [],
        }
        theirChanges = {
            "dirs_created": [],
            "dirs_deleted": [],
            "dirs_modified": [],
            "dirs_moved": [],
            "files_created": [],
            "files_deleted": ["deleted_file"],
            "files_modified": [],
            "files_moved": [],
        }
        synchroniser = Synchroniser(ownChanges, theirChanges)
        ownActions, theirActions = synchroniser.getActions()
        expectedOwnActions = [("delete", "deleted_file")]
        expectedTheirActions = []
        self.assertCountEqual(ownActions, expectedOwnActions)
        self.assertCountEqual(theirActions, expectedTheirActions)

    def test_file_deleted_on_both_devices(self):
        ownChanges = {
            "dirs_created": [],
            "dirs_deleted": [],
            "dirs_modified": [],
            "dirs_moved": [],
            "files_created": [],
            "files_deleted": ["deleted_file"],
            "files_modified": [],
            "files_moved": [],
        }
        theirChanges = {
            "dirs_created": [],
            "dirs_deleted": [],
            "dirs_modified": [],
            "dirs_moved": [],
            "files_created": [],
            "files_deleted": ["deleted_file"],
            "files_modified": [],
            "files_moved": [],
        }
        synchroniser = Synchroniser(ownChanges, theirChanges)
        ownActions, theirActions = synchroniser.getActions()
        expectedOwnActions = []
        expectedTheirActions = []
        self.assertCountEqual(ownActions, expectedOwnActions)

    def test_file_created_on_own_device(self):
        ownChanges = {
            "dirs_created": [],
            "dirs_deleted": [],
            "dirs_modified": [],
            "dirs_moved": [],
            "files_created": ["created_file"],
            "files_deleted": [],
            "files_modified": [],
            "files_moved": [],
        }
        theirChanges = {
            "dirs_created": [],
            "dirs_deleted": [],
            "dirs_modified": [],
            "dirs_moved": [],
            "files_created": [],
            "files_deleted": [],
            "files_modified": [],
            "files_moved": [],
        }
        synchroniser = Synchroniser(ownChanges, theirChanges)
        ownActions, theirActions = synchroniser.getActions()
        expectedOwnActions = []
        expectedTheirActions = [("create", "created_file")]
        self.assertCountEqual(ownActions, expectedOwnActions)
        self.assertCountEqual(theirActions, expectedTheirActions)

    def test_file_created_on_their_device(self):
        ownChanges = {
            "dirs_created": [],
            "dirs_deleted": [],
            "dirs_modified": [],
            "dirs_moved": [],
            "files_created": [],
            "files_deleted": [],
            "files_modified": [],
            "files_moved": [],
        }
        theirChanges = {
            "dirs_created": [],
            "dirs_deleted": [],
            "dirs_modified": [],
            "dirs_moved": [],
            "files_created": ["created_file"],
            "files_deleted": [],
            "files_modified": [],
            "files_moved": [],
        }
        synchroniser = Synchroniser(ownChanges, theirChanges)
        ownActions, theirActions = synchroniser.getActions()
        expectedOwnActions = [("create", "created_file")]
        expectedTheirActions = []
        self.assertCountEqual(ownActions, expectedOwnActions)
        self.assertCountEqual(theirActions, expectedTheirActions)

    def test_file_created_on_both_devices(self):
        ownChanges = {
            "dirs_created": [],
            "dirs_deleted": [],
            "dirs_modified": [],
            "dirs_moved": [],
            "files_created": ["created_file"],
            "files_deleted": [],
            "files_modified": [],
            "files_moved": [],
        }
        theirChanges = {
            "dirs_created": [],
            "dirs_deleted": [],
            "dirs_modified": [],
            "dirs_moved": [],
            "files_created": ["created_file"],
            "files_deleted": [],
            "files_modified": [],
            "files_moved": [],
        }
        synchroniser = Synchroniser(ownChanges, theirChanges)
        ownActions, theirActions = synchroniser.getActions()
        expectedOwnActions = [("create", "created_file")]
        expectedTheirActions = [("create", "created_file")]
        self.assertCountEqual(ownActions, expectedOwnActions)
        self.assertCountEqual(theirActions, expectedTheirActions)

    def test_file_modified_on_own_device(self):
        ownChanges = {
            "dirs_created": [],
            "dirs_deleted": [],
            "dirs_modified": [],
            "dirs_moved": [],
            "files_created": [],
            "files_deleted": [],
            "files_modified": ["modified_file"],
            "files_moved": [],
        }
        theirChanges = {
            "dirs_created": [],
            "dirs_deleted": [],
            "dirs_modified": [],
            "dirs_moved": [],
            "files_created": [],
            "files_deleted": [],
            "files_modified": [],
            "files_moved": [],
        }
        synchroniser = Synchroniser(ownChanges, theirChanges)
        ownActions, theirActions = synchroniser.getActions()
        expectedOwnActions = []
        expectedTheirActions = [("modify", "modified_file")]
        self.assertCountEqual(ownActions, expectedOwnActions)
        self.assertCountEqual(theirActions, expectedTheirActions)

    def test_file_modified_on_their_device(self):
        ownChanges = {
            "dirs_created": [],
            "dirs_deleted": [],
            "dirs_modified": [],
            "dirs_moved": [],
            "files_created": [],
            "files_deleted": [],
            "files_modified": [],
            "files_moved": [],
        }
        theirChanges = {
            "dirs_created": [],
            "dirs_deleted": [],
            "dirs_modified": [],
            "dirs_moved": [],
            "files_created": [],
            "files_deleted": [],
            "files_modified": ["modified_file"],
            "files_moved": [],
        }
        synchroniser = Synchroniser(ownChanges, theirChanges)
        ownActions, theirActions = synchroniser.getActions()
        expectedOwnActions = [("modify", "modified_file")]
        expectedTheirActions = []
        self.assertCountEqual(ownActions, expectedOwnActions)
        self.assertCountEqual(theirActions, expectedTheirActions)

    def test_file_modified_on_both_devices(self):
        ownChanges = {
            "dirs_created": [],
            "dirs_deleted": [],
            "dirs_modified": [],
            "dirs_moved": [],
            "files_created": [],
            "files_deleted": [],
            "files_modified": ["modified_file"],
            "files_moved": [],
        }
        theirChanges = {
            "dirs_created": [],
            "dirs_deleted": [],
            "dirs_modified": [],
            "dirs_moved": [],
            "files_created": [],
            "files_deleted": [],
            "files_modified": ["modified_file"],
            "files_moved": [],
        }
        synchroniser = Synchroniser(ownChanges, theirChanges)
        ownActions, theirActions = synchroniser.getActions()
        expectedOwnActions = [("modify", "modified_file")]
        expectedTheirActions = [("modify", "modified_file")]
        self.assertCountEqual(ownActions, expectedOwnActions)
        self.assertCountEqual(theirActions, expectedTheirActions)

    def test_file_moved_on_own_device(self):
        ownChanges = {
            "dirs_created": [],
            "dirs_deleted": [],
            "dirs_modified": [],
            "dirs_moved": [],
            "files_created": [],
            "files_deleted": [],
            "files_modified": [],
            "files_moved": [("moved_file_src", "moved_file_dest")],
        }
        theirChanges = {
            "dirs_created": [],
            "dirs_deleted": [],
            "dirs_modified": [],
            "dirs_moved": [],
            "files_created": [],
            "files_deleted": [],
            "files_modified": [],
            "files_moved": [],
        }
        synchroniser = Synchroniser(ownChanges, theirChanges)
        ownActions, theirActions = synchroniser.getActions()
        expectedOwnActions = []
        expectedTheirActions = [("move", ("moved_file_src", "moved_file_dest"))]
        self.assertCountEqual(ownActions, expectedOwnActions)
        self.assertCountEqual(theirActions, expectedTheirActions)

    def test_file_moved_on_their_device(self):
        ownChanges = {
            "dirs_created": [],
            "dirs_deleted": [],
            "dirs_modified": [],
            "dirs_moved": [],
            "files_created": [],
            "files_deleted": [],
            "files_modified": [],
            "files_moved": [],
        }
        theirChanges = {
            "dirs_created": [],
            "dirs_deleted": [],
            "dirs_modified": [],
            "dirs_moved": [],
            "files_created": [],
            "files_deleted": [],
            "files_modified": [],
            "files_moved": [("moved_file_src", "moved_file_dest")],
        }
        synchroniser = Synchroniser(ownChanges, theirChanges)
        ownActions, theirActions = synchroniser.getActions()
        expectedOwnActions = [("move", ("moved_file_src", "moved_file_dest"))]
        expectedTheirActions = []
        self.assertCountEqual(ownActions, expectedOwnActions)
        self.assertCountEqual(theirActions, expectedTheirActions)

    def test_file_moved_on_both_devices_to_same_destination(self):
        ownChanges = {
            "dirs_created": [],
            "dirs_deleted": [],
            "dirs_modified": [],
            "dirs_moved": [],
            "files_created": [],
            "files_deleted": [],
            "files_modified": [],
            "files_moved": [("moved_file_src", "moved_file_dest")],
        }
        theirChanges = {
            "dirs_created": [],
            "dirs_deleted": [],
            "dirs_modified": [],
            "dirs_moved": [],
            "files_created": [],
            "files_deleted": [],
            "files_modified": [],
            "files_moved": [("moved_file_src", "moved_file_dest")],
        }
        synchroniser = Synchroniser(ownChanges, theirChanges)
        ownActions, theirActions = synchroniser.getActions()
        expectedOwnActions = []
        expectedTheirActions = []
        self.assertCountEqual(ownActions, expectedOwnActions)
        self.assertCountEqual(theirActions, expectedTheirActions)

    def test_file_moved_on_both_devices_to_different_destinations(self):
        ownChanges = {
            "dirs_created": [],
            "dirs_deleted": [],
            "dirs_modified": [],
            "dirs_moved": [],
            "files_created": [],
            "files_deleted": [],
            "files_modified": [],
            "files_moved": [("moved_file_src", "moved_file_dest_own")],
        }
        theirChanges = {
            "dirs_created": [],
            "dirs_deleted": [],
            "dirs_modified": [],
            "dirs_moved": [],
            "files_created": [],
            "files_deleted": [],
            "files_modified": [],
            "files_moved": [("moved_file_src", "moved_file_dest_their")],
        }
        synchroniser = Synchroniser(ownChanges, theirChanges)
        ownActions, theirActions = synchroniser.getActions()
        expectedOwnActions = [("create", "moved_file_dest_their")]
        expectedTheirActions = [("create", "moved_file_dest_own")]
        self.assertCountEqual(ownActions, expectedOwnActions)
        self.assertCountEqual(theirActions, expectedTheirActions)

    def test_file_deleted_on_own_device_but_modified_on_their_device(self):
        ownChanges = {
            "dirs_created": [],
            "dirs_deleted": [],
            "dirs_modified": [],
            "dirs_moved": [],
            "files_created": [],
            "files_deleted": ["modified_file"],
            "files_modified": [],
            "files_moved": [],
        }
        theirChanges = {
            "dirs_created": [],
            "dirs_deleted": [],
            "dirs_modified": [],
            "dirs_moved": [],
            "files_created": [],
            "files_deleted": [],
            "files_modified": ["modified_file"],
            "files_moved": [],
        }
        synchroniser = Synchroniser(ownChanges, theirChanges)
        ownActions, theirActions = synchroniser.getActions()
        expectedOwnActions = [("create", "modified_file")]
        expectedTheirActions = []
        self.assertCountEqual(ownActions, expectedOwnActions)
        self.assertCountEqual(theirActions, expectedTheirActions)

    def test_file_deleted_on_their_device_but_modified_on_own_device(self):
        ownChanges = {
            "dirs_created": [],
            "dirs_deleted": [],
            "dirs_modified": [],
            "dirs_moved": [],
            "files_created": [],
            "files_deleted": [],
            "files_modified": ["modified_file"],
            "files_moved": [],
        }
        theirChanges = {
            "dirs_created": [],
            "dirs_deleted": [],
            "dirs_modified": [],
            "dirs_moved": [],
            "files_created": [],
            "files_deleted": ["modified_file"],
            "files_modified": [],
            "files_moved": [],
        }
        synchroniser = Synchroniser(ownChanges, theirChanges)
        ownActions, theirActions = synchroniser.getActions()
        expectedOwnActions = []
        expectedTheirActions = [("create", "modified_file")]
        self.assertCountEqual(ownActions, expectedOwnActions)
        self.assertCountEqual(theirActions, expectedTheirActions)

    def test_file_deleted_on_own_device_but_moved_on_their_device(self):
        ownChanges = {
            "dirs_created": [],
            "dirs_deleted": [],
            "dirs_modified": [],
            "dirs_moved": [],
            "files_created": [],
            "files_deleted": ["moved_file_src"],
            "files_modified": [],
            "files_moved": [],
        }
        theirChanges = {
            "dirs_created": [],
            "dirs_deleted": [],
            "dirs_modified": [],
            "dirs_moved": [],
            "files_created": [],
            "files_deleted": [],
            "files_modified": [],
            "files_moved": [("moved_file_src", "moved_file_dest")],
        }
        synchroniser = Synchroniser(ownChanges, theirChanges)
        ownActions, theirActions = synchroniser.getActions()
        expectedOwnActions = [("create", "moved_file_dest")]
        expectedTheirActions = []
        self.assertCountEqual(ownActions, expectedOwnActions)
        self.assertCountEqual(theirActions, expectedTheirActions)

    def test_file_deleted_on_their_device_but_moved_on_own_device(self):
        ownChanges = {
            "dirs_created": [],
            "dirs_deleted": [],
            "dirs_modified": [],
            "dirs_moved": [],
            "files_created": [],
            "files_deleted": [],
            "files_modified": [],
            "files_moved": [("moved_file_src", "moved_file_dest")],
        }
        theirChanges = {
            "dirs_created": [],
            "dirs_deleted": [],
            "dirs_modified": [],
            "dirs_moved": [],
            "files_created": [],
            "files_deleted": ["moved_file_src"],
            "files_modified": [],
            "files_moved": [],
        }
        synchroniser = Synchroniser(ownChanges, theirChanges)
        ownActions, theirActions = synchroniser.getActions()
        expectedOwnActions = []
        expectedTheirActions = [("create", "moved_file_dest")]
        self.assertCountEqual(ownActions, expectedOwnActions)
        self.assertCountEqual(theirActions, expectedTheirActions)

    def test_file_modified_and_moved_on_own_device(self):
        ownChanges = {
            "dirs_created": [],
            "dirs_deleted": [],
            "dirs_modified": [],
            "dirs_moved": [],
            "files_created": [],
            "files_deleted": [],
            "files_modified": ["moved_file_src"],
            "files_moved": [("moved_file_src", "moved_file_dest")],
        }
        theirChanges = {
            "dirs_created": [],
            "dirs_deleted": [],
            "dirs_modified": [],
            "dirs_moved": [],
            "files_created": [],
            "files_deleted": [],
            "files_modified": [],
            "files_moved": [],
        }
        synchroniser = Synchroniser(ownChanges, theirChanges)
        ownActions, theirActions = synchroniser.getActions()
        expectedOwnActions = []
        expectedTheirActions = [("create", "moved_file_dest")]
        self.assertCountEqual(ownActions, expectedOwnActions)
        self.assertCountEqual(theirActions, expectedTheirActions)

        pass

    def test_file_modified_and_moved_on_their_device(self):
        ownChanges = {
            "dirs_created": [],
            "dirs_deleted": [],
            "dirs_modified": [],
            "dirs_moved": [],
            "files_created": [],
            "files_deleted": [],
            "files_modified": [],
            "files_moved": [],
        }
        theirChanges = {
            "dirs_created": [],
            "dirs_deleted": [],
            "dirs_modified": [],
            "dirs_moved": [],
            "files_created": [],
            "files_deleted": [],
            "files_modified": ["moved_file_src"],
            "files_moved": [("moved_file_src", "moved_file_dest")],
        }
        synchroniser = Synchroniser(ownChanges, theirChanges)
        ownActions, theirActions = synchroniser.getActions()
        expectedOwnActions = [("create", "moved_file_dest")]
        expectedTheirActions = []
        self.assertCountEqual(ownActions, expectedOwnActions)
        self.assertCountEqual(theirActions, expectedTheirActions)

    def test_file_modified_and_moved_on_both_devices(self):
        ownChanges = {
            "dirs_created": [],
            "dirs_deleted": [],
            "dirs_modified": [],
            "dirs_moved": [],
            "files_created": [],
            "files_deleted": [],
            "files_modified": ["moved_file_src"],
            "files_moved": [("moved_file_src", "moved_file_dest_own")],
        }
        theirChanges = {
            "dirs_created": [],
            "dirs_deleted": [],
            "dirs_modified": [],
            "dirs_moved": [],
            "files_created": [],
            "files_deleted": [],
            "files_modified": ["moved_file_src"],
            "files_moved": [("moved_file_src", "moved_file_dest_their")],
        }
        synchroniser = Synchroniser(ownChanges, theirChanges)
        ownActions, theirActions = synchroniser.getActions()
        expectedOwnActions = [("create", "moved_file_dest_their")]
        expectedTheirActions = [("create", "moved_file_dest_own")]
        self.assertCountEqual(ownActions, expectedOwnActions)
        self.assertCountEqual(theirActions, expectedTheirActions)

