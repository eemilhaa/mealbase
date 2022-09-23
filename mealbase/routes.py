from flask import render_template, request, redirect

from mealbase import users


def create_routes(app, db):
    @app.route("/log_meal", methods=["GET", "POST"])
    def log_meal():
        if request.method == "GET":
            return render_template("log_meal.html")

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "GET":
            return render_template("login.html")

        username = request.form["username"]
        password = request.form["password"]
        users.login(username, password, db)
        return redirect("/")

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "GET":
            return render_template("register.html")
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]
            role = request.form["role"]
            users.register(username, password, role, db)
            return redirect("/")

    @app.route("/logout")
    def logout():
        users.logout()
        return redirect("/")
