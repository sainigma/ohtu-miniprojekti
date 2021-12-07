import os
from ui.screen_io import screen_io

class ConsoleIO:
    """
    Implementation based on 
    https://github.com/ohjelmistotuotanto-hy/syksy2021-python/blob/master/koodi/viikko3/login-robot/src/console_io.py
    """

    def write(self, value) -> None:
        print(value)

    def read(self, prompt) -> str:
        return input(prompt)

if os.getenv("EXPERIMENTAL") == "True":
    console_io = screen_io
else:
    console_io = ConsoleIO()
