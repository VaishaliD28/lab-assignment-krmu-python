# library_manager/book.py

class Book:
    def __init__(self, title, author, isbn, status="available"):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.status = status   # "available" or "issued"

    def __str__(self):
        return f"{self.title} by {self.author} (ISBN: {self.isbn}) - {self.status}"

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "status": self.status,
        }

    def is_available(self):
        return self.status == "available"

    def issue(self):
        if self.is_available():
            self.status = "issued"
            return True
        return False

    def return_book(self):
        if not self.is_available():
            self.status = "available"
            return True
        return False
