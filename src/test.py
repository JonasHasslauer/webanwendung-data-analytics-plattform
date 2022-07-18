import sqlite3
import os


connection = sqlite3.connect('Datenbank/my_logins4.db', check_same_thread=False)
cursor= connection.cursor()

#soll die Datenbanken löschen, wenn die user sich 2 Tage nicht mehr angemeldet haben

def cleardata():
        names = cursor.execute("SELECT username FROM LOGINS WHERE lastlogin<DATETIME('NOW', '- 2 days')").fetchall()
        for name in names:
            x = str(name)
            x = x.rsplit("'", 1)
            y = str(x[0])
            z = y.split("'", 1)
            a = z[1]
            os.remove(os.getcwd() + "/Datenbank/" + a)

cleardata()