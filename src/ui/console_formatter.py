from ui.console_io import ConsoleIO

class ConsoleFormatter(ConsoleIO):
    """
    Provides high-level implementations to print formatted data to a curses window
    """

    def __init__(self):
        super().__init__()

        self.max_per_view = int(self.height * 0.72)

    def _shorten_string(self, string, max_length):
        if string is None:
            return ''
        if len(string) > max_length:
            string = string[:max_length-3] + '...'
        return string

    def _split_string_to_chunks(self, string, max_length):
        string_length = len(string)
        return [string[i:i+max_length] for i in range(0, string_length, max_length)]

    def _print_bookmarks_chunk(self, bookmarks, title):
        id_offset = 0
        title_offset = 5
        url_offset = int(self.width * 0.45)
        title_max_length = url_offset - id_offset - title_offset
        url_max_length = self.width - url_offset - 5
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
            if bookmark.id is not None:
                self.write(f'<dim>{bookmark.id}', 0, id_offset)

                url = self._shorten_string(bookmark.url, url_max_length)
                self.write(url, -1, url_offset + 1)
                
                title = self._shorten_string(bookmark.title, title_max_length)
                self.write(title, -1, title_offset)

    def print_bookmarks(self, bookmarks, title="Bookmarks"):
        bookmarks_chunks = self._make_chunks(bookmarks)
        cursor = 1
        chunk_cursor = 0
        n_chunks = len(bookmarks_chunks)
        while chunk_cursor < n_chunks:
            bookmarks_chunk = bookmarks_chunks[chunk_cursor]
            prompt = f"\nShowing results {cursor} to {cursor + len(bookmarks_chunk) - 1}/{len(bookmarks)}"
            if n_chunks > 1:
                prompt += ' Navigate with arrow keys or'
            self._print_bookmarks_chunk(bookmarks_chunk, f"{title}:")

            user_input = self._wait_user_input(prompt)
            move_dir = self._do_input_action(user_input, chunk_cursor)
            if move_dir == "break":
                break

            if chunk_cursor < n_chunks and n_chunks > 1:
                cursor += move_dir * self.max_per_view
                chunk_cursor += move_dir
            if chunk_cursor >= n_chunks:
                chunk_cursor = n_chunks - 1
                cursor -= move_dir * self.max_per_view

    def _make_chunks(self, bookmarks):
        bookmarks_chunks = []
        prints = 0
        while prints < len(bookmarks):
            cursor = prints
            prints = prints + self.max_per_view
            bookmarks_chunks.append(bookmarks[cursor:prints])
        return bookmarks_chunks
    
    def _wait_user_input(self, prompt):
        user_input = ''
        while user_input not in ['n','r','q','b','enter','right','left','up','down']:
            user_input = self.read_chr(
                f"{prompt} [r]esume to return", 20000000
                )
        return user_input

    def _do_input_action(self, user_input, chunk_cursor):
        if user_input in ['r','q','b']:
            return "break"
        if user_input in ['right', 'n', 'down']:
            return 1
        if user_input in ['left', 'up'] and chunk_cursor > 0:
            return -1
        return 0
