import sqlite3 as sql
import pandas as pd

conj = sql.connect("Datenbank/Verbindung.db")
curj = conj.cursor()
CreateUpload = "CREATE TABLE if not EXISTS Verbindung(connection_id INTEGER UNIQUE PRIMARY KEY not null , username VARCHAR(10) not null, Dateiname VARCHAR(30) not null)"

curj.execute(CreateUpload)


def test():
    conj = sql.connect("Datenbank/Verbindung.db")
    curj = conj.cursor()
    curj.execute("SELECT * FROM Verbindung")
    Befehl = curj.fetchall()
    print(Befehl)




def pandastest():
    df = pd.read_csv('Uploads/Testdatei.csv', sep=';')
    print(df)
    # conj = sql.connect('filename.db')
    df.to_sql('file.db', sql.connect('Datenbank/file.db'), schema=None, if_exists='fail', index=True, index_label=None,
              chunksize=None, dtype=None, method=None)


def savefile(file, filename):
    df = pd.read_csv(file, sep=';')
    db = "Datenbank/" + filename + ".db"
    df.to_sql(filename, sql.connect("Datenbank/" + filename + ".db"), schema=None, if_exists='fail',
              index=True, index_label=None, chunksize=None,
              dtype=None, method=None)
