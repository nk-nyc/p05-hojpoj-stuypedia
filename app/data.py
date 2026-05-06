import sqlite3                      # enable control of an sqlite database
import hashlib                      # for consistent hashes
import secrets                      # to generate ids

DB_FILE="data.db"

def create_table(contents):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute(contents)
    db.commit()
    db.close()

def create_users_table():

    contents =  """
                CREATE TABLE IF NOT EXISTS users (
                    username        TEXT    NOT NULL UNIQUE,
                    password        TEXT    NOT NULL,
                    id              INTEGER NOT NULL    PRIMARY KEY,
                    anon_user       TEXT    NOT NULL
                )"""
    create_table(contents)


def clean_list(raw_output):

    clean_output = []

    for lst in raw_output:
        for item in lst:
            if str(item) != 'None' and item != "":
                clean_output += [item]

    return clean_output

def user_exists(username):
    all_users = get_all_users()
    for user in all_users:
        if (user == username):
            return True
    return False

def get_all_users():

    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    data = c.execute('SELECT username FROM users').fetchall()

    db.commit()
    db.close()

    return clean_list(data)
# checks if provided password in login attempt matches user password
def auth(username, password):

    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    if not user_exists(username):
        db.commit()
        db.close()

        #raise ValueError("Username does not exist")
        return False

    # use ? for unsafe/user provided variables
    passpointer = c.execute('SELECT password FROM users WHERE username = ?', (username,))
    real_pass = passpointer.fetchone()[0]

    db.commit()
    db.close()

    password = password.encode('utf-8')

    # hash password here
    if real_pass != str(hashlib.sha256(password).hexdigest()):
        #raise ValueError("Incorrect password")
        return False

    return True