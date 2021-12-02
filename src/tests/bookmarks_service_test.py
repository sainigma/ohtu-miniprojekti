import unittest
import json
from services.bookmarks_service import BookmarksService
from db_connection import DBConnection
from entities.bookmark import Bookmark
# poista kun bookmarks_service on integroitu
from services.bookmarks_service_json import BookmarksServiceJSON

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
        db_connection = DBConnection('./src/tests/dummy.db', True)
        self.db = BookmarksService(db_connection)

        with open('./src/tests/dummy.json') as jsonFile:
            dummies = json.load(jsonFile)['db']
        for dummy in dummies:
            self.db.create(dummy["url"])

    def test_database_initializes(self):
        dbLength = len(self.db.get_all())
        self.assertTrue(dbLength == 6)

    def test_entries_can_be_added(self):
        dbLength0 = len(self.db.get_all())
        id0 = self.db.create(self.mockEntry["url"]).id
        dbLength1 = len(self.db.get_all())
        self.assertGreater(dbLength1, dbLength0)
        
        bookmark = self.db.get_one(id=id0)
        url = self.mockEntry["url"]
        self.assertIsNotNone(bookmark)
        self.assertEqual(bookmark.id, id0)
        self.assertEqual(bookmark.url, url)

    def test_entry_validation_works(self):
        dbLength0 = len(self.db.get_all())
        try:
            self.db.create("tämä urli ei toimi")
        except:
            return
        self.fail("Create-method did not raise an exception")


    def test_fetch_nonexisting_bookmark(self):
        bookmark = self.db.get_one(id=3247987324)
        self.assertTrue(bookmark is None)

    def test_entries_can_be_removed(self):
        dbLength0 = len(self.db.get_all())
        self.db.delete(1)
        dbLength1 = len(self.db.get_all())

        obj = self.db.get_one(id=1)
        self.assertTrue(dbLength0 > dbLength1 and obj == None)

    def test_remove_nonexisting_entry(self):
        dbLength0 = len(self.db.get_all())
        self.db.delete(324893247)
        dbLength1 = len(self.db.get_all())

        self.assertTrue(dbLength0 == dbLength1)
