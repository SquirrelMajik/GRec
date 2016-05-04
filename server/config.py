# coding=utf-8
from __future__ import absolute_import

import os
from datetime import timedelta


class Config(object):
    DEBUG = True
    SECRET_KEY = 'Grec_666'

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    TEMP_DIR = os.path.join(BASE_DIR, "temp")

    # DB_HOST = '127.0.0.1'
    # DB_PORT = 27017

    ALLOW_ORIGINS = ['*']
    ALLOW_CREDENTIALS = False

    EXPIRES_IN = timedelta(seconds=3600 * 24 * 30)

    # logging
    LOG_FOLDER = os.path.join(BASE_DIR, 'deploy')
    LOGGING = {
        'error': {
            'format': '%(asctime)s %(levelname)s: %(message)s'+
                      ' [in %(pathname)s:%(lineno)d]',
            'file': os.path.join(LOG_FOLDER, "error.log")
        }
    }

    LOGGING_ROTATING_MAX_BYTES = 64 * 1024 * 1024
    LOGGING_ROTATING_BACKUP_COUNT = 5


class DevelopmentConfig(Config):
    # DB_DBNAME = 'grec_dev'
    pass


class TestCaseConfig(Config):
    # DB_DBNAME = 'grec_testcase'
    pass


class TestingConfig(Config):
    # DB_DBNAME = 'grec_test'
    pass


class ProductionConfig(Config):
    DEBUG = False
    # DB_DBNAME = 'grec_prd'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    "testcase": TestCaseConfig,
    'default': DevelopmentConfig
}
