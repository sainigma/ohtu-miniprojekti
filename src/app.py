from ui.console_io import console_io as default_console_io
from entities.bookmark import Bookmark
from repositories.bookmarks_repository import BookmarksRepository


class App:
    def __init__(self, ui=default_console_io):
        self.ui = ui

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
            self.ui.write("Show-command is not yet implemented")
        elif input == "edit":
            self.ui.write("Edit-command is not yet implemented")
        else:
            self.usage()

    def welcome(self):
        self.ui.write("Welcome to Bookmarker!")

    def quit(self):
        self.ui.write("See you again!")

    def add(self):
        title = self.ui.read("Title: ")
        bookmark = Bookmark(title)
        BookmarksRepository().insert(bookmark.get_bookmark())

    def show(self):
        self.ui.write("Show-command is not yet implemented")

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
