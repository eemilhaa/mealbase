def add_user(name, password_hash, role, db):
    sql = """
        INSERT INTO users (name, password, role)
        VALUES (:name, :password, :role)
    """
    db.session.execute(
        sql,
        {"name": name, "password": password_hash, "role": role},
    )
    db.session.commit()


def get_user(name, db):
    sql = """
        SELECT id, name, password, role FROM users WHERE name=:name
    """
    result = db.session.execute(sql, {"name": name})
    user = result.fetchone()
    return user
