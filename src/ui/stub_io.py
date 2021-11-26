class StubIO:
    """
    Implementation based on 
    https://github.com/ohjelmistotuotanto-hy/syksy2021-python/blob/master/koodi/viikko3/login-robot/src/stub_io.py
    """

    def __init__(self, inputs=None):
        self.inputs = inputs or []
        self.outputs = []

    def write(self, value) -> None:
        self.outputs.append(value)

    def read(self, prompt) -> str:
        if len(self.inputs) > 0:
            return self.inputs.pop(0)

        return ""

    def add_input(self, value) -> None:
        self.inputs.append(value)
