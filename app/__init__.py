from flask import Flask, render_template
from flask import session, request, redirect, url_for
from data import *
import sqlite3
import json
import datetime

app = Flask(__name__)
app.secret_key = 'supersecret'

create_users_table()
create_classes_table()
create_teachers_table()
create_events_table()

@app.route("/")
def prep():
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

        if auth(username, password): #check if already exists
            return render_template("register.html", error="Account already created.")

        if not (password == verify_pass):
            return render_template("register.html", error="Passwords must match.")

        if not '@nycstudents.net' in username:
            return render_template("register.html", error="Must be a valid nycstudents email.")

        if not len(password) > 7:
            return render_template("register.html", error="Passwords must be at least eight characters.")

        #now checking questions
        if (not (request.form.get('q1').strip().lower() == 'five') or not (request.form.get('q2').strip().lower() == 'six')) or (not (request.form.get('q3').strip().lower() == 'three') or not (request.form.get('q4').strip().lower() == 'six')):
            return render_template("register.html", error = "One or more answer is incorrect!")

        execute_register = register_user(username, password)
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
        if not auth(username, password):
            return render_template("login.html", error="Username or password is incorrect")

        # if password is correct redirect home
        session["username"] = username
        return redirect(url_for("home"))

    else:
        return render_template("login.html")

@app.route('/home', methods=['GET', 'POST'])
def home():
    print(session['username'])
    class_list = get_user_classes(session['username'][0])
    all_events = get_events(session['username'])
    today = datetime.date.today()

    upcoming = sorted(
        [e for e in all_events if e['start'] >= str(today)],
        key=lambda e: e['start']
    )[:5]
    if class_list:
        print(class_list)
        return render_template('home.html', your_classes=class_list, upcoming=upcoming)
    else:
        return render_template('home.html', upcoming=upcoming)

@app.route('/logout', methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/modify', methods=['GET', 'POST'])
def modify():
    # need to get class list here from user
    if 'username' not in session:
        return(url_for('login'))
    else:
        class_list = get_user_classes(session['username'][0])
        # get searched classes
        if 'search' in request.form:
            # gotta write search
            searched_classes = get_searched_classes(request.form.get('search'))
            if class_list:
                return render_template('modify.html', your_classes=class_list, searched=searched_classes)
            else:
                return render_template('modify.html', searched=searched_classes)
        if class_list:
            return render_template('modify.html', your_classes=class_list)
        else:
            return render_template('modify.html')


@app.route('/calendar', methods=['GET', 'POST'])
def calendar():
    if 'username' not in session:
        return(url_for('login'))
    return render_template('calendar.html')

@app.route('/events', methods=['GET'])
def get_calendar_events():
    events = get_events(session['username'])
    return json.dumps(events)

@app.route('/events', methods=['POST'])
def add_calendar_event():
    data = request.get_json()
    save_event(session['username'], data['title'], data['start'], data['color'], data['allDay'])
    return json.dumps({"status": "ok"})

@app.route('/findclass', methods=['GET', 'POST'])
def findclass():
    if 'username' not in session:
        return(url_for('login'))
    if 'search' in request.form:
        # gotta write search
        searched_classes = get_searched_classes(request.form.get('search'))
    return render_template('findclass.html')

@app.route('/addclass', methods=['GET', 'POST'])
def addclass():
    if 'username' not in session:
        return(url_for('login'))
    return render_template('addclass.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
