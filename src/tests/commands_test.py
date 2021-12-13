import unittest
from commands.commands import Add, Show, Edit, Search, Unknown, Delete
from commands.commands_import_export import ImportJson, Export
from commands.commands import InvalidInputException
from unittest.mock import ANY, Mock
from entities.bookmark import Bookmark

class TestCommands(unittest.TestCase):
    def setUp(self):
        self.io = Mock()
        self.service = Mock()
        self.bookmark = Bookmark(1, "Test", "test.com")
        
    def test_print_correct_message_when_bookmark_is_added_successfully(self):
        self.service.get_title_by_url.return_value = "test.com"
        self.io.read_chr.return_value = "y"
        self.service.create.return_value = self.bookmark
        add = Add(self.io, self.service)

        add._run_command([])

        self.io.write.assert_called_with('\nBookmark "1: Test, test.com" created!')

    def test_print_correct_message_when_there_are_not_any_bookmarks_to_show(self):
        self.service.get_all.return_value = []
        show = Show(self.io, self.service)

        show._run_command([])

        self.io.write.assert_called_with("No bookmarks")

        show._show_range(0,1)

        self.io.write.assert_called_with("No bookmarks")
    
    def test_print_titles_of_all_bookmarks(self):
        self.service.get_all.return_value = [self.bookmark]
        self.service.get_cursor.return_value = 0
        self.service.bookmarks_amount.return_value = 1
        show = Show(self.io, self.service)
        
        show._run_command([])

        self.io.print_bookmarks.assert_called_with([self.bookmark])
    
    def test_print_given_amount_of_titles(self):
        self.service.get_all.return_value = [self.bookmark, Bookmark(2, "Test2", "test2.com")]
        show = Show(self.io, self.service)

        show._run_command([2])

        self.io.print_bookmarks.assert_called_with(self.service.get_all.return_value)

    def test_print_given_range_of_titles(self):
        self.service.get_all.return_value = [Bookmark(2, "Test2", "test2.com"), Bookmark(3, "Test3", "test3.com")]
        self.io.print_bookmarks_range.return_value = None
        show = Show(self.io, self.service)

        show._run_command([1,2])

        self.io.print_bookmarks.assert_called_with(self.service.get_all.return_value)

    def test_print_marched_titles(self):
        self.io.read.return_value = "Test"
        self.service.get_by_title.return_value = [self.bookmark]
        search = Search(self.io, self.service)

        search._run_command([])

        self.io.write.assert_called_with("Found 1 results", 1)

    def test_print_accepted_commands_when_unknown_command_was_given(self):
        unknown = Unknown(self.io)

        unknown._run_command([])

        self.io.write.assert_called_with("""
            Acceptable commands:
            'q' - quit,
            'h' - help,
            'b' - back,
            'add' - add a new bookmark,
            'show' - show given amount of bookmarks,
            'search' - search bookmarks by a term,
            'select' - select a bookmark,
            'edit' - edit a selected bookmark,
            'delete' - delete a selected bookmark,
            'export' - export current bookmarks to a json file in the directory 'export'
        """)
    
    def test_import_valid_json_validate_true(self):
        data = {"db":[{"title": "Google", "url": "http://www.google.com"}]}
        command = ImportJson(self.io, self.service)

        self.assertTrue(command.validate_json(data))
    
    def test_import_invalid_json_validate_false(self):
        data = {"db":[{"kissa": "koira", "vauva": "lapsi"}]}
        command = ImportJson(self.io, self.service)

        self.assertFalse(command.validate_json(data))
    
    def test_add_bookmark_calls_bookmark_service_create_method_with_arguments(self):
        data = {"db":[{"title": "Google", "url": "http://www.google.com"}]}
        command = ImportJson(self.io, self.service)
        self.service.create.return_value = Bookmark(1, "Google", "http://www.google.com")
        
        command.add_bookmarks_to_repository(data)

        self.service.create.assert_called_once_with("http://www.google.com", "Google")

    def test_add_bookmark_text_when_bookmark_added(self):
        data = {"db":[{"title": "Google", "url": "http://www.google.com"}]}
        command = ImportJson(self.io, self.service)
        bookmark = Bookmark(1, "Google", "http://www.google.com")
        self.service.create.return_value = Bookmark(1, "Google", "http://www.google.com")

        command.add_bookmarks_to_repository(data)
        self.io.write.assert_called_with(f"Added " + bookmark.short_str())
    
    def test_add_bookmark_text_when_bookmark_not_added(self):
        data = {"db":[{"title": "Google", "url": "google.com"}]}
        command = ImportJson(self.io, self.service)
        self.service.create.return_value = None

        command.add_bookmarks_to_repository(data)
        self.io.write.assert_called_with("Invalid bookmark: Google")
    
    
