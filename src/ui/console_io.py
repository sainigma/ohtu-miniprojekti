import time
import curses

class ConsoleIO:
    """
    Implementation based on 
    https://github.com/ohjelmistotuotanto-hy/syksy2021-python/blob/master/koodi/viikko3/login-robot/src/console_io.py
    """
    # pylint: disable=too-many-instance-attributes
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
        self.ascii_codes = {
            10:'enter',
            263:'backspace',127:'backspace',
            258:'down',
            260:'left',
            261:'right',
            259:'up',
        }
        self.commands_up = []
        self.commands_down = []

    def clear_line(self, y_position, character=' ', underline=False):
        self.window.addstr(
            y_position,
            0,
            character * (self.width-1),
            curses.A_UNDERLINE if underline else curses.A_NORMAL
            )
        self.window.border()

    def _get_attributes(self, line):
        attributes = curses.A_NORMAL
        if '<bold>' in line:
            attributes = attributes | curses.A_BOLD
            line = line.replace('<bold>','')
        if '<blink>' in line:
            attributes = attributes | curses.A_BLINK
            line = line.replace('<blink>','')
        if '<dim>' in line:
            attributes = attributes | curses.A_DIM
            line = line.replace('<dim>','')
        if '<u>' in line:
            attributes = attributes | curses.A_UNDERLINE
            line = line.replace('<u>','')
        if '<italic>' in line:
            attributes = attributes | curses.A_ITALIC
            line = line.replace('<italic>', '')
        if '<reverse>' in line:
            attributes = attributes | curses.A_REVERSE
            line = line.replace('<reverse>', '')
        return (line, attributes)

    def write(self, string :str, y_offset = 0, x_offset = 0) -> None:
        if '\n' in string:
            lines = string.split('\n')
        else:
            lines = [string]
        self.cursor = self.cursor + y_offset
        for line in lines:
            line, attributes = self._get_attributes(line)
            if self.cursor > self.height - 3:
                self.window.addstr(
                    self.cursor + 1,
                    self.offset + x_offset,
                    'End of screen reached. Press any key to continue'
                    )    
                self.read_chr('')
                self.clear()

            line.replace('\n', '')
            self.window.addstr(self.cursor, self.offset + x_offset, line, attributes)
            self.cursor = self.cursor + 1
            self.window.refresh()


    def read(self, prompt, y_position = -1, value='') -> str:
        if y_position < 0:
            y_position = self.height -1
        
        string_buffer = value
        result = None
        self.clear_line(y_position)
        self.window.addstr(y_position, self.offset, f"{prompt}{value}")
        
        while not result:
            character = self.window.getch()
            ok = True
            if character in range(32, 127):
                if character == 34:
                    character = 39
                string_buffer += chr(character)
                self.window.addstr(y_position, len(prompt) + self.offset, string_buffer)
            elif self._is_backspace(character) and len(string_buffer) > 0: #backspace
                string_buffer = string_buffer[:-1]
                self.clear_line(y_position)
                self.window.addstr(y_position, self.offset, prompt)
                self.window.addstr(y_position, len(prompt) + self.offset, string_buffer)
            elif character in self.ascii_codes:
                if self.ascii_codes[character] == 'up' and len(self.commands_up) > 0:
                    self.commands_down.append(string_buffer)
                    string_buffer = self.commands_up.pop(-1)
                elif self.ascii_codes[character] == 'down' and len(self.commands_down) > 0:
                    self.commands_up.append(string_buffer)
                    string_buffer = self.commands_down.pop(-1)
                elif self.ascii_codes[character] == 'enter':
                    result = string_buffer
                    self.commands_up.append(result)
                    self.commands_down = []
                else:
                    ok = False
                if ok:
                    self.clear_line(y_position)
                    self.window.addstr(y_position, self.offset, prompt)
                    self.window.addstr(y_position, len(prompt) + self.offset, string_buffer)
            if not ok:
                time.sleep(0.017)
        return result

    def read_chr(self, prompt, y_position = None) -> chr:
        if len(prompt) > 0 and y_position is None:
            self.write(prompt)
        elif y_position is not None:
            if y_position >= self.height:
                y_position = self.height - 2
            self.window.addstr(y_position, self.offset, prompt)
            self.window.refresh()
        result = None
        while not result:
            character = self.window.getch()
            if character in range(32, 127):
                result = chr(character)
            elif character in self.ascii_codes:
                result = self.ascii_codes[character]
            else:
                print(character)
                time.sleep(0.017)
        return result

    def get_cursor(self):
        return self.cursor

    def clear(self) -> None:
        self.cursor = 1
        self.window.erase()
        self.window.clear()
        self.window.border()
        self.height, self.width = self.window.getmaxyx()

    def exit(self, prompt=""):
        curses.nocbreak()
        self.window.keypad(0)
        curses.echo()
        curses.endwin()
        print(prompt)
    
    def _is_backspace(self, char: int) -> bool:
        if char in self.ascii_codes and self.ascii_codes[char] == 'backspace':
            return True
        return False

class MockConsoleIO:
    def clear_line(self):
        pass
    def write(self, value):
        print(value)

    def get_cursor(self):
        return 1

    def read(self, prompt, y_position=0, value=''):
        return input(prompt)

    def read_chr(self, prompt):
        return input(prompt)
    
    def clear(self):
        pass
    def exit(self):
        pass
