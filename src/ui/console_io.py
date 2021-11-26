class ConsoleIO:
    """
    Implementation based on 
    https://github.com/ohjelmistotuotanto-hy/syksy2021-python/blob/master/koodi/viikko3/login-robot/src/console_io.py
    """

    def write(self, value) -> None:
        print(value)

    def read(self, prompt) -> str:
        return input(prompt)


console_io = ConsoleIO()
