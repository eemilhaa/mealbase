from secrets import token_hex
from flask import session, abort
from werkzeug.security import check_password_hash, generate_password_hash


def register(name, password, role, db):
    _validate_username(name, db)
    _validate_password(password)
    _add_new_user(name, password, role, db)
    _login(name, password, db)


def login(name, password, db):
    if not name or not password:
        raise Exception("Input both a username and a password")
    _login(name, password, db)


def _login(name, password, db):
    user = _get_user(name, db)
    print(user)
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


def _validate_username(name, db):
    if _get_user(name, db):
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


def _get_user(name, db):
    sql = """
        SELECT id, name, password, role FROM users WHERE name=:name
    """
    result = db.session.execute(sql, {"name": name})
    user = result.fetchone()
    return user
