from typing import Optional
from app.model import kindle_model


def validate_target(target: str, allowed_keys: list) -> dict:
    """Validate that the target is either None or one of the allowed keys."""
    if target is not None and target not in allowed_keys:
        return {
            "status": "failed",
            "reason": f"Invalid target. Allowed keys for searching are {', '.join(allowed_keys)}.",
        }
    return None


def list_books(library_path: str):
    library_instance = kindle_model.Library(library_path)
    return library_instance.list_books()


def find_book(key: str, value: str, library_path: str, target: Optional[str] = None):
    allowed_keys = [
        "pages",
        "year",
        "last_read_page",
        "percentage_read",
        "last_read_date",
        "author",
        "country",
        "imageLink",
        "language",
        "link",
        "title",
        "uuid",
    ]

    validation_error = validate_target(target, allowed_keys)
    if validation_error:
        return validation_error

    library_instance = kindle_model.Library(library_path)
    found = library_instance.find_books(**{key: value})

    if not found:
        return {"status": "failed", "reason": "No books found matching the criteria."}

    if target:
        return [book.get(target) for book in found]
    else:
        return found


def add_book_user(book_uuid: str, global_library_path: str, user_library_path: str):
    user_library_instance = kindle_model.Library(user_library_path)
    global_library_instance = kindle_model.Library(global_library_path)

    found_user = user_library_instance.find_books(uuid=book_uuid)
    if found_user:
        return {"status": "failed", "reason": "Book already exists in user's library."}

    found_global = global_library_instance.find_books(uuid=book_uuid)
    if not found_global:
        return {
            "status": "failed",
            "reason": "No book with the specified UUID exists in the global library.",
        }

    add_book = kindle_model.Book.from_json(found_global[0])
    user_library_instance.add_book(add_book)
    return {"status": "success", "book added": found_global}


def add_book_global(data: dict, global_library_path: str):
    global_library_instance = kindle_model.Library(global_library_path)
    new_book = kindle_model.Book.from_dict(data)
    global_library_instance.add_book(new_book)
    return {"status": "success", "book added": new_book.to_dict()}


def subtract_book_user(book_uuid: str, user_library_path: str):
    user_library_instance = kindle_model.Library(user_library_path)
    found_user = user_library_instance.find_books(uuid=book_uuid)

    if not found_user:
        return {"status": "failed", "reason": "Book not found in the user library."}

    user_library_instance.remove_book(book_uuid)
    return {
        "status": "success",
        "book removed": found_user,
        "remaining_books": user_library_instance.list_books(),
    }


def find_top_book_user(user_library_path: str, target: Optional[str] = None):
    allowed_keys = [
        "pages",
        "year",
        "last_read_page",
        "percentage_read",
        "last_read_date",
    ]

    validation_error = validate_target(target, allowed_keys)
    if validation_error:
        return validation_error

    user_library_instance = kindle_model.Library(user_library_path)
    books_user = user_library_instance.list_books()

    if not books_user:
        return {"status": "failed", "reason": "No books in user's library."}

    sorted_books = sorted(
        books_user, key=lambda book: book.get(target, float("-inf")), reverse=True
    )
    return {"status": "success", f"highest_value: {target}": sorted_books[0]}


def change_book_page_user(book_uuid: str, page_number: str, user_library_path: str):
    try:
        page_number = int(page_number)
    except ValueError:
        return {"status": "failed", "reason": "Page number must be an integer."}

    user_library_instance = kindle_model.Library(user_library_path)
    found_books = user_library_instance.find_books(uuid=book_uuid)

    if not found_books:
        return {
            "status": "failed",
            "reason": "No book with the specified UUID exists in user's library.",
        }

    total_pages = found_books[0].get("pages", None)
    if total_pages is not None and page_number > total_pages:
        return {
            "status": "failed",
            "reason": "Page number exceeds total pages of the book.",
        }

    user_library_instance.update_reading_status(book_uuid, page_number)
    updated_book = user_library_instance.find_books(uuid=book_uuid)

    return {"status": "success", "updated_book": updated_book}
