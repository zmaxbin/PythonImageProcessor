# -*- coding:utf-8 -*-
# Date:2017-09-12

import cv2
import numpy
from img2binary import im2bw,im2bw2
from CFS import myCFS
from PIL import Image

def rgb2hsl(R,G,B):
    hslList = []
    var_max = max(R,G,B)
    var_min = min(R,G,B)
    diffrence = var_max - var_min
    mysum = int(var_max) + int(var_min)
    h = 0
    s = 0
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

    l = mysum/2.0

    if l == 0 or var_max == var_min:
        s = 0
    elif l > 0 and l <= 0.5:
        s = diffrence / mysum
    elif l > 0.5:
        s = diffrence / (2-2*l)

    hslList.append(h)
    hslList.append(s)
    hslList.append(l)

    return hslList

def hsl2rgb(hslList):
    rgbList = []
    h = hslList[0]
    s = hslList[1]
    l = hslList[2]
    if s != 0:
        q = 0
        if l < 0.5:
            q = l*(l+s)
        elif l >= 0.5:
            q = l+s-(l*s)
        p = 2*l-q
        hk = h/360.0
        tR = hk + (1.0/3)
        tG = hk
        tB = hk - (1.0/3)
        if tR < 0:
            tR = tR + 1.0
        elif tR > 1:
            tR = tR - 1.0
        if tG < 0:
            tG = tG + 1.0
        elif tG > 1:
            tG = tG - 1.0
        if tB < 0:
            tB = tB + 1.0
        elif tB > 1:
            tB = tB - 1.0

        if tR < (1.0/6):
            R = p + ((q-p)*6*tR)
        elif tR >= (1.0/6) and tR < (1.0/2):
            R = q
        elif tR >= (1.0/2) and tR < (2.0/3):
            R = p + ((q-p)*6*(2.0/3-tR))
        else:
            R = p

        if tG < (1.0/6):
            G = p + ((q-p)*6*tG)
        elif tG >= (1.0/6) and tG < (1.0/2):
            G = q
        elif tG >= (1.0/2) and tG < (2.0/3):
            G = p + ((q-p)*6*(2.0/3-tG))
        else:
            G = p

        if tB < (1.0/6):
            B = p + ((q-p)*6*tB)
        elif tB >= (1.0/6) and tB < (1.0/2):
            B = q
        elif tB >= (1.0/2) and tB < (2.0/3):
            B = p + ((q-p)*6*(2.0/3-tB))
        else:
            B = p
    else:
        R = l
        G = l
        B = l
    rgbList.append(R)
    rgbList.append(G)
    rgbList.append(B)
    return rgbList

from collections import Counter
def getMaxFour(colorList):
    myList = []
    myDict = dict(Counter(colorList))
    if myDict[0] > 160:
        myList.append(0)
    else:
        myDict.pop(0)
    maxIndex = sorted(myDict, key=lambda x: myDict[x])[-1]
    secondIndex = sorted(myDict, key=lambda x: myDict[x])[-2]
    thirdIndex = sorted(myDict, key=lambda x: myDict[x])[-3]
    fourthIndex = sorted(myDict, key=lambda x: myDict[x])[-4]
    fifthIndex = sorted(myDict, key=lambda x: myDict[x])[-5]
    sixthIndex = sorted(myDict, key=lambda x: myDict[x])[-6]

    # seventhIndex = sorted(myDict, key=lambda x: myDict[x])[-7]
    # eighthIndex = sorted(myDict, key=lambda x: myDict[x])[-8]

    myList.append(maxIndex)
    myList.append(secondIndex)
    myList.append(thirdIndex)
    myList.append(fourthIndex)
    if myDict[fifthIndex] > 50:
        myList.append(fifthIndex)
    if myDict[sixthIndex] > 50:
        myList.append(sixthIndex)
    # if myDict[seventhIndex] > 60:
    #     myList.append(seventhIndex)
    # if myDict[eighthIndex] > 60:
    #     myList.append(eighthIndex)
    return myList


