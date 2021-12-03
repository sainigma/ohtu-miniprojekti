import unittest
import json
from services.bookmarks_service import BookmarksService
from entities.bookmark import Bookmark

class BookmarksServiceSQLTest(unittest.TestCase):
    def setUp(self):
        self.mockEntry = {
            "title":"Mockentry",
            "url":"https://google.com",
            "tags":[
                {
                    "type":"Kirjoittaja",
                    "content":"Asd Dasd"
                },
                {
                    "type":"tyyppi",
                    "content":"Testidata"
                },
            ]
        }
        self.bookmarks = BookmarksService()

        with open('./src/tests/dummy.json') as jsonFile:
            dummies = json.load(jsonFile)['db']
        for dummy in dummies:
            self.bookmarks.create(dummy["url"], dummy["title"])

    def test_initializes(self):
        self.assertEqual('./src/tests/dummy.db', self.bookmarks.repository.db.dbPath)

    def test_database_initializes(self):
        dbLength = self.bookmarks.bookmarks_amount()
        self.assertEqual(dbLength, 6)


    def test_entries_can_be_added(self):
        dbLength0 = len(self.bookmarks.get_all())
        id0 = self.bookmarks.create(self.mockEntry["url"], self.mockEntry["title"]).id
        dbLength1 = len(self.bookmarks.get_all())
        self.assertGreater(dbLength1, dbLength0)
        
        bookmark = self.bookmarks.get_one(id=id0)
        url = self.mockEntry["url"]
        self.assertIsNotNone(bookmark)
        self.assertEqual(bookmark.id, id0)
        self.assertEqual(bookmark.url, url)
    
    def test_entry_validation_works(self):
        self.assertIsNone(self.bookmarks.create("tämä urli ei toimi", "turha title"))

    def test_fetch_nonexisting_bookmark(self):
        bookmark = self.bookmarks.get_one(id=3247987324)
        self.assertTrue(bookmark is None)

    def test_entries_can_be_removed(self):
        dbLength0 = len(self.bookmarks.get_all())
        self.bookmarks.delete(1)
        dbLength1 = len(self.bookmarks.get_all())

        obj = self.bookmarks.get_one(id=1)
        self.assertTrue(dbLength0 > dbLength1 and obj == None)

    def test_remove_nonexisting_entry(self):
        dbLength0 = len(self.bookmarks.get_all())
        self.bookmarks.delete(324893247)
        dbLength1 = len(self.bookmarks.get_all())

        self.assertTrue(dbLength0 == dbLength1)