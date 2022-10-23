import datetime
from flask import session

from mealbase.queries import log_queries


def meal_exists(meal, user_id, db):
    if not meal:
        raise Exception("Input the meal name")
    _validate_input(meal, max_length=100)
    return log_queries.meal_exists(meal, user_id, db)


def log_known_meal(meal, log_date, user_id, db):
    if not meal:
        raise Exception("Input the meal name")
    log_queries.log_known_meal(meal, log_date, user_id, db)
    _delete_log_from_session()


def log_new_meal(meal, log_date, ingredients, user_id, db):
    if not meal or not ingredients:
        raise Exception("Input the ingredients")
    _validate_input(meal, max_length=100)
    _validate_input(ingredients, max_length=300)
    log_queries.log_new_meal(meal, log_date, ingredients, user_id, db)
    _delete_log_from_session()


def get_meals_with_ingredient(ingredient, user_id, db):
    return log_queries.get_meals_with_ingredient(ingredient, user_id, db)


def save_log_to_session(meal, date):
    session["meal"] = meal
    session["date"] = date


def get_log_from_session():
    if "meal" in session and "date" in session:
        return session["meal"], session["date"]


def _delete_log_from_session():
    del session["meal"]
    del session["date"]


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
    suggestions.reverse()
    return suggestions


def _validate_input(input, max_length):
    correct_length = len(input) <= max_length
    if not correct_length:
        raise Exception(
            "Too much input"
        )
