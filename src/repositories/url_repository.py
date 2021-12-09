from services.url_validator import get_url

class UrlRepository:
    def __init__(self, databaseConnection):
        self.db = databaseConnection

    def _insert_url(self, url):
        query = f'select id from Urls where url = "{url}";'
        result = self.db.execute(query)
        if len(result) > 0:
            return result[0][0]
        
        query = f'insert into Urls (url) values ("{url}");'
        self.db.execute(query)
        return self.db.execute('select max(id) from Urls')[0][0]

    def create_url(self, url):
        site_info = get_url(url)
        if not site_info:
            return False

        urlId = self._insert_url(url)
        return {
          'id':urlId,
          'info':site_info
        }
