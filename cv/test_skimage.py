from skimage import (io,
                     filters,
                     color,
                     exposure,
                     feature,
                     measure,
                     img_as_ubyte)
import numpy as np


def color_feature(img):
    # pre deal
    img = img[:, :, :3]

    img_hsv = color.rgb2hsv(img)

    io.imsave("output/skimage_color_0.png", img_hsv)

    blur = filters.gaussian(img_hsv, sigma=1)

    io.imsave("output/skimage_color_1.png", blur)

    # cal hist
    hist = exposure.histogram(blur)

    return hist


def edge_feature(img):
    # pre deal
    img_gray = color.rgb2gray(img)

    io.imsave("output/skimage_edge_0.png", img_gray)

    blur = filters.gaussian(img_gray, sigma=5)

    io.imsave("output/skimage_edge_1.png", blur)

    # cal hu
    moments = measure.moments(blur)
    hu = measure.moments_hu(moments)

    # cal edge curvature
    thresh = filters.threshold_otsu(blur)

    binary = (blur <= thresh)

    io.imsave("output/skimage_edge_2.png", np.where(binary, 0, 255))

    edge = feature.canny(binary, sigma=0)

    io.imsave("output/skimage_edge_3.png", np.where(edge, 0, 255))

    contours = measure.find_contours(binary, level=0.5)
    print(len(contours))
    contours = measure.find_contours(edge, level=0.5)
    print(len(contours))

    return hu


def texture_feature(img):
    # pre deal
    img_gray = color.rgb2gray(img)

    img_gray = img_as_ubyte(img_gray)

    # glcm
    G = feature.greycomatrix(img_gray, [1],
                             [0, np.pi / 4, np.pi / 2, 3 * np.pi / 4])

    p = G / G.sum()

    asm = np.square(p).sum()
    ent = np.square(p).sum()

    def correlation(p):
        row, col = p.shape

        i = np.arange(row)
        j = np.arange(col)
        sum_by_row = p.sum(axis=0)
        sum_by_col = p.sum(axis=1)

        ui = (i * sum_by_row).sum()
        uj = (j * sum_by_col).sum()

        si = np.sqrt((np.square(i - ui) * sum_by_row).sum())
        sj = np.sqrt((np.square(j - uj) * sum_by_col).sum())

        cor = ((np.array([i]) * np.array([j]) * p - ui * uj) / (si * sj)).sum()

        return cor

    cor = correlation(p)

    return asm, ent, cor


if __name__ == "__main__":
    img = io.imread("f_test.png")

    c_feature = color_feature(img)

    e_feature = edge_feature(img)

    t_feature = texture_feature(img)
