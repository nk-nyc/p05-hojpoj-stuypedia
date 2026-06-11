from flask import Flask, render_template
from flask import session, request, redirect, url_for
from data import *
import sqlite3
import json
import datetime
import os
import secrets
from dotenv import load_dotenv
from authlib.integrations.flask_client import OAuth

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
oauth = OAuth(app)

google = oauth.register(
    name='google',
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)
create_users_table()
create_classes_table()
create_teachers_table()
create_events_table()
create_student_classes_table()
create_class_data_table()

@app.route('/auth/login')
def google_login():
    redirect_uri = os.getenv('GOOGLE_REDIRECT_URI')
    return google.authorize_redirect(redirect_uri, prompt='select_account')

@app.route('/auth/callback')
def google_callback():
    token = google.authorize_access_token()
    user_info = token['userinfo']
    email = user_info['email']
    
    #if not email.endswith('@nycstudents.net'):
    #    return redirect(url_for('login') + '?error=Must use nycstudents email')
    
    # Auto-register if needed
    if user_exists(email):
        session['username'] = email
        return redirect(url_for('home'))
    
    session['pending_google_email'] = email
    return redirect(url_for('google_verify'))

@app.route('/google-verify', methods=['GET', 'POST'])
def google_verify():
    if 'pending_google_email' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        if (not (request.form.get('q1').strip().lower() == 'five') or 
            not (request.form.get('q2').strip().lower() == 'six')) or \
           (not (request.form.get('q3').strip().lower() == 'three') or 
            not (request.form.get('q4').strip().lower() == 'six')):
            return render_template('google_verify.html', error='One or more answer is incorrect!')
        
        email = session.pop('pending_google_email')
        register_user(email, secrets.token_hex(16))
        session['username'] = email
        return redirect(url_for('home'))
    
    return render_template('google_verify.html')

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

        if username == 'stuypedia_admin' and auth(username, password):
            session["username"] = "stuypedia_admin"
            return redirect(url_for('home'))

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
    class_list = get_user_classes(session['username'])
    if session['username'] == 'stuypedia_admin':
        class_list = get_all_student_classes()
        return render_template('admin_home.html', classes=class_list)
    all_events = get_events(session['username'])
    today = datetime.date.today()

    upcoming = sorted(
        [e for e in all_events if e['start'] >= str(today)],
        key=lambda e: e['start']
    )[:5]
    if class_list:
        return render_template('home.html', your_classes=class_list, upcoming=upcoming)
    else:
        return render_template('home.html', upcoming=upcoming)

