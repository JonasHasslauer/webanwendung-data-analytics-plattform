import os
import sqlite3

from flask import Flask, render_template, request, session, redirect, url_for, flash
from werkzeug.exceptions import BadRequestKeyError

from src.DatabaseUser import DatabaseUser
from src.DatabaseFile import DatabaseFile

from Chart import *
from filtern import *
from PIL import Image

import seaborn as sns

app = Flask(__name__, template_folder="./templates")
app.secret_key = "key"
extensions = {'csv'}


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

        if '/' not in username:
            if not databaseUserObject.checkIfUserExists(username):
                try:
                    databaseUserObject.addUser(username, firstname, lastname, birthday, password)
                    flash("Account erfolgreich registriert.")
                    return redirect(url_for("login"))
                except sqlite3.IntegrityError as e:
                    flash("username bereits vergeben. Bitte anderen username benutzen.")
                    return redirect(url_for("register"))
            else:  # Nutzer muss sich mit anderem Namen registrieren
                flash("username bereits vergeben. Bitte anderen username benutzen.")
                return render_template(url_for("register"))
        else:
            flash("username enhält '/', bitte melden Sie sich mit einem anderen username an")
            return redirect(url_for("register"))
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
            img = Image.open("static/detailseite.jpg")
            img.save('static/name.png')

            return redirect(url_for('uebersichtsseite'))
        else:
            flash("Benutzerdaten überprüfen oder einen Account anlegen.")
            return redirect(url_for('login'))
    else:
        return redirect(url_for('index'))


@app.route('/uebersichtsseite/<string:table>', methods=["POST", "GET"])
def specUebersicht(table):
    if 'username' in session:
        current_username = session['username']
        databaseFileObject2 = DatabaseFile("Datenbank/" + current_username)
        filenames = databaseFileObject2.getAllTableNamesAsList()
        currentDataDF = pd.read_sql_query("SELECT * FROM " + table, databaseFileObject2.connection)

        databaseUserObject = DatabaseUser("Datenbank/my_logins4.db")
        user_list = databaseUserObject.getUser(current_username)

        # Zeilen- und Spaltenfilter kombiniert
        if request.method == 'POST' and request.form.get("checkbox"):
            spalte = request.form.get("spalte")  # Eingabe von Website Spalte
            wert = request.form.get("wert")  # Eingabe von Website Wert
            operator = request.form.get("operator")  # Eingabe von Website Operator
            spaltenfilter = request.form.get("spaltenfilter")  # Eingabe von Website
            zeilen = request.form.get("zeilen")
            global newDF
            newDF = currentDataDF
            if zeilen:
                print("Zeilenauswahl")
                newDF = zeilenAuswählen(newDF, zeilen)
            else:
                print(zeilen)
            zeilenFilterDF = zeilenFiltern(newDF, spalte, int(wert), operator)  # Zeilen werden gefiltert

            if spaltenfilter == 'Alle' or None:  # Eingabe Alle anzeigen oder keine Eingabe (keine Eingabe funkioniert nicht)
                currentDataDF.to_html(header="true", table_id="table")
                return render_template("uebersichtsseite.html", filenames=filenames,
                                       tables=[
                                           currentDataDF.to_html(classes='table table-striped text-center', index=False,
                                                                 justify="center", col_space=20)],
                                       titles=currentDataDF.columns.values, tablename=table, user_list=user_list)
            else:
                filterlist = spaltenfilter.split(',')  # Trennt Eingabe in einzelne Spaltennamen
                newDF = spaltenFiltern(zeilenFilterDF, filterlist)  # Spalten werden gefiltert
                newDF.to_html(header="true", table_id="table")  # Dataframe an HTML übergeben
                return render_template("uebersichtsseite.html", filenames=filenames,
                                       tables=[newDF.to_html(classes='table table-striped text-center', index=False,
                                                             justify="center", col_space=20)],
                                       titles=newDF.columns.values, table=table, tablename=table, user_list=user_list)

        # Zeilenfilter
        elif request.method == 'POST' and request.form.get("spalte"):
            spalte = request.form.get("spalte")  # Eingabe von Website Spalte
            wert = request.form.get("wert")  # Eingabe von Website Wert
            operator = request.form.get("operator")  # Eingabe von Website Operator
            zeilen = request.form.get('zeilen')
            newDF = currentDataDF
            if zeilen:
                print("Zeilenauswahl")
                newDF = zeilenAuswählen(newDF, zeilen)
            else:
                print(zeilen)
            newDF = zeilenFiltern(newDF, spalte, int(wert), operator)  # Zeilen werden gefiltert
            newDF.to_html(header="true", table_id="table")  # Dataframe an HTML übergeben
            return render_template("uebersichtsseite.html", filenames=filenames,
                                   tables=[newDF.to_html(classes='table table-striped text-center', index=False,
                                                         justify="center", col_space=20)], titles=newDF.columns.values,
                                   table=table, tablename=table, user_list=user_list)

        # Spaltenfilter
        elif request.method == 'POST' and request.form.get("spaltenfilter"):
            spaltenfilter = request.form.get("spaltenfilter")
            if spaltenfilter == 'Alle' or None:  # Eingabe Alle anzeigen oder keine Eingabe (keine Eingabe funkioniert nicht)
                currentDataDF.to_html(header="true", table_id="table")
                return render_template("uebersichtsseite.html", filenames=filenames,
                                       tables=[
                                           currentDataDF.to_html(classes='table table-striped text-center', index=False,
                                                                 justify="center", col_space=20)],
                                       titles=currentDataDF.columns.values, tablename=table, user_list=user_list)
            else:
                filterlist = spaltenfilter.split(',')  # Trennt Eingabe in einzelne Spaltennamen
                zeilen = request.form.get('zeilen')
                newDF = currentDataDF
                if zeilen:
                    print("Zeilenauswahl")
                    newDF = zeilenAuswählen(newDF, zeilen)
                else:
                    print(zeilen)
                newDF = spaltenFiltern(newDF, filterlist)  # Spalten werden gefiltert
                newDF.to_html(header="true", table_id="table")  # Dataframe an HTML übergeben
                return render_template("uebersichtsseite.html", filenames=filenames,
                                       tables=[newDF.to_html(classes='table table-striped text-center', index=False,
                                                             justify="center", col_space=20)],
                                       titles=newDF.columns.values, table=table, tablename=table, user_list=user_list)
        elif request.method == 'POST' and request.form.get("subset"):
            DFname = "SubsetVon" + table + "_" + request.form.get("subset")
            databaseFileObject2.saveDataFrame(newDF, DFname)
            newDF.to_html(header="true", table_id="table")  # Dataframe an HTML übergeben
            return render_template("uebersichtsseite.html", filenames=filenames,
                                   tables=[newDF.to_html(classes='table table-striped text-center', index=False,
                                                         justify="center", col_space=20)],
                                   titles=newDF.columns.values, table=table, user_list=user_list)


        else:
            return render_template("uebersichtsseite.html", filenames=filenames,
                                   tables=[currentDataDF.to_html(classes='table table-striped text-center', index=False,
                                                                 justify="center", col_space=20)],
                                   titles=currentDataDF.columns.values,
                                   table=table, tablename=table, user_list=user_list)
    else:
        return redirect(url_for('index'))


