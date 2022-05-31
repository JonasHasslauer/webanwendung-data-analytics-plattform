import os
import unittest
from src.Datenbank import Datenbank
from src.database import Datenbank
testdatenbank = Datenbank('src/Datenbank/testdatenbank.db')


class TestDatenbank(unittest.TestCase):
    def test_create_login_table(self):
        //print(os.path.dirname)
        db = Datenbank("src/Datenbank/my_logins4.db")
        self.assertEqual(db.createLoginTable(), True)


    def test_get_all_usernames_from_database(self):
        self.fail()

    def test_check_if_user_exists(self):
        self.fail()

    def test_add_user(self):
        self.fail()

    def test_change_time_stamp(self):
        self.fail()

    def test_check_users(self):
        self.fail()

    def test_clear_data(self):
        self.fail()


if __name__ == '__main__':
    unittest.main()
