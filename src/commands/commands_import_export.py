import json
import os
from datetime import datetime
from commands.commands import Command, InvalidInputException

class Export(Command):
    def _run_command(self, argv):
        bookmarks = self.service.get_all()
        if bookmarks:
            data = self.convert_to_json(bookmarks)
            self.write_to_file(data, argv)

    def convert_to_json(self, bookmarks):
        data = {}
        data["bookmarks"] = []
        for bookmark in bookmarks:
            data["bookmarks"].append({
                "title": bookmark.title,
                "url": bookmark.url
            })
        return data
    
    def write_to_file(self, data, argv):
        if len(argv) == 1:
            path = self.check_path(str(argv[0]))
            with open(path, "w") as outfile:
                json.dump(data, outfile, sort_keys=True, indent=4)
                self.io.write("Exported successfully!")
        else:
            with open("export/" + str(datetime.now()) + ".json", "w") as outfile:
                json.dump(data, outfile, sort_keys=True, indent=4)
                self.io.write("Exported successfully!")
    
    def check_path(self, path):
        if path.find("export/") != 0:
            path = "export/" + path
        if os.path.splitext(path)[1] != ".json":
            path += ".json"
        return path

class ImportJson(Command):

    def _run_command(self, argv):
        if len(argv) == 0:
            raise InvalidInputException("Import argument missing")
        try:
            with open(argv[0], "r") as file:
                data = json.load(file)
        except:
            raise InvalidInputException("File not found")

        if not self.validate_json(data):
            raise InvalidInputException("Invalid json")

        self.add_bookmarks_to_repository(data)
        self.io.write("Bookmarks imported successfully!")

    def add_bookmarks_to_repository(self, data):
        added = []
        
        for entry_bookmark in data["db"]:
            bookmark = self.service.create(entry_bookmark["url"], entry_bookmark["title"])
            if bookmark is not None:
                added.append(bookmark)
                self.io.write("Added " + bookmark.short_str())
            else:
                self.io.write("Invalid bookmark: " + entry_bookmark["title"])
            
        return added
    
    def validate_json(self, data) -> bool:
        if "db" not in data:
            return False
        for e in data["db"]:
            if "url" not in e or "title" not in e:
                return False
        return True