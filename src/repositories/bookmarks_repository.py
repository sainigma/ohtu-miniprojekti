from typing import List
from db_connection import database_connection
from repositories.url_repository import UrlRepository
from repositories.tags_repository import TagsRepository
from entities.bookmark import Bookmark

class BookmarksRepository:
    def __init__(self, databaseConnection=database_connection):
        self.db = databaseConnection
        self.url_repository = UrlRepository(databaseConnection)
        self.tags_repository = TagsRepository(databaseConnection)
        self.count = 0

    def _get_last_insertation(self):
        return self.db.execute('select max(id) from Bookmarks;')[0][0]

    def create_bookmark(self, url, title) -> Bookmark:
        url_info = self.url_repository.create_url(url)
        if not url_info:
            return None

        url_id = url_info['id']
        #site_info = url_info['info']
        #meta_tags = site_info['meta']

        bookmark_create_query = f'insert into Bookmarks (title, urlid) values ("{title}", {url_id});'
        self.db.execute(bookmark_create_query)
        bookmark_id = self._get_last_insertation()

        self.count = self.count + 1
        return Bookmark(id=bookmark_id, title=title, url=url)

    def get_count(self):
        query = "select count(id) from Bookmarks;"
        result = self.db.execute(query)
        return result[0][0]
        
    def get_bookmark_range(self, offset=0, row_count=50) -> List[Bookmark]:
        query = f"""select b.id, b.title, u.url from Bookmarks b 
                    left join Urls u on u.id = b.urlid limit {offset}, {row_count};"""
        bookmarks = self.db.execute(query)
        return parse_bookmark_list(bookmarks)

    def get_bookmark_complete(self, id):
        bookmark_query = f"""select b.id, b.title, u.url from Bookmarks b
                            left join Urls u on u.id = b.urlid where b.id = {id};"""
        result = self.db.execute(bookmark_query)
        if len(result) == 0:
            return None
        
        bookmark = tuple_to_bookmark(result[0])
        bookmark = self.tags_repository.get_tags_for_bookmark(bookmark)
        return bookmark

    def _format_search_str(self, search_string: str) -> str:
        search_string = search_string.replace('*','%')
        if search_string[0] == '"' and search_string[-1] == '"':
            return search_string[1:-1]
        return "%" + search_string + "%"

    def find_bookmarks_by_title(self, search_string : str) -> List[Bookmark]:
        search_string = self._format_search_str(search_string)
        query = f'select * from Bookmarks where title like "{search_string}";'
        result = self.db.execute(query)
        return parse_bookmark_list(result)

    def find_bookmarks_by_url(self, search_string : str) -> List[Bookmark]:
        search_string = self._format_search_str(search_string)
        query = f"""select b.id, b.title, u.url from Urls u 
                    left join Bookmarks b on u.id = b.urlid where u.url like "{search_string}";"""
        result = self.db.execute(query)
        return parse_bookmark_list(result)

    def delete(self, id):
        exists_query = f"select count(id) from Bookmarks where id = {id};"
        bookmark_exists = self.db.execute(exists_query)[0][0]
        if bookmark_exists == 0:
            return False

        self.count = self.count - 1
        query = f"delete from Bookmarks where id = {id};"
        self.db.execute(query)
        # Tarkasta orpoutuuko bookmarkin resurssit
        return True

    def clear(self):
        self.db.execute("delete from Bookmarks;")
        self.db.execute("delete from Urls;")
        self.db.execute("delete from Tags;")
        self.db.execute("delete from TagTypes;")

def tuple_to_bookmark(b) -> Bookmark:
    return Bookmark(id=b[0], title=b[1], url=b[2])

def parse_bookmark_list(bookmarks) -> List[Bookmark]:
    return list(map(tuple_to_bookmark, bookmarks))

bookmarks_repository = BookmarksRepository()