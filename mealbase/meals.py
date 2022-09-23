def log_meal(meal, ingredients, user_id, db):
    sql = """
        INSERT INTO meals (user_id, name)
        VALUES (:user_id, :name);
    """
    db.session.execute(
        sql,
        {"user_id": user_id, "name": meal},
    )
    db.session.commit()