@app.route('/uebersichtsseite', methods=["POST", "GET"])
def uebersichtsseite():
    if 'username' in session:
        try:
            current_username = session['username']
            databaseFileObject = DatabaseFile("Datenbank/" + current_username)
            filenames = databaseFileObject.getAllTableNamesAsList()

            databaseUserObject = DatabaseUser("Datenbank/my_logins4.db")
            user_list = databaseUserObject.getUser(current_username)

            if request.method == 'POST' and (
                    request.form.get('submit') == 'Refresh' or request.form.get('uebersichtsseite') == 'uebersichtsseite'):
                return render_template("uebersichtsseite.html", filenames=filenames, user_list=user_list)

            # if request.method == 'POST' and request.form.get('uebersichtsseite') == 'uebersichtsseite':
            #    return render_template("uebersichtsseite.html", filenames=filenames, user_list=user_list)

            # Dateiupload
            elif request.method == 'POST' and request.files['file']:
                file = request.files['file']
                namesplitted = file.filename.split('.')
                seperator = request.form.get('seperator')
                name = namesplitted[0]
                if name[0].isnumeric():
                    name = "a" + name
                fileExists = databaseFileObject.databaseIsExisting(name)
                if not fileExists:
                    if seperator is None:
                        databaseFileObject.saveFile(file, name, seperator=",")
                    else:
                        databaseFileObject.saveFile(file, name, seperator)
                        return render_template("uebersichtsseite.html", filenames=filenames, fileFlag=False,
                                               user_list=user_list)
                else:
                    return render_template("uebersichtsseite.html", filenames=filenames, fileFlag=fileExists,
                                           user_list=user_list)
            else:
                return render_template("uebersichtsseite.html", filenames=filenames, fileFlag=False, user_list=user_list)

        except BadRequestKeyError:
            return render_template("uebersichtsseite.html", filenames=filenames, fileFlag=False, user_list=user_list)
    else:
        return redirect(url_for('index'))


