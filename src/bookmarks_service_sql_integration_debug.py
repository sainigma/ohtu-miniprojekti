from repositories.app_repository import AppRepository
from services.bookmarks_service_sql import BookmarksServiceSQL

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

f = bookmarks.findByTitle("Mock%")
print(f)