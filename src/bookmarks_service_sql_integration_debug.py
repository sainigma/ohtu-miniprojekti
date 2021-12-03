from services.bookmarks_service import BookmarksService

#repo = AppRepository(reinitialize=True)
bookmarks = BookmarksService()

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
'''
print(bookmarks.create(mockEntry["url"]))
print(bookmarks.create(mockEntry["url"]))
print(bookmarks.get_all())
print("pituus:", len(bookmarks.get_all()))
b = bookmarks.get_one(id=1)
print(b['title'])

f = bookmarks.get_by_title("Mock*")
print(f)
'''
