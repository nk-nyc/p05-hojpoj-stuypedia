from flask import Flask, render_template
from flask import session, request, redirect, url_for
import data
import sqlite3
import json

app = Flask(__name__)

data.create_users_table()

@app.route("/")
def home():
    if 'username' in session:
        return redirect(url_for('home'))
    
    return redirect(url_for('login'))

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
