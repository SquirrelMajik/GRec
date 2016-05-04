import numpy as np
import urllib
from sklearn import preprocessing, metrics
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC


def load_data():
    # url with dataset
    url = "http://archive.ics.uci.edu/ml/machine-learning-databases" + \
          "/pima-indians-diabetes/pima-indians-diabetes.data"
    # download the file
    raw_data = urllib.urlopen(url)
    # load the CSV file as a numpy matrix
    dataset = np.loadtxt(raw_data, delimiter=",")
    # separate the data from the target attributes
    X = dataset[:, 0:7]
    y = dataset[:, 8]

    return X, y


def normalize_data(X):
    # normalize the data attributes
    # x′=(x−min) / (max−min)
    normalized_X = preprocessing.normalize(X)
    # standardize the data attributes
    # x′=(x−μ) / σ
    standardized_X = preprocessing.scale(X)

    print(normalized_X)
    print(standardized_X)

    return normalized_X, standardized_X


def select_feature(X, y):
    model = ExtraTreesClassifier()
    model.fit(X, y)
    # display the relative importance of each attribute
    print(model.feature_importances_)


def logistic_regression(X, y):
    model = LogisticRegression()
    model.fit(X, y)
    print(model)
    # make predictions
    expected = y
    predicted = model.predict(X)
    # summarize the fit of the model
    print(metrics.classification_report(expected, predicted))
    print(metrics.confusion_matrix(expected, predicted))


def bayes(X, y):
    model = GaussianNB()
    model.fit(X, y)
    print(model)
    # make predictions
    expected = y
    predicted = model.predict(X)
    # summarize the fit of the model
    print(metrics.classification_report(expected, predicted))
    print(metrics.confusion_matrix(expected, predicted))


def knn(X, y):
    # fit a k-nearest neighbor model to the data
    model = KNeighborsClassifier()
    model.fit(X, y)
    print(model)
    # make predictions
    expected = y
    predicted = model.predict(X)
    # summarize the fit of the model
    print(metrics.classification_report(expected, predicted))
    print(metrics.confusion_matrix(expected, predicted))


def decision_tree(X, y):
    # fit a CART model to the data
    model = DecisionTreeClassifier()
    model.fit(X, y)
    print(model)
    # make predictions
    expected = y
    predicted = model.predict(X)
    # summarize the fit of the model
    print(metrics.classification_report(expected, predicted))
    print(metrics.confusion_matrix(expected, predicted))


def svm(X, y):
    # fit a SVM model to the data
    model = SVC()
    model.fit(X, y)
    print(model)
    # make predictions
    expected = y
    predicted = model.predict(X)
    # summarize the fit of the model
    print(metrics.classification_report(expected, predicted))
    print(metrics.confusion_matrix(expected, predicted))


if __name__ == '__main__':
    X, y = load_data()
    normalize_data(X)
