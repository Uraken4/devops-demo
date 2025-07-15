import unittest
from app import app

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_message_endpoint(self):
        response = self.app.get('/api/message')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Hello DevOps"})

if __name__ == '__main__':
    unittest.main()
