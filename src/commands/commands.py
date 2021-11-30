from entities.bookmark import Bookmark


class Add:
    def __init__(self, io, repository):
        self.io = io
        self.repository = repository
    
    def execute(self):
        title = self.io.read("Title: ")
        self.add_bookmark(title)
    
    def add_bookmark(self, title):
        bookmark = Bookmark(title)
        self.repository.insert(bookmark.as_dict())
        self.io.write(f'Bookmark "{title}" created!')

class Show:
    def __init__(self, io, repository):
        self.io = io
        self.repository = repository
    
    def execute(self):
        bookmarks = self.repository.get_all()
        if not bookmarks:
            self.io.write("No bookmarks")
        else:
            for bookmark in bookmarks:
                self.io.write(bookmark["title"])

class Edit:
    def __init__(self, io, repository):
        self.io = io
        self.repository = repository
    
    def execute(self):
        self.io.write("Edit-command is not yet implemented")

class Delete:
    def __init__(self, io, repository):
        self.io = io
        self.repository = repository
    
    def execute(self):
        self.io.write("Delete-command incomplete")

class Search:
    def __init__(self, io, repository):
        self.io = io
        self.repository = repository
    
    def execute(self):
        term = self.io.read("Term: ")
        self.search_by_title(term)
    
    def search_by_title(self, title):
        self.io.write(
            "\n".join(
                [bookmark["title"] for bookmark in self.repository.find_by_title(title)]
                )
            )

class Unknown:
    def __init__(self, io):
        self.io = io
    
    def execute(self):
        self.io.write("""
            Acceptable commands:
            'q' - quit,
            'add' - add a new bookmark,
            'show' - show given amount of bookmarks,
            'edit' - edit a bookmark
        """)