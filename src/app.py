import sqlite3

import pandas as pd
from flask import Flask, render_template, request, session, redirect, url_for

import src.DatabaseFile
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
    if 'username' in session:
        databaseFileObject2 = DatabaseFile("Datenbank/file")
        filenames = databaseFileObject2.getAllTableNamesAsList()
        currentDataDF = pd.read_sql_query("SELECT * FROM " + table, databaseFileObject2.connection)

        # Zeilen- und Spaltenfilter kombiniert
        if request.method == 'POST' and request.form.get("checkbox"):
            spalte = request.form.get("spalte")  # Eingabe von Website Spalte
            wert = request.form.get("wert")  # Eingabe von Website Wert
            operator = request.form.get("operator")  # Eingabe von Website Operator
            spaltenfilter = request.form.get("spaltenfilter")  # Eingabe von Website
            zeilenFilterDF = zeilenFiltern(currentDataDF, spalte, int(wert), operator)  # Zeilen werden gefiltert

            if spaltenfilter == 'Alle' or None:  # Eingabe Alle anzeigen oder keine Eingabe (keine Eingabe funkioniert nicht)
                currentDataDF.to_html(header="true", table_id="table")
                return render_template("uebersichtsseite.html", filenames=filenames,
                                       tables=[
                                           currentDataDF.to_html(classes='table table-striped text-center', index=False, justify="center", col_space=20)],
                                       titles=currentDataDF.columns.values, tablename=table)
            else:
                filterlist = spaltenfilter.split(',')  # Trennt Eingabe in einzelne Spaltennamen
                global newDF
                newDF = spaltenFiltern(zeilenFilterDF, filterlist)  # Spalten werden gefiltert
                newDF.to_html(header="true", table_id="table")  # Dataframe an HTML übergeben
                return render_template("uebersichtsseite.html", filenames=filenames,
                                       tables=[newDF.to_html(classes='table table-striped text-center', index=False, justify="center", col_space=20)],
                                       titles=newDF.columns.values, table=table, tablename=table)

        # Zeilenfilter
        elif request.method == 'POST' and request.form.get("spalte"):
            spalte = request.form.get("spalte")  # Eingabe von Website Spalte
            wert = request.form.get("wert")  # Eingabe von Website Wert
            operator = request.form.get("operator")  # Eingabe von Website Operator
            newDF = zeilenFiltern(currentDataDF, spalte, int(wert), operator)  # Zeilen werden gefiltert
            newDF.to_html(header="true", table_id="table")  # Dataframe an HTML übergeben
            return render_template("uebersichtsseite.html", filenames=filenames,
                                   tables=[newDF.to_html(classes='table table-striped text-center', index=False,
                                                         justify="center", col_space=20)], titles=newDF.columns.values,
                                                        table=table, tablename=table)

        # Spaltenfilter
        elif request.method == 'POST' and request.form.get("spaltenfilter"):
            spaltenfilter = request.form.get("spaltenfilter")
            if spaltenfilter == 'Alle' or None:  # Eingabe Alle anzeigen oder keine Eingabe (keine Eingabe funkioniert nicht)
                currentDataDF.to_html(header="true", table_id="table")
                return render_template("uebersichtsseite.html", filenames=filenames,
                                       tables=[currentDataDF.to_html(classes='table table-striped text-center', index=False, justify="center", col_space=20)],
                                       titles=currentDataDF.columns.values, tablename=table)
            else:
                filterlist = spaltenfilter.split(',')  # Trennt Eingabe in einzelne Spaltennamen
                newDF = spaltenFiltern(currentDataDF, filterlist)  # Spalten werden gefiltert
                newDF.to_html(header="true", table_id="table")  # Dataframe an HTML übergeben
                return render_template("uebersichtsseite.html", filenames=filenames,
                                       tables=[newDF.to_html(classes='table table-striped text-center', index=False, justify="center", col_space=20)],
                                       titles=newDF.columns.values, table=table, tablename=table)


        elif request.method == 'POST' and request.form.get("subset"):
            DFname = request.form.get("subset")

            databaseFileObject2.saveDataFrame(newDF, DFname)
            newDF.to_html(header="true", table_id="table")  # Dataframe an HTML übergeben
            return render_template("uebersichtsseite.html", filenames=filenames,
                                   tables=[newDF.to_html(classes='table table-striped text-center', index=False, justify="center", col_space=20)],
                                   titles=newDF.columns.values, table=table, tablename=table)


        else:
            return render_template("uebersichtsseite.html", filenames=filenames,
                                   tables=[currentDataDF.to_html(classes='table table-striped text-center', index=False, justify="center", col_space=20)],
                                   titles=currentDataDF.columns.values,
                                   table=table, tablename=table)
    else:
        return redirect(url_for('index'))


