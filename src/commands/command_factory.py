from commands.commands import Delete, Help, Add, ImportJson, Show, Edit, Search, Unknown, Select, Export


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
            "select": Select(self.io, service),
            "delete": Delete(self.io, service),
            "export": Export(self.io, service),
            "import": ImportJson(self.io, service)
        }
    
    def get_command(self, command):
        if command in self.commands:
            return self.commands[command]
        return Unknown(self.io)
