from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config
from flask_redis import FlaskRedis
import logging

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = current_app.config["SQLALCHEMY_DATABASE_URI"]


db = SQLAlchemy()
redis_store = FlaskRedis()
# login_manager = LoginManager()
# login_manager.session_protection = 'strong'
# login_manager.login_view = 'main.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.config['SQLALCHEMY_POOL_SIZE'] = 50
    app.config['SQLALCHEMY_POOL_RECYCLE'] = 3600
    app.config['SQLALCHEMY_POOL_TIMEOUT'] = 30
    app.config['SQLALCHEMY_MAX_OVERFLOW'] = 30
    config[config_name].init_app(app)
    redis_store.init_app(app)
    db.init_app(app)

    # login_manager.init_app(app)
    file_handler = logging.FileHandler('cms_error.log')
    logging_format = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
    file_handler.setFormatter(logging_format)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)

    from .wang_yi import wangyi
    app.register_blueprint(wangyi)

    return app