import json
import random
from os import getenv


class BookmarksServiceJSON:
    def __init__(self, dbpath):
        self.db = []
        if dbpath:
            with open(dbpath) as file:
                self.db = json.load(file)['db']

    def validate(self, bookmark):
        if "title" in bookmark and "tags" in bookmark:
            return True
        return False

    # Vastaanottaa dict-objektin, jolla on tietueina title ja tags
    # Joko tähän tai bookmarkkiin typecast bookmark -> dict
    # Palauttaa onnistuneessa luonnissa bookmarkin id:n tietokannassa, muutoin -1
    def insert(self, bookmark):
        if not self.validate(bookmark):
            return -1

        # normaalisti tietokanta generoi id:n, tässä simulaatio
        new_id = random.randrange(21213, 239479832)
        bookmark["id"] = new_id
        self.db.append(bookmark)
        return new_id

    def get_one(self, id):
        for bookmark in self.db:
            if bookmark["id"] == id:
                return bookmark

        return None
    
    def get_all(self, start=0, n_bookmarks=None):
        if n_bookmarks is None:
            return self.db
        return self.db[start: start + n_bookmarks]

    def remove(self, bookmark_id):
        bookmark = self.get_one(bookmark_id)
        if bookmark is None:
            return False
        self.db.remove(bookmark)
        return True
    
    def bookmarks_amount(self):
        return len(self.db)
    
    def find_by_title(self, title: str):
        return [bookmark for bookmark in self.db if title in bookmark["title"]]
    
    def clear(self):
        self.db.clear()


def get_dummy_db_path():
    if getenv("USE_DUMMY_DB") == "True":
        return "./src/tests/dummy.json"
    return None

bookmarks_service = BookmarksServiceJSON(dbpath=get_dummy_db_path())
