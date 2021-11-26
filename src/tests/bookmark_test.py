import unittest
from entities.bookmark import Bookmark

class TestBookmark(unittest.TestCase):
    def setUp(self):
        self.bookmark = Bookmark("2222", "Kirja")

    def test_constructor_creates_bookmark(self):
        bookmark = Bookmark("123456", "Kirja")

        self.assertEqual(bookmark.id, "123456")
        self.assertEqual(bookmark.title, "Kirja")
    
    def test_add_tag_functions_properly(self):
        self.bookmark.add_tag("tira")

        self.assertIn("tira", self.bookmark.tags)
    
    def test_no_duplicate_tags_allowed(self):
        self.bookmark.add_tag("Tira")
        self.bookmark.add_tag("tira")
        self.assertSetEqual(self.bookmark.tags, {"tira"})

    def test_get_bookmark_returns_correct_dict(self):
        self.bookmark.add_tag("tira")
        self.bookmark.add_tag("tärkeä")

        self.assertDictEqual(self.bookmark.get_bookmark(),
        {"id": "2222",
        "name": "Kirja",
        "tags": {"tira", "tärkeä"}})
    
    def test_find_tag_returns_true_if_found(self):
        self.bookmark.add_tag("tira")
        self.bookmark.add_tag("tärkeä")
        self.assertTrue(self.bookmark.find_tag("tira"))
        self.assertTrue(self.bookmark.find_tag("tärkeä"))
        self.assertFalse(self.bookmark.find_tag("ei löydy"))