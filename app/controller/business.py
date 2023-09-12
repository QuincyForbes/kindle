from typing import Optional, Dict, List, Union
from app.model import kindle_model


# Global allowed keys for searching
ALLOWED_KEYS = [
    "pages",
    "year",
    "title",
    "author",
    "uuid",
    "reading_status",
    "genre",
    "last_read_date",
]


class BookNotFoundError(Exception):
    """Raised when a book is not found."""

    pass


class ValidationError(Exception):
    """Raised when there's a validation error."""

    pass


def validate_target(target: Optional[str]) -> None:
    """Validate that the target is either None or one of the allowed keys."""
    if target is not None and target not in ALLOWED_KEYS:
        raise ValidationError(
            f"Invalid target. Allowed keys for searching are {', '.join(ALLOWED_KEYS)}."
        )


def list_books(library_path: str) -> List[Dict[str, Union[str, int]]]:
    library_instance = kindle_model.Library(library_path)
    return library_instance.list_books()


def find_book(
    key: str, value: str, library_path: str, target: Optional[str] = None
) -> List[Dict[str, Union[str, int]]]:
    validate_target(target)
    library_instance = kindle_model.Library(library_path)
    found = library_instance.find_books(**{key: value})
    if not found:
        raise BookNotFoundError("No books found matching the criteria.")
    if target:
        return [{target: book[target]} for book in found]
    return found


def add_book_user(
    book_uuid: str, global_library_path: str, user_library_path: str
) -> Dict[str, Union[str, Dict[str, Union[str, int]]]]:
    user_library_instance = kindle_model.Library(user_library_path)
    global_library_instance = kindle_model.Library(global_library_path)
    found_user = user_library_instance.find_books(uuid=book_uuid)
    if found_user:
        raise ValidationError("Book already exists in user's library.")
    found_global = global_library_instance.find_books(uuid=book_uuid)
    if not found_global:
        raise BookNotFoundError("Book not found in the global library.")
    book_to_add = kindle_model.Book.from_json(found_global[0])
    user_library_instance.add_book(book_to_add)
    return {"status": "success", "book added": book_to_add.to_dict()}


def add_book_global(
    data: Dict[str, Union[str, int]], global_library_path: str
) -> Dict[str, Union[str, Dict[str, Union[str, int]]]]:
    global_library_instance = kindle_model.Library(global_library_path)
    new_book = kindle_model.Book(**data)
    global_library_instance.add_book(new_book)
    return {"status": "success", "book added": new_book.to_dict()}


def subtract_book_user(
    book_uuid: str, user_library_path: str
) -> Dict[str, Union[str, int]]:
    user_library_instance = kindle_model.Library(user_library_path)
    found_user = user_library_instance.find_books(uuid=book_uuid)
    if not found_user:
        raise BookNotFoundError("Book not found in the user library.")
    user_library_instance.remove_book(book_uuid)
    return {"status": "success", "book removed": book_uuid}


def find_top_book_user(
    user_library_path: str, target: Optional[str] = None
) -> Dict[str, Union[str, Dict[str, Union[str, int]]]]:
    validate_target(target)
    user_library_instance = kindle_model.Library(user_library_path)
    books_user = user_library_instance.list_books()
    if not books_user:
        raise BookNotFoundError("No books in user's library.")
    top_book = max(books_user, key=lambda book: book.get(target, float("-inf")))
    return {"status": "success", f"highest_value: {target}": top_book}


def change_book_page_user(
    book_uuid: str, page_number: str, user_library_path: str
) -> Dict[str, str]:
    try:
        page_number = int(page_number)
    except ValueError:
        raise ValidationError("Page number must be an integer.")
    user_library_instance = kindle_model.Library(user_library_path)
    found_books = user_library_instance.find_books(uuid=book_uuid)
    if not found_books:
        raise BookNotFoundError(
            "No book with the specified UUID exists in user's library."
        )
    total_pages = found_books[0].get("pages", None)
    if total_pages is not None and page_number > total_pages:
        raise ValidationError("Page number exceeds total pages of the book.")
    user_library_instance.update_reading_status(book_uuid, page_number)
    return {"status": "success", "book updated": book_uuid}
