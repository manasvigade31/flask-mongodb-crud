from flask import Flask
from flask_pymongo import PyMongo
from .config import Config
from flask_bcrypt import Bcrypt

mongo = PyMongo()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    bcrypt.init_app(app)
    mongo.init_app(app)

    from .routes import app as routes_blueprint
    app.register_blueprint(routes_blueprint)

    return app
