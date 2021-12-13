import unittest
from unittest import mock
from unittest.mock import Mock, patch, mock_open
from commands.commands_import_export import Export, ImportJson

class TestExport(unittest.TestCase):
    def setUp(self) -> None:
        self.io = Mock()
        self.service = Mock()
        self.bookmark = Mock(title="Test", url="test.com")
        
        self.export = Export(self.io)

    def test_convert_to_json_style(self):
        bookmarks = [self.bookmark]

        self.assertEqual(self.export.convert_to_json(bookmarks), {"bookmarks":[{"title":"Test","url":"test.com"}]})

    def test_check_path(self):
        path = self.export.check_path("export/test.json")
        self.assertEqual(path, "export/test.json")

        path = self.export.check_path("test.json")
        self.assertEqual(path, "export/test.json")

        path = self.export.check_path("test")
        self.assertEqual(path, "export/test.json")

    def test_open_given_file(self):
        m = mock_open()
        with patch('builtins.open', m):
            with open('export/test.json', 'w') as h:
                h.write('{"bookmarks":[{"title":"Test","url":"test.com"}]}')
        
        self.export.write_to_file({"bookmarks":[{"title":"Test","url":"test.com"}]}, ['export/test.json'])
        m.assert_called_with('export/test.json', 'w')
    
    def test_open_file_created_by_default(self):
        with patch('datetime.datetime') as dt_mock:
            dt_mock.now.return_value.strftime.return_value = '2021-12-13 12:22:44.123456'
        
        m = mock_open()
        with patch('builtins.open', m):
            with open('export/2021-12-13 12:22:44.123456.json', 'w') as h:
                h.write('{"bookmarks":[{"title":"Test","url":"test.com"}]}')

        self.export.write_to_file({"bookmarks":[{"title":"Test","url":"test.com"}]}, [])
        m.assert_called_with('export/2021-12-13 12:22:44.123456.json', 'w')