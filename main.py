from flask import Flask, render_template
import sqlite3
from flask import g

app = Flask(__name__)

DATABASE = '/path/to/database.db'

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
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/home')
def home():
    products = get_db().execute(
        'SELECT p.id, label, image, price, description'
        ' FROM product p '
        ' WHERE p.id = ?'
    ).fetchall()
    return render_template('index.html', products = products)

@app.route('/product')
def get_product(id):
    product = get_db().execute(
        'SELECT p.id, label, image, price, description'
        ' FROM product p '
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    return render_template('product.html', product = product)