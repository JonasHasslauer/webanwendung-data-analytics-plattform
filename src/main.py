from flask import Flask, render_template, request, session, redirect
from werkzeug.utils import secure_filename
import os

from src.accountcontroller import AccountController

ac_controller = AccountController()

app.secret_key = "lelrel"
folder = "webanwendung-data-analytics-plattform/src/Dateien"
extensions = set({'csv'})


def allowed(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensions


@app.route("/")
def helloworld():
    return render_template("homepage.html")


@app.route("/test")
def show_test():
    return "<h1>This is the test page.</h1>"


# @app.route("/login", methods=["POST"])
# def show_test_button():
#    username = request.form.get("username")
#    return render_template("login.html", name = username)

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


@app.route('/readFile', methods=['POST'])       #unnötig, war nur ausprobiert
def read_file():
    personen = []
    with open("Datei.csv", "r") as file:        #die gespeicherte Datei auslesen ??
        for line in file:
            vorname, nachname, alter, geschlecht = line.split(",")
            person = {'vorname': vorname, 'nachname': nachname, 'alter': alter, 'geschlecht': geschlecht}
            personen.append(person)
    return render_template('read.html', personen=personen)


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return render_template("homepage.html")


app.run(debug=True)
