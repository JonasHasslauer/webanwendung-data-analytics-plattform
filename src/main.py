from flask import Flask, render_template, request, session, redirect, url_for
from werkzeug.utils import secure_filename
import os
import pandas as pd
import sqlite3 as sql
import bcrypt

connect = sql.connect("Datenbank/my_logins4.db")
cursor = connect.cursor()
CreateTable = "CREATE TABLE if not EXISTS Logins(username VARCHAR(10) PRIMARY KEY not null, firstname VARCHAR(100) not null, lastname VARCHAR (100) not null, birthday DATE not null, password BINARY(64) not null)";
cursor.execute(CreateTable)
connect.commit()


def AddUSER(username, firstname, lastname, birthday, password):
    con = sql.connect("Datenbank/my_logins4.db")
    cur = con.cursor()
    cur.execute("INSERT INTO Logins(username,firstname, lastname, birthday,password) VALUES (?,?,?,?,?)",
                (username, firstname, lastname, birthday, password))
    con.commit()
    con.close()


def check_User(username, password):
    con = sql.connect("Datenbank/my_logins4.db")
    cur = con.cursor()
    cur.execute("SELECT username, password FROM Logins WHERE username=? and password=?", (username, password))
    result = cur.fetchall()
    if result:
        return True
    else:
        return False


app = Flask(__name__, template_folder="./templates")
app.secret_key = "key"
folder = os.getcwd() + "\\Uploads"
extensions = set({'csv'})


def allowed(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensions


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

        AddUSER(username, firstname, lastname, birthday, password)
        return redirect(url_for("index"))

    else:
        return render_template("register.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if check_User(username, password):
            session["username"] = username
        return redirect(url_for("uebersichtsseite"))
    else:
        redirect(url_for("index"))


@app.route('/uebersichtsseite', methods=["POST", "GET"])
def uebersichtsseite():
    if 'username' in session:
        return render_template("uebersichtsseite.html", username=session['username'])
        if request.method == 'POST':
            if 'file' not in request.files:
                return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if allowed(file.filename):
            filename = secure_filename(file.filename)
        file.save(os.path.join(folder, filename))
        return render_template('uebersichtsseite.html', Liste=os.listdir(
            "Uploads"))  # auf der Übersichtsseite wird temporär nicht die datei angezeigt
    else:
        return "Username oder Passwort ist falsch!"


list = pd.read_csv(os.getcwd() + "/Uploads" + "/Testdatei.csv", sep=";", decimal=".", header=0)
# hier muss statt Testdatei.csv filename stehen die ausgewählt wurde bzw auch das temporäre anzeigen lassen
list.columns.values


@app.route('/detailseite', methods=["POST", "GET"])
def detailseite():
    return render_template('detailseite.html', Liste=list.columns.values, bild="bewerbungen.png")


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
