from typing import Any, Optional
from flask import Blueprint, request, jsonify
from app.controller.business import (
    find_book,
    add_book_user,
    subtract_book_user,
    find_top_book_user,
    change_book_page_user,
    add_book_global,
    list_books,
)
from app.controller.exceptions import (
    ValidationError,
    BookNotFoundError,
    ValueError,
    UpdateError,
)


global_json = "data.json"
user_json = "user_library/user_library.json"

book_routes = Blueprint("book_routes", __name__)


def register_routes(app: Any) -> None:
    """
    Register the book-related routes with the main Flask app.

    Args:
        app (Any): The Flask app instance.
    """

    app.register_blueprint(book_routes)


def format_response(data: dict, status: int = 200) -> tuple[dict[str, str], int]:
    """
    Utility function to consistently format API responses.

    Args:
        data (Union[List[Dict[str, Any]], Dict[str, Any]]): The data to be returned in the response.
        status (int, optional): HTTP status code. Defaults to 200.

    Returns:
        Any: JSON formatted response.
    """
    return jsonify({"data": data, "status": status})


@book_routes.route("/user/books", methods=["GET"])
def get_all_books_user() -> tuple[dict[str, str], int]:
    """
    Retrieve all books from the user library.

    Returns:
        Any: JSON formatted list of books or error message.
    """
    try:
        books = list_books(user_json)
        return format_response(books)
    except BookNotFoundError as bnf:
        return {"error": str(bnf)}, 404


@book_routes.route("/global/books", methods=["GET"])
def get_all_books_global() -> tuple[dict[str, str], int]:
    """
    Retrieve all books from the global library.

    Returns:
        Any: JSON formatted list of books or error message.
    """
    try:
        books = list_books(global_json)
        return format_response(books)
    except BookNotFoundError as bnf:
        return {"error": str(bnf)}, 404


@book_routes.route(
    "/global/books/search/<key>/<value>", defaults={"target": None}, methods=["GET"]
)
@book_routes.route("/global/books/search/<key>/<value>/<target>", methods=["GET"])
def search_book_global(
    key: str, value: str, target: Optional[str] = None
) -> tuple[dict[str, str], int]:
    """
    Search for books in the global library based on a key-value pair with an optional target.

    Args:
        key (str): Attribute to search by (e.g., "author", "title").
        value (str): Value of the attribute to search for.
        target (Optional[str], optional): Additional filtering target. Defaults to None.

    Returns:
        Any: JSON formatted list of books or error message.
    """
    try:
        books = find_book(key, value, global_json, target=target)
        return format_response(books)
    except ValidationError as ve:
        return {"error": str(ve)}, 400
    except BookNotFoundError as bnf:
        return {"error": str(bnf)}, 404


@book_routes.route(
    "/user/books/search/<key>/<value>", defaults={"target": None}, methods=["GET"]
)
@book_routes.route("/user/books/search/<key>/<value>/<target>", methods=["GET"])
def search_book_user(
    key: str, value: str, target: Optional[str] = None
) -> tuple[dict[str, str], int]:
    """
    Search for books in the user library based on a key-value pair with an optional target.

    Args:
        key (str): Attribute to search by (e.g., "author", "title").
        value (str): Value of the attribute to search for.
        target (Optional[str], optional): Additional filtering target. Defaults to None.

    Returns:
        Any: JSON formatted list of books or error message.
    """
    try:
        books = find_book(key, value, global_json, target=target)
        return format_response(books)
    except ValidationError as ve:
        return {"error": str(ve)}, 400
    except BookNotFoundError as bnf:
        return {"error": str(bnf)}, 404


@book_routes.route("/user/books/<uuid>", methods=["POST"])
def add_book_to_user_library(uuid: str) -> tuple[dict[str, str], int]:
    """
    Add a book to the user library using its UUID.

    Args:
        uuid (str): The unique identifier for the book.

    Returns:
        Any: JSON formatted success message or error message.
    """
    try:
        response = add_book_user(uuid, global_json, user_json)
        return format_response(response)
    except ValidationError as ve:
        return {"error": str(ve)}, 400
    except BookNotFoundError as bnf:
        return {"error": str(bnf)}, 404


@book_routes.route("/global/books", methods=["POST"])
def add_book_to_global_library() -> tuple[dict[str, str], int]:
    """
    Remove a specific book from the user library using its UUID.

    Args:
        uuid (str): The unique identifier for the book.

    Returns:
        Any: JSON formatted success message or error message.
    """
    try:
        json = request.get_json()
        response = add_book_global(json, global_json)
        return format_response(response)
    except ValidationError as ve:
        return {"error": str(ve)}, 400
    except BookNotFoundError as bnf:
        return {"error": str(bnf)}, 404


@book_routes.route("/user/books/<uuid>", methods=["DELETE"])
def remove_book_from_user_library(uuid: str) -> tuple[dict[str, str], int]:
    """
    Remove a specific book from the user library using its UUID.

    Args:
        uuid (str): The unique identifier for the book to be removed.

    Returns:
        Any: JSON formatted response indicating removal success or an error message.
    """
    try:
        response = subtract_book_user(uuid, user_json)
        return format_response(response)
    except ValidationError as ve:
        return {"error": str(ve)}, 400
    except BookNotFoundError as bnf:
        return {"error": str(bnf)}, 404


@book_routes.route("/user/books/top/<target>", methods=["GET"])
def get_top_user_book(target: str) -> tuple[dict[str, str], int]:
    """
    Retrieve the top book in the user library based on a specific attribute.

    Args:
        target (str): Attribute to determine the "top" book (e.g., "rating").

    Returns:
        Any: JSON formatted book details or error message.
    """
    try:
        book = find_top_book_user(user_json, target=target)
        return format_response(book)
    except ValidationError as ve:
        return {"error": str(ve)}, 400
    except BookNotFoundError as bnf:
        return {"error": str(bnf)}, 404


# Endpoint to get the last book read by the user.
@book_routes.route("/user/books/last-read", methods=["GET"])
def get_last_user_book() -> tuple[dict[str, str], int]:
    """
    Retrieve the last book read by the user based on the 'last_read_date' attribute.

    Returns:
        Any: JSON formatted book details or error message.
    """
    try:
        book = find_top_book_user(user_json, "last_read_date")
        return format_response(book)
    except ValidationError as ve:
        return {"error": str(ve)}, 400
    except BookNotFoundError as bnf:
        return {"error": str(bnf)}, 404


# Endpoint to update the reading status of a book in the user library.
@book_routes.route("/user/books/<uuid>/page/<page_number>", methods=["PATCH"])
def update_book_page_for_user(
    uuid: str, page_number: int
) -> tuple[dict[str, str], int]:
    """
    Retrieve the last book read by the user based on the 'last_read_date' attribute.

    Returns:
        Any: JSON formatted book details or error message.
    """
    try:
        page_number = int(page_number)
        response = change_book_page_user(uuid, page_number, user_json)
        return format_response(response)
    except ValidationError as ve:
        return {"error": str(ve)}, 400
    except BookNotFoundError as bnf:
        return {"error": str(bnf)}, 404
    except ValueError as vee:
        return {"error": str(vee)}, 400
    except UpdateError as ue:
        return {"error": str(ue)}, 400
