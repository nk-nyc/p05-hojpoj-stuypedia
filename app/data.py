from operator import ge
import sqlite3                      # enable control of an sqlite database
import hashlib                      # for consistent hashes
import secrets                      # to generate ids
import random
from flask import request
import math
import re

DB_FILE="data.db"

def create_table(contents):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute(contents)
    db.commit()
    db.close()

def generate_anon():
    animal_list = ["aardvark","albatross","alligator","alpaca","anaconda","angelfish","ant","anteater","antelope","ape","armadillo","auk","axolotl","baboon","badger","barracuda","bat","bear","beaver","bee","bison","blackbird","boar","bobcat","buffalo","butterfly","camel","capybara","caracal","caribou","cassowary","cat","caterpillar","catfish","cattle","chameleon","cheetah","chickadee","chicken","chimpanzee","chinchilla","chipmunk","cicada","clam","cobra","cod","coyote","crab","crane","crocodile","crow","cuckoo","deer","dingo","dog","dolphin","donkey","dormouse","dove","dragonfly","duck","dugong","eagle","earthworm","echidna","eel","elephant","elk","emu","falcon","ferret","finch","fish","flamingo","flea","fly","fox","frog","gaur","gazelle","gecko","gerbil","giraffe","gnat","gnu","goat","goldfish","goose","gorilla","grasshopper","guinea pig","gull","hamster","hare","hawk","hedgehog","heron","herring","hippopotamus","hornet","horse","hummingbird","hyena","ibex","iguana","impala","jackal","jaguar","jellyfish","kangaroo","kingfisher","koala","komodo dragon","kookaburra","kouprey","krill","ladybug","lemur","leopard","lion","llama","lobster","locust","lynx","macaw","magpie","mallard","manatee","mandrill","mantis","marlin","marmoset","marmot","mayfly","meerkat","mink","mole","mongoose","monkey","moose","mosquito","mouse","mule","narwhal","newt","nightingale","ocelot","octopus","opossum","orangutan","oryx","ostrich","otter","owl","ox","oyster","panther","parrot","partridge","peacock","pelican","penguin","pheasant","pig","pigeon","pony","porcupine","porpoise","quail","rabbit","raccoon","rat","raven","reindeer","rhinoceros","rook","salamander","salmon","sandpiper","sardine","scorpion","seahorse","seal","shark","sheep","shrew","shrimp","skunk","sloth","slug","snail","snake","sparrow","spider","squid","squirrel","starfish","stingray","stork","swallow","swan","tapir","tarsier","termite","tiger","toad","trout","tuna","turkey","turtle","viper","vulture","wallaby","walrus","wasp","weasel","whale","wolf","wombat","woodpecker","worm","wren","yak","zebra"]

    adjective_list = ["adorable","adventurous","aggressive","agreeable","alert","alive","amused","angry","annoyed","anxious","arrogant","ashamed","attractive","average","awful","beautiful","better","bewildered","black","bloody","blue","blue-eyed","blushing","bored","brainy","brave","breakable","bright","busy","calm","careful","cautious","charming","cheerful","clean","clear","clever","cloudy","clumsy","colorful","combative","comfortable","concerned","condemned","confused","cooperative","courageous","crazy","creepy","crowded","cruel","curious","cute","dangerous","dark","dead","defeated","defiant","delightful","depressed","determined","different","difficult","disgusted","distinct","disturbed","dizzy","doubtful","drab","dull","eager","easy","elated","elegant","embarrassed","enchanting","encouraging","energetic","enthusiastic","envious","evil","excited","expensive","exuberant","fair","faithful","famous","fancy","fantastic","fierce","filthy","fine","foolish","fragile","frail","frantic","friendly","frightened","funny","gentle","gifted","glamorous","gleaming","glorious","good","gorgeous","graceful","grieving","grotesque","grumpy","handsome","happy","harsh","healthy","heavy","helpful","helpless","hilarious","homeless","homely","horrible","hungry","hurt","ill","important","impossible","inexpensive","innocent","inquisitive","itchy","jealous","jittery","jolly","joyous","kind","lazy","light","lively","lonely","long","lovely","lucky","magnificent","misty","modern","motionless","muddy","mushy","mysterious","nasty","naughty","nervous","nice","nutty","obedient","obnoxious","odd","old-fashioned","open","outrageous","outstanding","panicky","perfect","plain","pleasant","poised","poor","powerful","precious","prickly","proud","puzzled","quaint","real","relieved","repulsive","rich","scary","selfish","shiny","shy","silly","sleepy","smiling","smoggy","sore","sparkling","splendid","spotless","stormy","strange","stupid","successful","super","talented","tame","tasty","tender","tense","terrible","thankful","thoughtful","thoughtless","tired","tough","troubled","ugliest","ugly","uninterested","unsightly","unusual","upset","uptight","vast","victorious","vivacious","wandering","weary","wicked","wide","wild","witty","wonderful","worried","wretched","yellow","young","yummy","zany","zealous","zesty"]

    animal = animal_list[random.randrange(99)]
    adjective = adjective_list[random.randrange(99)]

    return adjective + "_" + animal

