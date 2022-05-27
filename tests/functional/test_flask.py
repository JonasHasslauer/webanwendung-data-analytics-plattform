import unittest
from src.Datenbank import Datenbank
from src.__init__ import app


db = Datenbank('src\\Datenbank\\my_logins4.db')


class TestFlask(unittest.TestCase):
    def setUp(self) -> None:
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://///Users/johan/webanwendung-data-analytics-plattform/src/Datenbank/my_logins4.db"

        self.app = app.test_client()


    def tearDown(self) -> None:
        pass


    def test_root(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()

