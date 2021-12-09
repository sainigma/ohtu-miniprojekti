class StubIO:
    """
    Implementation based on 
    https://github.com/ohjelmistotuotanto-hy/syksy2021-python/blob/master/koodi/viikko3/login-robot/src/stub_io.py
    """

    def __init__(self):
        self.input = []
        self.output = []
        self.prompt = []

    def write(self, value) -> None:
        self.output.append(value)

    def read(self, prompt) -> str:
        self.prompt.append(prompt)
        if self.input:
            return self.input.pop(0)

        return ""

    def clear(self) -> None:
        pass

    def set_input(self, value) -> None:
        self.input.append(value)
