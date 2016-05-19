import cv2
import numpy as np


def show_and_bak(img, dest, wait=1):
    cv2.imshow(dest, img)
    cv2.waitKey(wait)
    cv2.destroyAllWindows()

    cv2.imwrite(dest, img)


def read(src):
    img = cv2.imread(src, -1)

    show_and_bak(img, "output/test_0.png")

    return img


def pre(img):
    blur = cv2.GaussianBlur(img, (5, 5), 0)

    show_and_bak(blur, "output/test_1.png")

    return blur


def hist_color(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    show_and_bak(hsv, "output/test_2.png")

    blur = cv2.GaussianBlur(hsv, (5, 5), 0)

    show_and_bak(blur, "output/test_3.png")

    hist = cv2.calcHist([hsv], [0, 1], None, [180, 256], [0, 180, 0, 256])

    show_and_bak(hist, "output/test_4.png")

    return hist


def hist_edge(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    show_and_bak(gray, "output/test_5.png")

    blur = cv2.GaussianBlur(gray, (25, 25), 0)

    show_and_bak(blur, "output/test_6.png")

    ret, thresh = cv2.threshold(blur, 0, 255,
                                cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    show_and_bak(thresh, "output/test_7.png")

    canny = cv2.Canny(thresh, 100, 200)

    show_and_bak(canny, "output/test_8.png")

    moments = cv2.moments(thresh)
    hu_moments = cv2.HuMoments(moments)

    image, contours, hierarchy = cv2.findContours(canny, cv2.RETR_TREE,
                                                  cv2.CHAIN_APPROX_NONE)

    edge_curvature = cal_edge_curvature(thresh, contours)

    thresh_with_contours = cv2.drawContours(thresh, contours,
                                            -1, (127, 255, 127), 3)

    show_and_bak(thresh_with_contours, "output/test_9.png")
    show_and_bak(image, "output/test_10.png")

    return hu_moments, edge_curvature


def cal_edge_curvature(img, contours):
    width, height = img.shape
    r = max(width, height) // 4
    empty_img = create_empty_image(width, height)
    circle_img = cv2.circle(empty_img,
                            (width // 2, height // 2),
                            r, (255, 255, 255), -1)
    circle_img = cv2.cvtColor(circle_img, cv2.COLOR_BGR2GRAY)

    S = cv2.countNonZero(circle_img)

    def count_non_zore_in_edge(dot):
        white_img = create_white_image(width, height)

        x, y = dot[0]
        mask = cv2.circle(white_img, (x, y), r, (0, 0, 0), -1)
        mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(mask, 0, 255,
                                  cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        img_for_cal = cv2.subtract(img, mask)

        # show_and_bak(img_for_cal, "output/test_11.png")

        return cv2.countNonZero(img_for_cal)

    I = np.array([count_non_zore_in_edge(dot)
                  for contour in contours for dot in contour])

    c = I / S

    return c


def create_empty_image(width, height):
    return np.zeros((width, height, 3), np.uint8)


def invert(img):
    return 255 - img


def create_white_image(width, height):
    empty_img = create_empty_image(width, height)
    return invert(empty_img)


def test(img):
    width, height, _ = img.shape
    white_img = create_white_image(width, height)
    r = max(width, height) // 4
    cv2.circle(white_img, (width // 2, height // 2), r, 0, -1)
    show_and_bak(white_img, "output/test_11.png")


if __name__ == "__main__":
    img = read("f_test.png")
    pre_img = pre(img)
    color_hist = hist_color(img)
    hu_moments, edge_curvature = hist_edge(img)
