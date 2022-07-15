import sqlite3 as sql
import pandas as pd
import os
from flask import session, flash
import hashlib



class Database:
    connection = ""
    cursor = ""

    def __init__(self, database: str):
        self.connection = sql.connect(database, check_same_thread=False)
        self.cursor = self.connection.cursor()


class DatabaseFile(Database):

    def __init__(self, database: str):
        super().__init__(database)

    def getAllTableNamesAsList(self):
        command = """SELECT tbl_name
                     FROM sqlite_master
                     WHERE type='table' ORDER BY rootpage DESC"""
        exec = self.cursor.execute(command).fetchall()
        listValues = [item[0] for item in exec]
        return listValues


    def getAllDataToFileFromTable(self, tablename: str) -> pd.DataFrame:
        command = "SELECT * FROM " + tablename
        return pd.read_sql_query(command, self.connection)

    def databaseIsExisting(self, databasename: str) -> bool:
        if databasename in self.getAllTableNamesAsList():
            return True
        return False

    def allowed(self, file) -> bool:
        filename = file.filename
        last = filename.split('.').pop()
        if last == 'csv':
            return True
        else:
            return False

    def deleteFile(self, tablename:str):
        print('löschen')
        self.cursor.execute("DROP TABLE " + tablename)

    def saveFile(self, file, name:str, seperator):
        current_username = session['username']
        name = name.replace("-", "_")
        name = name.replace(" ", "_")
        if DatabaseFile.allowed(self, file) == True:
            file.save("name.csv")
            pd.read_csv("name.csv", sep=seperator).to_sql(name, sql.connect("Datenbank/" + current_username,
                                                                      check_same_thread=False),
                                                    schema=None, if_exists='replace', index=True, index_label=None,
                                                    chunksize=None,
                                                    dtype=None, method=None)
            os.remove("name.csv")
            flash(u'Datei erfolgreich hochgeladen.', 'success')
        else:
            flash(u'Die Datei ist keine csv-Datei. Bitte laden Sie nur csv-Dateien hoch!', 'error')

    def saveDataFrame(self, file, name):
        file.to_sql(name, sql.connect("Datenbank/" + session["username"], check_same_thread=False),schema=None, if_exists='replace', index=True, index_label=None,
                                                chunksize=None,
                                                dtype=None, method=None)


class DatabaseUser(Database):

    createTable = "CREATE TABLE if not EXISTS Logins(username VARCHAR(10) UNIQUE PRIMARY KEY not null, firstname " \
                  "VARCHAR(" \
                  "100) not null, lastname VARCHAR (100) not null, birthday DATE not null, password BINARY (64)not " \
                  "null, " \
                  "accountcreated TIMESTAMP not null, lastlogin TIMESTAMP not null)"

    def __init__(self, database: str):
        super().__init__(database)
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

    def getUser(self, username) -> list:
        firstnames = self.cursor.execute("SELECT firstname from Logins Where username =?", [username]).fetchone()
        firstname = firstnames[0]
        lastnames = self.cursor.execute("SELECT lastname from Logins Where username =?", [username]).fetchone()
        lastname = lastnames[0]
        birthdays = self.cursor.execute("SELECT birthday from Logins Where username =?", [username]).fetchone()
        birthday = birthdays[0]
        return [username, firstname, lastname, birthday]

    def deleteUser(self, table: str, username: str):
        if self.cursor.execute(f"DELETE FROM {table} WHERE username=?", [username]):
            return True

    def clearData(self):
        self.cursor.execute("DELETE FROM LOGINS WHERE lastlogin < DATETIME('NOW', '-2 days')")
        self.connection.commit()
        # self.connection.close()

