from secrets import token_hex
from flask import session, abort
from werkzeug.security import check_password_hash, generate_password_hash

from mealbase.queries import user_queries


def register(name, password, db):
    _validate_username(name, db)
    _validate_password(password)
    _add_new_user(name, password, db)
    _login(name, password, db)


def login(name, password, db):
    if not name or not password:
        raise Exception("Input both a username and a password")
    _login(name, password, db)


def logout():
    del session["user_name"]
    del session["user_id"]


def check_csrf(request_token):
    if session["csrf_token"] != request_token:
        abort(403)


def user_id():
    return session.get("user_id", 0)


def _login(name, password, db):
    user = user_queries.get_user(name, db)
    print(user)
    if not user:
        raise Exception("Wrong username / password")
    password_ok = check_password_hash(user["password"], password)
    if not password_ok:
        raise Exception("Wrong username / password")
    session["user_name"] = name
    session["user_id"] = user["id"]
    session["csrf_token"] = token_hex(16)


def _validate_username(name, db):
    if user_queries.get_user(name, db):
        raise Exception(
            f'Username "{name}" is already taken'
        )
    correct_length = len(name) >= 3 and len(name) <= 20
    special_characters = [char for char in name if not char.isalnum()]
    if not correct_length:
        raise Exception(
            "Name length should be 3-20 characters"
        )
    if special_characters:
        raise Exception(
            f"""
            Name should only contain alphanumeric characters.
            These are not alphanumeric: {"".join(special_characters)}
            """
        )


def _validate_password(password):
    correct_lenght = len(password) >= 3
    no_special_characters = password.isalnum()
    if not correct_lenght:
        raise Exception(
            "Password length should be at least 3 characters"
        )
    if no_special_characters:
        raise Exception(
            "Password should contain at least one special character"
        )


def _add_new_user(name, password, db):
    hash_value = generate_password_hash(password)
    user_queries.add_user(name, hash_value, db)
