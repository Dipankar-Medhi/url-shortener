
import random
import sqlite3
from flask import Flask, request
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.utils import redirect

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urlsDB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.before_first_request
def create_tables():
    db.create_all()


class Url(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String())
    shorten_url = db.Column(db.String())

    def __init__(self, original_url, shorten_url):
        self.original_url = original_url
        self.shorten_url = shorten_url

    def __repr__(self) -> str:
        return self.shorten_url


def shorten():
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    while True:
        shortRoute = "".join(random.choice(chars) for _ in range(9))

        short_inDB = Url.query.filter_by(shorten_url=shortRoute).first()
        if not short_inDB:
            return shortRoute


@app.route('/', methods=['POST', 'GET'])
def home_post():
    if request.method == 'POST':
        long_url = request.form.get('url')
        inDB = Url.query.filter_by(original_url=long_url).first()
        if inDB:
            return render_template('index.html', shrt_url=inDB.shorten_url)

        short_url = shorten()
        new_url = Url(long_url, short_url)
        db.session.add(new_url)
        db.session.commit()
        return render_template('index.html', shrt_url=short_url)
    else:
        return render_template('index.html')


@app.route('/history')
def history_get():
    urls = Url.query.all()
    return render_template('history.html', data=urls)


@app.route('/sh/<short_url>')
def redirecting(short_url):
    inDB = Url.query.filter_by(shorten_url=short_url).first()
    if inDB:
        return redirect(inDB.original_url)
    else:
        return 'Url doesnot exist'


if __name__ == "__main__":
    app.run(debug=True)
