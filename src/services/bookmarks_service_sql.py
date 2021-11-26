class BookmarksServiceSQL:
    def __init__(self, databaseConnection):
        self.db = databaseConnection

    def validate(self, bookmark):
        if "title" in bookmark and "tags" in bookmark:
            return True
        return False

    def insertTag(self, tag, bookmarkID):
        idArr = self.db.execute(f'select id from TagTypes where title = "{tag["type"]}"')
        
        if len(idArr) < 1:
            self.db.execute(f'insert into TagTypes (title) values ("{tag["type"]}")')
            idArr = self.db.execute('select max(id) from TagTypes')
        tagTypeID = idArr[0][0]

        self.db.execute(f'insert into Tags (bookmarkid, tagtypeid, content) \
            values ({bookmarkID}, {tagTypeID}, "{tag["content"]}")')

    # Vastaanottaa dict-objektin, jolla on tietueina title ja tags
    # Joko tähän tai bookmarkkiin typecast bookmark -> dict
    # Palauttaa onnistuneessa luonnissa bookmarkin id:n tietokannassa, muutoin -1
    def insert(self, bookmark):
        if not self.validate(bookmark):
            return -1
        
        addBookmarkQuery = f'insert into Bookmarks (title) values ("{bookmark["title"]}");'
        self.db.execute(addBookmarkQuery)
        bookmarkID = self.db.execute('select max(id) from Bookmarks')[0][0]
        
        #1-n ongelma, tän voi todnäk toteuttaa yhdelläkin komennolla
        for tag in bookmark["tags"]:
            self.insertTag(tag, bookmarkID)

        return bookmarkID

    def find(self, params):
        pass

    def parseTags(self,tags):
        result = []
        for tag in tags:
            result.append({
                "type":tag[0],
                "content":tag[1]
            })
        return result

    def resultToBookmark(self, bookmark, tags):
        return {
            "id":bookmark[0],
            "title":bookmark[1],
            "tags":self.parseTags(tags)
        }

    # Palauttaa oletuksena kaiken, yksittäisen entryn jos id on asetettu haussa
    # ja valikoiman jos params on asetettu. Palauttaa listan dict-objekteja
    # start ja bookmarks määrittää mistä kohdasta listaa entryjä haetaan ja kuinka monta
    def get(self, id=None, start=0, bookmarks=10):
        if id is None:
            query = "select id, title from Bookmarks"
            result = self.db.execute(query)
        else:
            bookmarkQuery = f"select b.id, b.title from Bookmarks b where id = {id}"
            bookmark = self.db.execute(bookmarkQuery)
            if len(bookmark) > 0:
                bookmark = bookmark[0]
            else:
                return None

            tagsQuery = f"select tagtype.title, tag.content from Tags tag \
                left join Tagtypes tagtype on tag.tagtypeid = tagtype.id where tag.bookmarkid = {bookmark[0]}"
            tags = self.db.execute(tagsQuery)
            return self.resultToBookmark(bookmark, tags)
        return result

    def remove(self, bookmark_id):
        query = f"delete from Bookmarks where id = {bookmark_id}"
        self.db.execute(query)
        return True
