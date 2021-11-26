import sys
from ui.console_io import console_io as default_console_io
from entities.bookmark import Bookmark
from repositories.bookmarks_repository import bookmark_repository as default_bookmark_repository


class App:
    def __init__(self, ui=default_console_io, repository=default_bookmark_repository):
        self.ui = ui
        self.repository = repository

    def run(self):
        self.welcome()
        while True:

            command = self.read_input()
            self.parse_input(command)

    def read_input(self):
        return self.ui.read("Give command: ")

    def parse_input(self, input):
        if input == "q":
            self.quit()
        if input == "add":
            self.add()
        elif input == "show":
            self.show()
        elif input == "edit":
            self.ui.write("Edit-command is not yet implemented")
        else:
            self.usage()

    def welcome(self):
        self.ui.write("Welcome to Bookmarker!")

    def quit(self):
        self.ui.write("See you again!")
        sys.exit()

    def add(self):
        title = self.ui.read("Title: ")
        self.add_bookmark(title)
    
    def add_bookmark(self, title):
        bookmark = Bookmark(title)
        self.repository.insert(bookmark.get_bookmark())
        self.ui.write(f'Bookmark "{title}" created!')

    def show(self):
        bookmarks_amount = self.repository.bookmarks_amount() + 1
        bookmarks = self.repository.get(None, 0, bookmarks_amount)
        for bookmark in bookmarks:
            self.ui.write(bookmark["title"])

    def edit(self):
        self.ui.write("Edit-command is not yet implemented")

    def usage(self):
        self.ui.write("""
            Acceptable commands:
            'q' - quit,
            'add' - add a new bookmark,
            'show' - show given amount of bookmarks,
            'edit' - edit a bookmark
        """)


app = App()
