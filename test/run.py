import cv
import ml
import os

from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn import cross_validation

from collections import defaultdict
import json

FEATURE_DIR = "data"
IMAGES_DIR = "images"


def is_image_file(src):
    return src.endswith(".jpg") or src.endswith(".png")


def save_data():
    if not os.path.isdir(FEATURE_DIR):
        os.mkdir(FEATURE_DIR)

    color_file = open(os.path.join(FEATURE_DIR, "color.txt"), 'w')
    hu_file = open(os.path.join(FEATURE_DIR, "hu.txt"), 'w')
    curvature_file = open(os.path.join(FEATURE_DIR, "curvature.txt"), 'w')
    glcm_file = open(os.path.join(FEATURE_DIR, "glcm.txt"), 'w')

    for root, dirs, files in os.walk(IMAGES_DIR):
        for file in files:
            _class = root[-4:]
            file_path = os.path.join(root, file)
            if is_image_file(file_path):
                print(file_path)
                color, hu, curvature, glcm = cv.get_features(
                    file_path)

                _class_str = ',{}\n'.format(_class)
                color_file.write(",".join(map(str, color)) + _class_str)
                hu_file.write(",".join(map(str, hu)) + _class_str)
                curvature_file.write(
                    ",".join(map(str, curvature)) + _class_str)
                glcm_file.write(",".join(map(str, glcm)) + _class_str)

    color_file.close()
    hu_file.close()
    curvature_file.close()
    glcm_file.close()


def test_classifler(classifler, X, y):
    return cross_validation.cross_val_score(classifler, X, y, cv=5)


def test_knn(X, y):
    model = KNeighborsClassifier(10)
    return test_classifler(model, X, y).mean()


def test_svm(X, y):
    model = SVC()
    return test_classifler(model, X, y).mean()


def test_knn_and_snm(data_file):
    X, y = ml.load_data(data_file)
    return test_knn(X, y), test_svm(X, y)


def test_data():
    result = defaultdict(defaultdict)
    for root, dirs, files in os.walk(FEATURE_DIR):
        for f in files:
            file_path = os.path.join(root, f)
            print(file_path)
            predict_result = test_knn_and_snm(file_path)
            print(predict_result)
            result[f[:-4]]["knn"] = predict_result[0]
            result[f[:-4]]["svm"] = predict_result[1]

    return result


def cal_weights(result):
    total = 0
    for feature in result:
        total += result[feature]["knn"] + result[feature]["svm"]

    weights = defaultdict(defaultdict)

    for feature in result:
        weights[feature]["knn"] = result[feature]["knn"] / total
        weights[feature]["svm"] = result[feature]["svm"] / total

    print(json.dumps(weights, indent=4))

    return weights


def run():
    # save_data()
    result = test_data()
    cal_weights(result)



if __name__ == '__main__':
    run()
