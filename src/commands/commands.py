import os
import sys
import json
# from jsonschema import validate, ValidationError
from datetime import datetime
from ui.app_state import app_state

class InvalidInputException(Exception):
    pass

class CommandStoppedException(Exception):
    pass

class Command:
    def __init__(self, io, service=None):
        self.io = io
        self.service = service
    
    def execute(self, argv):
        self._run_command(argv)
    
    def _read_new_arg(self, prompt) -> str:
        arg = self.io.read(prompt, self.io.get_cursor())
        if arg.strip() == 'b':
            raise CommandStoppedException()
        return arg
    
    def _run_command(self, argv):
        pass

    
class Help(Command):
    def _run_command(self, argv):
        Unknown._run_command(self, argv)
        self.io.write("""
            To delete a bookmark, first choose 'select', type the ID of the bookmark and then 'delete'
        """)

class Add(Command):    
    def _run_command(self, argv):
        url = self._read_new_arg("Url: ")

        url_title = self.service.get_title_by_url(url)
        if url_title is None:
            raise InvalidInputException("Invalid url")
        
        title = self._set_title(url_title)
        bookmark = self.service.create(url, title)
        self.io.write(f'\nBookmark "{bookmark.short_str()}" created!')
    
    def _set_title(self, url_title):
        user_input = ''
        while user_input not in ['y', 'n']:
            user_input = self.io.read_chr(f'Do you want to keep the title "{url_title}"? [y/n]')
        if user_input == 'n':
            return self._create_new_title()
        return url_title
    
    def _create_new_title(self):
        return self._read_new_arg("Title: ")

class Show(Command):

    def _run_command(self, argv):
        if len(argv) == 0:
            self._show_all()
        elif len(argv) == 1:
            count = argv[0]
            self._show_range(0, count)
        elif len(argv) >= 2:
            start = argv[0]
            count = argv[1]
            self._show_range(start, count)
        else:
            raise InvalidInputException("Wrong number of arguments.")
    
    def _show_all(self):
        bookmarks = self.service.get_all()
        if not bookmarks:
            self.io.write("No bookmarks")
        else:
            self.io.print_bookmarks_range(bookmarks)

    def _show_range(self, start, count):
        bookmarks = self.service.get_all(start, count)
        if not bookmarks:
            self.io.write("No bookmarks")
            return
        should_show_next_page = self.io.print_bookmarks_range(bookmarks)
        if should_show_next_page:
            self._show_range(start + count, count)


class Edit(Command):
    def _run_command(self, argv):
        raise InvalidInputException("Edit-command is not yet implemented")

class Delete(Command):
    def _run_command(self, argv):
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
    def _run_command(self, argv):
        self.io.write("""
            To delete a bookmark: type in ID of the bookmark, press enter and then type 'delete'
            To edit a bookmark: type in ID of the bookmark, press enter and then type 'edit'
            To go back: type in 'b'
        """)

        show_command = Show(self.io, self.service)

        show_command._run_command([])

        id = self._read_new_arg("Id: ")

        bookmark = self.service.get_one(id)
        if bookmark is None:
            raise InvalidInputException("Invalid id")
        app_state.selected = bookmark
        self.io.write(bookmark.short_str() + " selected")

class Search(Command):
    def _run_command(self, argv):
        if argv and argv[0] == 'url':
            if len(argv) == 1:
                term = self._read_new_arg("Url:")
            else:
                term = argv[1]
            search_method = self.search_by_url
        else:
            if argv:
                term = argv[0]
            else:
                term = self._read_new_arg("Term: ")
            search_method = self.search_by_title

        search_method(term)

    def search_by_url(self, url):
        bookmarks = self.service.get_by_url(url)
        self.parse_results(bookmarks, "Could not find any bookmarks with that url")

    def search_by_title(self, title):
        bookmarks = self.service.get_by_title(title)
        self.parse_results(bookmarks, "Could not find any bookmarks with that title")

    def parse_results(self, bookmarks, msg):
        if not bookmarks:
            raise InvalidInputException(msg)
        self.io.print_bookmarks(bookmarks, "Search results")
        self.io.write(f"Found {len(bookmarks)} results", 1)

class Quit(Command):
    def _run_command(self, argv):
        self.io.exit()
        sys.exit(0)

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
    pass
    def _run_command(self, argv):
        try:
            with open(argv, "r") as file:
                data = json.load(file.read())
        except:
            raise InvalidInputException("File not found")

        if not self.validate_json(data):
            raise InvalidInputException("Invalid file format")

        self.add_bookmarks_to_repository(data)
        self.io.write("Bookmarks imported successfully!")

    def add_bookmarks_to_repository(self, data):
        added = []

        for entry in data:
            bookmark = self.service.create(entry["url"], entry["title"])
            added.append(bookmark)
        return added
    
    def validate_json(self, data):
        # valid_schema = {
        #     "title": "string",
        #     "url": "string"
        # }
        # try:
        #     validate(data, valid_schema)
        # except ValidationError as error:
        #     return False
        return True

    
    
class Unknown(Command):
    def _run_command(self, argv):
        self.io.clear()
        self.io.write(f'command unrecognized.')
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