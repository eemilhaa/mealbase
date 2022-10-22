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


def log_new_meal(meal, log_date, ingredients, user_id, db):
    if not meal or not ingredients:
        raise Exception("Input the ingredients")
    _validate_input(meal, max_length=100)
    _validate_input(ingredients, max_length=300)
    log_queries.log_new_meal(meal, log_date, ingredients, user_id, db)


def meal_to_session(meal):
    session["meal"] = meal


def meal_from_session():
    return session["meal"]


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
