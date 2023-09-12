## Kindle Backend API Documentation

This API is designed for managing books in a Kindle application. The API allows users to interact with both a global library and a user-specific library.

### Base URL:

Local Server:
http://localhost:5000/

### Endpoints:

#### Keys:

```
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
"uuid"
```

#### 1. Get all books from the User Library:

- **URL**: `/user/books`
- **Method**: `GET`
- **Description**: Retrieves all books from the user library.

#### 2. Get all books from the Global Library:

- **URL**: `/global/books`
- **Method**: `GET`
- **Description**: Retrieves all books from the global library.

#### 3. Search for a book in the Global Library:

- **URL**: `/global/books/search/<key>/<value>` or `/global/books/search/<key>/<value>/<target>`
- **Method**: `GET`
- **Parameters**:
  - `key`: The field by which to search (e.g., "title", "author").
  - `value`: The value to search for in the specified key.
  - `target` (Optional): Specific attribute of the book to retrieve (e.g., "title", "author").
- **Description**: Retrieves a book from the global library based on the provided key-value pair. If a target is provided, only that attribute of the book will be returned.

#### 4. Search for a book in the User Library:

- **URL**: `/user/books/search/<key>/<value>` or `/user/books/search/<key>/<value>/<target>`
- **Method**: `GET`
- **Parameters**:
  - `key`: The field by which to search (e.g., "title", "author").
  - `value`: The value to search for in the specified key.
  - `target` (Optional): Specific attribute of the book to retrieve (e.g., "title", "author").
- **Description**: Retrieves a book from the user's library based on the provided key-value pair. If a target is provided, only that attribute of the book will be returned.

#### 5. Add a book to the User Library:

- **URL**: `/user/books/<uuid>`
- **Method**: `PUT`
- **Parameters**:
  - `uuid`: Unique identifier of the book.
- **Description**: Adds a book from the global library to the user's library using the provided UUID.

#### 6. Add a book to the Global Library:

- **URL**: `/global/books`
- **Method**: `PUT`
- **Parameters**:
  - `data` (Request Body): JSON object containing book details.

```
{
  "author": "Leo Tolstoy",
  "country": "Russia",
  "imageLink": "images/anna-karenina.jpg",
  "language": "Russian",
  "link": "https://en.wikipedia.org/wiki/Anna_Karenina\n",
  "pages": 864,
  "title": "Anna Karenina",
  "year": 1877,
  "last_read_page": 0,
  "percentage_read": 0.0,
  "last_read_date": 0.0
}
```

- **Description**: Adds a new book to the global library.

#### 7. Remove a book from the User Library:

- **URL**: `/user/books/<uuid>`
- **Method**: `DELETE`
- **Parameters**:
  - `uuid`: Unique identifier of the book.
- **Description**: Removes a book from the user's library.

#### 8. Get the highest value of the specified target from the User Library:

- **URL**: `/user/books/top/<target>`
- **Method**: `GET`
- **Parameters**:
  - `target` (Optional): Specific attribute of the book to retrieve (e.g., "title", "author").
- **Description**: Retrieves the target with the highest value from the user's library. If a target is provided, only that attribute of the book will be returned.

#### 9. Update the last read page of a book in the User Library:

- **URL**: `/user/books/<uuid>/page/<page_number>`
- **Method**: `POST`
- **Parameters**:
  - `uuid`: Unique identifier of the book.
  - `page_number`: The page number to update.
- **Description**: Updates the last read page number for a specific book in the user's library.

#### 10. Get the last read book from the User Library:

- **URL**: `/user/books/last_read`
- **Method**: `GET`
- **Description**: Gets the last read book in the user's library.
