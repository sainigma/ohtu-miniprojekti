import os

class ConsoleIO:
    """
    Implementation based on 
    https://github.com/ohjelmistotuotanto-hy/syksy2021-python/blob/master/koodi/viikko3/login-robot/src/console_io.py
    """

    def write(self, value) -> None:
        print(value)

    def read(self, prompt) -> str:
        return input(prompt)

    def clear(self) -> None:
        name = os.name
        if name == 'posix':
            os.system('clear')
        elif name == 'nt':
            os.system('cls')

console_io = ConsoleIO()
