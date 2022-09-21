from flask import render_template, request, session, redirect

from mealbase import users


def create_routes(app, db):
    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "GET":
            return render_template("login.html")

        username = request.form["username"]
        password = request.form["password"]
        # TODO: check username and password
        session["username"] = username
        return redirect("/")
