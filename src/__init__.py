import sqlite3

from flask import Flask, render_template, request, session, redirect, url_for

import os
import pandas as pd

from Datenbank import Datenbank

app = Flask(__name__, template_folder="./templates")
app.secret_key = "key"
extensions = set({'csv'})

db = Datenbank('Datenbank/my_logins4.db')

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
        # hashedpw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        # password_hash = hashedpw.decode("utf-8")

        if not db.checkIfUserExists(username):
            try:
                db.addUser(username, firstname, lastname, birthday, password)
                return redirect(url_for("login"))
            except sqlite3.IntegrityError as e:
                print("Fehler erschienen: ", e)
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
    #if 'username' in session:
     #   return render_template('uebersichtsseite.html', username=session['username'], Liste=["eins", "zwei"])
    connection = sqlite3.connect("Datenbank/file")
    data = connection.cursor()
    filename = connection.cursor()
    data.execute('SELECT * FROM Lager')
    filename.execute('SELECT name FROM sqlite_master WHERE type = "table"')
    columnnames = [tuple[0] for tuple in data.description]
    items = data.fetchall()
    filenames = filename.fetchall()
    if request.method == 'POST':
        file = request.files['file']
        name = file.filename
        db.saveFile(file, name)
    return render_template("uebersichtsseite.html", items=items, filenames=filenames, columnnames=columnnames)


@app.route('/detailseite', methods=["POST", "GET"])
def detailseite():
    return render_template('detailseite.html', Liste=list.columns.values, bild = "bewerbungen.png")


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("index"))


db.clearData()

if __name__ == "__main__":
    app.run(debug=True)
