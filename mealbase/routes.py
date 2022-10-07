from flask import render_template, request, redirect

from mealbase import users
from mealbase import meals


def create_routes(app, db):
    @app.route("/log_meal", methods=["GET", "POST"])
    def log_meal():
        if request.method == "GET":
            return render_template("log_meal.html")
        meal = request.form["meal"]
        ingredients = request.form["ingredients"]
        meals.log_meal(meal, ingredients, users.user_id(), db)
        return redirect("/")

    @app.route("/meal_log")
    def meal_log():
        meal_log = meals.get_log(users.user_id(), db)
        return render_template("meal_log.html", log=meal_log)

    @app.route("/all_ingredients")
    def all_ingredients():
        all_ingredients = meals.get_ingredients(users.user_id(), db)
        return render_template("ingredients.html", ingredients=all_ingredients)

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
