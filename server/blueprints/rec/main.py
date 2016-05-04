# coding=utf-8
from __future__ import absolute_import

from flask import (Blueprint,
                   request)

from apiresps import APIError

from utils.helpers import route_inject
from utils.api_utils import make_json_response

from .routes import urlpatterns


bp_name = "rec"

open_api_endpoints = [
    "{}.flower_rec".format(bp_name)
]

blueprint = Blueprint(bp_name, __name__)

route_inject(blueprint, urlpatterns)


@blueprint.before_app_first_request
def before_first_request():
    pass


@blueprint.before_request
def before():
    if request.endpoint in open_api_endpoints:
        pass


@blueprint.errorhandler(APIError)
def blueprint_api_err(err):
    return make_json_response(err)
