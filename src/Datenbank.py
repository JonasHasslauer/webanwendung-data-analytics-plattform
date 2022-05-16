import hashlib
import sqlite3 as sql

con = sql.connect("Datenbank/my_logins4.db")
cur = con.cursor()
CreateTable = "CREATE TABLE if not EXISTS Logins(username VARCHAR(10) UNIQUE PRIMARY KEY not null, firstname VARCHAR(" \
              "100) not null, lastname VARCHAR (100) not null, birthday DATE not null, password BINARY (64)not null, " \
              "accountcreated TIMESTAMP not null, lastlogin TIMESTAMP not null) "
cur.execute(CreateTable)
con.commit()


def AddUSER(username, firstname, lastname, birthday, password):
    con = sql.connect("Datenbank/my_logins4.db")
    cur = con.cursor()
    hashedpsw = hashlib.sha256(password.encode("utf-8")).hexdigest()
    cur.execute(
        "INSERT INTO Logins(username,firstname, lastname, birthday,password, accountcreated, lastlogin) VALUES (?,?,"
        "?,?,?, current_date, current_timestamp)",
        (username, firstname, lastname, birthday, hashedpsw))
    con.commit()
    con.close()


def changetimestamp():
    con = sql.connect("Datenbank/my_logins4.db")
    cur = con.cursor()
    cur.execute("UPDATE Logins SET lastlogin == current_timestamp")
    con.commit()
    con.close()


def check_User(username, password):
    con = sql.connect("Datenbank/my_logins4.db")
    cur = con.cursor()
    currentHash = hashlib.sha256(password.encode("utf-8")).hexdigest()
    cur.execute("SELECT password from Logins Where username =?", [username])
    row = cur.fetchone()
    if row is None:

        return False
    else:
        fetchedhash = row[0]
        if fetchedhash == currentHash:

            return True
        else:

            return False


def cleardata():
    con = sql.connect("Datenbank/my_logins4.db")
    cur = con.cursor()
    # cur.execute("DELETE FROM Logins WHERE  createtime< DATETIME('NOW', '-1 days')")
    cur.execute("DELETE FROM LOGINS WHERE lastlogin < DATETIME('NOW', '-100 minutes')")
    con.commit()
    con.close()