def register_user(username, password):

    if user_exists(username):
        #raise ValueError("Username already exists")
        return "Username already exists"

    if password == "":
        #raise ValueError("You must enter a non-empty password")
        return "Password cannot be empty"

    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    anon = generate_anon()

    # hash password here
    password = password.encode('utf-8')
    password = str(hashlib.sha256(password).hexdigest())
    id = len(get_all_users()) + 1

    # use ? for unsafe/user provided variables
    c.execute('INSERT INTO users VALUES (?, ?, ?, ?, ?)', (username, password, id, anon, ""))

    db.commit()
    db.close()

    return "success"

#data collected: difficulty, enjoyment, workload, hours per night, teaching quality, resources

def create_class_data_table():
    contents = """
        CREATE TABLE IF NOT EXISTS class_data (
            id          INTEGER     PRIMARY KEY AUTOINCREMENT,
            class_id    INTEGER     NOT NULL ,
            user_id    INTEGER     NOT NULL,
            teacher     TEXT        NOT NULL,
            difficulty  INTEGER     NOT NULL,
            enjoyment   INTEGER     NOT NULL,
            workload    INTEGER     NOT NULL,
            hours       INTEGER     NOT NULL,
            teaching_quality INTEGER     NOT NULL,
            resources    TEXT
        )"""
    create_table(contents)


def create_users_table():

    contents =  """
                CREATE TABLE IF NOT EXISTS users (
                    username        TEXT    NOT NULL UNIQUE,
                    password        TEXT    NOT NULL,
                    id              INTEGER NOT NULL    PRIMARY KEY,
                    anon_user       TEXT    NOT NULL,
                    classes         TEXT
                )"""
    create_table(contents)
    register_user("stuypedia_admin", "SuperSecurePassword")

def create_classes_table():

    contents = """
            CREATE TABLE IF NOT EXISTS classes (
                id          INTEGER     PRIMARY KEY AUTOINCREMENT,
                name        TEXT        NOT NULL UNIQUE,
                teachers    TEXT        NOT NULL,
                grades      INTEGER     NOT NULL,
                subject     TEXT        NOT NULL
            )"""
    create_table(contents)

def check_class_for_uniqueness(name):
    classes = get_all_classes()
    for i in range(len(classes)):
        if classes[i][1] == name:
            return False
    return True

def fix_grade_format(grades):
    final_str = ""
    for i in range(len(grades)):
        if (not grades[i] == '[' and not grades[i] == ']') and (not grades[i] == ',' and not grades[i] == r"'"):
            final_str += grades[i]
    return final_str

def add_user_class(username, class_id):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    classes = c.execute('SELECT classes FROM users WHERE username = ?', (username,)).fetchone()[0]
    if classes:
        if str(class_id) in classes.split():
            return False  # Class is already added
        else:
            new_classes = classes + " " + str(class_id)
    else:
        new_classes = str(class_id)
    c.execute('UPDATE users SET classes = ? WHERE username = ?', (new_classes, username))
    db.commit()
    db.close()

def user_id_from_username(username):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    data = c.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone()
    db.commit()
    db.close()

    if data:
        return data[0]
    else:
        return None

