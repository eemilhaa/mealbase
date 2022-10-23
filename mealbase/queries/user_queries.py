def add_user(name, password_hash, db):
    sql = """
        INSERT INTO users (name, password)
        VALUES (:name, :password)
    """
    db.session.execute(
        sql,
        {"name": name, "password": password_hash},
    )
    db.session.commit()


def get_user(name, db):
    sql = """
        SELECT id, name, password FROM users WHERE name=:name
    """
    result = db.session.execute(sql, {"name": name})
    user = result.fetchone()
    return user
