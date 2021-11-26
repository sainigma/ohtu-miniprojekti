from ui.console_io import console_io as default_console_io

class App:
    def __init__(self, ui=default_console_io):
        self.ui = ui
        
    def run(self):
        self.ui.write("Welcome to Bookmarker!")
        while True:
            command = self.ui.read("Give command: ")
            if command == "q":
                self.ui.write("See you again!")
                break
            if command == "add":
                self.ui.write("Add-command is not yet implemented")
            elif command == "show":
                self.ui.write("Show-command is not yet implemented")
            elif command == "edit":
                self.ui.write("Edit-command is not yet implemented")
            else:
                self.ui.write("""
                Acceptable commands:
                'q' - quit,
                'add' - add a new bookmark,
                'show' - show given amount of bookmarks,
                'edit' - edit a bookmark
                """)

app = App()
