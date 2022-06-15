import sqlite3 as sql
import pandas as pd
import os
from flask import session, flash

class DatabaseFile:
    connection = ""
    cursor = ""

    def __init__(self, database: str):
        self.connection = sql.connect(database, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def getAllTableNamesAsList(self):
        command = """SELECT tbl_name
                     FROM sqlite_master
                     WHERE type='table' ORDER BY rootpage DESC"""
        exec = self.cursor.execute(command).fetchall()
        listValues = [item[0] for item in exec]
        return listValues

    def checkIfTableWithNameExists(self):
        pass
        # check which user to get the specific database (maliks changes)
        # check Table names

    def getAllDataToFileFromTable(self, tablename: str) -> pd.DataFrame:
        command = "SELECT * FROM " + tablename
        return pd.read_sql_query(command, self.connection)

    def isFileExisting(self, filename: str) -> bool:
        if filename in self.getAllTableNamesAsList():
            return True
        return False

    def saveFile(self, file, name, seperator):
        current_username = session['username']
        filename = file.filename
        name = name.replace("-", " ")
        namesplitted = filename.split('.')
        last = namesplitted.pop()
        if last == 'csv':
            file.save("name.csv")
            if seperator == ',':
                pd.read_csv("name.csv", sep=',').to_sql(name, sql.connect("Datenbank/" + current_username,
                                                                          check_same_thread=False),
                                                        schema=None, if_exists='replace', index=True, index_label=None,
                                                        chunksize=None,
                                                        dtype=None, method=None)
            elif seperator == ';':
                pd.read_csv("name.csv", sep=';').to_sql(name, sql.connect("Datenbank/" + current_username,
                                                                          check_same_thread=False),
                                                        schema=None, if_exists='replace', index=True, index_label=None,
                                                        chunksize=None,
                                                        dtype=None, method=None)
            os.remove("name.csv")
            flash("Datei erfolgreich hochgeladen.")


    def saveDataFrame(self, file, name):
        file.to_sql(name, sql.connect("Datenbank/" + session["username"], check_same_thread=False),schema=None, if_exists='replace', index=True, index_label=None,
                                                chunksize=None,
                                                dtype=None, method=None)