@app.route('/logout', methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        username = session['username']

        # Current password
        if not auth(username, current_password):
            return render_template(
                'profile.html',
                username=username,
                error='Current password is incorrect.'
            )

        # Passwords match
        if new_password != confirm_password:
            return render_template(
                'profile.html',
                username=username,
                error='New passwords do not match.'
            )

        # Check length
        if len(new_password) < 8:
            return render_template(
                'profile.html',
                username=username,
                error='Password must be at least 8 characters.'
            )

        change_password(username, new_password)

        return render_template(
            'profile.html',
            username=username,
            success='Password updated successfully.'
        )

    return render_template(
        'profile.html',
        username=session['username']
    )

def change_password(username, new_password):
	db = sqlite3.connect(DB_FILE)
	c = db.cursor()
	
	hashed_password = hashlib.sha256(
		new_password.encode('utf-8')
	).hexdigest()
	
	c.execute(
		'UPDATE users SET password = ? WHERE username = ?',
		(hashed_password, username)
	)
	db.commit()
	db.close()


@app.route('/delete_class/<int:class_id>', methods=['DELETE'])
def delete_class(class_id):
    delete_classid(class_id)
    return json.dumps({"status": "ok"})

@app.route('/delete_student_class/<int:class_id>', methods=['DELETE'])
def delete_student_class(class_id):
    delete_student_classid(class_id)
    return json.dumps({"status": "ok"})

@app.route('/approve_class/<int:class_id>', methods=['POST'])
def approve_class(class_id):
    approve_classid(class_id)
    return json.dumps({"status": "ok"})

@app.route('/classlist', methods=['GET', 'POST'])
def classlist():
    if not session['username'] == 'stuypedia_admin':
        return redirect(url_for(home))
    classlist = get_all_classes()
    for i in range(len(classlist)):
        classlist[i] = list(classlist[i])
        classlist[i][3] = fix_grade_format(classlist[i][3])
    return render_template('classlist.html', classes=classlist)

@app.route('/createclass', methods=["GET", "POST"])
def create_class():
    if not session['username'] == 'stuypedia_admin':
        return redirect(url_for(home))
    if len(request.form.getlist('grade')) == 0:
        return render_template('createclass.html', error='Please select at least one grade.')
    # create class
    if 'name' in request.form:
        name = request.form.get('name')
        teachers = request.form.get('teachers')
        grade = request.form.getlist('grade')
        subject = request.form.get('subject')
        if not check_class_for_uniqueness(name):
            return render_template('createclass.html', error='Class name already exists.')
        create(name, teachers, grade, subject)
    return render_template('createclass.html')

@app.route('/modify', methods=['GET', 'POST'])
def modify():
    # need to get class list here from user
    if 'username' not in session:
        return(url_for('login'))
    else:
        class_list = get_user_classes(session['username'])
        # get searched classes
        if 'search' in request.form:
            # gotta write search
            searched_classes = get_searched_classes(request.form.get('search'))

            if class_list:
                for i in range(len(class_list)):
                    name = get_class_name_from_id(class_list[i])
                    class_list[i] = [name, class_list[i]]
                return render_template('modify.html', your_classes=class_list, searched=searched_classes)
            else:
                return render_template('modify.html', searched=searched_classes)
        if class_list:
                for i in range(len(class_list)):
                    class_list[i] = [get_class_name_from_id(class_list[i]), class_list[i]]
                return render_template('modify.html', your_classes=class_list)
        return render_template('modify.html', your_classes=class_list)


@app.route('/calendar', methods=['GET', 'POST'])
def calendar():
    if 'username' not in session:
        return redirect(url_for('login'))
    class_ids = get_user_classes(session['username']) or []
    user_classes = [(get_class_name_from_id(cid), cid) for cid in class_ids]
    return render_template('calendar.html', user_classes=user_classes)

@app.route('/events', methods=['GET'])
def get_calendar_events():
    events = get_events(session['username'])
    return json.dumps(events)

@app.route('/events', methods=['POST'])
def add_calendar_event():
    data = request.get_json()
    new_id = save_event(
        session['username'],
        data['title'], data['start'],
        data.get('end'), data['color'],
        data.get('linked_class'), data['allDay'],
        is_public=int(data.get('is_public', 0))
    )
    return json.dumps({"status": "ok", "id": new_id})

@app.route('/events/<int:event_id>', methods=['DELETE'])
def remove_calendar_event(event_id):
    delete_event(event_id, session['username'])
    return json.dumps({"status": "ok"})

@app.route('/events/<int:event_id>', methods=['PUT'])
def update_calendar_event(event_id):
    data = request.get_json()
    update_event(event_id, session['username'],
                 data['title'], data['start'], data.get('end'),
                 data['color'], data.get('linked_class'), data['allDay'],
                 data.get('is_public', 0))
    return json.dumps({"status": "ok"})

@app.route('/shared-events', methods=['GET'])
def get_shared_events():
    events = get_shared_events_for_user(session['username'])
    return json.dumps(events)

@app.route('/findclass', methods=['GET', 'POST'])
def findclass():
    if 'username' not in session:
        return(url_for('login'))
    if 'search' in request.form:
        # gotta write search
        searched_classes = get_searched_classes(request.form.get('search'))
        return render_template('findclass.html', searched=searched_classes)
    return render_template('findclass.html')

@app.route('/addclass/<int:class_id>', methods=['POST', 'GET'])
def addClass(class_id):
    add_user_class(session['username'], class_id)
    return json.dumps({"status": "ok"})

@app.route('/addclass', methods=['GET', 'POST'])
def addclass():
    if 'username' not in session:
        return(url_for('login'))
    if 'name' in request.form:
        name = request.form.get('name')
        teachers = request.form.get('teachers')
        grade = request.form.getlist('grade')
        subject = request.form.get('subject')
        create_student_class(name, teachers, grade, subject)

    return render_template('addclass.html')

@app.route('/editclass/<int:class_id>', methods=['GET', 'POST'])
def edit_class(class_id):
    if 'username' not in session:
        return redirect('/login')
    if not session['username'] == 'stuypedia_admin':
        return redirect('/home')
    class_data = get_class_info(class_id)
    new_subj = class_data[1]
    new_grades = class_data[2]
    new_teachers = class_data[3]
    if request.method == 'POST':
        if not request.form.get('subject') == '':
            new_subj = request.form.get('subject')
        if 'grade' in request.form:
            new_grades = request.form.getlist('grade')
        if 'teachers' in request.form:
            new_teachers = request.form.get('teachers')
        update_class(class_id, new_subj, new_grades, new_teachers)
    return render_template('editclass.html', class_data=class_data)

@app.route('/events/<int:event_id>/visibility', methods=['PUT'])
def update_event_visibility(event_id):
    data = request.get_json()
    update_event_visibility_db(event_id, session['username'], data['is_public'])
    return json.dumps({"status": "ok"})

@app.route('/classpage/<int:class_id>', methods=['GET', 'POST'])
def classpage(class_id):
    if 'username' not in session:
        return(redirect('/login'))
    saved = False
    prettified_data = None
    if class_saved_by_user(class_id, session['username']):
        saved = True
    if review_already_made(class_id, user_id_from_username(session['username'])):
        prettified_data, responders, resources = prettify_class_data(class_id)
        #data by teacher
        teacher_data = {}
        teachers = get_teachers_for_class(class_id)

        for teacher in teachers:
            teacher_data[teacher] = prettify_class_data_by_teacher(class_id, teacher)
        return render_template('classpage.html', teacher_data = teacher_data, class_info=get_class_info(class_id), error='You have already reviewed this class.', saved=saved, class_data=prettified_data, responders=responders, resources=fix_resource_names(resources))

    if request.method == 'POST':
        teacher = request.form.get('teacher')
        difficulty = request.form.get('difficulty')
        enjoyment = request.form.get('enjoyment')
        workload = request.form.get('workload')
        hours = request.form.get('hours')
        teaching_quality = request.form.get('teaching_quality')
        if not request.form.get('resources'):
            if get_class_data(class_id):
                prettified_data, responders, resources = prettify_class_data(class_id)
            else:
                responders=None
                resources=None
            teacher_data = {}
            teachers = get_teachers_for_class(class_id)
            for teacher in teachers:
                teacher_data[teacher] = prettify_class_data_by_teacher(class_id, teacher)
            return render_template('classpage.html', res_error='Please select at least one resource.', teacher_data = teacher_data, class_info=get_class_info(class_id), saved=saved, class_data=prettified_data, responders=responders, resources=fix_resource_names(resources))
        resources = request.form.getlist('resources')
        # Save the review to the database
        save_class_review(class_id, user_id_from_username(session['username']), teacher, difficulty, enjoyment, workload, hours, teaching_quality, resources)
        return redirect('/classpage/' + str(class_id))
    saved = class_saved_by_user(class_id, session['username'])
    class_info = get_class_info(class_id)

    if get_class_data(class_id):
        prettified_data, responders, resources = prettify_class_data(class_id)
    else:
        teacher_data = {}
        teachers = get_teachers_for_class(class_id)
        return render_template('classpage.html', teacher_data = teacher_data, class_info=get_class_info(class_id), saved=saved, class_data=None, responders=None, resources=None)

    #data by teacher
    teacher_data = {}
    teachers = get_teachers_for_class(class_id)

    if len(teachers) > 1:
        for teacher in teachers:
            teacher_data[teacher] = prettify_class_data_by_teacher(class_id, teacher)
    else:
        teacher_data[teachers[0]] =prettify_class_data_by_teacher(class_id, teachers[0])
    #gotta render class data
    return render_template('classpage.html', teacher_data = teacher_data, class_info=get_class_info(class_id), saved=saved, class_data=prettified_data, responders=responders, resources=fix_resource_names(resources))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
