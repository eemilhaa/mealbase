from flask import Flask
from flask import redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy

from config import DATABASE_URL


app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
db = SQLAlchemy(app)


@app.route("/")
def index():
    result = db.session.execute("SELECT name FROM users")
    users = result.fetchall()
    return render_template("index.html", count=len(users), users=users)
