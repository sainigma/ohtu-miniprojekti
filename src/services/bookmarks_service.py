from typing import List
from db_connection import database_connection
from entities.bookmark import Bookmark
from services.url_validator import get_url

class BookmarksService:
    def __init__(self, databaseConnection=database_connection):
        self.db = databaseConnection

    def insert_tag(self, tag, bookmarkID):
        idArr = self.db.execute(f'select id from TagTypes where title = "{tag["type"]}"')
        
        if len(idArr) < 1:
            self.db.execute(f'insert into TagTypes (title) values ("{tag["type"]}")')
            idArr = self.db.execute('select max(id) from TagTypes')
        tagTypeID = idArr[0][0]

        self.db.execute(f'insert into Tags (bookmarkid, tagtypeid, content) \
            values ({bookmarkID}, {tagTypeID}, "{tag["content"]}")')

    def insert_url(self, url):
        query = f'select id from Urls where url = "{url}";'
        result = self.db.execute(query)
        if len(result) > 0:
            return result[0][0]
        
        query = f'insert into Urls (url) values ("{url}");'
        self.db.execute(query)
        return self.db.execute('select max(id) from Urls')[0][0]

    def create(self, url) -> Bookmark:
        res = get_url(url)
        if not res:
            raise Exception("Invalid url " + url)
        title = res["title"]
        bookmarkDict = {
            "url": url, "title": title, "tags": []
        }
        
        urlId = self.insert_url(bookmarkDict["url"])

        addBookmarkQuery = f'insert into Bookmarks (title, urlid) values ("{title}", {urlId});'
        self.db.execute(addBookmarkQuery)
        bookmarkID = self.db.execute('select max(id) from Bookmarks')[0][0]

        return Bookmark(id=bookmarkID, title=title, url=url)

    def _tuple_to_bookmark(self, b) -> Bookmark:
        return Bookmark(id=b[0], title=b[1], url=b[2])

    def _parse_bookmark_list(self, bookmarks) -> List[Bookmark]:
        return list(map(self._tuple_to_bookmark, bookmarks))

    def get_by_title(self, title) -> List[Bookmark]:
        searchString = title.replace('*','%')
        query = f'select * from Bookmarks where title like "{searchString}"'
        result = self.db.execute(query)
        return self._parse_bookmark_list(result)

    def _parse_tags(self,tags):
        result = []
        for tag in tags:
            result.append({
                "type":tag[0],
                "content":tag[1]
            })
        return result
    
    def get_all(self, start=0, bookmarks=None) -> List[Bookmark]:
        query = "select b.id, b.title, u.url from Bookmarks b left join Urls u on u.id = b.urlid;"
        result = self.db.execute(query)
        return self._parse_bookmark_list(result)

    def get_one(self, id) -> Bookmark:
        bookmarkQuery = f"select b.id, b.title, u.url from Bookmarks b \
            left join Urls u on u.id = b.urlid where b.id = {id}"
        bookmark = self.db.execute(bookmarkQuery)
        if len(bookmark) > 0:
            bookmark = bookmark[0]
        else:
            return None

        #tagsQuery = f"select tagtype.title, tag.content from Tags tag \
        #    left join Tagtypes tagtype on tag.tagtypeid = tagtype.id where tag.bookmarkid = {bookmark[0]}"
        #tags = self.db.execute(tagsQuery)
        return self._tuple_to_bookmark(bookmark)

    def bookmarks_amount(self):
        query = "select count(id) from Bookmarks;"
        result = self.db.execute(query)
        return result[0][0]

    def delete(self, bookmark_id) -> int:
        query = f"delete from Bookmarks where id = {bookmark_id}"
        self.db.execute(query)
        # Tarkasta orpoutuuko bookmarkin resurssit
        return bookmark_id

    def clear(self):
        self.db.execute("delete from Bookmarks;")
        self.db.execute("delete from Urls;")
        self.db.execute("delete from Tags;")
        self.db.execute("delete from TagTypes;")


bookmarks_service = BookmarksService()
