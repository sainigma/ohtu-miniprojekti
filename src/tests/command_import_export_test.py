import unittest
from unittest.mock import Mock, MagicMock, patch, mock_open, ANY
from commands.commands import InvalidInputException
from commands.commands_import_export import Export, ImportJson

class TestExport(unittest.TestCase):
    def setUp(self):
        self.io = Mock()
        self.service = Mock()
        self.bookmark = Mock(title="Test", url="test.com")
        
        self.export = Export(self.io, self.service)

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
        
        self.export._write_to_file({"bookmarks":[{"title":"Test","url":"test.com"}]}, 'export/test.json')
        m.assert_called_with('export/test.json', 'w')
    
    def test_open_file_created_by_default(self):
        with patch('datetime.datetime') as dt_mock:
            dt_mock.now.return_value.strftime.return_value = '2021-12-13 12:22:44.123456'
        
        m = mock_open()
        with patch('builtins.open', m):
            with open('export/2021-12-13 12:22:44.123456.json', 'w') as h:
                h.write('{"bookmarks":[{"title":"Test","url":"test.com"}]}')

        self.export._write_to_file({"bookmarks":[{"title":"Test","url":"test.com"}]}, self.export._parse_path([]))
        m.assert_called_with('export/2021-12-13 12:22:44.123456.json', 'w')
    
    def test_run_command(self):
        self.service.get_all.return_value = self.bookmark
        self.export.convert_to_json = MagicMock(return_value='{"bookmarks":[{"title":"Test","url":"test.com"}]}')
        self.export._write_to_file = MagicMock()

        self.export._run_command([])

        self.export.convert_to_json.assert_called_with(self.bookmark)
        self.export._write_to_file.assert_called_with('{"bookmarks":[{"title":"Test","url":"test.com"}]}', ANY)

class TestImportJson(unittest.TestCase):
    def setUp(self):
        self.io = Mock()
        self.service = Mock()
        self.bookmark = Mock(title="Test", url="test.com")
        
        self.importjson = ImportJson(self.io, self.service)
    
    def test_run_command_without_argument(self):
        with self.assertRaises(InvalidInputException) as context:
            self.importjson._run_command([])
        
        self.assertTrue('Import argument missing' in str(context.exception))

    def test_run_command_with_unvalid_argument(self):
        with self.assertRaises(InvalidInputException) as context:
            self.importjson._run_command(["test"])
        
        self.assertTrue('File not found' in str(context.exception))
    
    def test_run_command_opens_file_successfully(self):
        m = mock_open()
        with patch('builtins.open', m):
            with open('export/test.json', 'r') as h:
                pass
        self.importjson.validate_json = MagicMock(return_value=True)
        self.importjson.add_bookmarks_to_repository = MagicMock()

        self.importjson._run_command(['export/test.json'])
        m.assert_called_with('export/test.json', 'r')

    def test_import_valid_json_validate_true(self):
        data = {"db":[{"title": "Google", "url": "http://www.google.com"}]}

        self.assertTrue(self.importjson.validate_json(data))
    
    def test_import_invalid_json_validate_false(self):
        data = {"db":[{"kissa": "koira", "vauva": "lapsi"}]}

        self.assertFalse(self.importjson.validate_json(data))
    
    def test_add_bookmark_calls_bookmark_service_create_method_with_arguments(self):
        data = {"db":[{"title": "Google", "url": "http://www.google.com"}]}
        self.service.create.return_value = self.bookmark

        self.bookmark.short_str = MagicMock(return_value='Google')
        
        self.importjson.add_bookmarks_to_repository(data)

        self.service.create.assert_called_once_with("http://www.google.com", "Google")

    def test_add_bookmark_text_when_bookmark_added(self):
        data = {"db":[{"title": "Google", "url": "http://www.google.com"}]}
        self.service.create.return_value = self.bookmark

        self.bookmark.short_str = MagicMock(return_value='Google')

        self.importjson.add_bookmarks_to_repository(data)
        self.io.write.assert_called_with("Added Google")
    
    def test_add_bookmark_text_when_bookmark_not_added(self):
        data = {"db":[{"title": "Google", "url": "google.com"}]}
        self.service.create.return_value = None

        self.importjson.add_bookmarks_to_repository(data)
        self.io.write.assert_called_with("Invalid bookmark: Google")
