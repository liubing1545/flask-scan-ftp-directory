from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from celery import Celery
from config import config, Config
from flask.ext.apscheduler import APScheduler


bootstrap = Bootstrap()
db = SQLAlchemy()
celery = Celery(__name__, broker=Config.CELERY_BROKER_URL)
scheduler = APScheduler()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    bootstrap.init_app(app)
    db.init_app(app)
    scheduler.init_app(app)
    #scheduler.start()
    celery.conf.update(app.config)

    if not app.debug and not app.testing and not app.config['SSL_DISABLE']:
        from flask.ext.sslify import SSLify
        sslify = SSLify(app)

    from .api_1_0 import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')


    #app.debug = False

    return app
