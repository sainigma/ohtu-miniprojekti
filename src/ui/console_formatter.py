from ui.console_io import ConsoleIO

class ConsoleFormatter(ConsoleIO):
    """
    Provides high-level implementations to print formatted data to an ncurses window
    """
    
    def _print_bookmarks_chunk(self, bookmarks, title):
        id_offset = 0
        title_offset = 5
        url_offset = 80
        self.clear()
        self.write(f"{title}")
        self.clear_line(self.cursor + 1, ' ', True)
        self.write("<bold><u>id", 1, id_offset)
        self.write("<bold><u>title", -1, title_offset)
        self.write("<bold><u>url", -1, url_offset)
        if not bookmarks:
            self.write("No bookmarks")
            return
        for bookmark in bookmarks:
            self.write(f'<dim>{bookmark.id}', 0, id_offset)
            self.write(bookmark.url, -1, url_offset)
            title_length = len(bookmark.title)
            title_max_length = url_offset - id_offset - title_offset
            bookmark_title_chunks = [
                bookmark.title[i:i+title_max_length] for i in range(0, title_length, title_max_length)
            ]
            self.write(bookmark_title_chunks[0], -1, title_offset)            
            for title_chunk in bookmark_title_chunks[1:]:
                self.write(title_chunk, 0, title_offset)
    
    def print_bookmarks(self, bookmarks, title="Bookmarks"):
        count = len(bookmarks)

        max_allowed_per_view = int(self.height * 0.75)

        bookmarks_chunks = []
        prints = 0
        while prints < count:
            cursor = prints
            prints = prints + max_allowed_per_view
            bookmarks_chunks.append(bookmarks[cursor:prints])

        cursor = 1
        chunk_cursor = 0
        chunks = len(bookmarks_chunks)
        while chunk_cursor < chunks:
            bookmarks_chunk = bookmarks_chunks[chunk_cursor]
            prompt = f"\nShowing results {cursor} to {cursor + len(bookmarks_chunk) - 1}/{count}"
            self._print_bookmarks_chunk(bookmarks_chunk, f"{title}:")
            
            if chunk_cursor < chunks and chunks > 1:
                user_input = ''
                while user_input not in ['n','r','q','b','enter','right','left']:
                    user_input = self.read_chr(
                        f"{prompt} Navigate with arrow keys or [r]esume to return", 20000000
                        )
                if user_input in ['r','q','b']:
                    break
                if user_input in ['right', 'n']:
                    chunk_cursor = chunk_cursor + 1
                    cursor = cursor + max_allowed_per_view
                elif user_input in ['left'] and chunk_cursor > 0:
                    chunk_cursor = chunk_cursor - 1
                    cursor = cursor - max_allowed_per_view
            else:
                chunk_cursor = chunk_cursor + 1
                self.write(f'{prompt} Reached end')