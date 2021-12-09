from ui.console_io import ConsoleIO
from services.bookmarks_service import bookmarks_service

class ConsoleFormatter(ConsoleIO):
    """
    Provides high-level implementations to print formatted data to an ncurses window
    """
    def __init__(self) -> None:
        super().__init__()
        self.service = bookmarks_service
    
    def print_bookmarks(self, bookmarks, title):
        id_offset = 0
        title_offset = 5
        url_offset = 80
        self.clear()
        self.write(f"{title}:")
        self.write("id", 1, id_offset)
        self.write("title", -1, title_offset)
        self.write("url", -1, url_offset)
        if not bookmarks:
            self.write("No bookmarks")
            return
        for bookmark in bookmarks:
            self.write(f'{bookmark.id}', 0, id_offset)
            self.write(bookmark.url, -1, url_offset)
            title_length = len(bookmark.title)
            title_max_length = url_offset - id_offset - title_offset
            bookmark_title_chunks = [
                bookmark.title[i:i+title_max_length] for i in range(0, title_length, title_max_length)
            ]
            self.write(bookmark_title_chunks[0], -1, title_offset)            
            for title_chunk in bookmark_title_chunks[1:]:
                self.write(title_chunk, 0, title_offset)
    
    def print_bookmarks_range(self, bookmarks, cursor=0, count=0):
        count = len(bookmarks)
        self.print_bookmarks(bookmarks, "Bookmarks")

        if len(bookmarks) <= count:
            prompt = f"\nShowing results {cursor + 1} to {cursor + len(bookmarks)}/{count}."
            if cursor + len(bookmarks) < count:
                user_input = ''
                while user_input not in ['n', 'r']:
                    user_input = self.read_chr(f"{prompt} Press [n] for more, [r] to resume")
                if user_input == 'n':
                    return True
            else:
                self.write(f'{prompt} Reached end')
        return False
