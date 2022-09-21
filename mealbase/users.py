def get_user_names(db):
    result = db.session.execute("SELECT name FROM users")
    users = result.fetchall()
    return users
