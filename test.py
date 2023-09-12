import unittest
from flask import Flask, json
from app.routes import routes
from app.controller.business import BookNotFoundError


class BookRoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        routes.register_routes(self.app)
        self.client = self.app.test_client()

    def extract_data(self, response):
        return json.loads(response.data)["data"]

    def test_get_all_books_user_success(self):
        response = self.client.get("/user/books")
        self.assertEqual(response.status_code, 200)
        data = self.extract_data(response)
        self.assertIsInstance(data, list)

    def test_get_all_books_global_success(self):
        response = self.client.get("/global/books")
        self.assertEqual(response.status_code, 200)
        data = self.extract_data(response)
        self.assertIsInstance(data, list)

    def test_search_book_global_success(self):
        response = self.client.get("/global/books/search/title/Oedipus the King")
        self.assertEqual(response.status_code, 200)
        data = self.extract_data(response)
        self.assertIsInstance(data, list)

    def test_search_book_user_success(self):
        response = self.client.get("/user/books/search/title/Oedipus the King")
        self.assertEqual(response.status_code, 200)
        data = self.extract_data(response)
        self.assertIsInstance(data, list)

    def test_add_book_to_global_library_success(self):
        mock_data = {
            "author": "Test",
            "country": "Test",
            "imageLink": "Test",
            "language": "Test",
            "link": "https://en.wikipedia.org/wiki/Anna_Karenina\n",
            "pages": 864,
            "title": "Anna Karenina",
            "year": 1877,
            "last_read_page": 0,
            "percentage_read": 0.0,
            "last_read_date": 0.0,
        }
        response = self.client.post("/global/books", json=mock_data)
        self.assertEqual(response.status_code, 200)
        data = self.extract_data(response)
        self.assertEqual(data["status"], "success")

    def test_search_book_global_with_target_success(self):
        response = self.client.get("/global/books/search/title/Oedipus the King/author")
        self.assertEqual(response.status_code, 200)
        data = self.extract_data(response)
        self.assertIn("author", data[0])

    def test_search_book_user_with_target_success(self):
        response = self.client.get("/user/books/search/title/Oedipus the King/author")
        self.assertEqual(response.status_code, 200)
        data = self.extract_data(response)
        self.assertIn("author", data[0])

    def test_get_top_user_book_success(self):
        response = self.client.get("/user/books/top/last_read_date")
        self.assertEqual(response.status_code, 200)
        data = self.extract_data(response)
        self.assertIsInstance(data, dict)

    def test_get_last_user_book_success(self):
        response = self.client.get("/user/books/last-read")
        self.assertEqual(response.status_code, 200)
        data = self.extract_data(response)
        self.assertIsInstance(data, dict)


if __name__ == "__main__":
    unittest.main()