@app.route('/detailseite/<string:table>', methods=["POST", "GET"])
def detailseite(table):
    if 'username' in session:
        current_username = session[
            'username']  # der username wird gebraucht, um auf die richtige Datenbank zugreifen zu können
        databaseObject = DatabaseFile(
            "Datenbank/" + current_username)  # das databaseObject wird benutzt, um Methoden aus databaseFile aufzurufen
        currentDataDF = pd.read_sql_query("SELECT * FROM " + table, databaseObject.connection)
        my_list = currentDataDF.columns.values.tolist()  # Listen der column names für die Auswahl, welche Spalten für die Diagramme verwendet werden sollen
        ListeInt = currentDataDF.select_dtypes(
            include=np.number).columns.values.tolist()  # für die y-Achse können nur Zahlen verwendet werden -> nur columns mit numerics stehen zur Auswahl
        databaseUserObject = DatabaseUser("Datenbank/my_logins4.db")
        user_list = databaseUserObject.getUser(
            current_username)  # aktuelle User-Daten werden gebraucht, um den aktuellen User in der Nav bar anzuzeigen
        ChartObject = Chart(databaseObject, table)  # ChartObject wird verwendet, um die Diagramme zu erstellen

        try:
            if request.method == 'POST' and request.form.get("diagrammart"):
                diagrammart = request.form.get("diagrammart")  # kriegt aus Frontend, welches Diagrammart gewünscht ist, ruft
                #Methoden aus Chart.py auf, um das jeweilige Diagramm zu erstellen
                if diagrammart == "Balkendiagramm":
                    xAchse = request.form.get("xAchse")  # kriegt aus Frontend die column names die für x- bzw. y-Achse
                    # verwendet werden sollen
                    yAchse = request.form.get("yAchse")
                    ChartObject.makeBarChart(xAchse, yAchse)
                    return render_template("detailseite.html", Liste=my_list, ListeY=ListeInt, table=table,
                                           user_list=user_list)
                                #die Listen werden übergeben, für die Dropdowns auf der Detailseite, in denen man die Spalten für das Diagramm auswählen kann
                                #die table wird übergeben, um die Daten aus der Tabelle zu kriegen, user_list wird für den User in der Nav bar gebracuht
                elif diagrammart == "Tortendiagramm":
                    xAchse = request.form.get("xAchse")
                    yAchse = request.form.get("yAchse")
                    ChartObject.makePieChart(xAchse, yAchse)
                    return render_template("detailseite.html", Liste=my_list, ListeY=ListeInt, table=table,
                                           user_list=user_list)
                elif diagrammart == "Liniendiagramm":
                    xAchse = request.form.get("xAchse")
                    yAchse = request.form.get("yAchse")
                    ChartObject.makeLineChart(xAchse, yAchse)
                    return render_template("detailseite.html", Liste=my_list, ListeY=ListeInt, table=table,
                                           user_list=user_list)
                elif diagrammart == "Wordcloud":
                    ChartObject.makeWordCloud()
                    return render_template("detailseite.html", table=table, user_list=user_list, Liste=my_list,
                                           ListeY=ListeInt, )
                elif diagrammart == "Wortartenanalyse":
                    ChartObject.makeWortartenAnalyse()
                    return render_template("detailseite.html", table=table, user_list=user_list, Liste=my_list,
                                           ListeY=ListeInt, )
            else:
                return render_template("detailseite.html", Liste=my_list,
                                       ListeY=ListeInt, table=table,
                                       user_list=user_list)  # muss Liste übergeben, für erstes Landing

        except (Exception, UnboundLocalError) as e:
            # hier ist eine Anzeige  eingebaut die nur dann angezeit wird wenn ein Fehler bei den Diagrammen aufgetreten ist
            flash('Leider hat die Eingabe kein gültiges Ergebnis erzeugt.'
                  " Bitte überprüfen sie Ihre Eingabe")
            return render_template("detailseite.html", Liste=my_list, ListeY=ListeInt, table=table,
                                   user_list=user_list)  # muss Liste übergeben, für erstes Landing

    else:
        return redirect(url_for('index'))


@app.route("/impressum", methods=["POST", "GET"])
def impressum():
    if 'username' in session:
        current_username = session['username']
        databaseUserObject = DatabaseUser("Datenbank/my_logins4.db")
        user_list = databaseUserObject.getUser(current_username)
        return render_template("impressum.html", user_list=user_list)
    else:
        return redirect(url_for('index'))


@app.route("/benutzerhandbuch", methods=["POST"])
def benutzerhandbuch():
    if 'username' in session:
        current_username = session['username']
        databaseUserObject = DatabaseUser("Datenbank/my_logins4.db")
        user_list = databaseUserObject.getUser(current_username)
        return render_template("benutzerhandbuch.html", user_list=user_list)


@app.route("/logout", methods=["POST"])
def logout():
    if request.method == "POST" and request.form.get("delete") == "Account löschen":
        databaseUserObject.deleteUser("Logins", session['username'])
        os.remove(os.getcwd() + "/Datenbank/" + session['username'])
        redirect(url_for('login'))
        session.clear()
    return redirect(url_for("index"))


@app.errorhandler(404)
def page_not_found(error):
    flash("Keine Datei ausgewählt. Bitte Datei aus dem Dateiarchiv auswählen.")
    return redirect(url_for('uebersichtsseite'))


@app.errorhandler(500)
def page_error(error):
    flash("Ein Problem ist aufgetreten.")
    return redirect(url_for('login'))


databaseUserObject.clearData()

if __name__ == "__main__":
    app.run(debug=True)
