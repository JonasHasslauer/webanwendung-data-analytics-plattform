import unittest
from src.database import Datenbank
from src.app import app
import os



class TestFlask(unittest.TestCase):
    def setUp(self) -> None:
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('src/Datenbank/my_logins4.db')

        self.app = app.test_client()


    def tearDown(self) -> None:
        pass


    def test_root(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()

