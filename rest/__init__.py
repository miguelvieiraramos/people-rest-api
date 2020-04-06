from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    from rest.controllers.people import people

    app.register_blueprint(people)
    return app
