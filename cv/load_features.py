import test_skimage
import os

FEATURE_DIR = "feature"
IMAGES_DIR = "images"


def is_image_file(src):
    return src.endswith(".jpg") or src.endswith(".png")


def run():
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
                color, hu, curvature, glcm = test_skimage.get_features(
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


if __name__ == '__main__':
    run()
