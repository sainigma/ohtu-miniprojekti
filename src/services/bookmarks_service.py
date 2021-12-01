from db_connection import database_connection

class BookmarksService:
    def __init__(self, databaseConnection=database_connection):
        self.db = databaseConnection

    def validate(self, bookmark):
        if "title" in bookmark and "tags" in bookmark and "url" in bookmark:
            return True
        return False

    def insert_tag(self, tag, bookmarkID):
        idArr = self.db.execute(f'select id from TagTypes where title = "{tag["type"]}"')
        
        if len(idArr) < 1:
            self.db.execute(f'insert into TagTypes (title) values ("{tag["type"]}")')
            idArr = self.db.execute('select max(id) from TagTypes')
        tagTypeID = idArr[0][0]

        self.db.execute(f'insert into Tags (bookmarkid, tagtypeid, content) \
            values ({bookmarkID}, {tagTypeID}, "{tag["content"]}")')

    def insert_url(self, url):
        query = 'select id from Urls where url = "{url}";'
        result = self.db.execute(query)
        if len(result) > 0:
            return result[0][0]
        
        query = 'insert into Urls (url) values ("{url}");'
        self.db.execute(query)
        return self.db.execute('select max(id) from Urls')[0][0]

    def insert(self, bookmark):
        """Palauttaa onnistuneessa luonnissa bookmarkin id:n tietokannassa, muutoin -1
        """
        if not self.validate(bookmark):
            return -1
        
        urlId = self.insert_url(bookmark["url"])

        addBookmarkQuery = f'insert into Bookmarks (title, urlid) values ("{bookmark["title"]}", {urlId});'
        self.db.execute(addBookmarkQuery)
        bookmarkID = self.db.execute('select max(id) from Bookmarks')[0][0]
        
        #1-n ongelma, tän voi todnäk toteuttaa yhdelläkin komennolla
        for tag in bookmark["tags"]:
            self.insert_tag(tag, bookmarkID)

        return bookmarkID

    def _parse_bookmark_list(self, bookmarks):
        return list(map(lambda bookmark: {"id":bookmark[0], "title":bookmark[1]}, bookmarks))

    def find_by_title(self, title):
        searchString = title.replace('*','%')
        query = f'select * from Bookmarks where title like "{searchString}"'
        result = self.db.execute(query)
        return self._parse_bookmark_list(result)

    def find_by_tag(self, tag):
        '''
        tag_template1 = "kurssi:CS 120931"
        tag_template2 = "kirja:Asd"
        tag_template3 = "*:fdsjlkj"
        '''
        return None

    def find(self, params):
        return None

    def _parse_tags(self,tags):
        result = []
        for tag in tags:
            result.append({
                "type":tag[0],
                "content":tag[1]
            })
        return result

    def _result_to_bookmark(self, bookmark, tags):
        return {
            "id":bookmark[0],
            "title":bookmark[1],
            "tags":self._parse_tags(tags)
        }
    
    def get_all(self, start=0, bookmarks=None):
        query = "select b.id, b.title, u.url from Bookmarks b left join Urls u on u.id = b.urlid;"
        result = self.db.execute(query)
        return self._parse_bookmark_list(result)

    def get_one(self, id):
        bookmarkQuery = f"select b.id, b.title, u.url from Bookmarks b \
            left join Urls u on u.id = b.urlid where b.id = {id}"
        bookmark = self.db.execute(bookmarkQuery)
        if len(bookmark) > 0:
            bookmark = bookmark[0]
        else:
            return None

        tagsQuery = f"select tagtype.title, tag.content from Tags tag \
            left join Tagtypes tagtype on tag.tagtypeid = tagtype.id where tag.bookmarkid = {bookmark[0]}"
        tags = self.db.execute(tagsQuery)
        return self._result_to_bookmark(bookmark, tags)

    def bookmarks_amount(self):
        query = "select count(id) from Bookmarks;"
        result = self.db.execute(query)
        return result[0][0]

    def remove(self, bookmark_id):
        query = f"delete from Bookmarks where id = {bookmark_id}"
        self.db.execute(query)
        # Tarkasta orpoutuuko bookmarkin resurssit
        return True

    def clear(self):
        self.db.execute("delete from Bookmarks;")
        self.db.execute("delete from Urls;")
        self.db.execute("delete from Tags;")
        self.db.execute("delete from TagTypes;")


bookmarks_service = BookmarksService()
