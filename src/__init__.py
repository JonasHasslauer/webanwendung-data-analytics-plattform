import os
import sqlite3

import matplotlib.pyplot as plt
from flask import Flask, render_template, request, session, redirect, url_for, flash, abort
from werkzeug.exceptions import BadRequestKeyError

from src.Database import DatabaseUser
from src.Database import DatabaseFile

from Chart import *
from filtern import *
from PIL import Image

from initialisierung_seaborn import *
import seaborn as sns

app = Flask(__name__, template_folder="./templates")
app.secret_key = "key"

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
                if len(username) <= 10:
                    try:
                        databaseUserObject.addUser(username, firstname, lastname, birthday, password)
                        flash("Account erfolgreich registriert.", 'success')
                        return redirect(url_for("login"))
                    except sqlite3.IntegrityError as e:
                        flash("username bereits vergeben. Bitte anderen username benutzen.", 'error')
                        return redirect(url_for("register"))
                else: #Nutzer muss kürzeren Namen wählen
                    flash("username ist zu lang, der username darf höchstens 10 Zeichen haben", 'error')
                    return redirect(url_for("register"))
            else:  # Nutzer muss sich mit anderem Namen registrieren
                flash("username bereits vergeben. Bitte anderen username benutzen.", 'info')
                return render_template(url_for("register"))
        else:
            flash("username enthält '/', bitte melden Sie sich mit einem anderen username an", 'error')
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
            flash("Benutzerdaten überprüfen oder einen Account anlegen.", 'info')
            return redirect(url_for('login'))
    else:
        return redirect(url_for('index'))