def handleImage(img):
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
                h = rgb2hsl(R,G,B)[0]
                # if h != 0:
                colorList.append(h)
    return colorList

# 判断是否有干扰线
def has_interfering_line(img):
    GrayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh1 = cv2.threshold(GrayImage, 254, 255, cv2.THRESH_BINARY)  #  当前点值大于阈值时，取Maxval,也就是第四个参数，下面再不说明，否则设置为0
    mycfs = myCFS(thresh1,6,20)
    newImage,number_of_character = mycfs.cfs()
    if number_of_character > 3:
        return False
    else:
        return True

def cleanImage(img,fourList):
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
            if int(R) + int(G) + int(B) != 765:
                if row-1>=0 and row+1<=height and col-1>=0 and col+1<=width:
                    h_list = []
                    w_cnt = 0
                    tempB1, tempG1, tempR1 = img[row - 1, col] #上面
                    if int(tempB1) + int(tempG1) + int(tempR1) != 765:
                        h1 = rgb2hsl(tempR1, tempG1, tempB1)
                        h_list.append(h1)
                    tempB2, tempG2, tempR2 = img[row + 1, col] #下面
                    if int(tempB2) + int(tempG2) + int(tempR2) != 765:
                        h2 = rgb2hsl(tempR2, tempG2, tempB2)
                        h_list.append(h2)
                    tempB3, tempG3, tempR3 = img[row, col - 1] #左边
                    if int(tempB3) + int(tempG3) + int(tempR3) != 765:
                        h3 = rgb2hsl(tempR3, tempG3, tempB3)
                        h_list.append(h3)
                    tempB4, tempG4, tempR4 = img[row, col + 1] #右边
                    if int(tempB4) + int(tempG4) + int(tempR4) != 765:
                        h4 = rgb2hsl(tempR4, tempG4, tempB4)
                        h_list.append(h4)

                    # tempB5, tempG5, tempR5 = img[row - 1, col-1] #左上
                    # if int(tempB5) + int(tempG5) + int(tempR5) != 765:
                    #     h5 = rgb2hsl(tempR5, tempG5, tempB5)
                    #     h_list.append(h5)
                    # tempB6, tempG6, tempR6 = img[row - 1, col+1] #右上
                    # if int(tempB6) + int(tempG6) + int(tempR6) != 765:
                    #     h6 = rgb2hsl(tempR6, tempG6, tempB6)
                    #     h_list.append(h6)
                    # tempB7, tempG7, tempR7 = img[row+1, col - 1] #左下
                    # if int(tempB7) + int(tempG7) + int(tempR7) != 765:
                    #     h7 = rgb2hsl(tempR7, tempG7, tempB7)
                    #     h_list.append(h7)
                    # tempB8, tempG8, tempR8 = img[row+1, col + 1] #右下
                    # if int(tempB8) + int(tempG8) + int(tempR8) != 765:
                    #     h8 = rgb2hsl(tempR8, tempG8, tempB8)
                    #     h_list.append(h8)

                    color = []
                    for data in h_list:
                        for i in fourList:
                            if data[0]  == i:
                                w_cnt = w_cnt + 1
                                color = data
                    if w_cnt > 0:
                        color = hsl2rgb(color)
                        recoverB[row,col] = color[2]
                        recoverG[row,col] = color[1]
                        recoverR[row,col] = color[0]
                    else:
                        recoverB[row,col] = 255
                        recoverG[row,col] = 255
                        recoverR[row,col] = 255

                elif col + 1 >width:
                    h_list = []
                    w_cnt = 0
                    tempB1, tempG1, tempR1 = img[row - 1, col]  # 上面
                    if int(tempB1) + int(tempG1) + int(tempR1) != 765:
                        h1 = rgb2hsl(tempR1, tempG1, tempB1)
                        h_list.append(h1)
                    tempB2, tempG2, tempR2 = img[row + 1, col]  # 下面
                    if int(tempB2) + int(tempG2) + int(tempR2) != 765:
                        h2 = rgb2hsl(tempR2, tempG2, tempB2)
                        h_list.append(h2)
                    tempB3, tempG3, tempR3 = img[row, col - 1]  # 左边
                    if int(tempB3) + int(tempG3) + int(tempR3) != 765:
                        h3 = rgb2hsl(tempR3, tempG3, tempB3)
                        h_list.append(h3)

                    # tempB4, tempG4, tempR4 = img[row - 1, col-1]  # 左上
                    # if int(tempB4) + int(tempG4) + int(tempR4) != 765:
                    #     h4 = rgb2hsl(tempR4, tempG4, tempB4)
                    #     h_list.append(h4)
                    # tempB5, tempG5, tempR5 = img[row + 1, col-1]  # 左下
                    # if int(tempB5) + int(tempG5) + int(tempR5) != 765:
                    #     h5 = rgb2hsl(tempR5, tempG5, tempB5)
                    #     h_list.append(h5)

                    color = []
                    for data in h_list:
                        for i in fourList:
                            if data[0] == i:
                                w_cnt = w_cnt + 1
                                color = data
                    if w_cnt > 0:
                        color = hsl2rgb(color)
                        recoverB[row,col] = color[2]
                        recoverG[row,col] = color[1]
                        recoverR[row,col] = color[0]
                    else:
                        recoverB[row,col] = 255
                        recoverG[row,col] = 255
                        recoverR[row,col] = 255

                elif col - 1 < 0:
                    h_list = []
                    w_cnt = 0
                    tempB1, tempG1, tempR1 = img[row - 1, col]  # 上面
                    if int(tempB1) + int(tempG1) + int(tempR1) != 765:
                        h1 = rgb2hsl(tempR1, tempG1, tempB1)
                        h_list.append(h1)
                    tempB2, tempG2, tempR2 = img[row + 1, col]  # 下面
                    if int(tempB2) + int(tempG2) + int(tempR2) != 765:
                        h2 = rgb2hsl(tempR2, tempG2, tempB2)
                        h_list.append(h2)
                    tempB3, tempG3, tempR3 = img[row, col + 1]  # 右边
                    if int(tempB3) + int(tempG3) + int(tempR3) != 765:
                        h3 = rgb2hsl(tempR3, tempG3, tempB3)
                        h_list.append(h3)

                    # tempB4, tempG4, tempR4 = img[row-1, col+1]  # 右上
                    # if int(tempB4) + int(tempG4) + int(tempR4) != 765:
                    #     h4 = rgb2hsl(tempR4, tempG4, tempB4)
                    #     h_list.append(h4)
                    # tempB5, tempG5, tempR5 = img[row + 1, col+1]  # 右下
                    # if int(tempB5) + int(tempG5) + int(tempR5) != 765:
                    #     h5 = rgb2hsl(tempR5, tempG5, tempB5)
                    #     h_list.append(h5)

                    color = []
                    for data in h_list:
                        for i in fourList:
                            if data[0] == i:
                                w_cnt = w_cnt + 1
                                color = data
                    if w_cnt > 0 :
                        color = hsl2rgb(color)
                        recoverB[row,col] = color[2]
                        recoverG[row,col] = color[1]
                        recoverR[row,col] = color[0]
                    else:
                        recoverB[row,col] = 255
                        recoverG[row,col] = 255
                        recoverR[row,col] = 255

            # elif rgb2hsl(R, G, B)[0] in fourList:
            #     recoverB[row, col] = B
            #     recoverG[row, col] = G
            #     recoverR[row, col] = R

            else:
                recoverB[row, col] = 255
                recoverG[row, col] = 255
                recoverR[row, col] = 255
    merged = cv2.merge([recoverB,recoverG,recoverR])
    return merged

