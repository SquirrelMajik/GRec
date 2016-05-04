# coding=utf-8
from __future__ import absolute_import

import multiprocessing


bind = "127.0.0.1:6002"
workers = multiprocessing.cpu_count() * 2 + 1
accesslog = "deploy/grec.access.log"
errorlog = "deploy/grec.error.log"
pidfile = "deploy/grec.pid"
raw_env = "GREC_CONFIG_NAME=production"
