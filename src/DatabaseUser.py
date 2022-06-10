import hashlib
import sqlite3 as sql
import pandas as pd
import os

from flask import session



class DatabaseUser:
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
        self.createLoginTable()

    def createLoginTable(self):
        command = self.createTable
        self.cursor.execute(command)
        self.connection.commit()
        return True

    def getAllUsernamesFromDatabase(self):
        return self.cursor.execute("Select username from Logins").fetchall()

    def checkIfUserExists(self, username: str) -> bool:
        print(self.getAllUsernamesFromDatabase())
        if username.lower() in self.getAllUsernamesFromDatabase():
            return True
        else:
            return False

    def addUser(self, username, firstname, lastname, birthday, password):
        hashedPassword = hashlib.sha256(password.encode("utf-8")).hexdigest()
        self.cursor.execute(
            "INSERT INTO Logins(username,firstname, lastname, birthday,password, accountcreated, lastlogin) "
            "VALUES ( "
            "?,?, "
            "?,?,?, current_date, current_timestamp)",
            (username.lower(), firstname, lastname, birthday, hashedPassword))
        self.connection.commit()
        # self.connection.close()

    def changeTimeStamp(self, username: str):
        self.cursor.execute("UPDATE Logins SET lastlogin == current_timestamp WHERE username = ?", [username.lower()])
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

    def saveFile(self, file, name):
        # TODO check if csv
        # if allowed(file.filename):     --> funktioniert noch nicht ganz
        file.save("name.csv")
        current_username = session['username']
        print(current_username+"wird gespeichert")
        pd.read_csv("name.csv", sep=';').to_sql(name, sql.connect("Datenbank/"+current_username, check_same_thread=False),
                                                schema=None, if_exists='replace', index=True, index_label=None,
                                                chunksize=None,
                                                dtype=None, method=None)
        os.remove("name.csv")
        # TODO check if db already exists -> overwrite? --> if_exists='replace' fixt das --> soll umbenannt und anders abgespeichert werden
        # else:
        # return render_template("uebersichtsseite.html", Liste=["eins", "zwei", "zwei", "zwei"])
