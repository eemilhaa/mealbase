def meal_exists(meal, user_id, db):
    meal_id = _get_id("meals", meal, db, user_id,)
    if meal_id:
        return True
    return False


def log_new_meal(meal, log_date, ingredients, user_id, db):
    meal_id = _add_new_meal(meal, user_id, db)
    ingredient_ids = _add_ingredients(ingredients, db)
    _add_meal_ingredient_relations(
        meal_id, ingredient_ids, user_id, db
    )
    _add_meal_to_log(meal_id, log_date, db)


def log_known_meal(meal, log_date, user_id, db):
    meal_id = _get_id("meals", meal, db, user_id,)
    _add_meal_to_log(meal_id, log_date, db)


def get_log(user_id, db):
    sql = """
        SELECT meals.name, meal_log.date
        FROM meals, meal_log
        WHERE meals.id = meal_log.meal_id AND meals.user_id=:user_id
        ORDER BY meal_log.date DESC;
    """
    result = db.session.execute(
        sql,
        {"user_id": user_id}
    )
    all_meals = result.fetchall()
    return all_meals


def get_ingredients(user_id, db):
    sql = """
        SELECT DISTINCT ingredients.name FROM ingredients, meal_ingredients
        WHERE meal_ingredients.user_id=:user_id
        AND ingredients.id=meal_ingredients.ingredient_id;
    """
    result = db.session.execute(
        sql,
        {"user_id": user_id}
    )
    all_ingredients = result.fetchall()
    return all_ingredients


def get_ingredient_history(user_id, db):
    sql = """
        SELECT ingredients.name, meal_log.date
        FROM ingredients, meal_ingredients, meal_log
        WHERE meal_ingredients.user_id=:user_id
        AND ingredients.id=meal_ingredients.ingredient_id
        AND meal_log.meal_id=meal_ingredients.meal_id
        ORDER BY meal_log.date DESC;
    """
    result = db.session.execute(
        sql,
        {"user_id": user_id}
    )
    ingredient_history = result.fetchall()
    return ingredient_history


def get_meals_with_ingredient(ingredient, user_id, db):
    sql = """
        SELECT meals.name
        FROM meals, meal_ingredients
        WHERE meal_ingredients.user_id=:user_id
        AND meals.user_id=:user_id
        AND meal_ingredients.ingredient_id=(
            SELECT id FROM ingredients WHERE name=:ingredient
        )
        AND meals.id=meal_ingredients.meal_id;
    """
    result = db.session.execute(
        sql,
        {"ingredient": ingredient, "user_id": user_id}
    )
    meals_with_ingredient = result.fetchall()
    return meals_with_ingredient


def _get_id(table, name, db, user_id=None):
    sql_user = f"""
        SELECT id FROM {table} WHERE name=:name AND user_id=:user_id;
    """
    sql_no_user = f"""
        SELECT id FROM {table} WHERE name=:name;
    """
    if user_id:
        result = db.session.execute(
            sql_user,
            {"name": name.lower(), "user_id": user_id}
        )
    else:
        result = db.session.execute(sql_no_user, {"name": name})
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


def _add_ingredients(ingredients, db):
    sql = """
        INSERT INTO ingredients (name)
        VALUES (:name)
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
                {"name": ingredient.lower()},
            )
            try:
                id = result.fetchone()[0]
                ingredient_ids.append(id)
                db.session.commit()
            except TypeError:
                pass
    return ingredient_ids


def _add_meal_ingredient_relations(meal_id, ingredient_ids, user_id, db):
    sql = """
        INSERT INTO meal_ingredients (user_id, meal_id, ingredient_id)
        VALUES (:user_id, :meal_id, :ingredient_id);
    """
    if len(ingredient_ids) > 0:
        for ingredient_id in ingredient_ids:
            db.session.execute(
                sql,
                {
                    "user_id": user_id,
                    "meal_id": meal_id,
                    "ingredient_id": ingredient_id
                },
            )
            db.session.commit()


def _add_meal_to_log(meal_id, log_date, db):
    sql = """
        INSERT INTO meal_log (meal_id, date)
        VALUES (:meal_id, :date);
    """
    db.session.execute(
        sql,
        {"meal_id": meal_id, "date": log_date}
    )
    db.session.commit()
