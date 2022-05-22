import hashlib
import sqlite3 as sql
import pandas as pd

conj = sql.connect("Datenbank/Verbindung.db")
curj = conj.cursor()
CreateUpload = "CREATE TABLE if not EXISTS Verbindung(connection_id INTEGER UNIQUE PRIMARY KEY not null , username VARCHAR(10) not null, Dateiname VARCHAR(30) not null, Speicherdatum date not null)"

curj.execute(CreateUpload)


def test():
    conj = sql.connect("Datenbank/Verbindung.db")
    curj = conj.cursor()
    curj.execute("SELECT * FROM Verbindung")
    Befehl = curj.fetchall()
    print(Befehl)


print(test())

def AddConnection(username, filename):
    con = sql.connect("Datenbank/Verbindung.db")
    cur = con.cursor()
    cur.execute(
        "INSERT INTO Verbindung(username, Dateiname, Speicherdatum) VALUES (?,?, current_date)",
        (username, filename))
    con.commit()
    con.close()

def savefile(file, name):
    df = pd.read_csv(file, sep=';')
    print(file)
    db = "Datenbank/" + name + ".db"
    dbname = name + '.db'

    df.to_sql(dbname, sql.connect(db), schema=None, if_exists='fail', index=True, index_label=None, chunksize=None,
              dtype=None, method=None)


#savefile('tda.csv', 'tda.csv')
#AddConnection('Johanna', 'tda')
#AddConnection('Johanna', 'filex')
#AddConnection('Johanna', 'filey')
#AddConnection('Samim', 'filez')
#AddConnection('Jonas', 'filea')
#AddConnection('Samim', 'fileb')
#AddConnection('Samim', 'filec')

def getfilenames(Username):
    con = sql.connect("Datenbank/Verbindung.db")
    cur = con.cursor()
    cur.execute("SELECT Dateiname FROM Verbindung WHERE username is ?", (Username,))
    Befehl = cur.fetchall()
    return Befehl

print(getfilenames('Johanna'))



''' 
def save():
    df = pd.read_csv('Uploads/Testdatei.csv', sep=';')
    print(df)
    df.to_sql('file.db', sql.connect('Datenbank/file.db'), schema=None, if_exists='fail', index=True, index_label=None,
              chunksize=None,
              dtype=None, method=None)
'''
