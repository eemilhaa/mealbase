from db import db


def get_user_names():
    result = db.session.execute("SELECT name FROM users")
    users = result.fetchall()
    return users
