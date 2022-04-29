import unittest
from requests import get

class TestFlaskApi(unittest.TestCase):
    def test_home(self):
        response = get('http://172.17.0.2:3200/users/test')
        self.assertEqual(response.json()['res']['email_address'], "test@test.test")