from flask import Flask
app = Flask(__name__)

from flask import url_for
from flask import request
from markupsafe import escape
from flask import render_template


@app.route('/')
@app.route('/<name>')
def hello(name=""):
    print(url_for('static', filename='style.css'))
    return render_template('login.html', name=name)




