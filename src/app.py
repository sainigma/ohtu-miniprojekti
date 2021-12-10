from os import getenv
from repositories.bookmarks_repository import BookmarksRepository
from db_connection import DBConnection
from services.bookmarks_service import BookmarksService
from ui.app_ui import AppUi

from ui.console_formatter import ConsoleFormatter
from ui.stub_io import StubIO

class App:
    def __init__(self, ui):
        self.ui = ui

    def run(self):
        self.ui.welcome()
        while True:

            command = self.ui.read_input()
            self.ui.parse_command(command)
            self.ui.execute_command()


def testing() -> bool:
    return getenv("TESTING") == "True"

def init_test_app() -> App:
    io = StubIO()
    db_conn = DBConnection('./src/tests/dummy.db', True)
    repository = BookmarksRepository(database_connection=db_conn)
    service = BookmarksService(repository=repository)
    ui = AppUi(io, service)

    test_app = App(ui)

    return test_app

def init_app() -> App:
    if testing():
        return init_test_app()

    io = ConsoleFormatter()
    db_conn = DBConnection()
    repository = BookmarksRepository(database_connection=db_conn)
    service = BookmarksService(repository=repository)
    ui = AppUi(io, service)

    console_app = App(ui)

    return console_app

app = init_app()
