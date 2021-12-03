from typing import List
from entities.bookmark import Bookmark
from repositories.bookmarks_repository import bookmarks_repository
from services.url_validator import get_url

class BookmarksService:
    def __init__(self, repository=bookmarks_repository):
        self.repository = repository
        self.cursor = 0
        self.bookmarks_returned_on_get_all = 10

    def create(self, url:str, title:str) -> Bookmark:
        return bookmarks_repository.create_bookmark(url,title)

    def get_one(self, id:int) -> Bookmark:
        return bookmarks_repository.get_bookmark_complete(id)

    def get_all(self, start=0) -> List[Bookmark]:
        self.cursor = start
        return self.repository.get_bookmark_range(
            self.cursor, 
            self.cursor + self.bookmarks_returned_on_get_all
            ) 

    def get_more(self) -> List[Bookmark]:
        self.cursor = self.cursor + self.bookmarks_returned_on_get_all
        return self.get_all(self.cursor)

    def get_by_title(self, title:str) -> List[Bookmark]:
        return self.repository.find_bookmarks_by_title(title)

    def get_title_by_url(self, url:str) -> List[Bookmark]:
        site_info = get_url(url)
        if not site_info:
            return None
        return site_info['title']

    def clear(self):
        self.repository.clear()

    def delete(self, bookmark_id : int) -> bool:
        return self.repository.delete(bookmark_id)

    def bookmarks_amount(self):
        return self.repository.get_count()

bookmarks_service = BookmarksService()
