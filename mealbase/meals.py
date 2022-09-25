def log_meal(meal, ingredients, user_id, db):
    meal_id = _get_id("meals", meal, db)
    if not meal_id:
        meal_id = _add_new_meal(meal, user_id, db)
        ingredient_ids = _add_ingredients(ingredients, user_id, db)
        _add_meal_ingredient_relations(meal_id, ingredient_ids, db)
    # _log_meal()


def _get_id(table, name, db):
    sql = f"""
        SELECT id FROM {table} WHERE name=:name
    """
    result = db.session.execute(sql, {"name": name})
    try:
        id = result.fetchone()[0]
        return id
    except TypeError:
        return False


def _add_new_meal(meal, user_id, db):
    sql = """
        INSERT INTO meals (user_id, name)
        VALUES (:user_id, :name)
        RETURNING id;
    """
    result = db.session.execute(
        sql,
        {"user_id": user_id, "name": meal.lower()},
    )
    id = result.fetchone()[0]
    db.session.commit()
    return id


def _add_ingredients(ingredients, user_id, db):
    sql = """
        INSERT INTO ingredients (user_id, name)
        VALUES (:user_id, :name)
        ON CONFLICT DO NOTHING
        RETURNING ID;
    """
    ingredient_list = ingredients.split(", ")
    ingredient_ids = []
    for ingredient in ingredient_list:
        id = _get_id("ingredients", ingredient, db)
        if id:
            ingredient_ids.append(id)
        else:
            result = db.session.execute(
                sql,
                {"user_id": user_id, "name": ingredient.lower()},
            )
            try:
                id = result.fetchone()[0]
                ingredient_ids.append(id)
                db.session.commit()
            except TypeError:
                pass
    return ingredient_ids


def _add_meal_ingredient_relations(meal_id, ingredient_ids, db):
    sql = """
        INSERT INTO meal_ingredients (meal_id, ingredient_id)
        VALUES (:meal_id, :ingredient_id);
    """
    if len(ingredient_ids) > 0:
        for ingredient_id in ingredient_ids:
            db.session.execute(
                sql,
                {"meal_id": meal_id, "ingredient_id": ingredient_id}
            )
            db.session.commit()
