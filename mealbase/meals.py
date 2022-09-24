def log_meal(meal, ingredients, user_id, db):
    meal_id = _get_meal_id(meal, db)
    if not meal_id:
        meal_id = _add_new_meal(meal, user_id, db)
        ingredient_ids = _add_new_ingredients(ingredients, user_id, db)
        _add_meal_ingredient_relations(meal_id, ingredient_ids, db)


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
    id = result.fetchone()[0]
    db.session.commit()
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
        if result:
            id = result.fetchone()[0]
            ingredient_ids.append(id)
            db.session.commit()
    return ingredient_ids


def _add_meal_ingredient_relations(meal_id, ingredient_ids, db):
    sql = """
        INSERT INTO meal_ingredients (meal_id, ingredient_id)
        VALUES (:meal_id, :ingredient_id);
    """
    for ingredient_id in ingredient_ids:
        for i in range(100):
            print(ingredient_id)
        db.session.execute(
            sql,
            {"meal_id": meal_id, "ingredient_id": ingredient_id}
        )
        db.session.commit()
