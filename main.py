from flask import Flask, render_template, request, session, redirect, url_for, flash, abort
import sqlite3
from flask import g
from pathlib import Path

app = Flask(__name__)

DATABASE = 'database.db'
SQL_SCRIPT = 'db/database.sql'

app.secret_key = 'fed8e6793a470fd16956e29d57a229ea616f482679ea552f3cda7b7677dcfd3e'

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

@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
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
            session['user_id'] = user[0]
            if user[5] == 1:
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('home'))
        flash(error)
    return render_template('login.html')

@app.route("/")
@app.route('/home')
def home():
    products = get_db().execute(
        'SELECT id, label, image, price, description FROM products'
    ).fetchall()
    return render_template('index.html', products = products)

@app.route('/admin')
def admin():
    products = get_db().execute(
        'SELECT id, label, image, price, description FROM products'
    ).fetchall()
    return render_template('admin.html', products = products)

@app.route('/product/<id>')
def get_product(id):
    product = get_db().execute(
        'SELECT id, label, image, price, description FROM products WHERE id = ?',
        (id)
    ).fetchone()
    return render_template('product.html', product = product)

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        label = request.form['label']
        image = request.form['image']
        price = request.form['price']
        description = request.form['description']
        error = None

        if not label or not image or not price or not description:
            error = 'A field is empty'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO products (label, image, price, description) VALUES (?, ?, ?, ?)',
                (label, image, price, description)
            )
            db.commit()
    return redirect(url_for('admin'))

def get_post(id):
    product = get_db().execute(
        'SELECT id, label, image, price, description FROM products WHERE id = ?',
        (id,)
    ).fetchone()
    if product is None:
        abort(404, f"Post id {id} doesn't exist.")
    # if check_author and post['author_id'] != g.user['id']:
    #     abort(403)
    return product

@app.route('/<id>/update', methods=('GET', 'POST'))
def update(id):
    product = get_post(id)
    if request.method == 'POST':
        label = request.form['label']
        image = request.form['image']
        price = request.form['price']
        description = request.form['description']
        error = None

        if not label or not image or not price or not description:
            error = 'A field is empty'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE products SET label = ?, image = ?, price = ?, description = ? WHERE id = ?',
                (label, image, price, description, id)
            )
            db.commit()

    return redirect(url_for('admin'))


@app.route('/<id>/delete', methods=('POST',))
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM products WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('admin'))

def db_init():
    if not Path(DATABASE).exists():
        with open(SQL_SCRIPT, 'r') as sql_file:
            sql_script = sql_file.read()

        db = sqlite3.connect(DATABASE)
        cursor = db.cursor()
        cursor.executescript(sql_script)
        db.commit()
        db.close()

db_init()