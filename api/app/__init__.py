from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
db = SQLAlchemy()

# A Dictionary to contained Trained Models for re-use
trained_models = {}


def create_app(config_name):
    '''Retuns flask app object based on config settings.
        Initializes DB and registers endpoints
    '''
    app = Flask(__name__)
    app.config.from_object(config_name)

    #init SQLAlchemy
    db.init_app(app)
    db.Model = Base

    # register API endpoints as blueprints
    from app.blueprints import main, datasets, predictors
    app.register_blueprint(main)
    app.register_blueprint(datasets)
    app.register_blueprint(predictors)

    return app
