import cv2


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
    thresh_with_contours = cv2.drawContours(thresh, contours,
                                            -1, (127, 255, 127), 3)

    show_and_bak(thresh_with_contours, "output/test_9.png")
    show_and_bak(image, "output/test_10.png")

    return hu_moments


if __name__ == "__main__":
    img = read("f_test.png")
    pre_img = pre(img)
    color_hist = hist_color(img)
    edge_hist = hist_edge(img)
