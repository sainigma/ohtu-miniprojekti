class Bookmark:
    def __init__(self, url):
        self.tags = []
        self.tagHashes = {}
        self.url = url
        self.fetch_title()
    
    def fetch_title(self):
        self.title = self.url

    def add_tag(self, tagType, tagContent):
        '''add tag if not already found
        '''
        tag = {
            'type':tagType.lower(),
            'content':tagContent
        }
        tag_hash = hash(f'{tagType.lower()}////{tagContent.lower()}')

        if tag_hash not in self.tagHashes:
            self.tags.append(tag)
            self.tagHashes[tag_hash] = 1

    def find_tag_by_type(self, tagType):
        '''search for tag, return true if found, false if not
        '''
        for tag in self.tags:
            if tag['type'] == tagType.lower():
                return True
        return False

    def as_dict(self):
        '''create and return a dictionary with bookmark object fields
        '''
        bookmark = {
            "title": self.title,
            "url": self.url,
            "tags": self.tags
        }
        return bookmark
    
    def __str__(self):
        tagStr = ""
        for tag in self.tags:
            tagStr += f"{tag['content']}  "
        return (f"title: {self.title}\n"
                f"url: {self.url}\n"
                f"tags:  {tagStr}")