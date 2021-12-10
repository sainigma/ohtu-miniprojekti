import unittest
from commands.commands import Add, Select, Show, Edit, Search, Unknown, Delete
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
        self.service.get_one.return_value = self.bookmark
        self.select = Select(self.io, self.service)
    
    def test_select(self):
        self.io.read.return_value = "0"
        self.io.get_cursor.return_value = 0
        self.select._run_command([])
        self.io.read.assert_called_with("Id: ", 0)
        self.assertEqual(self.bookmark, app_state.selected)
