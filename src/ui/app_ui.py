from ui.console_io import console_io as default_console_io
from services.bookmarks_service import bookmarks_service as default_bookmarks_service
from commands.command_factory import CommandFactory


class AppUi:
    def __init__(self, ui=default_console_io, service=default_bookmarks_service):
        self.ui = ui
        self.service = service
        self.command_factory = CommandFactory(self.ui, self.service)
        self.command = None

    def read_input(self):
        return self.ui.read("Give command: ")

    def parse_command(self, input):
        input = input.strip()
        self.command = self.command_factory.get_command(input)
    
    def execute_command(self):
        self.command.execute()

    def welcome(self):
        self.ui.write("\nWelcome to Bookmarker!\nType 'h' for help\n")

app_ui = AppUi()