from secrets import token_hex
from flask import session, abort
from werkzeug.security import check_password_hash, generate_password_hash


def register(name, password, role, db):
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
    return login(name, password, db)


def login(name, password, db):
    sql = """
        SELECT password, id, role FROM users WHERE name=:name
    """
    result = db.session.execute(sql, {"name": name})
    user = result.fetchone()
    check_password_hash(user["password"], password)
    session["user_name"] = name
    session["csrf_token"] = token_hex(16)


def logout():
    del session["user_name"]


def check_csrf(request_token):
    if session["csrf_token"] != request_token:
        abort(403)
