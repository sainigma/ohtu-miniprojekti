from repositories.app_repository import AppRepository
from services.bookmarks_service_sql import BookmarksServiceSQL
from entities.bookmark import Bookmark

repo = AppRepository(reinitialize=True)
bookmarks = BookmarksServiceSQL(repo)

mockEntry = {
  "title":"Mockentry",
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
print(bookmarks.get())
print("pituus:", len(bookmarks.get()))
b = bookmarks.get(id=1)
print(b['title'])

f = bookmarks.find_by_title("Mock*")
print(f)

b = Bookmark("otsikko")
b.add_tag("Kurssi", "CS 123218")
b.add_tag("Kurssi", "CS 324879")