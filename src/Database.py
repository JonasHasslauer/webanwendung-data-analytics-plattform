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

    def getConnection(self):
        return self.connection

    def setConnection(self, connection: str):
        self.connection = connection

    def getCursor(self):
        return self.cursor

    def setConnection(self, cursor: str):
        self.cursor = cursor


class DatabaseFile(Database):

    def __init__(self, database: str):
        super().__init__(database)


    def getAllTableNamesAsList(self):
        '''
        gibt alle Namen der Tables der aktuellen Datenbank als Liste zurück
        '''
        command = """SELECT tbl_name
                     FROM sqlite_master
                     WHERE type='table' ORDER BY rootpage DESC"""
        exec = self.cursor.execute(command).fetchall()
        listValues = [item[0] for item in exec]
        return listValues


    def getAllDataToFileFromTable(self, tablename: str) -> pd.DataFrame:
        '''
        diese Methode liest Daten aus einer Tabelle, und wandelt diese in ein Dataframe um
        :param tablename: der Name der Tabelle aus der Die Daten entnommen werden sollen
        :return: Dataframe mit den Daten aus der Tabelle
        '''
        command = "SELECT * FROM " + tablename
        return pd.read_sql_query(command, self.connection)

    def databaseIsExisting(self, databasename: str) -> bool:
        '''
        die Methode überprüft, ob die übergebene Tabelle in der Datenbank existiert
        :param databasename: der Name der Tabelle, die überprüft werden soll
        :return: boolean, ob die Tabelle in der Datenbank zu finden ist
        '''
        if databasename in self.getAllTableNamesAsList():
            return True
        return False

    def allowed(self, file) -> bool:
        '''
        die Methode überprüft, ob die Datei (die vom Anwender hochgeladen wird) eine csv Datei ist, und gibt ein True oder False zurück
        :param file: der Name des files, das überprüft werden soll
        :return:  boolean, ob es sich um eine csv-Datei handelt
        '''
        filename = file.filename
        last = filename.split('.').pop()
        if last == 'csv':
            return True
        else:
            return False

    def deleteFile(self, tablename:str):
        '''
        die Methode löscht die übergebene Tabelle aus der Datenbank
        :param tablename: die Tabelle, die gelöscht wird
        :return: nichts
        '''
        self.cursor.execute("DROP TABLE " + tablename)

    def saveFile(self, file, name:str, seperator):
        '''
        diese Methode speichert die übergebene Datei in die Datenbank, es müssen ein Name, unter dem sie gespeichert werden soll,
        und der gewünschte Seperator übergeben werden
        falls der Name unerlaubte Zeichen enthält (Leerzeichen oder -), werden diese in _ geändert
        :param file: die Datei, die gespeichert werden soll
        :param name: unter welchem Namen die Datei gespeichert werden soll
        :param seperator: der Seperator in der csv-Datei (sind die Spalten mit , oder ; getrennt)
        :return: nichts
        '''
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
        '''
        die Methode speichert ein übergebenes Dataframe in die SQL-Datenbank
        :param file: das zu speichernde Dataframe
        :param name: der Name, unter dem das Dataframe abgespeichert werden soll
        :return: nichts
        '''
        file.to_sql(name, sql.connect("Datenbank/" + session["username"], check_same_thread=False),schema=None, if_exists='replace', index=True, index_label=None,
                                                chunksize=None,
                                                dtype=None, method=None)


