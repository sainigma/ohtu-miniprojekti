class StubIO:
    """
    Implementation based on 
    https://github.com/ohjelmistotuotanto-hy/syksy2021-python/blob/master/koodi/viikko3/login-robot/src/stub_io.py
    """

    def __init__(self, input=None):
        self.input = ""
        self.output = ""
        self.prompt = ""

    def write(self, value) -> None:
        self.output = value

    def read(self, prompt) -> str:
        self.prompt = prompt
        if len(self.input) > 0:
            return self.input

        return ""

    def set_input(self, value) -> None:
        self.input = value
