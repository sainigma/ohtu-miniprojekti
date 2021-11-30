import unittest
import json
from repositories.app_repository import AppRepository
from services.bookmarks_service_sql import BookmarksServiceSQL
from repositories.bookmarks_repository import BookmarksRepository

class BookmarksServiceSQLTest(unittest.TestCase):
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
        appRepository = AppRepository('./src/tests/dummy.db', True)
        self.db = BookmarksServiceSQL(appRepository)

        with open('./src/tests/dummy.json') as jsonFile:
            dummies = json.load(jsonFile)['db']
        for dummy in dummies:
            self.db.insert(dummy)


    def test_database_initializes(self):
        dbLength = len(self.db.get_all())
        self.assertTrue(dbLength == 6)

    def test_entries_can_be_added(self):
        dbLength0 = len(self.db.get_all())
        id0 = self.db.insert(self.mockEntry)
        dbLength1 = len(self.db.get_all())
        self.assertTrue(dbLength1 > dbLength0)
        
        obj = self.db.get_one(id=id0)
        if obj != None:
            title = self.mockEntry["title"]
            self.assertTrue((dbLength1 > dbLength0) and obj["id"] == id0 and obj["title"] == title)
        else:
            self.assertTrue(False)

    def test_entry_validation_works(self):
        dbLength0 = len(self.db.get_all())
        obj = {"tilte":"asd","tasg":[]}
        id = self.db.insert(obj)
        dbLength1 = len(self.db.get_all())
        self.assertTrue(id == -1 and dbLength0 == dbLength1)

    def test_fetch_nonexisting_bookmark(self):
        bookmark = self.db.get_one(id=3247987324)
        self.assertTrue(bookmark is None)

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

    def test_finding_by_title(self):
        bookmarks = self.db.find_by_title("Jim Benson*")
        self.assertTrue(bookmarks[0]['title'] == "Jim Benson on Personal Kanban, Lean Coffee and collaboration")
    
    def test_finding_by_title_broad_results(self):
        bookmarks = self.db.find_by_title('*entry')
        self.assertTrue(len(bookmarks) == 2)

    # poista kun bookmarksrepository tarpeeton
    def test_class_complies_with_previous_version(self):
        old_methods = dir(BookmarksRepository)
        current_methods = dir(BookmarksServiceSQL)
        for method in old_methods:
            if method not in current_methods:
                print(method)
                self.assertTrue(False)
        self.assertTrue(True)