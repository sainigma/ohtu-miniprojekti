import json
import random


class BookmarksRepository:
    def __init__(self, dbpath="./src/tests/dummy.json"):
        self.db = []
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

    # Palauttaa oletuksena kaiken, yksittäisen entryn jos id on asetettu haussa
    # ja valikoiman jos params on asetettu. Palauttaa listan dict-objekteja
    # start ja bookmarks määrittää mistä kohdasta listaa entryjä haetaan ja kuinka monta
    def get(self, id=None, start=0, bookmarks=10):
        print(id)
        if id is None:
            return self.db[start: start + bookmarks]

        for bookmark in self.db:
            if bookmark["id"] == id:
                return bookmark

        return None

    def remove(self, bookmark_id):
        bookmark = self.get(bookmark_id)
        if bookmark is None:
            return False
        self.db.remove(bookmark)
        return True
