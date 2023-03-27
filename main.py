from flask import Flask, render_template
import sqlite3
from flask import g
from pathlib import Path

app = Flask(__name__)

DATABASE = 'database.db'
SQL_SCRIPT = 'db/database.sql'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
@app.route("/login")
def index():
    # cur = get_db().cursor()
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('index.html')

def main():
    if not Path(DATABASE).exists():
        print('create db')
        with open(SQL_SCRIPT, 'r') as sql_file:
            sql_script = sql_file.read()

        db = sqlite3.connect(DATABASE)
        cursor = db.cursor()
        cursor.executescript(sql_script)
        db.commit()
        db.close()

main()