
from services.bookmarks_service import BookmarksService
from repositories.bookmarks_repository import BookmarksRepository
from db_connection import DBConnection
from ui.app_ui import AppUi
from ui.stub_io import StubIO

class TestUtils:

    @staticmethod
    def get_test_app_ui():
        return AppUi(io=TestUtils.get_test_io(), service=TestUtils.get_test_service())
    
    @staticmethod
    def get_test_io():
        return StubIO()

    @staticmethod
    def get_test_service():
        return BookmarksService(repository=TestUtils.get_test_repository())

    @staticmethod
    def get_test_repository():
        return BookmarksRepository(database_connection=TestUtils.get_test_db_connection())
    
    @staticmethod
    def get_test_db_connection():
        return DBConnection('./src/tests/dummy.db', True)
        