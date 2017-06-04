# -*- coding:utf-8 -*-
# Date:2017-09-12

import cv2
import numpy

def img2gray(img):
    height = img.shape[0]
    width = img.shape[1]
    channels = img.shape[2]
    value = [0] * 3
    gray_img = numpy.zeros([height, width], numpy.uint8)
    for row in range(height):
        for col in range(width):
            for chan in range(channels):
                value[chan] = img[row, col, chan]
            R = value[2]
            G = value[1]
            B = value[0]
            if int(R) + int(G) + int(B) != 765:
                gray_img[row, col] = 0.2989 * R + 0.5870 * G + 0.1140 * B
            else:
                gray_img[row, col] = 255
    # cv2.imwrite('../data/result_19_2.png', gray_img)
    return gray_img


def im2bw(img):
    # img = img2gray(img)
    GrayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # ret, thresh1 = cv2.threshold(GrayImage, 254, 255, cv2.THRESH_BINARY)
    thresh1 = cv2.adaptiveThreshold(GrayImage, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY, 25, 5)
    # hist = cv2.calcHist([img], [0], None, [256], [0, 256])
    # s = []
    # for i in range(len(hist)):
    #     s.append(hist[i][0])
    # temp = s[200:255]
    # # s.remove(max(s))
    # flag = max(temp)
    # if flag > 100:
    #     ret, thresh1 = cv2.threshold(img, 254, 255, cv2.THRESH_BINARY)  #  当前点值大于阈值时，取Maxval,也就是第四个参数，下面再不说明，否则设置为0
    # else:
    #     ret, thresh1 = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY)
    # else:
    # thresh1 = cv2.adaptiveThreshold(img, 25, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 5)
    # elif 100 <= flag < 150:
    #     ret, thresh1 = cv2.threshold(img, flag+80, 255, cv2.THRESH_BINARY)
    # elif 150 <= flag < 200:
    #     ret, thresh1 = cv2.threshold(img, flag+50, 255, cv2.THRESH_BINARY)
    # else:
    #     ret, thresh1 = cv2.threshold(img, flag, 255, cv2.THRESH_BINARY)
    # contours, hierarchy = cv2.findContours(thresh1,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    # cv2.drawContours(img, contours, -1, (0, 0, 255), 3)
    # cv2.imshow("img", img)
    # cv2.waitKey(0)
    # cv2.imwrite('../data/final_image9.png', thresh1)
    # thresh1 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 13, 3)
    return thresh1

def im2bw2(img):
    GrayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh1 = cv2.threshold(GrayImage, 254, 255, cv2.THRESH_BINARY)
    return thresh1

if __name__ == '__main__':
    img = cv2.imread('../data/new/12.png')
    image = im2bw(img)
    cv2.imwrite("../data/result2/2.png",image)