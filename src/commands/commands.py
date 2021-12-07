import json
from datetime import datetime
import os
from services.url_validator import parse_results
from ui.app_state import app_state

class InvalidInputException(Exception):
    pass

class Command:
    def __init__(self, io, service=None):
        self.io = io
        self.service = service
    
class Help(Command):
    def execute(self, argv):
        Unknown.execute(self, argv)
        self.io.write("""
            To delete a bookmark, first choose 'select', type the ID of the bookmark and then 'delete'
        """)

class Add(Command):    
    def execute(self, argv):
        url = self.io.read("Url: ")

        if url == 'b':
            return

        url_title = self.service.get_title_by_url(url)
        if url_title is None:
            raise InvalidInputException("Invalid url")
        
        title = self._set_title(url_title)
        bookmark = self.service.create(url, title)
        self.io.write(f'Bookmark "{bookmark.short_str()}" created!')
    
    def _set_title(self, url_title):
        self.io.write(f'Title will be "{url_title}". Do you want to keep the title?')
        new = self.io.read("y/n: ")
        if new.strip() == "n":
            return self._create_new_title()
        if new.strip() == "y":
            return url_title
        raise InvalidInputException("Invalid command")
    
    def _create_new_title(self):
        return self.io.read("Title: ")

class Show(Command):
    def execute(self, argv):
        if len(argv) < 1:
            bookmarks = self.service.get_all()
        elif len(argv) == 1:
            bookmarks = self.service.get_all(0,int(argv[0]))
        else:
            bookmarks = self.service.get_all(int(argv[0]), int(argv[1]))
        
        if not bookmarks:
            self.io.write("No bookmarks")
            return
        for bookmark in bookmarks:
            self.io.write(bookmark.short_str())
        if len(bookmarks) < self.service.bookmarks_amount():
            print("showing results 0 to x, n for more")

class Edit(Command):
    def execute(self, argv):
        raise InvalidInputException("Edit-command is not yet implemented")

class Delete(Command):
    def execute(self, argv):
        if app_state.selected is None and not argv:
            raise InvalidInputException("Please select a bookmark to delete it")

        deletations = argv if app_state.selected is None else [app_state.selected.id]
        for id in deletations:
            if self.service.delete(id):
                self.io.write(f"Bookmark {id} deleted successfully")
            else:
                raise InvalidInputException(f"Bookmark {id} didn't exist!")
        app_state.selected = None
            

class Select(Command):
    def execute(self, argv):
        self.io.write("""
            To delete a bookmark: type in ID of the bookmark, press enter and then type 'delete'
            To edit a bookmark: type in ID of the bookmark, press enter and then type 'edit'
            To go back: type in 'b'
        """)

        Show.execute(self, argv=[])

        id = self.io.read("Id: ")
        if id == 'b':
            return
        bookmark = self.service.get_one(id)
        if bookmark is None:
            raise InvalidInputException("Invalid id")
        app_state.selected = bookmark
        self.io.write(bookmark.short_str() + " selected")

class Search(Command):
    def execute(self, argv):
        if argv and argv[0] == 'url':
            if len(argv) == 1:
                term = self.io.read("Url:")
            else:
                term = argv[1]
            search_method = self.search_by_url
        else:
            if argv:
                term = argv[0]
            else:
                term = self.io.read("Term: ")
            search_method = self.search_by_title
        if term == 'b':
            return
        search_method(term)

    def search_by_url(self, url):
        bookmarks = self.service.get_by_url(url)
        self.parse_results(bookmarks, "Could not find any bookmarks with that url")

    def search_by_title(self, title):
        bookmarks = self.service.get_by_title(title)
        self.parse_results(bookmarks, "Could not find any bookmarks with that title")

    def parse_results(self, bookmarks, msg):
        if not bookmarks:
            raise InvalidInputException("Could not find any bookmarks with that title")
        self.io.write(
            "\n".join(
                [bookmark.short_str() for bookmark in bookmarks]
                )
            )

class Export(Command):
    def execute(self, argv):
        if len(argv) > 1:
            return
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
    
class Unknown(Command):
    def execute(self, argv):
        self.io.write("""
            Acceptable commands:
            'q' - quit,
            'h' - help,
            'b' - back,
            'add' - add a new bookmark,
            'show' - show given amount of bookmarks,
            'search' - search bookmarks by a term,
            'select' - select a bookmark
            'edit' - edit a selected bookmark
            'delete' - delete a selected bookmark
        """)