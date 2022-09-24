def log_meal(meal, ingredients, user_id, db):
    meal_id = _get_meal_id(meal, db)
    if not meal_id:
        meal_id = _add_new_meal(meal, user_id, db)
        ingredient_ids = _add_new_ingredients(ingredients, user_id, db)


def _get_meal_id(meal, db):
    sql = """
        SELECT id FROM meals WHERE name=:name
    """
    result = db.session.execute(sql, {"name": meal})
    id = result.fetchone()
    return id


def _add_new_meal(meal, user_id, db):
    sql = """
        INSERT INTO meals (user_id, name)
        VALUES (:user_id, :name)
        RETURNING id;
    """
    result = db.session.execute(
        sql,
        {"user_id": user_id, "name": meal},
    )
    id = result.fetchone()
    db.session.commit()
    print(id)
    return id


def _add_new_ingredients(ingredients, user_id, db):
    sql = """
        INSERT INTO ingredients (user_id, name)
        VALUES (:user_id, :name)
        ON CONFLICT DO NOTHING
        RETURNING ID;
    """
    ingredient_list = ingredients.split(", ")
    ingredient_ids = []
    for ingredient in ingredient_list:
        result = db.session.execute(
            sql,
            {"user_id": user_id, "name": ingredient.lower()},
        )
        id = result.fetchone()
        print(ingredient, id)
        ingredient_ids.append(id)
        db.session.commit()
    return ingredient_ids
