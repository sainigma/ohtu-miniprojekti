from ui.stub_io import StubIO
from app import App


class AppLibrary:
    '''
        References from course material
    '''

    def __init__(self):
        self._io = StubIO()
        self._app = App(self._io)

    def input(self, value):
        self._io.set_input(value)
    
    def read_command(self):
        self._app.parse_input(self._io.read(prompt=""))
    
    def read_title(self):
        self._app.add_bookmark(self._io.read(prompt=""))

    def output_should_contain(self, value):
        output = self._io.output

        if not value in output:
            raise AssertionError(
                f"Output \"{value}\" is not in {str(output)}"
            )
    
    def prompt_should_contain(self, value):
        prompt = self._io.prompt

        if not value in prompt:
            raise AssertionError(
                f"Output \"{value}\" is not in {str(prompt)}"
            )

    
    def welcome(self):
        self._app.welcome()
