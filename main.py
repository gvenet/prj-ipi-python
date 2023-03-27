from flask import Flask, render_template, request, session, redirect, url_for, flash
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
@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        print('POST',email,password)
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM users WHERE email = (?)', (email,)
        ).fetchone()
        if user is None:
            error = 'Incorrect email.'
        elif user[6] != password:
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('login.html')

@app.route('/home')
def home():
    products = get_db().execute(
        'SELECT p.id, label, image, price, description FROM products p'
    ).fetchall()
    return render_template('index.html', products = products)

@app.route('/product/<id>')
def get_product(id):
    product = get_db().execute(
        'SELECT p.id, label, image, price, description FROM products p WHERE p.id = ?',
        (id)
    ).fetchone()
    return render_template('product.html', product = product)

def db_init():
    if not Path(DATABASE).exists():
        print('create db')
        with open(SQL_SCRIPT, 'r') as sql_file:
            sql_script = sql_file.read()

        db = sqlite3.connect(DATABASE)
        cursor = db.cursor()
        cursor.executescript(sql_script)
        db.commit()
        db.close()

db_init()