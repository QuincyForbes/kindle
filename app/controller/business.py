from app.model import kindle_model
from app.controller.exceptions import (
    ValidationError,
    BookNotFoundError,
    ValueError,
    BookRemovalError,
    UpdateError,
)


ALLOWED_KEYS = [
    "pages",
    "year",
    "title",
    "author",
    "uuid",
    "genre",
    "last_read_date",
    "language",
]

REQUIRED_KEYS = [
    "author",
    "country",
    "imageLink",
    "language",
    "link",
    "pages",
    "title",
    "year",
    "last_read_page",
    "percentage_read",
    "last_read_date",
]


def validate_keys(target) -> None:
    """
    Validate the given target to ensure it's an allowed key for searching.

    Args:
        target (str): Key to validate.

    Raises:
        ValidationError: If the target is not in the ALLOWED_KEYS.
    """
    if target is not None and target not in ALLOWED_KEYS:
        raise ValidationError(
            f"Invalid target. Allowed keys for searching are {', '.join(ALLOWED_KEYS)}."
        )


def validate_json(json_data) -> None:
    """
    Validate a given JSON data to ensure it contains the required keys.

    Args:
        json_data (dict): JSON data to validate.

    Raises:
        ValidationError: If the json_data is missing required keys or has extra ones.
    """
    if not json_data:
        raise ValidationError("JSON data is None.")

    json_keys = set(json_data.keys())
    required_keys_set = set(REQUIRED_KEYS)

    if json_keys != required_keys_set:
        missing_keys = required_keys_set - json_keys
        extra_keys = json_keys - required_keys_set

        error_messages = []

        if missing_keys:
            error_messages.append(f"Missing keys: {', '.join(missing_keys)}")

        if extra_keys:
            error_messages.append(f"Extra keys: {', '.join(extra_keys)}")

        raise ValidationError(f"Invalid JSON. {' '.join(error_messages)}")


def list_books(library_path: str) -> dict:
    """
    Find a book in a library based on a given key and value.

    Args:
        key (str): Key to search by.
        value (str): Value of the key to match.
        library_path (str): Path to the library's data file.
        target (str, optional): Target attribute. Defaults to None.

    Returns:
        dict: Dictionary containing the status and the found book details.

    Raises:
        ValidationError: If the key or target is not valid.
        BookNotFoundError: If no books match the criteria.
    """
    ...
    library_instance = kindle_model.Library(library_path)
    return {"status": "success", "Books": library_instance.list_books()}


def find_book(key: str, value: str, library_path: str, target=None) -> dict:
    """
    Find a book in a library based on a given key and value.

    Args:
        key (str): Key to search by.
        value (str): Value of the key to match.
        library_path (str): Path to the library's data file.
        target (str, optional): Target attribute. Defaults to None.

    Returns:
        dict: Dictionary containing the status and the found book details.

    Raises:
        ValidationError: If the key or target is not valid.
        BookNotFoundError: If no books match the criteria.
    """

    validate_keys(target)
    validate_keys(key)

    library_instance = kindle_model.Library(library_path)
    found = library_instance.find_books(**{key: value})
    if not found:
        raise BookNotFoundError("No books found matching the criteria.")

    if target:
        return {target: book[target] for book in found if target in book}

    return {"status": "success", "book found": found}


def add_book_user(
    book_uuid: str, global_library_path: str, user_library_path: str
) -> dict:
    """
    Add a book to a user's library from the global library using a given UUID.

    Args:
        book_uuid (str): UUID of the book to add.
        global_library_path (str): Path to the global library's data file.
        user_library_path (str): Path to the user's library data file.

    Returns:
        dict: Dictionary containing the status and details of the added book.

    Raises:
        ValidationError: If the book is already in the user's library.
        BookNotFoundError: If the book isn't found in the global library.
    """
    user_library_instance = kindle_model.Library(user_library_path)
    global_library_instance = kindle_model.Library(global_library_path)
    found_user = user_library_instance.find_books(uuid=book_uuid)
    if found_user:
        raise ValidationError("Book already exists in the user's library.")
    found_global = global_library_instance.find_books(uuid=book_uuid)
    if not found_global:
        raise BookNotFoundError("Book not found in the global library.")
    book_to_add = kindle_model.Book.from_json(found_global[0])
    user_library_instance.add_book(book_to_add)
    return {"status": "success", "book added": book_to_add.to_dict()}


