import unittest
from commands.commands import Search
from commands.commands import InvalidInputException
from unittest.mock import ANY, Mock
from entities.bookmark import Bookmark
from tests.commands_test import TestCommands

class TestSearchCommand(TestCommands):
    def test_search_command_with_url(self):
        argv = ['url', 'test.com']
        search = Search(self.io, self.service)

        search_results = [self.bookmark]

        self.service.get_by_url.return_value = search_results

        search._run_command(argv)

        self.service.get_by_url.assert_called_with('test.com')
        self.io.print_bookmarks.assert_called_with(search_results, ANY)

    def test_search_command_with_title(self):
        argv = ['Test']
        search = Search(self.io, self.service)

        search_results = [self.bookmark]

        self.service.get_by_title.return_value = search_results

        search._run_command(argv)

        self.service.get_by_title.assert_called_with('Test')
        self.io.print_bookmarks.assert_called_with(search_results, ANY)

    def test_search_command_with_no_results(self):
        argv = ['Test']
        search = Search(self.io, self.service)

        search_results = []

        self.service.get_by_title.return_value = search_results

        try:
            search._run_command(argv)
            self.service.get_by_title.assert_called_with('Test')
            self.fail('Did not raise exception')
        except InvalidInputException:
            pass