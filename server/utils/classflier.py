# coding=utf-8
from __future__ import absolute_import

from utils import ml
from collections import defaultdict

WEIGHTS = {
    "glcm": {
        "svm": 0.07771009588240906,
        "knn": 0.11122458259837771
    },
    "color": {
        "svm": 0.16709569187454637,
        "knn": 0.2161080629739599
    },
    "hu": {
        "svm": 0.06869264826430983,
        "knn": 0.10151042864266999
    },
    "curvature": {
        "svm": 0.1340354327472974,
        "knn": 0.12362305701642982
    }
}

DATA_FILES = {
    "color": "data/color.txt",
    "hu": "data/hu.txt",
    "curvature": "data/curvature.txt",
    "glcm": "data/glcm.txt",
}

# CLASS_NAMES = {
#     "0": "Narcissus",
#     "4": "Crocus Sativus",
#     "7": "Forsythia Suspensa",
#     "9": "Helianthus",
#     "10": "Daisy",
#     "14": "Trollius Chinensis",
#     "15": "Anemone Cathayensis Kitag",
#     "17": "Viola Zest"
# }

CLASS_NAMES = {
    "0": "水仙",
    "4": "藏红花",
    "7": "连翘",
    "9": "向日葵",
    "10": "雏菊",
    "14": "金莲花",
    "15": "银莲花",
    "16": "三色堇"
}


class classflier(object):
    def predict(self, features):
        result = dict()

        for name, feature in features.items():
            knn_predict, svm_predict = self._predict(name, feature)

            knn_predict = self.class_names[knn_predict]
            svm_predict = self.class_names[svm_predict]

            if knn_predict not in result:
                result[knn_predict] = 0
            if svm_predict not in result:
                result[svm_predict] = 0

            result[knn_predict] += self.wights[name]["knn"]
            result[svm_predict] += self.wights[name]["svm"]

        return result

    def _predict(self, name, feature):
        feature = feature.reshape(1, -1)
        knn_predict = self.model[name]["knn"].predict(feature)
        svm_predict = self.model[name]["svm"].predict(feature)

        return str(int(knn_predict)), str(int(svm_predict))

    def __init__(self, weights={}, data_files={}, class_names={}):
        self.wights = weights or WEIGHTS
        self.data_files = data_files or DATA_FILES
        self.class_names = class_names or CLASS_NAMES

        self.model = defaultdict(defaultdict)
        for name, data_file in DATA_FILES.items():
            X, y = ml.load_data(data_file)
            self.model[name]["knn"] = ml.knn_model(X, y)
            self.model[name]["svm"] = ml.svm_model(X, y)


# if __name__ == '__main__':
#     import cv
#     c = classflier()

#     def check(c, file_name):
#         color, hu, curvature, glcm = cv.get_features(file_name)
#         print(c.predict({
#             "color": color,
#             "hu": hu,
#             "curvature": curvature,
#             "glcm": glcm
#         }))

#     for i in range(12):
#         file_name = "test{}.png".format(i + 1)
#         check(c, file_name)
