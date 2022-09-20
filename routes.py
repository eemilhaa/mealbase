from flask import render_template

from app import app
from users import get_user_names


@app.route("/")
def index():
    users = get_user_names()
    return render_template("index.html", count=len(users), users=users)
