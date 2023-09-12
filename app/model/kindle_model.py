import json
from datetime import datetime
from typing import Union, Dict, Optional, List
from uuid import uuid4


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
        uuid: Optional[str] = None,
        last_read_page: Optional[int] = 0,
        percentage_read: Optional[float] = 0.0,
        last_read_date: Optional[float] = None,
    ):
        self.author = author
        self.country = country
        self.imageLink = imageLink
        self.language = language
        self.link = link
        self.pages = pages
        self.title = title
        self.year = year
        self.uuid = uuid or str(uuid4())
        self.last_read_page = last_read_page
        self.percentage_read = percentage_read
        self.last_read_date = last_read_date

    @classmethod
    def from_json(cls, json_data: Union[str, Dict]) -> "Book":
        try:
            data = json.loads(json_data) if isinstance(json_data, str) else json_data
            return cls(**data)
        except (json.JSONDecodeError, KeyError) as e:
            raise ValueError(f"Invalid JSON data for creating a Book instance: {e}")

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    def to_dict(self) -> Dict[str, Union[str, int, float]]:
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

    def update_last_read_date(self) -> None:
        """Update the last read date."""
        self.last_read_date = datetime.now().timestamp()

    def update_last_read_page(self, last_read_page: int) -> None:
        """Update the last read page and calculate the reading percentage."""
        self.last_read_page = last_read_page
        self.percentage_read = (last_read_page / self.pages) * 100 if self.pages else 0


class Library:
    def __init__(self, data_file: str):
        self.data_file = data_file
        self.books = self.load_library()

    def load_library(self) -> List[Book]:
        try:
            with open(self.data_file, "r") as f:
                data = json.load(f)
            return [Book.from_json(book) for book in data]
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def save_library(self) -> None:
        with open(self.data_file, "w") as f:
            json.dump([book.to_dict() for book in self.books], f, indent=4)

    def add_book(self, book: Book) -> None:
        self.books.append(book)
        self.save_library()

    def remove_book(self, uuid: str) -> None:
        self.books = [book for book in self.books if book.uuid != uuid]
        self.save_library()

    def list_books(self) -> List[Dict]:
        return [book.to_dict() for book in self.books]

    def find_books(self, **kwargs) -> List[Dict]:
        found_books = []
        for book in self.books:
            if all(getattr(book, key, None) == value for key, value in kwargs.items()):
                found_books.append(book.to_dict())
        return found_books

    def update_reading_status(self, uuid: str, last_read_page: int) -> None:
        for book in self.books:
            if book.uuid == uuid:
                book.update_last_read_date()
                book.update_last_read_page(int(last_read_page))
                self.save_library()
                break
