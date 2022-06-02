import sqlite3

from flask import Flask, render_template, request, session, redirect, url_for

from src.database import Datenbank

from filtern import *

app = Flask(__name__, template_folder="./templates")
app.secret_key = "key"
extensions = set({'csv'})

def allowed(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensions

db = Datenbank('Datenbank/my_logins4.db')

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

        if not db.checkIfUserExists(username):
            try:
                db.addUser(username, firstname, lastname, birthday, password)
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
        if db.checkUsers(password, username) is True:
            session['username'] = username
            db.changeTimeStamp(username)
            return redirect(url_for('uebersichtsseite'))
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))


@app.route('/uebersichtsseite', methods=["POST", "GET"])
def uebersichtsseite():
    if 'username' in session:
        connection = sqlite3.connect("Datenbank/file")  # Verbindung zur Datenbank
        data = connection.cursor()  # cursor auf Daten in Datenbank
        filename = connection.cursor()  # cursor auf einzelne Filenames in DB
        data.execute('SELECT * FROM Lager')
        df = pd.read_sql_query('SELECT * FROM Lager', connection)  # Erzeugen von Dataframe
        df.to_html(header="true", table_id="table")  # Dataframe an HTML übergeben
        filename.execute('SELECT name FROM sqlite_master WHERE type = "table"')  # Datenbankabfrage für Filenames
        filenames = filename.fetchall()
        data.close()
        filename.close()

        if request.method == 'POST' and request.form.get("checkbox"):
            spalte = request.form.get("spalte")  # Eingabe von Website Spalte
            wert = request.form.get("wert")  # Eingabe von Website Wert
            operator = request.form.get("operator")  # Eingabe von Website Operator
            spaltenfilter = request.form.get("spaltenfilter")  # Eingabe von Website
            df1 = zeilenFiltern(df, spalte, wert, operator)  # Zeilen werden gefiltert
            if spaltenfilter == 'Alle' or None:  # Eingabe Alle anzeigen oder keine Eingabe (keine Eingabe funkioniert nicht)
                df = pd.read_sql_query("SELECT * from Lager", connection)  # alle anzeigen
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
                df = pd.read_sql_query("SELECT * from Lager", connection)  # alle anzeigen
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
            db.saveFile(file, name)
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


db.clearData()

if __name__ == "__main__":
    app.run(debug=True)
