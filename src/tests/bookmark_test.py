from typing import Any
import unittest
from entities.bookmark import Bookmark


class TestBookmark(unittest.TestCase):
    def setUp(self):
        self.bookmark = Bookmark("Google", "https://www.google.com")

    def test_constructor_creates_bookmark(self):
        bookmark = Bookmark("Google", "https://www.google.com")

        self.assertEqual(bookmark.url, "https://www.google.com")
        self.assertEqual(bookmark.title, "Google")
    
    def test_add_tag_functions_properly(self):
        self.bookmark.add_tag("kurssi", "tira")
        tag = self.bookmark.as_dict()['tags'][0]
        self.assertTrue(tag['type'] == 'kurssi')
        self.assertTrue(tag['content'] == 'tira')

    def test_no_duplicate_tags_allowed(self):
        self.bookmark.add_tag("Kurssi", "Tira")
        self.bookmark.add_tag("Kurssi", "TiRa")
        tags = self.bookmark.as_dict()['tags']
        self.assertTrue(len(tags) == 1)
    
    def test_get_bookmark_returns_correct_dict(self):
        self.bookmark.add_tag("kurssi", "tira")
        self.bookmark.add_tag("prioriteetti", "tärkeä")

        bookmark_dict = self.bookmark.as_dict()
        target_dict = {
            'title':'Google',
            'url':'https://www.google.com',
            'tags':[
                {
                    'type':'kurssi',
                    'content':'tira'
                },{
                    'type':'prioriteetti',
                    'content':'tärkeä'
                }
            ]
        }
        self.assertDictEqual(bookmark_dict, target_dict)

    def test_find_tag_by_type_returns_true_if_found(self):
        self.bookmark.add_tag("Kurssi", "tira")
        self.bookmark.add_tag("prioriteetti", "tärkeä")
        self.assertTrue(self.bookmark.find_tag_by_type("kUrssI"))
        self.assertTrue(self.bookmark.find_tag_by_type("priorITEetti"))
        self.assertFalse(self.bookmark.find_tag_by_type("ei löydy"))