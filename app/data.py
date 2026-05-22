import sqlite3                      # enable control of an sqlite database
import hashlib                      # for consistent hashes
import secrets                      # to generate ids
import random
from flask import request

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
                id          INTEGER     NOT NULL UNIQUE,
                name        TEXT        NOT NULL UNIQUE,
                teachers    TEXT        NOT NULL,
                grades      INTEGER     NOT NULL,
                subject     TEXT        NOT NULL
            )"""
    create_table(contents)

def check_class_for_uniqueness(name):
    classes = get_all_classes()
    print(classes)
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

def create_teachers_table():

    contents = """
            CREATE TABLE IF NOT EXISTS teachers (
                id          INTEGER     NOT NULL UNIQUE,
                first       TEXT        NOT NULL,
                last        TEXT        NOT NULL,
                classes     TEXT        NOT NULL,
                subject     TEXT        NOT NULL
            )"""

def create(name, subject, grades, teachers):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    id = len(get_all_classes()) + 1

    data = c.execute('INSERT INTO classes VALUES (?, ?, ?, ?, ?)', (id, name, teachers, str(grades), subject))

    db.commit()
    db.close()

    return data


def get_all_classes():

    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    data = c.execute('SELECT * FROM classes').fetchall()

    db.commit()
    db.close()

    return data


def get_searched_classes(search):
    all_classes = get_all_classes()
    searched_classes = []
    i = 0
    while i < len(all_classes):
        if search in all_classes[i][1]: #if search matches class name
            searched_classes.append(all_classes[i][1])
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
    print(data)
    db.commit()
    db.close()

    if data:
        return data[0].split()
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
    c.execute('INSERT INTO classes VALUES (?, ?, ?, ?, ?)', (len(get_all_classes()) + 1, class_info[0], class_info[1], class_info[2], class_info[3]))
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
    id = len(get_all_student_classes()) + 1

    data = c.execute('INSERT INTO student_classes VALUES (?, ?, ?, ?, ?)', (id, name, teachers, str(grade), subject))

    db.commit()
    db.close()

    return data
def create_student_classes_table():
    contents = """
            CREATE TABLE IF NOT EXISTS student_classes (
                id          INTEGER     NOT NULL UNIQUE,
                name        TEXT        NOT NULL UNIQUE,
                teachers    TEXT        NOT NULL,
                grades      INTEGER     NOT NULL,
                subject     TEXT        NOT NULL
            )"""
    create_table(contents)

def create_events_table():
    contents = """
        CREATE TABLE IF NOT EXISTS events (
        id          INTEGER         NOT NULL PRIMARY KEY AUTOINCREMENT,
        username    TEXT            NOT NULL,
        title       TEXT            NOT NULL,
        start       TEXT            NOT NULL,
        end         TEXT,           
        color       TEXT,
        all_day     INTEGER
        )"""
    create_table(contents)

def save_event(username, title, start, end, color, all_day):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute('INSERT INTO events VALUES (NULL, ?, ?, ?, ?, ?, ?)',
              (username, title, start, end, color, int(all_day)))
    db.commit()
    db.close()

def get_events(username):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    data = c.execute('SELECT id, title, start, end, color, all_day FROM events WHERE username = ?',
                     (username,)).fetchall()
    db.commit()
    db.close()
    return [{"id": r[0], "title": r[1], "start": r[2], "end": r[3],
             "color": r[4], "allDay": bool(r[5])} for r in data]

def delete_event(event_id, username):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute('DELETE FROM events WHERE id = ? AND username = ?', (event_id, username))
    db.commit()
    db.close()