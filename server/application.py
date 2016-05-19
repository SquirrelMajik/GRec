# coding=utf-8
from __future__ import absolute_import

import traceback

from flask import Flask, current_app, request
# from mongokit import Connection as MongodbConn

from logging.handlers import RotatingFileHandler

import logging

from envs import CONFIG_NAME
from config import config
from utils.encoders import Encoder
from utils.api_utils import make_json_response, make_cors_headers
from apiresps.errors import (NotFound,
                             BadRequest,
                             MethodNotAllowed,
                             UncaughtException)

from utils.classflier import classflier


__version_info__ = ('0', '1', '0')
__version__ = '.'.join(__version_info__)

__artisan__ = ['Majik']


def create_app(config_name='development'):
    config_name = CONFIG_NAME or config_name

    app = Flask(__name__)

    app.version = __version__
    app.artisan = __artisan__

    # config
    app.config.from_object(config[config_name])
    app.json_encoder = Encoder
    app.debug = app.config.get("DEBUG")

    # classflier
    app.classflier = classflier()

    # logging
    if app.config.get("TESTING") is True:
        app.logger.setLevel(logging.FATAL)
    else:
        error_file_handler = RotatingFileHandler(
            app.config.get("LOGGING")["error"]["file"],
            maxBytes=app.config.get("LOGGING_ROTATING_MAX_BYTES"),
            backupCount=app.config.get("LOGGING_ROTATING_BACKUP_COUNT")
        )

        error_file_handler.setLevel(logging.WARNING)
        error_file_handler.setFormatter(
            logging.Formatter(app.config.get('LOGGING')['error']['format'])
        )

        app.logger.addHandler(error_file_handler)

    # database connections
    # app.mongodb_database = MongodbConn(
    #     host=app.config.get("DB_HOST"),
    #     port=app.config.get("DB_PORT"))

    # app.mongodb_conn = app.mongodb_database[app.config.get("DB_DBNAME")]

    from blueprints.rec import blueprint as rec_bp
    app.register_blueprint(rec_bp)

    # register error handlers
    @app.errorhandler(404)
    def app_error_404(error):
        return make_json_response(NotFound(repr(error)))

    @app.errorhandler(405)
    def app_error_405(error):
        return make_json_response(MethodNotAllowed(repr(error)))

    @app.errorhandler(400)
    def app_error_400(error):
        return make_json_response(BadRequest(repr(error)))

    @app.errorhandler(Exception)
    def app_error_uncaught(error):
        current_app.logger.warn(
            "Error: Uncaught\n{}".format(traceback.format_exc()))
        return make_json_response(UncaughtException(repr(error)))

    @app.before_request
    def app_before_request():
        # cors response
        if request.method == "OPTIONS":
            resp = current_app.make_default_options_response()
            cors_headers = make_cors_headers()
            resp.headers.extend(cors_headers)
            return resp

    print("-------------------------------------------------------")
    print("Grec: {}".format(app.version))
    print("Developers: {}".format(', '.join(app.artisan)))
    print("-------------------------------------------------------")

    return app
