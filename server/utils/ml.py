# coding=utf-8
from __future__ import absolute_import

import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC


def load_data(data_file):
    dataset = np.loadtxt(data_file, delimiter=",")

    X = dataset[:, 0:-1]
    y = dataset[:, -1]

    return X, y


def knn_model(X, y):
    model = KNeighborsClassifier(10)

    model.fit(X, y)

    return model


def svm_model(X, y):
    model = SVC()

    model.fit(X, y)

    return model


def init(data_file):
    X, y = load_data(data_file)

    knn = knn_model(X, y)
    svm = svm_model(X, y)

    return knn, svm
