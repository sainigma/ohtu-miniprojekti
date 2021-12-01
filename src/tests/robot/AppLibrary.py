from ui.stub_io import StubIO
from ui.app_ui import AppUi


class AppLibrary:
    '''
        References from course material
    '''

    def __init__(self):
        self._io = StubIO()
        self._app = AppUi(self._io)

    def input(self, value):
        self._io.set_input(value)
    
    def read_command(self):
        self._app.parse_command(self._io.read(prompt=""))

    def execute_command(self):
        self._app.execute_command()

    def output_should_contain(self, value):
        output = self._io.output

        if not value in output:
            raise AssertionError(
                f"Output \"{value}\" is not in {str(output)}"
            )
        
    def output_should_be(self, value):
        if not value == self._io.output:
            raise AssertionError(
                f"Output \"{value}\" is not equal to {str(self._io.output)}"
            )
    
    def prompt_should_contain(self, value):
        prompt = self._io.prompt

        if not value in prompt:
            raise AssertionError(
                f"Output \"{value}\" is not in {str(prompt)}"
            )

    
    def welcome(self):
        self._app.welcome()

    def reset(self):
        self._app.service.clear()
    
    def add_bookmark(self, title):
        self.input("add")
        self.read_command()
        self.input(title)
        self.execute_command()
