from flask import Flask, render_template, request, session, redirect, url_for, flash
import sqlite3
from flask import g
from pathlib import Path
import bcrypt

app = Flask(__name__)

##################################################################################################
#                                 GLOBALS                                                        #
##################################################################################################

DATABASE = 'database.db'
SQL_SCRIPT = 'db/database.sql'

app.secret_key = 'fed8e6793a470fd16956e29d57a229ea616f482679ea552f3cda7b7677dcfd3e'

class LogUser:
  def __init__(self, is_connected, is_admin):
    self.is_connected = is_connected
    self.is_admin = is_admin

logUser = LogUser(False, False)

##################################################################################################
#                                 UTILS                                                          #
##################################################################################################

@app.errorhandler(500)
@app.errorhandler(404)
def errorpath(e):
    return redirect(url_for('home'))

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def hash_pwd(pwd):
    salt = bcrypt.gensalt()
    pwd = pwd.encode('utf-8')
    hashed_pwd = bcrypt.hashpw(pwd, salt)
    return hashed_pwd

##################################################################################################
#                                 ROUTES                                                         #
##################################################################################################

@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        email = request.form['email']
        first_name = request.form['first-name']
        last_name = request.form['last-name']
        phone_number = request.form['phone-number']
        password = request.form['password']
        hashed_pwd = hash_pwd(password)
        logUser.is_admin = True if request.form.get('admin_checkbox') else False
        error = None

        if not email or not first_name or not last_name or not phone_number or not password:
            error = "a field is missing"

        if error is not None:
            flash(error, 'error')
        else:
            db = get_db()
            try:
                db.execute(
                    'INSERT INTO users (lastName, name, email, phoneNumber, role, password) VALUES (?, ?, ?, ?, ?, ?)',
                    (last_name, first_name, email, phone_number, logUser.is_admin, hashed_pwd)
                )
                db.commit()
                logUser.is_connected = True
                return redirect(url_for('home'))
            except:
                print('exception occured, user already existed')

    return render_template('register.html')

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

        if user and not bcrypt.checkpw(password.encode('utf-8'), user[6]):
            error = 'Incorrect password.'
        if not user:
            error = 'Incorrect email.'

        if error is None:
            session.clear()
            session['user_id'] = user[0]
            if user[5] == 1:
                logUser.is_connected = True
                logUser.is_admin = True
                return redirect(url_for('admin'))
            else:
                logUser.is_connected = True
                logUser.is_admin = False
                return redirect(url_for('home'))
        flash(error, 'error')

    return render_template('login.html', is_connected = logUser.is_connected)

@app.route("/disconnect")
def disconnect():
    logUser.is_admin = False
    logUser.is_connected = False
    return redirect(url_for('login'))

@app.route("/")
@app.route('/home')
def home():
    # print(logUser)
    if logUser.is_connected is False:
        return redirect(url_for('login'))

    products = get_db().execute(
        'SELECT id, label, image, price, description FROM products'
    ).fetchall()
    return render_template('index.html', products = products, is_admin = logUser.is_admin)

@app.route('/admin')
def admin():
    if logUser.is_admin is True:
        products = get_db().execute(
            'SELECT id, label, image, price, description FROM products'
        ).fetchall()
        return render_template('admin.html', products = products, is_admin = logUser.is_admin)
    return redirect(url_for('home'))

@app.route('/product/<id>')
def get_product(id):
    try:
        product = get_db().execute(
            'SELECT id, label, image, price, description FROM products WHERE id = ?',
            (id)
        ).fetchone()
        return render_template('product.html', product=product, productFound = True, is_admin = logUser.is_admin)
    except:
        return render_template('product.html', product = [0, 'product not found', '', 0, ''], productFound = False)

##################################################################################################
#                                 CRUD                                                           #
##################################################################################################

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
            flash(error, 'error')
        else:
            db = get_db()
            db.execute(
                'INSERT INTO products (label, image, price, description) VALUES (?, ?, ?, ?)',
                (label, image, price, description)
            )
            db.commit()
    return redirect(url_for('admin'))

@app.route('/<id>/update', methods=('GET', 'POST'))
def update(id):
    if request.method == 'POST':
        label = request.form['label']
        image = request.form['image']
        price = request.form['price']
        description = request.form['description']
        error = None

        if not label or not image or not price or not description:
            error = 'A field is empty'

        if error is not None:
            flash(error, 'error')
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
    db = get_db()
    db.execute('DELETE FROM products WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('admin'))

##################################################################################################
#                                 DB INIT                                                        #
##################################################################################################

def db_init():
    if not Path(DATABASE).exists():
        sql_script = Path(SQL_SCRIPT).read_text()
        db = sqlite3.connect(DATABASE)
        db.cursor().executescript(sql_script)
        db.commit()
        db.close()

db_init()