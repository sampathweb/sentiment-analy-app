from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
db = SQLAlchemy()

# A Dictionary to contained Trained Models for re-use
trained_models = {}


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_name)

    #init SQLAlchemy
    db.init_app(app)
    db.Model = Base

    # register our blueprints
    from app.blueprints import datasets, predictors
    app.register_blueprint(datasets)
    app.register_blueprint(predictors)

    return app
