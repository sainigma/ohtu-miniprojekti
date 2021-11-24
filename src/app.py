class App:
    def __init__(self):
        pass
    def run(self):
        print("Welcome to Bookmarker!")
        while True:
            command = input("Give command: ")
            if command == "q":
                print("See you again!")
                break
            if command == "add":
                print("Add-command is not yet implemented")
            else:
                print("Acceptable commands: 'q' - quit, 'add' - add a new bookmark")

app = App()
