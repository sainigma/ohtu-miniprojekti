import json

class DatabaseController:
  def __init__(self, dbpath="./src/tests/dummy.json"):
    self.db = {}
    with open(dbpath) as file:
      self.db = json.load(file)['db']

  def validate(self, obj):
    if True:
      return True
    return False

  def insert(self, obj):
    if not self.validate(obj):
      return False
    self.db.append(obj)
    return True

  def get(self, id=None, params=None):
    print(id)
    if id == None:
      return self.db
    else:
      for entry in self.db:
        if entry["id"] == id:
          return entry
    return None