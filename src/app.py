class App:
    def __init__(self):
        pass
    def run(self):
        print("Welcome to Bookmarker!")
        while True:
            command = input("Give command: ")
            if command == "quit":
                print("See you again!")
                break

app = App()
