from flask import Flask, render_template, request, session, redirect, url_for
from werkzeug.utils import secure_filename
import os
import pandas as pd
import Datenbank

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
        #hashedpw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        #password_hash = hashedpw.decode("utf-8")
        Datenbank.AddUSER(username, firstname, lastname, birthday, password)
        return redirect(url_for("index"))
    else:
        return render_template("register.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        if Datenbank.check_User(username, password) == True:
            session['username'] = username
            Datenbank.changetimestamp()
        return redirect(url_for('uebersichtsseite'))
    else:
        return redirect(url_for('index'))

@app.route('/uebersichtsseite', methods=["POST", "GET"])
def uebersichtsseite():
    if 'username' in session:
        return render_template('uebersichtsseite.html', username=session['username'], Liste=os.listdir("Uploads"))
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if allowed(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(folder, filename))
            return render_template('uebersichtsseite.html', Liste=os.listdir("Uploads"))

    else:
        return redirect(url_for('login'))

list = pd.read_csv(os.getcwd() + "/Uploads" + "/Testdatei.csv", sep=";", decimal=".", header=0)
# hier muss statt Testdatei.csv filename stehen die ausgewählt wurde bzw auch das temporäre anzeigen lassen
list.columns.values


@app.route('/detailseite', methods=["POST", "GET"])
def detailseite():
    if 'username' in session:
        return render_template('detailseite.html',username=session['username'], Liste=list.columns.values, bild="bewerbungen.png")
    else:
        return redirect(url_for('login'))

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("index"))

Datenbank.cleardata()


if __name__ == "__main__":
    app.run(debug=True)
