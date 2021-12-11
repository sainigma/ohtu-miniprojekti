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
    
    def edit_with_valid_id(self, read_chr_effects, read_effects, original_bookmark, comparison_bookmark, update_succeeds):
        argv = [1]
        self.service.get_one.return_value = original_bookmark

        self.io.read_chr.side_effect = read_chr_effects
        self.io.read.side_effect = read_effects

        self.service.update_bookmark.return_value = update_succeeds

        edit = Edit(self.io, self.service)
        edit._run_command(argv)

        try:
            new_bookmark = self.service.update_bookmark.call_args.args[0]
            self.assertEqual(new_bookmark.title, comparison_bookmark.title)
            self.assertEqual(new_bookmark.url, comparison_bookmark.url)
        except:
            self.assertTrue(comparison_bookmark == None)

    def test_edit_command_title_changes(self):
        read_chr_side_effects = ['n', 'y']
        read_side_effects = ['Uusi otsikko']
        original_bookmark = Bookmark(1, "Vanha otsikko", 'test.com')
        comparison_bookmark = Bookmark(1, 'Uusi otsikko', 'test.com')

        self.edit_with_valid_id(read_chr_side_effects, read_side_effects, original_bookmark, comparison_bookmark, True)
    
    def test_edit_command_url_changes(self):
        read_chr_side_effects = ['y', 'n']
        read_side_effects = ['https://www.google.com']
        original_bookmark = Bookmark(1, "Vanha otsikko", 'test.com')
        comparison_bookmark = Bookmark(1, 'Vanha otsikko', 'https://www.google.com')

        self.edit_with_valid_id(read_chr_side_effects, read_side_effects, original_bookmark, comparison_bookmark, True)

    def test_edit_command_everything_changes(self):
        read_chr_side_effects = ['n', 'n']
        read_side_effects = ['Uusi otsikko','https://www.google.com']
        original_bookmark = Bookmark(1, "Vanha otsikko", 'test.com')
        comparison_bookmark = Bookmark(1, 'Uusi otsikko', 'https://www.google.com')

        self.edit_with_valid_id(read_chr_side_effects, read_side_effects, original_bookmark, comparison_bookmark, True)

    def test_edit_command_nothing_changes(self):
        read_chr_side_effects = ['y', 'y']
        original_bookmark = Bookmark(1, "Vanha otsikko", 'test.com')

        self.edit_with_valid_id(read_chr_side_effects, [], original_bookmark, None, True)