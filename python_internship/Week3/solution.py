# Solution will be added here
from library import Library
def main():
    my_library = Library(["Python Basics", "Data Science", "Algorithms", "Machine Learning"])

    while True:
        print("\n=== Welcome to Library Management System ===")
        print("1. Display Books")
        print("2. Borrow Book")
        print("3. Return Book")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            my_library.display_books()
        elif choice == "2":
            book_name = input("Enter the book name you want to borrow: ")
            my_library.borrow_book(book_name)
        elif choice == "3":
            book_name = input("Enter the book name you want to return: ")
            my_library.return_book(book_name)
        elif choice == "4":
            print("Thank you for visiting the library!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
