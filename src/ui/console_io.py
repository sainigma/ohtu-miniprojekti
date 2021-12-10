import time
import curses

class ConsoleIO:
    """
    Implementation based on 
    https://github.com/ohjelmistotuotanto-hy/syksy2021-python/blob/master/koodi/viikko3/login-robot/src/console_io.py
    """
    def __init__(self):
        self._string_buffer = ""
        self.window = curses.initscr()
        curses.cbreak()
        curses.noecho()
        self.window.keypad(1)
        self.height, self.width = self.window.getmaxyx()
        self.cursor = 1
        self.window.border()
        self.offset = 3

    def clear_line(self, y_position, character=' '):
        self.window.addstr(y_position, self.offset, character * (self.width - self.offset - 3))

    def write(self, string :str, y_offset = 0, x_offset = 0) -> None:
        if '\n' in string:
            lines = string.split('\n')
        else:
            lines = [string]
        self.cursor = self.cursor + y_offset
        for line in lines:
            if self.cursor > self.height - 3:
                self.window.addstr(
                    self.cursor + 1,
                    self.offset + x_offset,
                    'End of screen reached. Press any key to continue'
                    )    
                self.read_chr('')
                self.clear()

            line.replace('\n', '')
            self.window.addstr(self.cursor, self.offset + x_offset, line)
            self.cursor = self.cursor + 1
            self.window.refresh()


    def read(self, prompt, y_position = -1) -> str:
        if y_position < 0:
            y_position = self.height -1
        
        string_buffer = ""
        result = None
        self.clear_line(y_position)
        self.window.addstr(y_position, self.offset, prompt)
        while not result:
            character = self.window.getch()
            if character in range(32, 122):
                string_buffer += chr(character)
                self.window.addstr(y_position, len(prompt) + self.offset, string_buffer)
            elif character == 263 and len(string_buffer) > 0: #backspace
                string_buffer = string_buffer[:-1]
                self.clear_line(y_position)
                self.window.addstr(y_position, self.offset, prompt)
                self.window.addstr(y_position, len(prompt) + self.offset, string_buffer)
            elif character == 10:
                result = string_buffer
            else:
                time.sleep(0.017)
        return result

    def read_chr(self, prompt) -> chr:
        if len(prompt) > 0:
            self.write(prompt)
        result = None
        while not result:
            character = self.window.getch()
            if character in range(32, 122):
                result = chr(character)
            else:
                time.sleep(0.017)
        return result

    def get_cursor(self):
        return self.cursor

    def clear(self) -> None:
        self.cursor = 1
        self.window.erase()
        self.window.border()
        self.height, self.width = self.window.getmaxyx()

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

    def get_cursor(self):
        return 1

    def read(self, prompt):
        return input(prompt)

    def read_chr(self, prompt):
        return input(prompt)
    
    def clear(self):
        pass
    def exit(self):
        pass
