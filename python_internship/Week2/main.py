from book import Book
from member import Member
from library import Library

def main():
    library = Library()

    while True:
        print("\n===== Library Management System =====")
        print("1. Add Book")
        print("2. List Books")
        print("3. Update Book")
        print("4. Delete Book")
        print("5. Add Member")
        print("6. List Members")
        print("7. Update Member")
        print("8. Delete Member")
        print("9. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            title = input("Enter book title: ")
            author = input("Enter book author: ")
            isbn = input("Enter book ISBN: ")
            library.add_book(Book(title, author, isbn))

        elif choice == "2":
            library.list_books()

        elif choice == "3":
            isbn = input("Enter ISBN of the book to update: ")
            new_title = input("New Title (press Enter to skip): ")
            new_author = input("New Author (press Enter to skip): ")
            library.update_book(isbn, new_title or None, new_author or None)

        elif choice == "4":
            isbn = input("Enter ISBN of the book to delete: ")
            library.delete_book(isbn)

        elif choice == "5":
            name = input("Enter member name: ")
            member_id = input("Enter member ID: ")
            library.add_member(Member(name, member_id))

        elif choice == "6":
            library.list_members()

        elif choice == "7":
            member_id = input("Enter member ID to update: ")
            new_name = input("New Name (press Enter to skip): ")
            library.update_member(member_id, new_name or None)

        elif choice == "8":
            member_id = input("Enter member ID to delete: ")
            library.delete_member(member_id)

        elif choice == "9":
            print("Exiting Library Management System.")
            break

        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
