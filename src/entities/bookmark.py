class Bookmark:
    def __init__(self, title):
        self.title = title
        self.tags = set()
    
    def add_tag(self, tag):
        #add tag if not already found
        if tag.lower() not in self.tags:
            self.tags.add(tag.lower())
    
    def find_tag(self, tag):
        #search for tag, return true if found, false if not
        if tag.lower() in self.tags:
            return True
        return False

    def get_bookmark(self):
        # create and return a dictionary with bookmark object fields
        bookmark = {
            "title": self.title,
            "tags": self.tags
        }
        return bookmark