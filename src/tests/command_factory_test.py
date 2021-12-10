import unittest
from unittest.mock import Mock
from commands.commands import Add, Delete, Edit, Help, Search, Select, Show, Unknown
from commands.commands_import_export import ImportJson, Export
from ui.stub_io import StubIO
from commands.command_factory import CommandFactory

class TestCommands(unittest.TestCase):
    def setUp(self):
        io = StubIO()
        service = Mock()
        self.command_factory = CommandFactory(io, service)
    
    def test_return_correct_command_object(self):
        help = self.command_factory.get_command("h")
        add = self.command_factory.get_command("add")
        show = self.command_factory.get_command("show")
        edit = self.command_factory.get_command("edit")
        search = self.command_factory.get_command("search")
        select = self.command_factory.get_command("select")
        delete = self.command_factory.get_command("delete")
        import_command = self.command_factory.get_command("import")
        export_command = self.command_factory.get_command("export")

        self.assertIsInstance(help, Help)
        self.assertIsInstance(add, Add)
        self.assertIsInstance(show, Show)
        self.assertIsInstance(edit, Edit)
        self.assertIsInstance(search, Search)
        self.assertIsInstance(select, Select)
        self.assertIsInstance(delete, Delete)
        self.assertIsInstance(import_command, ImportJson)
        self.assertIsInstance(export_command, Export)
    
    def test_return_unknown_object_when_unknown_command_was_given(self):
        unknown = self.command_factory.get_command("test")

        self.assertIsInstance(unknown, Unknown)