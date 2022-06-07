import sqlite3

import pandas as pd
from flask import Flask, render_template, request, session, redirect, url_for

from src.DatabaseUser import Datenbank
from src.DatabaseFile import DatabaseFile

from filtern import *

from src.Visualization.Chart import BarChart

app = Flask(__name__, template_folder="./templates")
app.secret_key = "key"
extensions = set({'csv'})

def allowed(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensions


databaseUserObject = Datenbank('Datenbank/my_logins4.db')


@app.route("/")
def index():
    return render_template("login.html")


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        birthday = request.form.get("birthday")
        username = request.form.get("username")
        password = request.form.get("password")

        if not databaseUserObject.checkIfUserExists(username):
            try:
                databaseUserObject.addUser(username, firstname, lastname, birthday, password)
                return redirect(url_for("login"))
            except sqlite3.IntegrityError as e:
                print("Es gab einen Fehler: ", e)
                return redirect(url_for("login"))
        else:  # Nutzer muss sich mit anderem Namen registrieren
            return render_template(url_for("register"))
    else:
        return render_template("register.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        if databaseUserObject.checkUsers(password, username) is True:
            session['username'] = username
            databaseUserObject.changeTimeStamp(username)
            return redirect(url_for('uebersichtsseite'))
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))


@app.route('/uebersichtsseite', methods=["POST", "GET"])
def uebersichtsseite():
    if 'username' in session:

        databaseFileObject = DatabaseFile("Datenbank/file")
        filenames = databaseFileObject.getAllTableNames()

        filename = databaseFileObject.cursor.execute('SELECT * FROM Lager')
        df = pd.read_sql_query('SELECT * FROM Lager', databaseFileObject.connection)  # Erzeugen von Dataframe
        df.to_html(header="true", table_id="table")  # Dataframe an HTML übergeben
        filename.execute('SELECT name FROM sqlite_master WHERE type = "table"')  # Datenbankabfrage für Filenames
        filenames = filename.fetchall()
        filename.close()

        if request.method == 'POST' and request.form.get("checkbox"):
            spalte = request.form.get("spalte")  # Eingabe von Website Spalte
            wert = request.form.get("wert")  # Eingabe von Website Wert
            operator = request.form.get("operator")  # Eingabe von Website Operator
            spaltenfilter = request.form.get("spaltenfilter")  # Eingabe von Website
            df1 = zeilenFiltern(df, spalte, wert, operator)  # Zeilen werden gefiltert
            if spaltenfilter == 'Alle' or None:  # Eingabe Alle anzeigen oder keine Eingabe (keine Eingabe funkioniert nicht)
                df = pd.read_sql_query("SELECT * from Lager", databaseFileObject.connection)  # alle anzeigen
                df.to_html(header="true", table_id="table")
                return render_template("uebersichtsseite.html", filenames=filenames,
                                       tables=[df.to_html(classes='data')], titles=df.columns.values)
            else:
                filterlist = spaltenfilter.split(',')  # Trennt Eingabe in einzelne Spaltennamen
                df2 = spaltenFiltern(df1, filterlist)  # Spalten werden gefiltert
                df2.to_html(header="true", table_id="table")  # Dataframe an HTML übergeben
                return render_template("uebersichtsseite.html", filenames=filenames,
                                   tables=[df2.to_html(classes='data')], titles=df2.columns.values)
        # Zeilenfilter
        elif request.method == 'POST' and request.form.get("spalte"):
            spalte = request.form.get("spalte")  # Eingabe von Website Spalte
            wert = request.form.get("wert")  # Eingabe von Website Wert
            operator = request.form.get("operator")  # Eingabe von Website Operator
            df = zeilenFiltern(df, spalte, wert, operator)  # Zeilen werden gefiltert
            df.to_html(header="true", table_id="table")  # Dataframe an HTML übergeben
            return render_template("uebersichtsseite.html", filenames=filenames,
                                   tables=[df.to_html(classes='data')], titles=df.columns.values)

        # Spaltenfilter
        elif request.method == 'POST' and request.form.get("spaltenfilter"):
            spaltenfilter = request.form.get("spaltenfilter")  # Eingabe von Website
            if spaltenfilter == 'Alle' or None:  # Eingabe Alle anzeigen oder keine Eingabe (keine Eingabe funkioniert nicht)
                df = pd.read_sql_query("SELECT * from Lager", databaseFileObject.connection)  # alle anzeigen
                df.to_html(header="true", table_id="table")
            else:
                filterlist = spaltenfilter.split(',')  # Trennt Eingabe in einzelne Spaltennamen
                df = spaltenFiltern(df, filterlist)  # Spalten werden gefiltert
                df.to_html(header="true", table_id="table")  # Dataframe an HTML übergeben
            return render_template("uebersichtsseite.html", filenames=filenames,
                                   tables=[df.to_html(classes='data')], titles=df.columns.values)

        elif request.method == 'POST' and request.files['file']:
            file = request.files['file']
            name = file.filename
            namesplitted = name.split('.')
            print(namesplitted[0])
            databaseFileObject.saveFile(file, namesplitted[0])
            return render_template("uebersichtsseite.html", filenames=filenames,
                                   tables=[df.to_html(classes='data')],
                                   titles=df.columns.values)

        else:
            return render_template("uebersichtsseite.html", filenames=filenames,
                                   tables=[df.to_html(classes='data')], titles=df.columns.values)

