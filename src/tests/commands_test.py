import unittest
from commands.commands import Add, Show, Edit, Search, Unknown, Delete
from unittest.mock import Mock
from entities.bookmark import Bookmark

class TestCommands(unittest.TestCase):
    def setUp(self):
        self.io = Mock()
        self.service = Mock()
        self.bookmark = Bookmark(1, "Test", "test.com")
    
    def test_print_correct_message_when_bookmark_is_added_successfully(self):
        self.service.get_title_by_url.return_value = "test.com"
        self.io.read.return_value = "y"
        self.service.create.return_value = self.bookmark
        add = Add(self.io, self.service)

        add.execute([])

        self.io.write.assert_called_with('Bookmark "1 Test" created!')

    def test_print_correct_message_when_there_are_not_any_bookmarks_to_show(self):
        self.service.get_all.return_value = []
        show = Show(self.io, self.service)

        show.execute([])

        self.io.write.assert_called_with("No bookmarks")
    
    def test_print_titles_of_all_bookmarks(self):
        self.service.get_all.return_value = [self.bookmark]
        self.service.bookmarks_amount.return_value = 50
        show = Show(self.io, self.service)
        
        show.execute([])

        self.io.write.assert_called_with("1 Test")
    
    def test_print_marched_titles(self):
        self.io.read.return_value = "Test"
        self.service.get_by_title.return_value = [self.bookmark]
        search = Search(self.io, self.service)

        search.execute([])

        self.io.write.assert_called_with("1 Test")
    
    def test_print_accepted_commands_when_unknown_command_was_given(self):
        unknown = Unknown(self.io)

        unknown.execute([])

        self.io.write.assert_called_with("""
            Acceptable commands:
            'q' - quit,
            'h' - help,
            'b' - back,
            'add' - add a new bookmark,
            'show' - show given amount of bookmarks,
            'search' - search bookmarks by a term,
            'select' - select a bookmark
            'edit' - edit a selected bookmark
            'delete' - delete a selected bookmark
        """)
    
    # def test_print_correct_message_when_deleting_invalid_id(self):
    #     self.io.read.return_value = 2
    #     delete = Delete(self.io, self.service)

    #     delete.execute()

    #     self.io.write_assert_called_with("Invalid id")
    
    # def test_deleting_valid_id_removes_entry_from_db(self):
    #     self.io.read.return_value = 1
    #     delete = Delete(self.io, self.service)

    #     delete.execute()

    #     self.io.write_assert_called_with(f"Bookmark {self.bookmark.id} deleted successfully")
    
