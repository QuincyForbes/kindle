import json
from datetime import datetime
from uuid import uuid4
from typing import Optional


class Book:
    def __init__(
        self,
        author: str,
        country: str,
        imageLink: str,
        language: str,
        link: str,
        pages: int,
        title: str,
        year: int,
        last_read_page: int,
        percentage_read: float,
        last_read_date: float,
        uuid: Optional[str] = None,
    ):
        """
        Initializes a Book instance with given details.

        Args:
            author (str): Author of the book.
            country (str): Country where the book was published.
            imageLink (str): Link to the book's cover image.
            language (str): Language of the book.
            link (str): Link to further details about the book.
            pages (int): Total number of pages in the book.
            title (str): Title of the book.
            year (int): Year when the book was published.
            last_read_page (int): Last page read by the user.
            percentage_read (float): Percentage of the book read by the user.
            last_read_date (float): Timestamp of the last time user read the book.
            uuid (Optional[str]): Unique identifier for the book. Defaults to None if not provided.
        """
        self.author = author
        self.country = country
        self.imageLink = imageLink
        self.language = language
        self.link = link
        self.pages = pages
        self.title = title
        self.year = year
        self.last_read_page = last_read_page
        self.percentage_read = percentage_read
        self.last_read_date = last_read_date
        self.uuid = uuid or str(uuid4())

    @classmethod
    def from_json(cls, json_data: dict) -> "Book":
        """
        Creates a Book instance from JSON data.

        Args:
            json_data (dict): Dictionary containing book details.

        Returns:
            Book: An instance of the Book class.
        """
        try:
            data = json.loads(json_data) if isinstance(json_data, str) else json_data
            return cls(**data)
        except (json.JSONDecodeError, KeyError) as e:
            raise ValueError(f"Invalid JSON data for creating a Book instance: {e}")

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    def to_dict(self) -> dict:
        return {
            "author": self.author,
            "country": self.country,
            "imageLink": self.imageLink,
            "language": self.language,
            "link": self.link,
            "pages": self.pages,
            "title": self.title,
            "year": self.year,
            "uuid": self.uuid,
            "last_read_page": self.last_read_page,
            "percentage_read": self.percentage_read,
            "last_read_date": self.last_read_date,
        }

    def update_last_read_date(self):
        """Update the last read date."""
        self.last_read_date = datetime.now().timestamp()

    def update_last_read_page(self, last_read_page: int):
        """Update the last read page and calculate the reading percentage."""
        self.last_read_page = last_read_page
        self.percentage_read = (last_read_page / self.pages) * 100 if self.pages else 0


class Library:
    """
    Represents a library of books with functionality to manage the collection.
    """

    def __init__(self, data_file: str):
        self.data_file = data_file
        self.books = self.load_library()
        """
        Initializes the Library instance with the given data file.

        Args:
            data_file (str): Path to the JSON data file containing the library data.
        """

    def load_library(self) -> list[Book]:
        """
        Loads books from the provided data file into the library.

        Returns:
            list[Book]: A list of Book instances loaded from the data file.
        """
        try:
            with open(self.data_file, "r") as f:
                data = json.load(f)
            return [Book.from_json(book) for book in data]
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def save_library(self) -> None:
        """
        Saves the current state of the library into the data file in JSON format.
        """
        with open(self.data_file, "w") as f:
            json.dump([book.to_dict() for book in self.books], f, indent=4)

    def add_book(self, book: Book) -> None:
        """
        Adds a book to the library based on its UUID and updates the library.

        Args:
            uuid (str): Unique identifier of the book to be added.
        """
        self.books.append(book)
        self.save_library()

    def remove_book(self, uuid: str) -> None:
        """
        Removes a book from the library based on its UUID and updates the library.

        Args:
            uuid (str): Unique identifier of the book to be added.
        """
        self.books = [book for book in self.books if book.uuid != uuid]
        self.save_library()

    def list_books(self) -> list[dict]:
        """
             Lists all the books present in the library.

        Returns:
            list[dict]: A list of dictionaries with each dictionary representing a book.
        """
        return [book.to_dict() for book in self.books]

    def find_books(self, **kwargs) -> list[dict]:
        """
        Searches for books in the library based on provided criteria.

        Args:
            **kwargs: Key-value pairs representing book attributes and their desired values.

        Returns:
            list[dict]: A list of dictionaries representing the books that match the criteria.
        """

        found_books = []
        for book in self.books:
            matches = True
            for key, value in kwargs.items():
                book_attr = getattr(book, key, None)
                if key == "uuid":  ## Disabled partial search for uuid.
                    if book_attr != value:
                        matches = False
                        break
                else:
                    if book_attr is None or value not in str(book_attr):
                        matches = False
                        break
            if matches:
                found_books.append(book.to_dict())
        return found_books

    def update_reading_status(self, uuid: str, last_read_page: int) -> None:
        """
            Updates the reading status of a book in the library.

        Args:
            uuid (str): Unique identifier of the book.
            last_read_page (int): The latest page read by the user for that book.
        """
        for book in self.books:
            if book.uuid == uuid:
                book.update_last_read_date()
                book.update_last_read_page(int(last_read_page))
                self.save_library()
                break