@app.route('/detailseite', methods=["POST", "GET"])
def detailseite():
    databaseObject = Datenbank("Datenbank/file")
    filename = databaseObject.cursor.execute('SELECT * FROM Sacramento')
    print("detailseite")

    if request.method == 'POST' and request.form.get("xAchse"):
        diagrammart = request.form.get("diagrammart")   #kriegt aus Frontend, welches Diagrammart geünscht ist
        print(diagrammart)                              #nur Kontrolle
        if diagrammart == "Balkendiagramm":
            xAchse = request.form.get("xAchse")         #kriegt asu Frontend die column names die für x- bzw. y-Achse verwendet werden sollen
            yAchse = request.form.get("yAchse")
            command = "SELECT * FROM Sacramento GROUP BY " + xAchse
            df = pd.read_sql_query(command, databaseObject.connection)  #wandelt Table in DataFrame um
            my_list = df.columns.values.tolist()                        #macht Liste aus column names des DataFrames
            ax = df.plot.bar(x=xAchse, y=yAchse).get_figure()           #erstellt plot mit x- und y-Achse
            ax.savefig('static/name.png')                               #speichert Bild zwischen, damit es angezeigt werden kann
            return render_template("detailseite.html", Liste=my_list )
        elif diagrammart == "Tortendiagramm":                           #macht noch keinen Sinn, zählt nicht, kann nur ein column entgegen nehmen
            xAchse = request.form.get("xAchse")
            yAchse = request.form.get("yAchse")
            command = "SELECT * FROM Sacramento GROUP BY " + xAchse
            df = pd.read_sql_query(command, databaseObject.connection)
            my_list = df.columns.values.tolist()
            ax = df.plot.pie(y= xAchse).get_figure()
            ax.savefig('static/name.png')
            return render_template("detailseite.html", Liste=my_list )
        elif diagrammart == "Liniendiagramm":
            xAchse = request.form.get("xAchse")
            yAchse = request.form.get("yAchse")
            command = "SELECT * FROM Sacramento GROUP BY " + xAchse
            df = pd.read_sql_query(command, databaseObject.connection)
            my_list = df.columns.values.tolist()
            ax = df.plot.line(x=xAchse, y=yAchse).get_figure()
            ax.savefig('static/name.png')
            return render_template("detailseite.html", Liste=my_list)
        elif diagrammart == "Wordcloud":
            xAchse = request.form.get("xAchse")
            yAchse = request.form.get("yAchse")
            command = "SELECT * FROM Sacramento GROUP BY " + xAchse
            df = pd.read_sql_query(command, databaseObject.connection)
            my_list = df.columns.values.tolist()
            wordcloudErstellen(df)                                      #ruft wordcloud auf, und erstellt wordcloud aus gesamtem dataframe
            return render_template("detailseite.html", Liste=my_list)
    else:
        print("bin im else zweig")
        command = "SELECT * FROM Sacramento"
        df = pd.read_sql_query(command, databaseObject.connection)
        my_list = df.columns.values.tolist()                        #erstellt Liste aus column names für Dropdowns (höchstens 15)
        return render_template('detailseite.html', Liste=my_list )  #muss Liste übergeben, für erstes Landing




@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("index"))


databaseUserObject.clearData()

if __name__ == "__main__":
    app.run(debug=True)
