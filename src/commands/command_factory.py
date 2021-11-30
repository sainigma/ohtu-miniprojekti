from commands import Add, Show, Edit, Search

class CommandFactory:
    def __init__(self, io):
        self.io = io

        self.commands = {
            "add": Add(self.io),
            "show": Show(self.io),
            "edit": Edit(self.io),
            "search": Search(self.io)
        }
    
    def set_command(self, command):
        if command in self.commands:
            return self.commands[command]

command_factory = CommandFactory()
