from flask import Flask, render_template, request, session, redirect
from werkzeug.utils import secure_filename
import os
import pandas as pd

from src.accountcontroller import AccountController

app = Flask(__name__, template_folder="./templates")

ac_controller = AccountController()

app.secret_key = "key"
folder = os.getcwd() + "\\Uploads"
extensions = set({'csv'})


def allowed(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensions


@app.route("/")
def homepage():
    return render_template("homepage.html")


@app.route("/test")
def show_test():
    return "<h1>This is the test page.</h1>"


@app.route("/createAccount")
def show_create_account():
    return render_template("createAccount.html")


@app.route("/submitAccount", methods=["POST"])
def create_account():
    firstname = request.form.get("firstname")
    lastname = request.form.get("lastname")
    birthday = request.form.get("birthday")
    username = request.form.get("username")
    password = request.form.get("password")
    ac_controller.create_account(firstname=firstname, lastname=lastname, birthday=birthday, username=username,
                                 password=password)
    print(ac_controller.get_managed_accounts())
    ac_controller.print_accounts()

    return render_template("homepage.html")


@app.route("/login", methods=["POST"])
def login():
    entered_username = request.form.get("username")
    entered_password = request.form.get("password")
    account = ac_controller.login(username=entered_username, password=entered_password)
    if account != None:
        account.print_account()
        session["username"] = account.username
        session["firstname"] = account.user.firstname
        session["lastname"] = account.user.lastname
        return render_template("account.html", ac=account)
    return render_template("homepage.html")


@app.route('/upload', methods=["POST"])
def upload_file():
    return render_template('upload.html')


@app.route('/fileUploaded', methods=['GET', 'POST'])
def upload_file1():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if allowed(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(folder, filename))
    return render_template('success.html')


@app.route('/uebersichtsseite', methods=["POST", "GET"])
def uebersichtseite():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if allowed(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(folder, filename))

    return render_template('uebersichtsseite.html', Liste=os.listdir("Uploads")) #auf der Übersichtsseite wird temporär nicht die datei angezeigt


list = pd.read_csv(os.getcwd() + "/Uploads" + "/Testdatei.csv", sep=";", decimal=".", header=0) #hier muss statt Testdatei.csv filename stehen die ausgewählt wurde bzw auch das temporäre anzeigen lassen
list.columns.values

@app.route('/detailseite', methods=["POST", "GET"])
def detailseite():
    return render_template('detailseite.html', Liste=list.columns.values, bild = "bewerbungen.png")


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return render_template("homepage.html")


app.run(debug=True)
