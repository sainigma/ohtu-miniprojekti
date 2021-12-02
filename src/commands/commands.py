

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
        print("creating " + url)
        bookmark = self.service.create(url)
        self.io.write(f'Bookmark "{bookmark.short_str()}" created!')

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
                self.io.write(bookmark.short_str())

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
        self.io.write("Delete-command is not yet implemented")

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
                [bookmark.short_str() for bookmark in self.service.get_by_title(title)]
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