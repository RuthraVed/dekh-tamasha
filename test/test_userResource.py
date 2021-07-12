import unittest

from setup_test_app import app


# TestUserResource
class TU(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_get_all(self):
        response = self.client.get('/api/users')
        print('XXXX:{response}')
        self.assertEqual(200, response.status_code)
