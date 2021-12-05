from ui.app_state import app_state

class Help:
    def __init__(self, io, service):
        self.io = io
        self.service = service
    
    def execute(self):
        Unknown.execute(self)
        self.io.write("""
            To delete a bookmark, first choose 'select', type the ID of the bookmark and then 'delete'
        """)

class Add:
    def __init__(self, io, service):
        self.io = io
        self.service = service
    
    def execute(self):
        url = self.io.read("Url: ")

        if url == 'b':
            return

        url_title = self.service.get_title_by_url(url)
        if url_title is None:
            self.io.write('Bookmark was not created')
            return
        
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
        raise Exception("Invalid command")
    
    def _create_new_title(self):
        return self.io.read("Title: ")

class Show:
    def __init__(self, io, service):
        self.io = io
        self.service = service
    
    def execute(self):
        bookmarks = self.service.get_all()
        if not bookmarks:
            self.io.write("No bookmarks")
            return
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
        self.app_state = app_state
    
    def execute(self):
        if self.app_state.selected is None:
            self.io.write("Please select a bookmark to delete it")
        else:    
            id = self.app_state.selected.id
            self.service.delete(id)
            self.io.write(f"Bookmark {id} deleted successfully")
            self.app_state.selected = None

class Select:
    def __init__(self, io, service) -> None:
        self.io = io
        self.service = service
        self.app_state = app_state
    
    def execute(self):

        self.io.write("""
            To delete a bookmark: type in ID of the bookmark, press enter and then type 'delete'
            To edit a bookmark: type in ID of the bookmark, press enter and then type 'edit'
            To go back: type in 'b'
        """)

        Show.execute(self)

        id = self.io.read("Id: ")
        if id == 'b':
            return
        bookmark = self.service.get_one(id)
        if bookmark is None:
            self.io.write("Invalid id")
            return
        self.app_state.selected = bookmark
        self.io.write(bookmark.short_str() + " selected")

class Search:
    def __init__(self, io, service):
        self.io = io
        self.service = service
    
    def execute(self):
        term = self.io.read("Term: ")
        if term == 'b':
            return
        self.search_by_title(term)
    
    def search_by_title(self, title):
        bookmarks = self.service.get_by_title(title)
        if not bookmarks:
            self.io.write("Could not find any bookmarks with that title")
            return
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
            'b' - back,
            'add' - add a new bookmark,
            'show' - show given amount of bookmarks,
            'search' - search bookmarks by a term,
            'select' - select a bookmark
            'edit' - edit a selected bookmark
            'delete' - delete a selected bookmark
        """)