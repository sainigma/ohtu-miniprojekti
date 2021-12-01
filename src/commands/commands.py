
from entities.bookmark import Bookmark
from services.url_validator import get_url

class Help:
    def __init__(self, io, service):
        self.io = io
        self.service = service
    
    def execute(self):
        Unknown.execute(self)
        self.io.write("""
            To delete a bookmark, first select 'edit' and then 'delete'
            (Not implemented yet)
        """)

class Add:
    def __init__(self, io, service):
        self.io = io
        self.service = service
    
    def execute(self):
        url = self.io.read("Url: ")
        self.add_bookmark(url)
    
    def add_bookmark(self, url):
        if not get_url(url):
            self.io.write("Error: URL not found")
            return
        bookmark = Bookmark(url)
        self.service.insert(bookmark.as_dict())
        self.io.write(f'Bookmark "{url}" created!')

class Show:
    def __init__(self, io, service):
        self.io = io
        self.service = service
    
    def execute(self):
        bookmarks = self.service.get_all()
        if not bookmarks:
            self.io.write("No bookmarks")
        else:
            for bookmark in bookmarks:
                self.io.write(bookmark["title"])

class Edit:
    def __init__(self, io, service):
        self.io = io
        self.service = service
    
    def execute(self):
        self.io.write("Edit-command is not yet implemented")

class Delete:
    def __init__(self, io, service):
        self.io = io
        self.service = service
    
    def execute(self):
        self.io.write("Delete-command incomplete")

class Search:
    def __init__(self, io, service):
        self.io = io
        self.service = service
    
    def execute(self):
        term = self.io.read("Term: ")
        self.search_by_title(term)
    
    def search_by_title(self, title):
        self.io.write(
            "\n".join(
                [bookmark["title"] for bookmark in self.service.find_by_title(title)]
                )
            )

class Unknown:
    def __init__(self, io):
        self.io = io
    
    def execute(self):
        self.io.write("""
            Acceptable commands:
            'q' - quit,
            'h' - help,
            'add' - add a new bookmark,
            'show' - show given amount of bookmarks,
            'edit' - edit a bookmark
        """)