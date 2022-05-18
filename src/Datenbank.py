import hashlib
import sqlite3 as sql


class Datenbank:
    connection = ""
    cursor = ""

    createTable = "CREATE TABLE if not EXISTS Logins(username VARCHAR(10) UNIQUE PRIMARY KEY not null, firstname " \
                  "VARCHAR(" \
                  "100) not null, lastname VARCHAR (100) not null, birthday DATE not null, password BINARY (64)not " \
                  "null, " \
                  "accountcreated TIMESTAMP not null, lastlogin TIMESTAMP not null)"

    def __init__(self, database: str):
        self.connection = sql.connect(database, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def createLoginTable(self):
        command = self.createTable
        self.cursor.execute(command)
        self.connection.commit()

    # TODO Methode 'getAllUsers' to check if the user's already created -> addUser

    def addUser(self, username, firstname, lastname, birthday, password):
        hashedPassword = hashlib.sha256(password.encode("utf-8")).hexdigest()
        self.cursor.execute(
            "INSERT INTO Logins(username,firstname, lastname, birthday,password, accountcreated, lastlogin) VALUES ("
            "?,?, "
            "?,?,?, current_date, current_timestamp)",
            (username.lower(), firstname, lastname, birthday, hashedPassword))
        self.connection.commit()
        # self.connection.close()

    def changeTimeStamp(self):
        self.cursor.execute("UPDATE Logins SET lastlogin == current_timestamp")
        self.connection.commit()
        # self.connection.close()

    def checkUsers(self, password, username) -> bool:
        currentHash = hashlib.sha256(password.encode("utf-8")).hexdigest()
        self.cursor.execute("SELECT password from Logins Where username =?", [username])
        row = self.cursor.fetchone()
        if row is not None:
            fetchedHash = row[0]
            if fetchedHash == currentHash:
                return True
            else:
                return False
        return False

    def clearData(self):
        self.cursor.execute("DELETE FROM LOGINS WHERE lastlogin < DATETIME('NOW', '-100 minutes')")
        self.connection.commit()
        # self.connection.close()
