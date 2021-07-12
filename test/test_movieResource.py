import unittest

from setup_test_app import app


# TestMovieResource
class TM(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_get_all(self):
        response = self.client.get('/api/movies')
        self.assertEqual(response.status_code, 200)

    def test_add_movie(self):
        movie_json = {
            "99popularity": 50.0,
            "director": "Abhishek D",
            "genre": ["Manual", "Automation"],
            "imdbScore": 5.0,
            "name": "Test Movie"
        }

        response = self.client.post('/api/movie', json=movie_json)
        self.assertEqual(200, response.status_code)
