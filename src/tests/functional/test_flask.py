import unittest
from src.database import Datenbank
from src.__init__ import app
import os
from src.filtern import *



class TestFlask(unittest.TestCase):
    def setUp(self) -> None:
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()


    def tearDown(self) -> None:
        pass


    def test_root(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()

