import unittest
from bookmark import Bookmark

class TestBookmark(unittest.TestCase):
    def setUp(self):
        pass

    def test_constructor_creates_object_correctly(self):
        bookmark = Bookmark("123456", "Kirja")

        self.assertEqual(bookmark.id, "123456")
        self.assertEqual(bookmark.title, "Kirja")