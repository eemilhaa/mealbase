from flask import render_template, request, redirect
from datetime import date

from mealbase import users
from mealbase import log


def create_routes(app, db):

    @app.route("/log_meal", methods=["GET", "POST"])
    def log_meal():
        if request.method == "GET":
            return render_template(
                "logging.html",
                default_date=date.today(),
            )
        users.check_csrf(request.form["csrf_token"])
        user_id = users.user_id()
        meal = request.form["meal"]
        log_date = request.form["date"]
        try:
            meal_exists = log.meal_exists(meal, user_id, db)
        except Exception as error:
            return render_template(
                "logging.html",
                default_date=date.today(),
                error=error,
                prefill_meal=meal,
            )
        if meal_exists:
            log.log_known_meal(meal, log_date, user_id, db)
            return redirect("/")
        log.save_log_to_session(meal, log_date)
        return redirect("/log_ingredients")

    @app.route("/log_ingredients", methods=["GET", "POST"])
    def log_ingredients():
        meal, log_date = log.get_log_from_session()
        if not meal:
            return redirect("/")
        if request.method == "GET":
            return render_template(
                "logging.html",
                meal=meal,
                log_ingredients=True,
            )
        users.check_csrf(request.form["csrf_token"])
        user_id = users.user_id()
        ingredients = request.form["ingredients"]
        try:
            log.log_new_meal(meal, log_date, ingredients, user_id, db)
        except Exception as error:
            return render_template(
                "logging.html",
                meal=meal,
                error=error,
                log_ingredients=True,
                prefill_ingredients=ingredients,
            )
        return redirect("/")

    @app.route("/meal_log")
    def meal_log():
        meal_log = log.get_log(users.user_id(), db)
        return render_template("meal_log.html", log=meal_log)

    @app.route("/all_ingredients")
    def all_ingredients():
        all_ingredients = log.get_ingredients(users.user_id(), db)
        return render_template("ingredients.html", ingredients=all_ingredients)

    @app.route("/suggestions")
    def suggestions():
        suggestions = log.generate_suggestions(users.user_id(), db)
        return render_template("suggestions.html", suggestions=suggestions)

    @app.route("/get_meals_with_<ingredient>")
    def get_meals_with_ingredient(ingredient):
        meals = log.get_meals_with_ingredient(ingredient, users.user_id(), db)
        return render_template(
            "meals_with_ingredient.html",
            ingredient=ingredient,
            meals=meals
        )

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "GET":
            return render_template("login.html")
        username = request.form["username"]
        password = request.form["password"]
        try:
            users.login(username, password, db)
        except Exception as error:
            return render_template(
                "login.html",
                error=error,
                prefill_username=username,
                prefill_password=password,
            )
        return redirect("/")

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "GET":
            return render_template("register.html")
        username = request.form["username"]
        password = request.form["password"]
        try:
            users.register(username, password, db)
        except Exception as error:
            return render_template(
                "register.html",
                error=error,
                prefill_username=username,
                prefill_password=password,
            )
        return redirect("/")

    @app.route("/logout")
    def logout():
        users.logout()
        return redirect("/")