# 两个图像做并集
def picANDpic(img1,img2):
    height = img1.shape[0]
    width = img1.shape[1]
    channels = img1.shape[2]
    value1 = [0] * 3
    value2 = [0] * 3
    recoverR = numpy.zeros([height, width], numpy.uint8)
    recoverG = numpy.zeros([height, width], numpy.uint8)
    recoverB = numpy.zeros([height, width], numpy.uint8)
    for row in range(height):
        for col in range(width):
            for chan in range(channels):
                value1[chan] = img1[row, col, chan]
                value2[chan] = img2[row,col,chan]
            R1 = value1[2]
            G1 = value1[1]
            B1 = value1[0]
            R2 = value2[2]
            G2 = value2[1]
            B2 = value2[0]
            if int(R1) + int(G1) + int(B1) != 765:
                recoverB[row, col] = B1
                recoverG[row, col] = G1
                recoverR[row, col] = R1
            else:
                recoverB[row, col] = B2
                recoverG[row, col] = G2
                recoverR[row, col] = R2
    merged = cv2.merge([recoverB,recoverG,recoverR])
    return merged

def originalImage(img,myList):
    height = img.shape[0]
    width = img.shape[1]
    channels = img.shape[2]
    value = [0] * 3
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
            h = rgb2hsl(R, G, B)[0]
            if h in myList:
                recoverB[row, col] = B
                recoverG[row, col] = G
                recoverR[row, col] = R
            else:
                recoverB[row, col] = 255
                recoverG[row, col] = 255
                recoverR[row, col] = 255
    merged = cv2.merge([recoverB, recoverG, recoverR])
    return merged

