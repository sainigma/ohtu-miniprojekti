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
        self._app.parse_input(value)

    def output_should_contain(self, value):
        outputs = self._io.outputs

        if not value in outputs:
            raise AssertionError(
                f"Output \"{value}\" is not in {str(outputs)}"
            )
    
    def welcome(self):
        self._app.welcome()
