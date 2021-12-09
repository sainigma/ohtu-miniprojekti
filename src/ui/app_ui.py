from ui.console_formatter import ConsoleFormatter
from services.bookmarks_service import bookmarks_service as default_bookmarks_service
from commands.commands import CommandStoppedException, InvalidInputException
from commands.command_factory import CommandFactory


class AppUi:
    def __init__(self, io, service=default_bookmarks_service):
        self.io = io
        self.service = service
        self.command_factory = CommandFactory(self.io, self.service)
        self.command = None
        self.argv = []
        self.results = []
        self.selected = None

    def read_input(self):
        return self.io.read("Give command: ")

    def parse_command(self, input):
        input = input.strip().lower()
        arguments = input.split(' ')
        self.argv = arguments[1:]
        self.command = self.command_factory.get_command(arguments[0])
    
    def execute_command(self):
        try:
            self.command.execute(self.argv)
        except InvalidInputException as error:
            self.io.write(str(error))
        except CommandStoppedException:
            return

    def welcome(self):
        self.io.clear()
        self.io.write("Welcome to Bookmarker!\nType 'h' for help\n")

app_ui = AppUi(io=ConsoleFormatter())
