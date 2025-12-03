# library_manager/inventory.py

import json
import logging
from pathlib import Path
from .book import Book


class LibraryInventory:
    def __init__(self, file_path="books.json"):
        self.file_path = Path(file_path)
        self.books = []
        self.load_from_file()

    def add_book(self, book: Book):
        self.books.append(book)
        logging.info(f"Book added: {book}")
        self.save_to_file()

    def search_by_title(self, title):
        title = title.lower()
        return [b for b in self.books if title in b.title.lower()]

    def search_by_isbn(self, isbn):
        for b in self.books:
            if b.isbn == isbn:
                return b
        return None

    def display_all(self):
        if not self.books:
            print("No books in inventory.")
        for b in self.books:
            print(b)

    def save_to_file(self):
        try:
            data = [b.to_dict() for b in self.books]
            with self.file_path.open("w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            logging.info("Books saved to file.")
        except Exception as e:
            logging.error(f"Error saving file: {e}")

    def load_from_file(self):
        if not self.file_path.exists():
            logging.info("No existing file. Starting with empty inventory.")
            self.books = []
            return

        try:
            with self.file_path.open("r", encoding="utf-8") as f:
                data = json.load(f)
            self.books = []
            for item in data:
                book = Book(
                    title=item.get("title", ""),
                    author=item.get("author", ""),
                    isbn=item.get("isbn", ""),
                    status=item.get("status", "available"),
                )
                self.books.append(book)
            logging.info("Books loaded from file.")
        except json.JSONDecodeError:
            logging.error("File is corrupted. Starting with empty inventory.")
            self.books = []
        except Exception as e:
            logging.error(f"Error loading file: {e}")
            self.books = []
