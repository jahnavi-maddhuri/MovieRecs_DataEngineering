import unittest
from app import app

from unittest.mock import patch, MagicMock
import pandas as pd
import os
from mylib.extract import extract

class FlaskAppTests(unittest.TestCase):

    def setUp(self):
        # Set up the test client
        self.app = app.test_client()
        self.app.testing = True

    def test_home_page(self):
        # Test the home page
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Movie Request Form', response.data)

    def test_movie_recommendations(self):
        # Test the movie recommendations
        response = self.app.post('/', data={
            'name': 'Test User',
            'genre': 'Drama',
            'mood': 'Relaxed'
        })
        self.assertEqual(response.status_code, 200)


class ExtractTests(unittest.TestCase):

    @patch('mylib.extract.requests.get')
    @patch('mylib.extract.os.getenv')
    def test_extract(self, mock_getenv, mock_get):
        # Mock the environment variable
        mock_getenv.return_value = 'fake_token'

        # Mock the API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "results": [
                {
                    "id": 1,
                    "title": "Test Movie",
                    "genre_ids": [28, 12]
                }
            ]
        }
        mock_get.return_value = mock_response

        # Call the extract function
        file_path = extract(file_path="test_movies.csv", directory="test_data")

        # Check if the file is created
        self.assertTrue(os.path.exists(file_path))

        # Read the CSV file and check its content
        movie_pd = pd.read_csv(file_path)
        self.assertEqual(len(movie_pd), 499)

        # Clean up
        os.remove(file_path)
        os.rmdir("test_data")

if __name__ == '__main__':
    unittest.main()

