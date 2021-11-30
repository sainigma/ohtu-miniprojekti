from repositories.app_repository import AppRepository
from services.bookmarks_service_sql import BookmarksServiceSQL
from entities.bookmark import Bookmark

repo = AppRepository(reinitialize=True)
bookmarks = BookmarksServiceSQL(repo)

mockEntry = {
    "title":"Mockentry",
    "url":"Mockentry",
    "tags":[
        {
            "type":"Kirjoittaja",
            "content":"Asd Dasd"
        },
        {
            "type":"tyyppi",
            "content":"Testidata"
        },
    ]
}

print(bookmarks.insert(mockEntry))
print(bookmarks.insert(mockEntry))
print(bookmarks.get_all())
print("pituus:", len(bookmarks.get_all()))
b = bookmarks.get_one(id=1)
print(b['title'])

f = bookmarks.find_by_title("Mock*")
print(f)

b = Bookmark("otsikko")
b.add_tag("Kurssi", "CS 123218")
b.add_tag("Kurssi", "CS 324879")
bookmarks.insert(b.as_dict())
f = bookmarks.find_by_title("*tsik*")[0]
full_b = bookmarks.get_one(id = f['id'])
print(full_b)