def add_book_global(json: dict, global_library_path: str) -> dict:
    """
    Add a book to a user's library from the global library using a given UUID.

    Args:
        global_library_path (str): Path to the global library's data file.

    Returns:
        dict: Dictionary containing the status and details of the added book.

    Raises:
        ValidationError: If the book is already in the user's library.
        BookNotFoundError: If the book isn't found in the global library.
    """
    validate_json(json)
    try:
        global_library_instance = kindle_model.Library(global_library_path)
        new_book = kindle_model.Book(**json)
        global_library_instance.add_book(new_book)

        return {"status": "success", "book added": new_book.to_dict()}

    except ValidationError as ve:
        return {"status": "error", "message": str(ve)}

    except BookNotFoundError as bnfe:
        return {"status": "error", "message": str(bnfe)}


def subtract_book_user(book_uuid: str, user_library_path: str) -> dict:
    """
    Remove a book from a user's library based on a given UUID.

    Args:
        book_uuid (str): UUID of the book to remove.
        user_library_path (str): Path to the user's library data file.

    Returns:
        dict: Dictionary containing the status and details of the removed book.

    Raises:
        BookNotFoundError: If the book isn't found in the user's library.
        BookRemovalError: If there's an issue removing the book.
    """
    user_library_instance = kindle_model.Library(user_library_path)
    book = user_library_instance.find_books(uuid=book_uuid)

    if not book:
        raise BookNotFoundError("Book not found in the user library.")

    try:
        user_library_instance.remove_book(book_uuid)
    except Exception as e:  # Catch all exceptions from remove_book method.
        raise BookRemovalError(
            f"Failed to remove book with UUID {book_uuid}. Error: {str(e)}"
        )

    return {"status": "success", "book removed": book}


def find_top_book_user(user_library_path: str, target: str) -> dict:
    """
    Remove a book from a user's library based on a given UUID.

    Args:
        user_library_path (str): Path to the user's library data file.

    Returns:
        dict: Dictionary containing the status and details of the removed book.

    Raises:
        BookNotFoundError: If the book isn't found in the user's library.
        BookRemovalError: If there's an issue removing the book.
    """
    validate_keys(target)
    user_library_instance = kindle_model.Library(user_library_path)
    books_user = user_library_instance.list_books()

    if not books_user:
        raise BookNotFoundError("No books in the user's library.")

    # Ensure at least one book has the target attribute.
    if not any(target in book for book in books_user):
        raise ValidationError(
            f"No books with the attribute: {target} found in the user's library."
        )

    try:
        top_book = max(books_user, key=lambda book: book.get(target, float("-inf")))
    except ValueError:
        raise ValidationError(
            f"Error finding the top book based on the attribute: {target}."
        )

    return {"status": "success", f"Highest Value {target}": top_book}


def change_book_page_user(
    book_uuid: str, page_number: int, user_library_path: str
) -> dict:
    """
    Remove a book from a user's library based on a given UUID.

    Args:
        book_uuid (str): UUID of the book to remove.
        user_library_path (str): Path to the user's library data file.

    Returns:
        dict: Dictionary containing the status and details of the removed book.

    Raises:
        BookNotFoundError: If the book isn't found in the user's library.
        BookRemovalError: If there's an issue removing the book.
    """
    try:
        page_number = int(page_number)
        if page_number <= 0:
            raise ValidationError("Page number must be a positive integer.")
    except ValueError:
        raise ValidationError("Page number must be an integer.")

    user_library_instance = kindle_model.Library(user_library_path)
    books = user_library_instance.find_books(uuid=book_uuid)

    if not books:
        raise BookNotFoundError(
            "No book with the specified UUID exists in the user's library."
        )

    book = books[0]
    if "pages" not in book:
        raise ValidationError("The book does not have a 'pages' attribute.")

    total_pages = book["pages"]
    if total_pages is not None and page_number > total_pages:
        raise ValidationError("Page number exceeds total pages of the book.")

    user_library_instance.update_reading_status(book_uuid, page_number)

    updated_books = user_library_instance.find_books(uuid=book_uuid)
    updated_book = updated_books[0]

    if updated_book["last_read_page"] != page_number:
        raise UpdateError(f"Page update for book:{book_uuid} failed.")
    return {"status": "success", "book updated": books}