@app.route('/uebersichtsseite/<string:table>', methods=["POST", "GET"])
def specUebersicht(table):
    if 'username' in session:
        current_username = session['username']
        databaseFileObject = DatabaseFile("Datenbank/" + current_username)
        filenames = databaseFileObject.getAllTableNamesAsList()
        currentDataDF = pd.read_sql_query("SELECT * FROM " + table, databaseFileObject.connection)

        databaseUserObject = DatabaseUser("Datenbank/my_logins4.db")
        user_list = databaseUserObject.getUser(current_username)

        if request.form.get('submit') == 'Überschriften':
            isHeader = True
        elif request.form.get('submit') == 'Keine Überschriften':
            isHeader = False
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
                newDF = zeilenAuswählen(newDF, zeilen)

            if operator == '> median' or '< median' or '> oQuartil' or '< oQuartil' or '> uQuartil' or '< oQuartil':
                zeilenFilterDF = zeilenfilternStatisch(newDF, spalte,  operator)

            else:
                zeilenFilterDF = zeilenFiltern(newDF, spalte, int(wert), operator)  # Zeilen werden gefiltert

            if spaltenfilter == 'Alle' or None:  # Eingabe Alle anzeigen oder keine Eingabe (keine Eingabe funkioniert nicht)
                currentDataDF.to_html(header="true", table_id="table")
                return render_template("uebersichtsseite.html", filenames=filenames,
                                       tables=[
                                           currentDataDF.to_html(classes='table table-striped text-center', index=False,
                                                                 justify="center", col_space=20, header=isHeader)],
                                       titles=currentDataDF.columns.values, tablename=table, user_list=user_list)
            else:
                filterlist = spaltenfilter.split(',')  # Trennt Eingabe in einzelne Spaltennamen
                newDF = spaltenFiltern(zeilenFilterDF, filterlist)  # Spalten werden gefiltert
                newDF.to_html(header="true", table_id="table")  # Dataframe an HTML übergeben
                return render_template("uebersichtsseite.html", filenames=filenames,
                                       tables=[newDF.to_html(classes='table table-striped text-center', index=False,
                                                             justify="center", col_space=20, header=isHeader)],
                                       titles=newDF.columns.values, table=table, tablename=table, user_list=user_list, header=isHeader)

        # Zeilenfilter
        elif request.method == 'POST' and request.form.get("spalte"):
            spalte = request.form.get("spalte")  # Eingabe von Website Spalte
            wert = request.form.get("wert")  # Eingabe von Website Wert
            operator = request.form.get("operator")  # Eingabe von Website Operator
            zeilen = request.form.get('zeilen')
            newDF = currentDataDF
            if zeilen:
                newDF = zeilenAuswählen(newDF, zeilen)
            if operator == '> median' or '< median' or '> oQuartil' or '< oQuartil' or '> uQuartil' or '< oQuartil':
                zeilenFilterDF = zeilenfilternStatisch(newDF, spalte, operator)

            else:
                zeilenFilterDF = zeilenFiltern(newDF, spalte, int(wert), operator)  # Zeilen werden gefiltert

            newDF.to_html(header="true", table_id="table")  # Dataframe an HTML übergeben
            return render_template("uebersichtsseite.html", filenames=filenames,
                                   tables=[newDF.to_html(classes='table table-striped text-center', index=False,
                                                         justify="center", col_space=20, header=isHeader)], titles=newDF.columns.values,
                                   table=table, tablename=table, user_list=user_list)

        # Spaltenfilter
        elif request.method == 'POST' and request.form.get("spaltenfilter"):
            spaltenfilter = request.form.get("spaltenfilter")
            if spaltenfilter == 'Alle' or None:  # Eingabe Alle anzeigen oder keine Eingabe (keine Eingabe funkioniert nicht)
                currentDataDF.to_html(header="true", table_id="table")
                return render_template("uebersichtsseite.html", filenames=filenames,
                                       tables=[
                                           currentDataDF.to_html(classes='table table-striped text-center', index=False,
                                                                 justify="center", col_space=20, header=isHeader)],
                                       titles=currentDataDF.columns.values, tablename=table, user_list=user_list, header=isHeader)
            else:
                filterlist = spaltenfilter.split(',')  # Trennt Eingabe in einzelne Spaltennamen
                zeilen = request.form.get('zeilen')
                newDF = currentDataDF
                if zeilen:
                    newDF = zeilenAuswählen(newDF, zeilen)
                newDF = spaltenFiltern(newDF, filterlist)  # Spalten werden gefiltert
                newDF.to_html(header="true", table_id="table")  # Dataframe an HTML übergeben
                return render_template("uebersichtsseite.html", filenames=filenames,
                                       tables=[newDF.to_html(classes='table table-striped text-center', index=False,
                                                             justify="center", col_space=20, header=isHeader)],
                                       titles=newDF.columns.values, table=table, tablename=table, user_list=user_list, header=isHeader)


        #hier wird die DAtei, die aktuell ausgewählt ist (table) aus der Datenbank entfernt, wenn der Button dafür gedrückt wird
        elif request.method == 'POST' and request.form.get("deletefile"):
            databaseFileObject.deleteFile(table)
            flash("Die ausgewählte Datei wurde aus der Datenbank entfernt.", 'info')
            return render_template("uebersichtsseite.html", filenames=filenames, user_list=user_list)


        elif request.method == 'POST' and request.form.get("subset"):
            DFname = "SubsetVon" + table + "_" + request.form.get("subset")     #unter diesem Namen wird das Subset gespeichert
            databaseFileObject.saveDataFrame(newDF, DFname)                     #hier wird die Methode aufgerufen, die das Subset dann als neues Dataframe speichert
            newDF.to_html(header="true", table_id="table")  # Dataframe an HTML übergeben
            flash('Das Subset wurde abgespeichert. Bitte refreshen Sie das Dateiarchiv, um es zu sehen', 'success')
            return render_template("uebersichtsseite.html", filenames=filenames,
                                   tables=[newDF.to_html(classes='table table-striped text-center', index=False,
                                                        justify="center", col_space=20, header=isHeader)],
                                   titles=newDF.columns.values, table=table, user_list=user_list)



        else:
            return render_template("uebersichtsseite.html", filenames=filenames,
                                   tables=[currentDataDF.to_html(classes='table table-striped text-center', index=False,
                                                                 justify="center", col_space=20, header=isHeader)],
                                   titles=currentDataDF.columns.values,
                                   table=table, tablename=table, user_list=user_list)
    else:
        abort(401)
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
                    request.form.get('submit') == 'Refresh' or request.form.get(
                'uebersichtsseite') == 'uebersichtsseite'):
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
                        return render_template("uebersichtsseite.html", filenames=filenames,
                                               user_list=user_list)
                else:
                    flash("Es existiert bereits eine Datei mit diesem Namen, diese wurde nicht überschrieben.", 'error')
                    return render_template("uebersichtsseite.html", filenames=filenames,
                                           user_list=user_list)
            else:
                return render_template("uebersichtsseite.html", filenames=filenames, user_list=user_list)

        except BadRequestKeyError:
            return render_template("uebersichtsseite.html", filenames=filenames, user_list=user_list)
    else:
        abort(401)
        return redirect(url_for('index'))


