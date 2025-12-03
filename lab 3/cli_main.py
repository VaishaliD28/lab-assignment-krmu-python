# cli/main.py

import logging
from library_manager import Book, LibraryInventory

logging.basicConfig(
    filename="library.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def print_menu():
    print("\n===== Library Menu =====")
    print("1. Add Book")
    print("2. Issue Book")
    print("3. Return Book")
    print("4. View All Books")
    print("5. Search Book")
    print("6. Exit")

def get_inventory():
    return LibraryInventory("books.json")

def add_book_cli(inventory):
    try:
        title = input("Enter title: ").strip()
        author = input("Enter author: ").strip()
        isbn = input("Enter ISBN: ").strip()

        if not title or not author or not isbn:
            print("All fields are required.")
            return

        book = Book(title, author, isbn)
        inventory.add_book(book)
        print("Book added successfully.")
    except Exception as e:
        logging.error(f"Error adding book: {e}")
        print("Something went wrong while adding book.")

def issue_book_cli(inventory):
    isbn = input("Enter ISBN to issue: ").strip()
    try:
        book = inventory.search_by_isbn(isbn)
        if not book:
            print("Book not found.")
            return
        if book.issue():
            print("Book issued.")
            logging.info(f"Issued: {book}")
            inventory.save_to_file()
        else:
            print("Book is already issued.")
    except Exception as e:
        logging.error(f"Error issuing book: {e}")
        print("Error while issuing book.")

def return_book_cli(inventory):
    isbn = input("Enter ISBN to return: ").strip()
    try:
        book = inventory.search_by_isbn(isbn)
        if not book:
            print("Book not found.")
            return
        if book.return_book():
            print("Book returned.")
            logging.info(f"Returned: {book}")
            inventory.save_to_file()
        else:
            print("Book is already available.")
    except Exception as e:
        logging.error(f"Error returning book: {e}")
        print("Error while returning book.")

def search_book_cli(inventory):
    print("1. Search by Title")
    print("2. Search by ISBN")
    choice = input("Enter choice: ").strip()
    try:
        if choice == "1":
            title = input("Enter title: ")
            results = inventory.search_by_title(title)
            if not results:
                print("No books found.")
            else:
                for b in results:
                    print(b)
        elif choice == "2":
            isbn = input("Enter ISBN: ")
            book = inventory.search_by_isbn(isbn)
            if book:
                print(book)
            else:
                print("No book found.")
        else:
            print("Invalid choice.")
    except Exception as e:
        logging.error(f"Error searching book: {e}")
        print("Error while searching.")

def main():
    inventory = get_inventory()

    while True:
        print_menu()
        choice = input("Enter your choice: ").strip()

        try:
            if choice == "1":
                add_book_cli(inventory)
            elif choice == "2":
                issue_book_cli(inventory)
            elif choice == "3":
                return_book_cli(inventory)
            elif choice == "4":
                inventory.display_all()
            elif choice == "5":
                search_book_cli(inventory)
            elif choice == "6":
                print("Exiting... Goodbye!")
                break
            else:
                print("Invalid choice. Please enter 1–6.")
        except Exception as e:
            logging.error(f"Unexpected error in main loop: {e}")
            print("An unexpected error occurred.")

if __name__ == "__main__":
    main()
