import unittest
from controllers.databaseController import DatabaseController

class DatabaseTest(unittest.TestCase):
  def setUp(self):
    self.mockEntry = {
      "title":"Mockentry",
      "id":7439,
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
    self.db = DatabaseController("./src/tests/dummy.json")

  def test_database_initializes(self):
    dbLength = len(self.db.get())
    self.assertTrue(dbLength > 0)

  def test_entries_can_be_added(self):
    dbLength0 = len(self.db.get())
    self.db.insert(self.mockEntry)
    dbLength1 = len(self.db.get())

    obj = self.db.get(id=self.mockEntry["id"])
    if obj != None:
      id = self.mockEntry["id"]
      title = self.mockEntry["title"]
      self.assertTrue((dbLength1 > dbLength0) and obj["id"] == id and obj["title"] == title)
    else:
      self.assertTrue(False)

  '''
  def test_entries_can_be_removed(self):
    dbLength0 = len(self.db.get())
    self.db.remove(1)
    dbLength1 = len(self.db.get())
  '''