import sys
from ui.app_ui import app_ui

class App:
    def __init__(self, ui=app_ui):
        self.ui = ui

    def run(self):
        self.ui.welcome()
        while True:

            command = self.ui.read_input()
            if command == "q":
                sys.exit()
            self.ui.parse_command(command)

app = App()
