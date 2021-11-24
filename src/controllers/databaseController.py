import json,random

class DatabaseController:
  def __init__(self, dbpath="./src/tests/dummy.json"):
    self.db = []
    with open(dbpath) as file:
      self.db = json.load(file)['db']

  def validate(self, obj):
    if "title" in obj and "tags" in obj:
      return True
    return False

  # Vastaanottaa dict-objektin, jolla on tietueina title ja tags
  # Joko tähän tai bookmarkkiin typecast bookmark -> dict
  # Palauttaa onnistuneessa luonnissa bookmarkin id:n tietokannassa, muutoin -1
  def insert(self, obj):
    if not self.validate(obj):
      return -1

    # normaalisti tietokanta generoi id:n, tässä simulaatio
    id = random.randrange(21213,239479832)
    obj["id"] = id
    self.db.append(obj)
    return id

  # Palauttaa oletuksena kaiken, yksittäisen entryn jos id on asetettu haussa
  # ja valikoiman jos params on asetettu. Palauttaa listan dict-objekteja
  # start ja bookmarks määrittää mistä kohdasta listaa entryjä haetaan ja kuinka monta
  def get(self, id=None, params=None, start=0, bookmarks=10):
    print(id)
    if id == None:
      return self.db[start : start + bookmarks]
    else:
      for entry in self.db:
        if entry["id"] == id:
          return entry
    return None
  
  def remove(self, id):
    obj = self.get(id)
    if obj == None:
      return False
    self.db.remove(obj)
    return True