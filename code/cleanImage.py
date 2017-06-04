# -*- coding:utf-8 -*-
# Date:2017-09-08

import cv2
import numpy

def rgb2hsv(R,G,B):
    var_max = max(R,G,B)
    var_min = min(R,G,B)
    diffrence = var_max - var_min
    h = 0
    if var_max == var_min:
        h = 0
    elif var_max == R and G >= B:
        h = 60 * (int(G)-int(B))/diffrence
    elif var_max == R and G < B:
        h = 60 * (int(G)-int(B))/diffrence + 360
    elif var_max == G:
        h = 60 * (int(B)-int(R))/diffrence + 120
    elif var_max == B:
        h = 60 * (int(R)-int(G))/diffrence + 240

    return h

from collections import Counter
def getMaxFour(colorList):
    myList = []
    myDict = dict(Counter(colorList))
    if myDict[0] > 150:
        myList.append(0)
    else:
        myDict.pop(0)
    maxIndex = sorted(myDict, key=lambda x: myDict[x])[-1]
    secondIndex = sorted(myDict, key=lambda x: myDict[x])[-2]
    thirdIndex = sorted(myDict, key=lambda x: myDict[x])[-3]
    fourthIndex = sorted(myDict, key=lambda x: myDict[x])[-4]
    fifthIndex = sorted(myDict, key=lambda x: myDict[x])[-5]
    sixthIndex = sorted(myDict, key=lambda x: myDict[x])[-6]
    myList.append(maxIndex)
    myList.append(secondIndex)
    myList.append(thirdIndex)
    myList.append(fourthIndex)
    if myDict[fifthIndex] > 40:
        myList.append(fifthIndex)
    if myDict[sixthIndex] > 40:
        myList.append(sixthIndex)
    return myList


def handleImage():
    img = cv2.imread('../data/new/56.png')
    height = img.shape[0]
    width = img.shape[1]
    channels = img.shape[2]
    value = [0] * 3
    colorList = []
    for row in range(height):
        for col in range(width):
            for chan in range(channels):
                value[chan] = img[row, col, chan]
            R = value[2]
            G = value[1]
            B = value[0]
            if R == 255 and G ==255 and B == 255:
                pass
            else:
                h = rgb2hsv(R,G,B)
                # if h != 0:
                colorList.append(h)
    return colorList

def handleImage2():
    img = cv2.imread('../data/new/56.png')
    height = img.shape[0]
    width = img.shape[1]
    channels = img.shape[2]
    value = [0] * 3
    colorList = []
    for row in range(height):
        for col in range(width):
            for chan in range(channels):
                value[chan] = img[row, col, chan]
            R = value[2]
            G = value[1]
            B = value[0]
            if R == 255 and G == 255 and B == 255:
                pass
            else:
                colorList.append(int(R)+int(G)+int(B))
    return colorList

def cleanImage(myList):
    img = cv2.imread('../data/new/56.png')
    height = img.shape[0]
    width = img.shape[1]
    channels = img.shape[2]
    value = [0] * 3
    # gray_img = numpy.zeros([height, width], numpy.uint8)
    recoverR = numpy.zeros([height, width], numpy.uint8)
    recoverG = numpy.zeros([height, width], numpy.uint8)
    recoverB = numpy.zeros([height, width], numpy.uint8)
    for row in range(height):
        for col in range(width):
            for chan in range(channels):
                value[chan] = img[row, col, chan]
            R = value[2]
            G = value[1]
            B = value[0]
            h = rgb2hsv(R, G, B)
            if h in myList:
                recoverB[row, col] = B
                recoverG[row, col] = G
                recoverR[row, col] = R
                # gray_img[row, col] = 0.2989 * R + 0.5870 * G + 0.1140 * B
            else:
                # gray_img[row, col] = 255
                recoverB[row, col] = 255
                recoverG[row, col] = 255
                recoverR[row, col] = 255
    merged = cv2.merge([recoverB, recoverG, recoverR])
    cv2.imwrite('../data/result2/gggg.png', merged)
    return merged

from matplotlib import pyplot as plt
def draw_hist(myList,Title,Xlabel,Ylabel,Xmin,Xmax):
    plt.hist(myList, 100)
    plt.xlabel(Xlabel)
    plt.xlim(Xmin, Xmax)
    plt.ylabel(Ylabel)
    plt.title(Title)
    plt.show()



def im2bw(img):
    # img = cv2.imread('../data/2_0.jpg',0)
    # hist = cv2.calcHist([img], [0], None, [256], [0, 256])
    # s = []
    # for i in range(len(hist)):
    #     s.append(hist[i][0])
    # s.remove(max(s))
    # flag = s.index(max(s))
    ret, thresh1 = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY)
    # contours, hierarchy = cv2.findContours(thresh1,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    # cv2.drawContours(img, contours, -1, (0, 0, 255), 3)
    # cv2.imshow("img", img)
    # cv2.waitKey(0)
    cv2.imwrite('../data/dddd.png', thresh1)



if __name__ == '__main__':
    myList = handleImage()
    # draw_hist(myList, 'pic', 'h', 'frequency', 0, 361)
    # im2bw()
    # myList = handleImage()
    List = getMaxFour(myList)
    img = cleanImage(List)
    # im2bw(img)
    # draw_hist(myList,'pic','h','frequency',0,765)
    # gray_img = cleanImage()
    # im2bw()
    # import numpy as np
    # import cv2
    #
    # img = cv2.imread('../data/result_8_1.png')
    # Z = img.reshape((-1, 3))
    #
    # Z = np.float32(Z)
    #
    # # define criteria, number of clusters(K) and apply kmeans()
    # criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    # K = 3
    # ret, label, center = cv2.kmeans(Z, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    #
    # # Now convert back into uint8, and make original image
    # center = np.uint8(center)
    # res = center[label.flatten()]
    # res2 = res.reshape((img.shape))
    #
    # cv2.imshow('res2', res2)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


