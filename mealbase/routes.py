from flask import render_template, request, redirect
from datetime import date

from mealbase import users
from mealbase import log


def create_routes(app, db):
    @app.route("/log_meal", methods=["GET", "POST"])
    def log_meal():
        if request.method == "GET":
            return render_template(
                "log_meal.html",
                default_date=date.today()
            )
        users.check_csrf(request.form["csrf_token"])
        meal = request.form["meal"]
        log_date = request.form["date"]
        ingredients = request.form["ingredients"]
        log.log_meal(meal, log_date, ingredients, users.user_id(), db)
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
            return _show_error_page(error, link="/login")
        return redirect("/")

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "GET":
            return render_template("register.html")
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]
            role = request.form["role"]
            try:
                users.register(username, password, role, db)
            except Exception as error:
                return _show_error_page(error, link="/register")
            return redirect("/")

    @app.route("/logout")
    def logout():
        users.logout()
        return redirect("/")


def _show_error_page(error, link="/"):
    return render_template(
        "error.html",
        content=error,
        redirect_to=link,
    )
