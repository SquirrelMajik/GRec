# coding=utf-8
from __future__ import absolute_import

from .controllers import *

urlpatterns = [
    # open api
    ("/", flower_rec, "POST"),
]
