import sqlite3

import pandas as pd
from flask import Flask, render_template, request, session, redirect, url_for

from src.DatabaseUser import DatabaseUser
from src.DatabaseFile import DatabaseFile

from filtern import *

app = Flask(__name__, template_folder="./templates")
app.secret_key = "key"
extensions = set({'csv'})


def allowed(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensions


databaseUserObject = DatabaseUser('Datenbank/my_logins4.db')


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


@app.route('/uebersichtsseite/<string:table>', methods=["POST", "GET"])
def specUebersicht(table):
    databaseFileObject2 = DatabaseFile("Datenbank/file")
    filenames = databaseFileObject2.getAllTableNamesAsList()
    currentDataDF = pd.read_sql_query("SELECT * FROM " + table, databaseFileObject2.connection)

    return render_template("uebersichtsseite.html", filenames=filenames, tables=[currentDataDF.to_html(classes='data')],
                           titles=currentDataDF.columns.values)


@app.route('/uebersichtsseite', methods=["POST", "GET"])
def uebersichtsseite():
    if 'username' in session:

        databaseFileObject = DatabaseFile("Datenbank/file")
        filenames = databaseFileObject.getAllTableNamesAsList()
        df = pd.read_sql_query("SELECT * FROM " + filenames[0], databaseFileObject.connection)  # Erzeugen von Dataframe
        df.to_html(header="true", table_id="table")  # Dataframe an HTML übergeben

        if request.form.get("file") == 'file':
            return redirect(url_for('specUebersicht', table='file'))

        if request.method == 'POST' and request.form.get("checkbox"):
            spalte = request.form.get("spalte")  # Eingabe von Website Spalte
            wert = request.form.get("wert")  # Eingabe von Website Wert
            operator = request.form.get("operator")  # Eingabe von Website Operator
            spaltenfilter = request.form.get("spaltenfilter")  # Eingabe von Website
            df1 = zeilenFiltern(df, spalte, wert, operator)  # Zeilen werden gefiltert
            if spaltenfilter == 'Alle' or None:  # Eingabe Alle anzeigen oder keine Eingabe (keine Eingabe funkioniert nicht)
                df = pd.read_sql_query("SELECT * from XLager", databaseFileObject.connection)  # alle anzeigen
                df.to_html(header="true", table_id="table")
                return render_template("uebersichtsseite.html", filenames=filenames,
                                       tables=[df.to_html(classes='data')], titles=df.columns.values)
            else:
                filterlist = spaltenfilter.split(',')  # Trennt Eingabe in einzelne Spaltennamen
                df2 = spaltenFiltern(df1, filterlist)  # Spalten werden gefiltert
                df2.to_html(header="true", table_id="table")  # Dataframe an HTML übergeben
                return render_template("uebersichtsseite.html", filenames=filenames.sort,
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
                df = pd.read_sql_query("SELECT * from XLager", databaseFileObject.connection)  # alle anzeigen
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
    return render_template('detailseite.html', Liste=list, bild="bewerbungen.png")


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("index"))


databaseUserObject.clearData()

if __name__ == "__main__":
    app.run(debug=True)
