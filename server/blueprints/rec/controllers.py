# coding=utf-8
from __future__ import absolute_import

from utils.api_utils import output_json
from utils.helpers import now
from flask import (request,
                   current_app)
import os
from utils import cv


@output_json
def flower_rec():
    image = get_image()
    features = extract_features(image)
    result = predict(features)

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


def extract_features(image_path):
    color, hu, curvature, glcm = cv.get_features(image_path)
    return {
        "color": color,
        "hu": hu,
        "curvature": curvature,
        "glcm": glcm
    }


def predict(features):
    predict_result = current_app.classflier.predict(features)

    def find_most_like(result):
        top_2 = sorted(result.items(), key=lambda x: x[1], reverse=True)[:2]
        print(top_2)
        first_like, second_like = top_2

        if first_like[1] - second_like[1] > 0.2 or \
           (first_like[1] > 0.4 and second_like[1] < 0.3):
            return [first_like[0]]
        else:
            return [first_like[0], second_like[0]]

    return find_most_like(predict_result)


def output_result(result):
    return {"maybe": " or ".join(result)}
