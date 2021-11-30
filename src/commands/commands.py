class Add:
    def __init__(self, io):
        self.io = io
    
    def execute(self):
        title = self.ui.read("Title: ")
        self.add_bookmark(title)
    
    def add_bookmark(self, title):
        bookmark = Bookmark(title)
        self.repository.insert(bookmark.as_dict())
        self.ui.write(f'Bookmark "{title}" created!')

class Show:
    def __init__(self, io):
        self.io = io
    
    def execute(self):
        bookmarks = self.repository.get_all()
        if not bookmarks:
            self.ui.write("No bookmarks")
        else:
            for bookmark in bookmarks:
                self.ui.write(bookmark["title"])

class Edit:
    def __init__(self, io):
        self.io = io
    
    def execute(self):
        self.ui.write("Edit-command is not yet implemented")

class Search:
    def __init__(self, io):
        self.io = io
    
    def execute(self):
        term = self.ui.read("Term: ")
        self.search_by_title(term)
    
    def search_by_title(self, title):
        self.ui.write(
            "\n".join(
                [bookmark["title"] for bookmark in self.repository.find_by_title(title)]
                )
            )