def dropNoise(cfsImage_new,tempImage):
    height = tempImage.shape[0]
    width = tempImage.shape[1]
    channels = tempImage.shape[2]
    value = [0] * 3
    recoverR = numpy.zeros([height, width], numpy.uint8)
    recoverG = numpy.zeros([height, width], numpy.uint8)
    recoverB = numpy.zeros([height, width], numpy.uint8)
    for row in range(height):
        for col in range(width):
            for chan in range(channels):
                value[chan] = tempImage[row, col, chan]
            R = value[2]
            G = value[1]
            B = value[0]
            if cfsImage_new[row,col] == 0:
                recoverR[row, col] = 255
                recoverG[row, col] = 255
                recoverB[row, col] = 255
            else:
                recoverR[row, col] = R
                recoverG[row, col] = G
                recoverB[row, col] = B
    merged = cv2.merge([recoverB, recoverG, recoverR])
    return merged



def preHandle(img):
    flag = has_interfering_line(img)
    oldImage = img
    if flag:
        for i in range(5):
            myList = handleImage(img)
            fourList = getMaxFour(myList)
            tempImage = cleanImage(img,fourList)
            # cv2.imwrite('../data/result2/test3.png', tempImage)
            cfsImage = im2bw(tempImage)
            mycfs = myCFS(cfsImage,15,30)
            cfsImage_new,cfs_number_of_character = mycfs.cfs()
            mergedImage = dropNoise(cfsImage_new,tempImage)
            # cv2.imwrite('../data/result2/test2.png', mergedImage)
            newImage = picANDpic(mergedImage,oldImage)
            img = newImage
            if i == 4:
                # cv2.imwrite('../data/result2/test1.png', mergedImage)
                fianl_cfsImage = im2bw(mergedImage)
                final_mycfs = myCFS(fianl_cfsImage, 15, 50)
                final_cfsImage_new, final_number_of_character = final_mycfs.cfs()
                final_mergedImage = dropNoise(final_cfsImage_new, mergedImage)
                # cv2.imwrite('../data/result3/test1.png', final_mergedImage)
                bwImg = im2bw(final_mergedImage)
                return bwImg
    else:
        print "This image has no interfering line"
        return im2bw(img)


if __name__ == '__main__':
    img = cv2.imread('../data/new/2.png')
    image = preHandle(img)
    cv2.imwrite("../data/result3/2.png",image)