class DatabaseUser(Database):


    def __init__(self, database: str):
        super().__init__(database)
        self.createLoginTable()

    def createLoginTable(self):
        '''
        erstellt die Tabelle mit den Logins, falls diese noch nicht exisiert, in Logins werden die user mit username (primary key), Vor-und Nachname,
        Geburtsdatum, Passwort (gehashed), Timestamp wann der Account erstellt wurde, und Timestamp des letzten Logins
        :return: True, wenn es geklappt hat
        '''
        createTable = "CREATE TABLE if not EXISTS Logins(username VARCHAR(10) UNIQUE PRIMARY KEY not null, firstname " \
                      "VARCHAR(" \
                      "100) not null, lastname VARCHAR (100) not null, birthday DATE not null, password BINARY (64)not " \
                      "null, " \
                      "accountcreated TIMESTAMP not null, lastlogin TIMESTAMP not null)"
        self.cursor.execute(createTable)
        self.connection.commit()
        return True

    def getAllUsernamesFromDatabase(self):
        '''
        die Methode gibt alle Usernames, die aktuell in der Logins Table gespeichert sind
        :return: Liste
        '''
        return self.cursor.execute("Select username from Logins").fetchall()

    def checkIfUserExists(self, username: str) -> bool:
        '''
        die Methode überprüft, ob der übergebene Username bereits in der Logins-Tabelle existiert
        :param username: der zu prüfende username
        :return: boolean, ob username bereits existiert
        '''
        print(self.getAllUsernamesFromDatabase())
        if username.lower() in self.getAllUsernamesFromDatabase():
            return True
        else:
            return False

    def addUser(self, username, firstname, lastname, birthday, password):
        '''
        die Methode erstellt mit den übergebenen Daten einen Eintrag in der Logins-Tabelle, wo die user abgespeichert werden
        Damit werden die Daten gespeichert, und können zum Login verwendet werden
        Zusätzlich zu den übergebenen Daten werden noch die timestamps zum erstellen des Accounts und zum letzten login ergänzt
        :param username: der gewählte username
        :param firstname: Vorname des Anwenders
        :param lastname: Nachname des Anwenders
        :param birthday: Geburtstag des Anwenders
        :param password: gewähltes Passwort, das aber gehashed in der Datenbank abgespeichert wird
        :return: nichts
        '''
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
        '''
        die Methode ändert den timestamp, z.B. um den aktuellen letzten login zu speichern
        :param username: der username zu dem der timestamp geändert werden soll
        :return:
        '''
        self.cursor.execute("UPDATE Logins SET lastlogin == current_timestamp WHERE username = ?", [username.lower()])
        self.connection.commit()
        # self.connection.close()

    def checkUsers(self, password, username) -> bool:
        '''
        die Methode überprüft (beim Login), ob der username so (mit diesem Passwort in Kombination) in der Logins-Tabelle gespeichert ist
        :param password: Passwort, das zum überprüfen übergeben wird
        :param username: der username wird überprüfen übergeben
        :return: boolean, ob username zum Passwort passt
        '''
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
        '''
        gibt zum username die restlichen Userdaten zurück (Liste mit username, Vorname, Nachname und Geburtstag)
        :param username: username des Users, der zurückg gegeben soll
        :return: Liste mit Userdaten
        '''
        firstnames = self.cursor.execute("SELECT firstname from Logins Where username =?", [username]).fetchone()
        firstname = firstnames[0]
        lastnames = self.cursor.execute("SELECT lastname from Logins Where username =?", [username]).fetchone()
        lastname = lastnames[0]
        birthdays = self.cursor.execute("SELECT birthday from Logins Where username =?", [username]).fetchone()
        birthday = birthdays[0]
        return [username, firstname, lastname, birthday]

    def deleteUser(self, table: str, username: str):
        '''

        :param table: Tabelle aus der der user gelöscht werden soll
        :param username: username des Users, der gelöscht werden soll
        :return: true, wenns geklappt hat
        '''
        if self.cursor.execute(f"DELETE FROM {table} WHERE username=?", [username]):
            return True

    def clearData(self):
        '''
        löscht alle 2 Tage (basierend auf den Timestamps des letzten logins die Userdaten, wenn sie nicht verwendet werden
        :return:
        '''
        #soll die Datenbanken löschen, wenn die user sich 2 Tage nicht mehr angemeldet haben
        names = self.cursor.execute("SELECT username FROM LOGINS WHERE lastlogin<DATETIME('NOW', '-2 days')").fetchall()
        for name in names:
            os.remove(os.getcwd() + "/Datenbank/" + name)

        self.cursor.execute("DELETE FROM LOGINS WHERE lastlogin < DATETIME('NOW', '-2 days')")
        self.connection.commit()

        # self.connection.close()