@app.route('/uebersichtsseite', methods=["POST", "GET"])
def uebersichtsseite():
    if 'username' in session:
        databaseFileObject = DatabaseFile("Datenbank/file")
        filenames = databaseFileObject.getAllTableNamesAsList()

        if request.method == 'POST' and request.form.get('submit') == 'Refresh':
            return render_template("uebersichtsseite.html", filenames=filenames)

        if request.method == 'POST' and request.form.get('uebersichtsseite') == 'uebersichtsseite':
            return render_template("uebersichtsseite.html", filenames=filenames)

        # Dateiupload
        elif request.method == 'POST' and request.files['file']:
            file = request.files['file']
            name = file.filename
            namesplitted = name.split('.')
            seperator = request.form.get('seperator')
            if seperator is None:
                src.DatabaseFile.saveFile(file, namesplitted[0], seperator=",")
            else:
                src.DatabaseFile.saveFile(file, namesplitted[0], seperator)
            return render_template("uebersichtsseite.html", filenames=filenames)
        else:
            return render_template("uebersichtsseite.html", filenames=filenames)

    else:
        return redirect(url_for('index'))


@app.route('/detailseite/<string:table>', methods=["POST", "GET"])
def detailseite(table):
    if 'username' in session:
        databaseObject = DatabaseFile("Datenbank/file")
        currentDataDF = pd.read_sql_query("SELECT * FROM " + table, databaseObject.connection)

        if request.method == 'POST' and request.form.get("xAchse"):
            diagrammart = request.form.get("diagrammart")  # kriegt aus Frontend, welches Diagrammart geünscht ist
            print(diagrammart)  # nur Kontrolle
            if diagrammart == "Balkendiagramm":
                xAchse = request.form.get("xAchse")  # kriegt aus Frontend die column names die für x- bzw. y-Achse
                # verwendet werden sollen
                yAchse = request.form.get("yAchse")
                command = "SELECT * FROM " + table + " GROUP BY " + xAchse
                df = pd.read_sql_query(command, databaseObject.connection)  # wandelt Table in DataFrame um
                my_list = df.columns.values.tolist()  # macht Liste aus column names des DataFrames
                ListeInt = df.select_dtypes(include=np.number).columns.values.tolist()
                ax = df.plot.bar(x=xAchse, y=yAchse).get_figure()  # erstellt plot mit x- und y-Achse
                ax.savefig('static/name.png')  # speichert Bild zwischen, damit es angezeigt werden kann
                currentDataDF.to_html(header="true", table_id="table")
                return render_template("detailseite.html", Liste=my_list, ListeY=ListeInt, table=table)
            elif diagrammart == "Tortendiagramm":  # macht noch keinen Sinn, zählt nicht, kann nur ein column entgegen nehmen
                xAchse = request.form.get("xAchse")
                yAchse = request.form.get("yAchse")
                command = "SELECT * FROM " + table
                df = pd.read_sql_query(command, databaseObject.connection)
                my_list = df.columns.values.tolist()
                ListeInt = df.select_dtypes(include=np.number).columns.values.tolist()
                ax = df.plot.pie(y=xAchse).get_figure()
                ax.savefig('static/name.png')
                currentDataDF.to_html(header="true", table_id="table")
                return render_template("detailseite.html", Liste=my_list, ListeY=ListeInt, table=table)
            elif diagrammart == "Liniendiagramm":
                xAchse = request.form.get("xAchse")
                yAchse = request.form.get("yAchse")
                command = "SELECT * FROM " + table + " GROUP BY " + xAchse
                df = pd.read_sql_query(command, databaseObject.connection)
                my_list = df.columns.values.tolist()
                ListeInt = df.select_dtypes(include=np.number).columns.values.tolist()
                ax = df.plot.line(x=xAchse, y=yAchse).get_figure()
                ax.savefig('static/name.png')
                currentDataDF.to_html(header="true", table_id="table")
                return render_template("detailseite.html", Liste=my_list, ListeY=ListeInt, table=table)
            elif diagrammart == "Wordcloud":
                xAchse = request.form.get("xAchse")
                yAchse = request.form.get("yAchse")
                command = "SELECT * FROM " + table + " GROUP BY " + xAchse
                df = pd.read_sql_query(command, databaseObject.connection)
                my_list = df.columns.values.tolist()
                ListeInt = df.select_dtypes(include=np.number).columns.values.tolist()
                wordcloudErstellen(df)  # ruft wordcloud auf, und erstellt wordcloud aus gesamtem dataframe
                currentDataDF.to_html(header="true", table_id="table")
                return render_template("detailseite.html", Liste=my_list, ListeY=ListeInt, table=table)
        else:
            command = "SELECT * FROM " + table
            df = pd.read_sql_query(command, databaseObject.connection)
            ListeInt = df.select_dtypes(include=np.number).columns.values.tolist()
            my_list = df.columns.values.tolist()  # erstellt Liste aus column names für Dropdowns (höchstens 15)
            currentDataDF.to_html(header="true", table_id="table")
            return render_template("detailseite.html", Liste=my_list,
                                   ListeY=ListeInt, table=table)  # muss Liste übergeben, für erstes Landing

    else:
        return redirect(url_for('index'))


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("index"))


databaseUserObject.clearData()

if __name__ == "__main__":
    app.run(debug=True)
