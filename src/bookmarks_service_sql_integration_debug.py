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

bookmarks.delete(93020491)
