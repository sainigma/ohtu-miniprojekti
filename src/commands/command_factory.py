from commands.commands import Help, Add, Show, Edit, Search, Unknown


class CommandFactory:
    def __init__(self, io, service):
        self.io = io
        self.service = service

        self.commands = {
            "h": Help(self.io, self.service),
            "add": Add(self.io, service),
            "show": Show(self.io, service),
            "edit": Edit(self.io, service),
            "search": Search(self.io, service),
        }
    
    def get_command(self, command):
        if command in self.commands:
            return self.commands[command]
        return Unknown(self.io)
