import unittest
from src.database import Datenbank
import sqlite3 as sql

class Test_UserInDb(unittest.TestCase):

    db = ""

    def setUp(self):
        self.db = Datenbank('/Users/johan/webanwendung-data-analytics-plattform/src/Datenbank/my_logins4.db')
        if ('jonashasslau1',) in self.db.getAllUsernamesFromDatabase():
            self.db.cursor.execute("DELETE FROM LOGINS WHERE username = ?", ['jonashasslau1'])

        self.db.addUser('JonasHasslau1', 'Jonas', 'Haßlauer', '12.06.2000', 'Katze123')



    def test_ifExists(self):
        self.assertTrue(('jonashasslau1',) in self.db.getAllUsernamesFromDatabase())

    def test_UserName(self):
        nameInDb = self.db.cursor.execute("SELECT username FROM LOGINS where username = ?", ['jonashasslau1']).fetchall()
        for row in nameInDb:
            self.assertEqual(row[0], 'JonasHasslau1'.lower())


    def test_FirstName(self):
        nameInDb = self.db.cursor.execute("SELECT firstname FROM LOGINS where username = ?",
                                          ['jonashasslau1']).fetchall()
        for row in nameInDb:
            self.assertEqual(row[0], 'Jonas')

    def test_LastName(self):
        nameInDb = self.db.cursor.execute("SELECT lastname FROM LOGINS where username = ?",
                                          ['jonashasslau1']).fetchall()
        for row in nameInDb:
            self.assertEqual(row[0], 'Haßlauer')

    def test_Birthday(self):
        bdayInDb = self.db.cursor.execute("SELECT birthday FROM LOGINS where username = ?",
                                          ['jonashasslau1']).fetchall()
        for row in bdayInDb:
            self.assertEqual(row[0], '12.06.2000')

    def test_password(self):
        passwordInDb = self.db.cursor.execute("SELECT birthday FROM LOGINS where username = ?",
                                          ['jonashasslau1']).fetchall()
        for row in passwordInDb:
            self.assertTrue(row[0] != 'Katze123')


    def test_checkUsers(self):
        self.assertTrue(self.db.checkUsers('Katze123', 'jonashasslau1'))

    def test_checkUsers2(self):
        self.assertFalse(self.db.checkUsers('Katze1234', 'jonashasslau1'))


    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
