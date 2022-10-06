from secrets import token_hex
from flask import session, abort
from werkzeug.security import check_password_hash, generate_password_hash


def register(name, password, role, db):
    if _username_exists(name, db):
        raise Exception("Username is already taken")
    _add_new_user(name, password, role, db)
    login(name, password, db)


def login(name, password, db):
    sql = """
        SELECT password, id, role FROM users WHERE name=:name
    """
    result = db.session.execute(sql, {"name": name})
    user = result.fetchone()
    # TODO could also do distinct errors here
    if not user:
        raise Exception("Wrong username / password")
    password_ok = check_password_hash(user["password"], password)
    if not password_ok:
        raise Exception("Wrong username / password")
    session["user_name"] = name
    session["user_id"] = user["id"]
    session["csrf_token"] = token_hex(16)


def logout():
    del session["user_name"]
    del session["user_id"]


# TODO
def check_csrf(request_token):
    if session["csrf_token"] != request_token:
        abort(403)


def user_id():
    return session.get("user_id", 0)


def _add_new_user(name, password, role, db):
    hash_value = generate_password_hash(password)
    sql = """
        INSERT INTO users (name, password, role)
        VALUES (:name, :password, :role)
    """
    db.session.execute(
        sql,
        {"name": name, "password": hash_value, "role": role},
    )
    db.session.commit()


def _username_exists(name, db):
    sql = """
        SELECT name FROM users WHERE name=:name
    """
    result = db.session.execute(sql, {"name": name})
    username = result.fetchone()
    return username
