from flask import Flask, render_template
from flask import session, request, redirect, url_for
import .data
import sqlite3
import json

app = Flask(__name__)

data.create_users_table()

@app.route("/")
def home():
    if 'username' in session:
        return redirect(url_for('home'))

    return redirect(url_for('login'))

@app.route("/register", methods=["GET", "POST"])
def register():
    if 'username' in session:
        return redirect(url_for('home'))
    if 'username' in request.form:
        username = request.form.get('username').strip().lower()
        password = request.form.get('password').strip()
        verify_pass = request.form.get('password2').strip()

        if not username or not password:
            return render_template("register.html", error="No username or password inputted")

        if data.auth(username, password): #check if already exists
            return render_template("register.html", error="Account already created.")

        if not (password == verify_pass):
            return render_template("register.html", error="Passwords must match.")

        if not '@nycstudents.net' in username:
            return render_template("register.html", error="Must be a valid nycstudents email.")

        if not len(password) > 7:
            return render_template("register.html", error="Passwords must be at least eight characters.")

        #now checking questions
        if not (request.form.get('q1').strip().lower() == 'five') or not (request.form.get('q2').strip().lower() == 'six'):
            return render_template("register.html", error = "One of more answer is incorrect!")

        execute_register = data.register_user(username, password)
        if execute_register == "success":
            print(execute_register)
            session['username'] = username
            return redirect(url_for("home"))
        else:
            return render_template("register.html", error = "An unknown error occurred.")

    else:
        return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login(): #code from p02 cerulean
    if 'username' in session:
        return redirect(url_for('home'))

    if 'username' in request.form:
        username = request.form.get('username').strip().lower()
        password = request.form.get('password').strip()

        # check if password is correct, if not then reload page
        if not data.auth(username, password):
            return render_template("login.html", error="Username or password is incorrect")

        # if password is correct redirect home
        session["username"] = username
        return redirect(url_for("home"))

    else:
        return render_template("login.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
