
from services.bookmarks_service import BookmarksService
from repositories.bookmarks_repository import BookmarksRepository
from db_connection import DBConnection

class TestUtils:

    @staticmethod
    def get_test_service():
        return BookmarksService(repository=TestUtils.get_test_repository())

    @staticmethod
    def get_test_repository():
        return BookmarksRepository(database_connection=TestUtils.get_test_db_connection())
    
    @staticmethod
    def get_test_db_connection():
        return DBConnection('./src/tests/dummy.db', True)
        