import logging
from exception import BookNotAvailableError

# Logging configuration
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class Library:
    def __init__(self, books):
        self.books = books  # list of available books

    def display_books(self):
        logging.info("Displaying all available books.")
        print("Available books:")
        for book in self.books:
            print(f"- {book}")

    def borrow_book(self, book_name):
        try:
            if book_name in self.books:
                self.books.remove(book_name)
                logging.info(f"Book borrowed: {book_name}")
                print(f"You have borrowed '{book_name}'. Enjoy reading!")
            else:
                raise BookNotAvailableError(book_name)
        except BookNotAvailableError as e:
            logging.error(e)
            print(e)

    def return_book(self, book_name):
        self.books.append(book_name)
        logging.info(f"Book returned: {book_name}")
        print(f"Thank you for returning '{book_name}'")
