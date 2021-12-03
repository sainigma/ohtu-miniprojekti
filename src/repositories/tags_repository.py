from entities.bookmark import Bookmark

class TagsRepository:
    def __init__(self, databaseConnection):
        self.db = databaseConnection    

    def get_tags_for_bookmark(self, bookmark : Bookmark):
        #id = bookmark.id
        #  mikä sisältää
        # tagsQuery = f"select tagtype.title, tag.content from Tags tag \
        #     left join Tagtypes tagtype on tag.tagtypeid = tagtype.id where tag.bookmarkid = {bookmark[0]}"
        # tags = self.db.execute(tagsQuery)
        return bookmark

    def insert_tag(self, tag, bookmarkID):
        idArr = self.db.execute(f'select id from TagTypes where title = "{tag["type"]}"')
      
        if len(idArr) < 1:
            self.db.execute(f'insert into TagTypes (title) values ("{tag["type"]}")')
            idArr = self.db.execute('select max(id) from TagTypes')
        tagTypeID = idArr[0][0]

        self.db.execute(f'insert into Tags (bookmarkid, tagtypeid, content) \
            values ({bookmarkID}, {tagTypeID}, "{tag["content"]}")')

def parse_tags(tags):
    result = []
    for tag in tags:
        result.append({
            "type":tag[0],
            "content":tag[1]
        })
    return result