@app.route('/detailseite/<string:table>', methods=["POST", "GET"])
def detailseite(table):
    if 'username' in session:

        #zunachst wird ein kleines Diagramm erstellt um seaborn zu initialisieren
        #Variante 1:
        #hier wird ein Wordcloud Diagramm erstellet

        text_3 = "Test"
        #wordcloudErstellen(text_3)

        #Variante 2:
        #hier wird eine seaborn balkendiagramm erstellt
        initialisierungSeaborn()


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
                diagrammart = request.form.get(
                    "diagrammart")  # kriegt aus Frontend, welches Diagrammart gewünscht ist, ruft
                # Methoden aus Chart.py auf, um das jeweilige Diagramm zu erstellen
                if diagrammart == "Balkendiagramm":
                    xAchse = request.form.get("xAchse")  # kriegt aus Frontend die column names die für x- bzw. y-Achse
                    # verwendet werden sollen
                    yAchse = request.form.get("yAchse")
                    ChartObject.makeBarChart(xAchse, yAchse)
                    return render_template("detailseite.html", bild = 'balkendiagramm.png', Liste=my_list, ListeY=ListeInt, table=table,
                                           user_list=user_list)
                    # die Listen werden übergeben, für die Dropdowns auf der Detailseite, in denen man die Spalten für das Diagramm auswählen kann
                    # die table wird übergeben, um die Daten aus der Tabelle zu kriegen, user_list wird für den User in der Nav bar gebracuht
                elif diagrammart == "Tortendiagramm":
                    xAchse = request.form.get("xAchse")
                    yAchse = request.form.get("yAchse")
                    ChartObject.makePieChart(xAchse, yAchse)
                    return render_template("detailseite.html", bild='piechart.png', Liste=my_list, ListeY=ListeInt, table=table,
                                           user_list=user_list)
                elif diagrammart == "Liniendiagramm":
                    xAchse = request.form.get("xAchse")
                    yAchse = request.form.get("yAchse")
                    ChartObject.makeLineChart(xAchse, yAchse)
                    return render_template("detailseite.html", bild='liniendiagramm.png', Liste=my_list, ListeY=ListeInt, table=table,
                                           user_list=user_list)
                elif diagrammart == "Wordcloud":
                    ChartObject.makeWordCloud()
                    return render_template("detailseite.html", table=table, bild='wordcloud.png', user_list=user_list, Liste=my_list,
                                           ListeY=ListeInt)
                elif diagrammart == "Wortartenanalyse":
                    ChartObject.makeWortartenAnalyse()
                    return render_template("detailseite.html", table=table, bild='wortartenanalyse.png', user_list=user_list, Liste=my_list,
                                           ListeY=ListeInt)
            else:
                return render_template("detailseite.html", Liste=my_list,
                                       ListeY=ListeInt, table=table, bild='detailseite.jpg',
                                       user_list=user_list)  # muss Liste übergeben, für erstes Landing

        except (Exception, UnboundLocalError) as e:
            # hier ist eine Anzeige  eingebaut die nur dann angezeit wird wenn ein Fehler bei den Diagrammen aufgetreten ist
            flash('Leider hat die Eingabe kein gültiges Ergebnis erzeugt.'
                  " Bitte überprüfen sie Ihre Eingabe", 'error')
            return render_template("detailseite.html", Liste=my_list, ListeY=ListeInt, table=table,
                                   user_list=user_list)  # muss Liste übergeben, für erstes Landing

    else:
        abort(401)
        return redirect(url_for('index'))


@app.route("/impressum", methods=["POST", "GET"])
def impressum():
    if 'username' in session:
        current_username = session['username']
        databaseUserObject = DatabaseUser("Datenbank/my_logins4.db")
        user_list = databaseUserObject.getUser(current_username)
        return render_template("impressum.html", user_list=user_list)
    else:
        abort(401)
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
        if os.path.exists('static/liniendiagramm.png'):
            os.remove('static/liniendiagramm.png')
        if os.path.exists('static/piechart.png'):
            os.remove('static/piechart.png')
        if os.path.exists('static/wordcloud.png'):
            os.remove('static/wprdcloud.png')
        if os.path.exists('static/wortartenanalyse.png'):
            os.remove('static/wortartenanalyse.png')
        if os.path.exists('static/balkendiagramm.png'):
            os.remove('static/balkendiagramm.png')

        redirect(url_for('login'))
        session.clear()
    return redirect(url_for("index"))

"""
@app.errorhandler(404)
def page_not_found(error):
    flash("Keine Datei ausgewählt. Bitte Datei aus dem Dateiarchiv auswählen.", 'info')
    return redirect(url_for('uebersichtsseite'))
"""

@app.errorhandler(500)
def page_error(error):
    flash("Ein Problem ist aufgetreten.", 'error')
    return redirect(url_for('login'))

@app.errorhandler(400)
def bad_Request(error):
    flash("Request nicht möglich auszuführen.", 'error')
    return redirect(url_for('login'))

@app.errorhandler(401)
def no_Session(error):
    flash("Bitte erst anmelden oder  registirieren.", 'error')
    return redirect(url_for('login'))

@app.errorhandler(504)
def timeout(error):
    flash("Länge der Wartezeit für den Request abgelaufen. Bitte erneut anmelden.", 'error')
    return redirect(url_for('login'))



databaseUserObject.clearData()

if __name__ == "__main__":
    app.run(debug=True)
