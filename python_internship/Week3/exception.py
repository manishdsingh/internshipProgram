 # Custom Exception for Book Not Available
class BookNotAvailableError(Exception):
    def __init__(self, book_name):
        super().__init__(f"Book '{book_name}' is not available right now!")
