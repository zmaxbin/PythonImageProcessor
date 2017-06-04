# -*- coding:utf-8 -*-
# Date:2017-9-19

import cv2
import numpy as np
import Queue
from PIL import Image, ImageOps
from cleanImage2 import preHandle
from CFS import myCFS
import hashlib
import time


def cutImage(height,width,newImage,img):
    cut_boundary = []
    flag = 0

    startFlage = False
    startFlage2 = False
    start_of_width = 0

    for i in range(4):
        for col in range(width):
            for row in range(height):
                pixel = newImage[row, col]
                if pixel == 1 and flag == 0:
                    startFlage = True
                elif pixel == 2 and flag == 1:
                    startFlage = True
                elif pixel == 3 and flag == 2:
                    startFlage = True
                elif pixel == 4 and flag == 3:
                    startFlage = True
            if startFlage == True and startFlage2 == False:
                startFlage2 = True
                start_of_width = col
            if startFlage2 == True and startFlage == False:
                end_of_width = col
                cut_boundary.append((start_of_width,end_of_width))
                flag += 1
                startFlage = False
                startFlage2 = False
                break
            startFlage = False

    count = 1
    for boundary in cut_boundary:
        myWidth = boundary[1] - boundary[0]
        finalImage = np.zeros([height, myWidth], np.uint8)
        for col in range(boundary[0],boundary[1],1):
            for row in range(height):
                pixel1 = img[row,col]
                pixel2 = newImage[row,col]
                if pixel1 == 0 and pixel2 == count:
                    finalImage[row,col-boundary[0]] = pixel1
                else:
                    finalImage[row,col-boundary[0]] = 255
        finalImage = Image.fromarray(finalImage)
        rotateImage(finalImage,count)
        # cv2.imwrite("../data/nice%d.png" %count,finalImage)
        count += 1


def cutEdge(image,count):
    inletter = False
    foundletter = False
    start = 0
    letters = []

    inletter1 = False
    foundletter1 = False
    start1 = 0
    letters1 = []

    for x in range(image.size[0]):
        for y in range(image.size[1]):
            pix = image.getpixel((x, y))
            if pix != 255:
                inletter = True
        if foundletter == False and inletter == True:
            foundletter = True
            start = x

        if foundletter == True and inletter == False:
            end = x
            letters.append((start, end))
            break
        inletter = False

    if len(letters) == 0:
        letters.append((0,image.size[0]))
    for letter in letters:
        newImg = image.crop((letter[0], 0, letter[1], image.size[1]))

        for y in range(newImg.size[1]):
            for x in range(newImg.size[0]):
                pix = newImg.getpixel((x, y))
                if pix != 255:
                    inletter1 = True
            if foundletter1 == False and inletter1 == True:
                foundletter1 = True
                start1 = y

            if foundletter1 == True and inletter1 == False:
                foundletter1 = False
                end1 = y
                letters1.append((start1, end1))
            inletter1 = False

        for l in letters1:
            im3 = newImg.crop((0,l[0],newImg.size[0],l[1]))
            resizeImage(im3,count)
            # im3.save("../data/nice%d.png" %count)
        letters1 = []



# 水平投影
def projection(image):
    myList = []
    flag = 0
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            pix = image.getpixel((x,y))
            if pix == 255:
                flag = 1
                break
            else:
                flag = 0
        myList.append(flag)
    return myList

# 旋转摆正图像
def rotateImage(pil_im,count):
    # pil_im = Image.open('../data/GG3.png')
    # print pil_im.size[0] 宽
    inverted_image = ImageOps.invert(pil_im)
    myDict = {}
    for angle in range(-20,20,1):
        newImage = inverted_image.rotate(angle, expand=True)
        myList = projection(newImage)
        index = myList.count(1)
        myDict[angle] = index
    maxIndex = sorted(myDict, key=lambda x: myDict[x])[0]
    finalImage = inverted_image.rotate(maxIndex, expand=True)
    finalImage = ImageOps.invert(finalImage)
    # finalImage.save("../data/temp.png")
    cutEdge(finalImage,count)
    # finalImage.save("../data/nice%d.png" %count)

def resizeImage(img,count):
    resized = img.resize((15, 25), resample=Image.NEAREST)
    resized.save("../data/testFile/%d.png" %count,format="png")
    # m = hashlib.md5(str(time.clock()).encode('utf-8'))
    # fileName = m.hexdigest()
    # resized.save("../data/cut/%s.png" % str(fileName), format="png")




if __name__ == '__main__':
    # img = cv2.imread("../data/new/24.png")
    # img = preHandle(img)
    # # cv2.imwrite("../data/result/aa.png",img)
    # height = img.shape[0]
    # width = img.shape[1]
    #
    # mycfs = myCFS(img, 10, 55)
    # newImage, number_of_character = mycfs.cfs()
    # # np.savetxt("../data/hahah.txt",newImage)
    # cutImage(height,width,newImage,img)
    for i in range(50):
        try:
            img = cv2.imread("../data/new1/%d.png" %i)
            img = preHandle(img)
            height = img.shape[0]
            width = img.shape[1]

            mycfs = myCFS(img,30,55)
            newImage,number_of_character = mycfs.cfs()
            # np.savetxt("../data/hahah.txt",newImage)
            cutImage(height,width,newImage,img)
        except Exception:
            print "出错的%d" %i