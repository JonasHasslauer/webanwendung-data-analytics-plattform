import sqlite3 as sql
import pandas as pd
import os
from flask import session

def saveFile(self, file, name):
    # TODO check if csv
    # if allowed(file.filename):     --> funktioniert noch nicht ganz
    file.save("name.csv")
    current_username = session['username']
    print(current_username + "wird gespeichert")
    pd.read_csv("name.csv", sep=';').to_sql(name, sql.connect("Datenbank/" + current_username, check_same_thread=False),
                                            schema=None, if_exists='replace', index=True, index_label=None,
                                            chunksize=None,
                                            dtype=None, method=None)
    os.remove("name.csv")


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
        return pd.read_sql_query(self.cursor.execute(command), self.connection)


    def saveDataFrame(self, file, name):
        file.to_sql(name, sql.connect("Datenbank/file", check_same_thread=False),schema=None, if_exists='replace', index=True, index_label=None,
                                                chunksize=None,
                                                dtype=None, method=None)
