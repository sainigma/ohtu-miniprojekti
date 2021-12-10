import unittest
from commands.commands import Add, Show, Edit, Search, Unknown, Delete
from commands.commands_import_export import ImportJson, Export
from commands.commands import InvalidInputException
from unittest.mock import ANY, Mock
from entities.bookmark import Bookmark
from ui.app_state import app_state

class TestCommands(unittest.TestCase):
    def setUp(self):
        self.io = Mock()
        self.service = Mock()
        self.bookmark = Bookmark(1, "Test", "test.com")
        self.delete = Delete(self.io, self.service)
    
    def test_delete_without_args_and_nothing_selected(self):
        app_state.selected = None

        try:
            self.delete._run_command([])
        except InvalidInputException:
            return
        self.fail()

    def test_delete_by_id(self):
        self.service.delete.return_value = True
        self.delete._run_command([0])
        self.service.delete.assert_called_with(0)
        self.io.write.assert_called_with("Bookmark 0 deleted successfully")
        self.assertIsNone(app_state.selected)

    def test_delete_not_found(self):
        self.service.delete.return_value = False
        try:
            self.delete._run_command([0])
        except InvalidInputException:
            self.service.delete.assert_called_with(0)
            return
        self.fail()