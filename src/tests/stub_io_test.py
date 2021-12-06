import unittest

from ui.stub_io import StubIO

class StubIOTest(unittest.TestCase):
    def setUp(self):
        self.io = StubIO()
    
    def test_method_write_adds_argument_to_output_list(self):
        self.io.write("test")

        self.assertEqual(self.io.output, ["test"])
    
    def test_method_set_input_adds_argument_to_input_list(self):
        self.io.set_input("test")

        self.assertEqual(self.io.input, ["test"])
    
    def test_return_empty_string_when_input_list_is_empty(self):
        result = self.io.read("")

        self.assertEqual(result, "")
    
    def test_return_first_item_of_input_list_when_it_is_not_empty(self):
        self.io.set_input("test")
        result = self.io.read("")
        self.assertEqual(result, "test")