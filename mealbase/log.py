import datetime

from mealbase.queries import log_queries


def log_meal(meal, log_date, ingredients, user_id, db):
    meal_id = log_queries.get_id("meals", meal, db, user_id,)
    if not meal_id:
        meal_id = log_queries.add_new_meal(meal, user_id, db)
        ingredient_ids = log_queries.add_ingredients(ingredients, db)
        log_queries.add_meal_ingredient_relations(
            meal_id, ingredient_ids, user_id, db
        )
    log_queries.add_meal_to_log(meal_id, log_date, db)


def get_log(user_id, db):
    all_meals = log_queries.get_log(user_id, db)
    return all_meals


def get_ingredients(user_id, db):
    all_ingredients = log_queries.get_ingredients(user_id, db)
    return all_ingredients


def generate_suggestions(user_id, db):
    ingredient_history = log_queries.get_ingredient_history(user_id, db)
    suggestions = _generate_suggestions(ingredient_history)
    return suggestions


def _generate_suggestions(ingredient_history):
    today = datetime.date.today()
    seen = []
    timedeltas = []
    for ingredient, date in ingredient_history:
        if ingredient not in seen:
            seen.append(ingredient)
            timedelta = today - date
            timedeltas.append((ingredient, timedelta.days))
    # TODO make number of suggestions dynamic?
    suggestions = timedeltas[-4:]
    return suggestions