def save_class_review(class_id, user_id, teacher, difficulty, enjoyment, workload, hours, teaching_quality, resources):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    # use ? for unsafe/user provided variables
    data = c.execute('INSERT INTO class_data VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (None, class_id, user_id, teacher, difficulty, enjoyment, workload, hours, teaching_quality, str(resources)))

    db.commit()
    db.close()

    return data

def review_already_made(class_id, user_id):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    data = c.execute('SELECT * FROM class_data WHERE class_id = ? AND user_id = ?', (class_id, user_id)).fetchone()
    db.commit()
    db.close()

    if data:
        return True
    else:
        return False

def create_teachers_table():

    contents = """
            CREATE TABLE IF NOT EXISTS teachers (
                id          INTEGER     PRIMARY KEY AUTOINCREMENT,
                first       TEXT        NOT NULL,
                last        TEXT        NOT NULL,
                classes     TEXT        NOT NULL,
                subject     TEXT        NOT NULL
            )"""

def create(name, subject, grades, teachers):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    # use ? for unsafe/user provided variables
    data = c.execute('INSERT INTO classes VALUES (?, ?, ?, ?, ?)', (None, name, teachers, str(grades), subject))

    db.commit()
    db.close()

    return data


def get_all_class_data():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    data = c.execute('SELECT * FROM class_data').fetchall()

    db.commit()
    db.close()

    return data

def get_class_data(class_id):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    data = c.execute('SELECT * FROM class_data WHERE class_id = ?', (class_id,)).fetchall()

    db.commit()
    db.close()

    return data

def get_from_class_data(class_id, request):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    data = c.execute('SELECT ? FROM class_data WHERE class_id = ?', (request, class_id,)).fetchall()

    db.commit()
    db.close()

    return data

def prettify_class_data(class_id):
    prettified_data = [] #2d array with each row being a category

    # Get all the data for the class
    all_data = get_class_data(class_id)

    # Calculate mean and median for each column
    for i in range(4, 9):
        column_data = [row[i] for row in all_data]
        if column_data:
            mean = sum(column_data) / len(column_data)
            sorted_data = sorted(column_data)
            n = len(sorted_data)
            if n % 2 == 0:
                median = (sorted_data[n//2 - 1] + sorted_data[n//2]) / 2
            else:
                median = sorted_data[n//2]
            prettified_data.append(['', mean, median])
    responders = len(all_data)
    prettified_data[0][0] = 'Difficulty'
    prettified_data[1][0] = 'Enjoymnet'
    prettified_data[2][0] = 'Workload'
    prettified_data[3][0] = 'Hours'
    prettified_data[4][0] = 'Teaching Quality'

    #count best resources
    resource_count = {}
    for row in all_data:
        resources = row[9]
        if resources:
            for resource in resources.split(','):
                resource = resource.strip()
                resource_count[resource] = resource_count.get(resource, 0) + 1

    #num of students who recommend each resource

    return (prettified_data, responders, resource_count)

def fix_resource_names(resource_count):
    fixed_count = {}
    for resource, count in resource_count.items():
        if resource == 'teacher_given':
            fixed_count['Teacher-provided resources'] = count
        elif resource == 'teacher_practice_problems':
            fixed_count['Teacher-provided practice problems'] = count
        elif resource == 'heimler_history':
            fixed_count['Heimler\'s History'] = count
        elif resource == 'khan_academy':
            fixed_count['Khan Academy'] = count
        elif resource == 'quizlet':
            fixed_count['Quizlet'] = count
        elif resource == 'crash_course':
            fixed_count['Crash Course'] = count
        elif resource == 'organic_chemistry':
            fixed_count['Organic Chemistry Tutor'] = count
        else:
            fixed_count[resource] = count
    return fixed_count

def get_class_data_by_teacher(class_id, teacher):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    #gotta see if teacher IN the tuple, not sure how to do that

    data = c.execute('SELECT * FROM class_data WHERE class_id = ? AND teacher LIKE "%{}%"'.format(teacher), (class_id,)).fetchall()

    db.commit()
    db.close()

    return data

def prettify_class_data_by_teacher(class_id, teacher):
    data = get_class_data_by_teacher(class_id, teacher)
    if not data:
        return None

    # Process the data to calculate mean and median for each column
    prettified_data = []
    for i in range(4, 9):
        column_data = [row[i] for row in data]
        if column_data:
            mean = sum(column_data) / len(column_data)
            sorted_data = sorted(column_data)
            n = len(sorted_data)
            if n % 2 == 0:
                median = (sorted_data[n//2 - 1] + sorted_data[n//2]) / 2
            else:
                median = sorted_data[n//2]
            prettified_data.append(['', mean, median])
    responders = len(data)
    prettified_data[0][0] = 'Difficulty'
    prettified_data[1][0] = 'Enjoymnet'
    prettified_data[2][0] = 'Workload'
    prettified_data[3][0] = 'Hours'
    prettified_data[4][0] = 'Teaching Quality'
    return prettified_data

def get_teachers_for_class(class_id):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    data = c.execute('SELECT subject FROM classes WHERE id = ?', (class_id,)).fetchall()

    db.commit()
    db.close()
    data = clean_list(re.split('[^a-zA-Z]', str(data[0])))
    print(data)
    return data

def get_all_classes():

    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    data = c.execute('SELECT * FROM classes').fetchall()

    db.commit()
    db.close()

    return data

def class_saved_by_user(class_id, username):
    user_classes = get_user_classes(username)
    if user_classes:
        return str(class_id) in user_classes
    return False

def get_searched_classes(search):
    all_classes = get_all_classes()
    searched_classes = []
    i = 0
    while i < len(all_classes):
        if search in all_classes[i][1]: #if search matches class name
            searched_classes.append(all_classes[i])
        i += 1
    return searched_classes

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

def get_user_classes(username):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    data = c.execute('SELECT classes FROM users WHERE username = ?', (username,)).fetchall()
    db.commit()
    db.close()

    if data and data[0][0]:
        return data[0][0].split()  # Return list of class IDs
    else:
        return None

def get_class_name_from_id(class_id):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    data = c.execute('SELECT name FROM classes WHERE id = ?', (class_id,)).fetchone()
    db.commit()
    db.close()

    if data:
        return data[0]
    else:
        return None

def get_all_anons():

    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    data = c.execute('SELECT anon_user FROM users').fetchall()

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

def delete_classid(class_id):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute('DELETE FROM classes WHERE id = ?', (class_id,))
    db.commit()
    db.close()

def delete_student_classid(class_id):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute('DELETE FROM student_classes WHERE id = ?', (class_id,))
    db.commit()
    db.close()

def approve_classid(class_id):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    class_info = c.execute('SELECT name, teachers, grades, subject FROM student_classes WHERE id = ?', (class_id,)).fetchone()
    c.execute('INSERT INTO classes VALUES (?, ?, ?, ?, ?)', (None, class_info[0], class_info[3], class_info[2], class_info[1]))
    c.execute('DELETE FROM student_classes WHERE id = ?', (class_id,))
    db.commit()
    db.close()

def get_all_student_classes():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    data = c.execute('SELECT * FROM student_classes').fetchall()

    db.commit()
    db.close()

    return data

def create_student_class(name, teachers, grade, subject):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    # use ? for unsafe/user provided variables
    data = c.execute('INSERT INTO student_classes VALUES (?, ?, ?, ?, ?)', (None, name, teachers, str(grade), subject))

    db.commit()
    db.close()

    return data
def create_student_classes_table():
    contents = """
            CREATE TABLE IF NOT EXISTS student_classes (
                id          INTEGER     PRIMARY KEY AUTOINCREMENT,
                name        TEXT        NOT NULL UNIQUE,
                teachers    TEXT        NOT NULL,
                grades      INTEGER     NOT NULL,
                subject     TEXT        NOT NULL
            )"""
    create_table(contents)

def create_events_table():
    contents = """
        CREATE TABLE IF NOT EXISTS events (
        id          INTEGER         PRIMARY KEY AUTOINCREMENT,
        username    TEXT            NOT NULL,
        title       TEXT            NOT NULL,
        start       TEXT            NOT NULL,
        end         TEXT,
        color       TEXT,
        linked_class       TEXT,
        all_day     INTEGER
        )"""
    create_table(contents)

def save_event(username, title, start, end, color, linked_class, all_day):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute('INSERT INTO events VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)',
              (username, title, start, end, color, linked_class, int(all_day)))
    db.commit()
    new_id = c.lastrowid
    db.close()
    return new_id

def get_events(username):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    data = c.execute('SELECT id, title, start, end, color, linked_class, all_day FROM events WHERE username = ?',
                     (username,)).fetchall()
    db.commit()
    db.close()
    return [{"id": r[0], "title": r[1], "start": r[2], "end": r[3],
             "color": r[4], "linked_class": r[5], "allDay": bool(r[6])} for r in data]

def delete_event(event_id, username):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute('DELETE FROM events WHERE id = ? AND username = ?', (event_id, username))
    db.commit()
    db.close()

def get_class_info(class_id):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    data = c.execute('SELECT name, teachers, grades, subject FROM classes WHERE id = ?', (class_id,)).fetchone()
    db.commit()
    db.close()

    return data
