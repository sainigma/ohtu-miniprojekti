import unittest
from services.bookmarks_service_json import BookmarksServiceJSON


class BookmarksServiceJSONTest(unittest.TestCase):
    def setUp(self):
        self.mockEntry = {
            "title": "Mockentry",
            "tags": [
                {
                    "type": "Kirjoittaja",
                    "content": "Asd Dasd"
                },
                {
                    "type": "tyyppi",
                    "content": "Testidata"
                },
            ]
        }
        self.db = BookmarksServiceJSON("./src/tests/dummy.json")

    def test_database_initializes(self):
        dbLength = len(self.db.get_all())
        self.assertTrue(dbLength > 0)

    def test_entries_can_be_added(self):
        dbLength0 = len(self.db.get_all())
        id0 = self.db.insert(self.mockEntry)
        dbLength1 = len(self.db.get_all())

        obj = self.db.get_one(id=id0)
        if obj != None:
            id = self.mockEntry["id"]
            title = self.mockEntry["title"]
            self.assertTrue((dbLength1 > dbLength0)
                            and obj["id"] == id and obj["title"] == title)
        else:
            self.assertTrue(False)

    def test_entry_validation_works(self):
        dbLength0 = len(self.db.get_all())
        obj = {"tilte": "asd", "tasg": []}
        id = self.db.insert(obj)
        dbLength1 = len(self.db.get_all())
        self.assertTrue(id == -1 and dbLength0 == dbLength1)

    def test_entries_can_be_removed(self):
        dbLength0 = len(self.db.get_all())
        self.db.remove(1)
        dbLength1 = len(self.db.get_all())

        obj = self.db.get_one(id=1)
        self.assertTrue(dbLength0 > dbLength1 and obj == None)

    def test_remove_nonexisting_entry(self):
        dbLength0 = len(self.db.get_all())
        self.db.remove(324893247)
        dbLength1 = len(self.db.get_all())

        self.assertTrue(dbLength0 == dbLength1)
