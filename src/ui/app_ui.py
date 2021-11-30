import sys
from ui.console_io import console_io as default_console_io
from entities.bookmark import Bookmark
from repositories.bookmarks_repository import bookmark_repository as default_bookmark_repository
from commands.command_factory import CommandFactory


class AppUi:
    def __init__(self, ui=default_console_io, repository=default_bookmark_repository):
        self.ui = ui
        self.repository = repository
        self.command_factory = CommandFactory(self.ui, self.repository)

    def read_input(self):
        return self.ui.read("Give command: ")

    def parse_command(self, input):
        input = input.strip()
        self.command_factory.set_command(input).execute()

    def welcome(self):
        self.ui.write("Welcome to Bookmarker!")

app_ui = AppUi()