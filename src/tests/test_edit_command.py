import unittest
from commands.commands import Edit
from commands.commands import InvalidInputException
from unittest.mock import ANY, Mock
from entities.bookmark import Bookmark
from tests.commands_test import TestCommands

class TestEditCommand(TestCommands):
    def test_edit_command_invalid_parameters(self):
        invalid_parameters = [
            ['f'],
            [],
            [32423489]
        ]
        self.service.get_one.return_value = None
        for argv in invalid_parameters:
            edit = Edit(self.io, self.service)
            try:
                edit._run_command(argv)
                self.fail("Did not raise exception")
            except InvalidInputException:
                pass