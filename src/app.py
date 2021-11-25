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
            elif command == "show":
                print("Show-command is not yet implemented")
            elif command == "edit":
                print("Edit-command is not yet implemented")
            else:
                print("""
                Acceptable commands:
                'q' - quit,
                'add' - add a new bookmark,
                'show' - show given amount of bookmarks,
                'edit' - edit a bookmark
                """)

app = App()
