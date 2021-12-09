import unittest

from app import App
from unittest.mock import Mock


class AppTest(unittest.TestCase):
    def setUp(self) -> None:
        self.io = Mock()
        self.app = App(self.io)
    
    '''
    def test_close_the_app_if_command_q(self):
        self.io.read_input.return_value = "q"
        with self.assertRaises(SystemExit) as cm:
            self.app.run()
        
        self.assertEqual(cm.exception.code, 0)
    '''