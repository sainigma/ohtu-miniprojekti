import unittest
from gateways.bookmarks_gateway import BookmarksGateway

class BookmarksGatewayTest(unittest.TestCase):
    def setUp(self):
        self.mockEntry = {
            "title":"Mockentry",
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
        self.db = BookmarksGateway("./src/tests/dummy.json")

    def test_database_initializes(self):
        dbLength = len(self.db.get())
        self.assertTrue(dbLength > 0)

    def test_entries_can_be_added(self):
        dbLength0 = len(self.db.get())
        id0 = self.db.insert(self.mockEntry)
        dbLength1 = len(self.db.get())

        obj = self.db.get(id=id0)
        if obj != None:
            id = self.mockEntry["id"]
            title = self.mockEntry["title"]
            self.assertTrue((dbLength1 > dbLength0) and obj["id"] == id and obj["title"] == title)
        else:
            self.assertTrue(False)

    def test_entry_validation_works(self):
        dbLength0 = len(self.db.get())
        obj = {"tilte":"asd","tasg":[]}
        id = self.db.insert(obj)
        dbLength1 = len(self.db.get())
        self.assertTrue(id == -1 and dbLength0 == dbLength1)

    def test_entries_can_be_removed(self):
        dbLength0 = len(self.db.get())
        self.db.remove(1)
        dbLength1 = len(self.db.get())

        obj = self.db.get(id=1)
        self.assertTrue(dbLength0 > dbLength1 and obj == None)

    def test_remove_nonexisting_entry(self):
        dbLength0 = len(self.db.get())
        self.db.remove(324893247)
        dbLength1 = len(self.db.get())

        self.assertTrue(dbLength0 == dbLength1)