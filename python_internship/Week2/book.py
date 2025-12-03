class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn

    def display_info(self):
        """Polymorphism: same method name can be used for different objects"""
        print(f"Book -> Title: {self.title}, Author: {self.author}, ISBN: {self.isbn}")
