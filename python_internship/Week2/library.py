from book import Book
from member import Member

class Library:
    def __init__(self):
        self.books = []    # List to store Book objects
        self.members = []  # List to store Member objects

    # ----- Book Operations -----
    def add_book(self, book):
        if isinstance(book, Book):
            self.books.append(book)
            print(f"Book '{book.title}' added successfully.")
        else:
            print("Invalid Book object.")

    def list_books(self):
        if not self.books:
            print("No books in library.")
        else:
            print("\nBooks in Library:")
            for book in self.books:
                book.display_info()

    def update_book(self, isbn, new_title=None, new_author=None):
        for book in self.books:
            if book.isbn == isbn:
                if new_title: book.title = new_title
                if new_author: book.author = new_author
                print(f"Book '{isbn}' updated successfully.")
                return
        print("Book not found.")

    def delete_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                self.books.remove(book)
                print(f"Book '{isbn}' deleted successfully.")
                return
        print("Book not found.")

    # ----- Member Operations -----
    def add_member(self, member):
        if isinstance(member, Member):
            self.members.append(member)
            print(f"Member '{member.name}' added successfully.")
        else:
            print("Invalid Member object.")

    def list_members(self):
        if not self.members:
            print("No members in library.")
        else:
            print("\nLibrary Members:")
            for member in self.members:
                member.display_info()

    def update_member(self, member_id, new_name=None):
        for member in self.members:
            if member.member_id == member_id:
                if new_name: member.name = new_name
                print(f"Member '{member_id}' updated successfully.")
                return
        print("Member not found.")

    def delete_member(self, member_id):
        for member in self.members:
            if member.member_id == member_id:
                self.members.remove(member)
                print(f"Member '{member_id}' deleted successfully.")
                return
        print("Member not found.")
