# -*- coding:utf-8 -*-

import cv2
import numpy
from PIL import Image
import matplotlib.pyplot as plt

def cleanImage():
    img = cv2.imread('D:/testImage/2.png')
    height = img.shape[0]
    width = img.shape[1]
    channels = img.shape[2]

    value = [0] * 3
    gray_img = numpy.zeros([height, width], numpy.uint8)
    for row in range(height):
        for column in range(width):
            for chan in range(channels):
                value[chan] = img[row, column, chan]
            R = value[2]
            G = value[1]
            B = value[0]
            if 7500000<(R << 16)|(G << 8)|B<15500000:
                gray_img[row, column] = 0
            else:
                gray_img[row, column] = 255

    cv2.imwrite('D:/trainImage/1.png', gray_img)



def new_image():
    img = cv2.imread('D:/testImage/1.png')
    height = img.shape[0]
    width = img.shape[1]
    channels = img.shape[2]

    value = [0] * 3
    gray_img = numpy.zeros([height, width], numpy.uint8)

    for row in range(height):
        for column in range(width):
            for chan in range(channels):
                value[chan] = img[row, column, chan]
            R = value[2]
            G = value[1]
            B = value[0]
            # new_value = 0.2989 * R + 0.5870 * G + 0.1140 * B
            new_value = 0.2989 * R + 0.5870 * G + 0.1140 * B # 转为灰度像素
            gray_img[row, column] = new_value

    # 根据阈值来二值化
    # ret,thresh1 = cv2.threshold(gray_img, 153, 255, cv2.THRESH_BINARY)
    # ret, thresh1 = cv2.threshold(gray_img, 119, 255, cv2.THRESH_BINARY_INV)
    # cv2.imshow('original image', img)
    # cv2.waitKey(0)
    # cv2.imshow('gray image', gray_img)
    # cv2.waitKey(0)
    cv2.imwrite('D:/trainImage/gray_img.png', gray_img)
    # cv2.imwrite('D:/trainImage/fimage1.png', thresh1)

def get_gray_pic():
    # 画灰度直方图
    src = cv2.imread('D:/trainImage/2.png')

    hist = cv2.calcHist([src], [0], None, [256], [0, 256])
    s = []
    for i in range(len(hist)):
        s.append(hist[i][0])
    s.remove(max(s))
    s.remove(max(s))
    s.remove(max(s))
    print s.index(max(s))
    plt.plot(hist)
    plt.show()

    cv2.waitKey()

if __name__ == '__main__':
    get_gray_pic()
