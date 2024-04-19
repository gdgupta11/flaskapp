import unittest
from flaskapp.app import app
from pymongo import MongoClient
from unittest.mock import patch

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.mongo_uri = "mongodb://admin:apollo13@mongo/" 
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client.profile
        self.collection = self.db.users

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_update(self):
        response = self.app.post('/update', data=dict(name='test', address='test', company='test', userid='88837494'))
        self.assertEqual(response.status_code, 302)

    @patch('flaskapp.app.MongoClient')
    def test_mongo_connection(self, mock_mongo):
        mock_mongo.return_value.server_info.return_value = True
        self.assertTrue(self.client.server_info())

if __name__ == '__main__':
    unittest.main()