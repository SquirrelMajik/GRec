# coding=utf-8
from __future__ import absolute_import

from utils.api_utils import output_json
from utils.helpers import now
from flask import (request,
                   current_app)
import os


@output_json
def flower_rec():
    image = get_image()
    features = extract_features(image)
    result = analyze(features)

    return output_result(result)


def get_image():
    file = request.files.get('grec_file')
    if not file:
        raise Exception("upload grec file, please!")

    file_ext = os.path.splitext(file.filename)[-1]
    temp_file_name = "{}{}".format(now(), file_ext)
    file_path = os.path.join(current_app.config['TEMP_DIR'], temp_file_name)
    file.save(file_path)
    return file_path


def extract_features(image):
    pass


def analyze(features):
    pass


def output_result(result):
    return {
        "result": "success"
    }
