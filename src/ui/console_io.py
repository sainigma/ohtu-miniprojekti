import os
import time
import curses

class ConsoleIO:
    """
    Implementation based on 
    https://github.com/ohjelmistotuotanto-hy/syksy2021-python/blob/master/koodi/viikko3/login-robot/src/console_io.py
    """
    def __init__(self):
        self.string_buffer = ""
        self.window = curses.initscr()
        curses.cbreak()
        curses.noecho()
        self.window.keypad(1)
        self.height, self.width = self.window.getmaxyx()
        self.cursor = 1
        #self.window.border(1)
        self.offset = 3

    def clear_line(self, character=' '):
        self.window.addstr(self.height - 1, self.offset, character * (self.width - self.offset - 3))

    def write(self, string :str, y_offset = 0, x_offset = 0) -> None:
        if '\n' in string:
            lines = string.split('\n')
        else:
            lines = [string]
        self.cursor = self.cursor + y_offset
        for line in lines:
            line.replace('\n', '')
            self.window.addstr(self.cursor, self.offset + x_offset, line)
            self.cursor = self.cursor + 1
            self.window.refresh()

    def read(self, prompt) -> str:
        self.string_buffer = ""
        result = None
        self.clear_line()
        self.window.addstr(self.height - 1, self.offset, prompt)
        while not result:
            character = self.window.getch()
            if character in range(32, 122):
                self.string_buffer = self.string_buffer + chr(character)
                self.window.addstr(self.height - 1, len(prompt) + self.offset, self.string_buffer)
            elif character == 263 and len(self.string_buffer) > 0: #backspace
                self.string_buffer = self.string_buffer[:-1]
                self.clear_line()
                self.window.addstr(self.height - 1, self.offset, prompt)
                self.window.addstr(self.height - 1, len(prompt) + self.offset, self.string_buffer)
            elif character == 10:
                result = self.string_buffer
            else:
                time.sleep(0.017)
        return result

    def read_chr(self, prompt) -> chr:
        self.write(prompt)
        result = None
        while not result:
            character = self.window.getch()
            if character in range(32, 122):
                result = chr(character)
            else:
                time.sleep(0.017)
        return result

    def clear(self) -> None:
        self.cursor = 1
        self.window.erase()
        #self.window.border(1)

    def exit(self, prompt=""):
        curses.nocbreak()
        self.window.keypad(0)
        curses.echo()
        curses.endwin()
        print(prompt)

class MockConsoleIO:
    def clear_line(self):
        pass
    def write(self, value):
        print(value)

    def read(self, prompt):
        return input(prompt)

    def read_chr(self, prompt):
        return input(prompt)
    
    def clear(self):
        pass
    def exit(self):
        pass

if os.getenv("TESTING") == "True":
    console_io = MockConsoleIO()
else:
    console_io = ConsoleIO()
