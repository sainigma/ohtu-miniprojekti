import unittest

from app import App
from ui.stub_io import StubIO


class AppTest(unittest.TestCase):
    def setUp(self) -> None:
        self.io = StubIO()
        self.app = App(self.io)

    def test_welcome_message(self):

        self.app.welcome()
        self.assertEqual(self.io.outputs[0], "Welcome to Bookmarker!")
