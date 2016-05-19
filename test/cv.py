# coding=utf-8
from __future__ import absolute_import

import numpy as np
from skimage import (io,
                     draw,
                     filters,
                     color,
                     exposure,
                     feature,
                     measure,
                     img_as_ubyte,
                     segmentation)


def color_feature(blur, hbins=15, sbins=15):
    hsv = color.rgb2hsv(blur)

    # cal hist
    h_hist = exposure.histogram(hsv[:, :, 0], nbins=hbins)
    s_hist = exposure.histogram(hsv[:, :, 1], nbins=sbins)

    return np.append(normalize(h_hist[0]), normalize(s_hist[0]))


def hu_feature(gray):

    moments = measure.moments(gray)
    hu = measure.moments_hu(moments)

    return normalize(hu)


def edge_curvature_feature(binary, cbins=15):

    contours = measure.find_contours(binary, level=0.5)

    c = cal_edge_curvature(binary, contours, cbins=cbins)

    return normalize(c[0])


def edge_feature(gray, binary, cbins=15):

    hu = hu_feature(gray)

    c_hist = edge_curvature_feature(binary, cbins=cbins)

    return hu, c_hist


def cal_edge_curvature(binary, contours, cbins=15):
    contours = contours[0]

    height = binary.shape[0]
    width = binary.shape[1]

    mask = np.zeros((height, width), dtype=np.uint8)
    radius = 20
    rr, cc = draw.circle(height // 2, width // 2, radius)
    mask[rr, cc] = 1
    S = np.count_nonzero(mask)

    def count_with_edge(dot):
        r, c = dot
        mask = np.zeros((height, width), dtype=np.uint8)
        rr, cc = draw.circle(r, c, radius)

        # min_r = np.where(rr >= 0)[0][0]
        # min_c = np.where(cc >= 0)[0][0]
        # min_i = max(min_r, min_c)

        # print(r, c)
        # print(height, width)
        # print(rr)
        # print(cc)
        # max_r = np.where(rr < height)[0][-1]
        # max_c = np.where(cc < width)[0][-1]
        # max_i = min(max_r, max_c)

        # # print(width, height)
        # # print(rr.shape)
        # # print(cc.shape)
        # # print(rr[min_i: max_i])
        # # print(cc[min_i: max_i])
        # rr = rr[min_i: max_i]
        # cc = cc[min_i: max_i]
        # print(rr)
        # print(cc)

        for _r, _c in zip(rr, cc):
            if 0 <= _r < height and 0 <= _c < width:
                mask[_r, _c] = 1

        # mask[rr, cc] = 1
        binary_for_cal = np.where(mask == 1, binary, False)
        return np.count_nonzero(binary_for_cal)

    I = np.array([count_with_edge(contour) for contour in contours])

    c = I / S

    c_hist = exposure.histogram(c, nbins=cbins)

    return c_hist


def texture_feature(gray):
    # glcm
    G_list = feature.greycomatrix(gray, [1],
                                  [0, np.pi / 4, np.pi / 2, 3 * np.pi / 4])

    def glcm(G):
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

            cor = (
                (np.array([i]) * np.array([j]) * p - ui * uj) / (si * sj)
            ).sum()

            return cor

        p = G / G.sum()

        asm = np.square(p).sum()
        ent = np.square(p).sum()

        cor = correlation(p)

        return np.array([asm, ent, cor])

    G = np.array([])
    for i in range(4):
        G = np.append(G, glcm(G_list[:, :, 0, i]))

    return G


def pre_deal(img):

    img = img[:, :, :3]

    blur = get_blur(img)

    gray = get_gray(blur)

    binary = get_binary(gray)

    blur = cut_img(blur, binary)

    # reprocess

    gray = get_gray(blur)

    return blur, gray, binary


def get_blur(img):
    return filters.gaussian(img, sigma=5)


def get_gray(blur):
    gray = color.rgb2gray(blur)
    return img_as_ubyte(gray)


def get_binary(gray):
    thresh = filters.threshold_otsu(gray)
    return (gray <= thresh)


def cut_img(img, binary):
    height = img.shape[0]
    width = img.shape[1]

    for r in range(height):
        for c in range(width):
            if binary[r, c]:
                img[r, c] = np.array([0, 0, 0])

    return img


def load_image(image_path):
    img = io.imread(image_path)

    return pre_deal(img)


def normalize(X):
    return (X - np.min(X)) / (np.max(X) - np.min(X))


def get_features(image_path, hbins=15, sbins=10, cbins=15):
    blur, gray, binary = load_image(image_path)

    color = color_feature(blur, hbins=hbins, sbins=sbins)

    hu, curvature = edge_feature(gray, binary, cbins=cbins)

    glcm = texture_feature(gray)

    return color, hu, curvature, glcm


if __name__ == '__main__':
    blur, gray, binary = load_image("f_test_bak.png")

    io.imsave("output/new_test_1.png", blur)

    io.imsave("output/new_test_2.png", gray)

    io.imsave("output/new_test_3.png", np.where(binary, 0, 255))
