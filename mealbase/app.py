from flask import Flask
from mealbase.config import DATABASE_URL, SECRET_KEY
from mealbase.routes import create_routes
from mealbase.db import db


def create_app():
    app = Flask(__name__)
    app.secret_key = SECRET_KEY
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
    db.init_app(app)
    create_routes(app=app, db=db)
    return app
