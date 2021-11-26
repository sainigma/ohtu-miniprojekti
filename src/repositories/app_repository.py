import sqlite3
import os.path

class AppRepository:
    def __init__(self, databasePath='./src/app.db', reinitialize=False):
        self.dbPath = databasePath
        if not os.path.exists(databasePath):
            self.initialize('./src/create.sql')
        elif reinitialize:
            os.remove(databasePath)
            self.initialize('./src/create.sql')

    def initialize(self, path):
        with open(path) as createFile:
            creationScript = createFile.read()
            self.executeScript(creationScript)

    def executeScript(self, query):
        with sqlite3.connect(self.dbPath) as conn:
            cursor = conn.cursor()
            cursor.executescript(query)
            conn.commit()

    def execute(self, query):
        with sqlite3.connect(self.dbPath) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            conn.commit()
            return rows
