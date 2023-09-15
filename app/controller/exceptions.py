class BookNotFoundError(Exception):
    """Raised when a book is not found."""

    pass


class ValidationError(Exception):
    """Raised when there's a validation error."""

    pass


class ValueError(Exception):
    """Raised when there's a validation error."""

    pass


class BookRemovalError(Exception):
    """Raised when a book removal operation fails."""

    pass


class UpdateError(Exception):
    """Raised when a books data update operation fails."""

    pass
