# -*- coding:utf-8 -*-
# Date:2017-9-19
# 最大连通域算法

import Queue
import numpy as np


class myCFS():
    def __init__(self,img,number,pixelNumber):
        self.pixelNumber = pixelNumber
        self.number = number
        self.img = img
        self.height = self.img.shape[0]
        self.width = self.img.shape[1]
        self.newImage = np.zeros([self.height, self.width], np.uint8)
        self.flag = np.zeros([self.height, self.width], np.uint8)
        self.myQueue = Queue.Queue()


    def cfs(self):
        myClass = 1
        number_of_character = 0
        for i in range(self.number):
            pixelNumber = 0
            myFlag = False
            for col in range(self.width):
                for row in range(self.height):
                    pixel = self.img[row, col]
                    newPixel = self.newImage[row,col]
                    is_visited = self.flag[row,col]
                    if pixel == 0 and newPixel == 0 and is_visited == 0:
                        tempQueue = Queue.Queue()
                        tempQueue.put([row,col])
                        self.myQueue.put([row,col])
                        tempFlag = self.flag.copy()
                        tempImage = self.newImage.copy()
                        pixelNumber = self.preHandle(tempQueue,tempFlag,tempImage,self.img,myClass)
                        if pixelNumber > self.pixelNumber:
                            self.handle2(self.myQueue,self.flag,self.newImage,self.img,myClass)
                            number_of_character += 1
                        else:
                            self.myQueue.get()
                            self.flag = tempFlag.copy()
                        myFlag = True
                        break
                if myFlag == True:
                    break
            if pixelNumber > self.pixelNumber:
                myClass += 1
            if number_of_character == 4:
                break
        return self.newImage,number_of_character

    # 检测连通域点数是否超过self.pixelNumber个，不超过则舍弃
    def preHandle(self,tempQueue,tempFlag,tempImage,img,myClass):
        cnt = 1
        while tempQueue.qsize() > 0:
            self.is_more_than_20pixel(tempQueue,tempFlag,tempImage,img,myClass)
            cnt += 1
        return cnt

    def handle2(self,myQueue,flag,newImage,img,myClass):
        while myQueue.qsize() > 0:
            self.handle(myQueue,flag,newImage,img,myClass)


    def is_more_than_20pixel(self,tempQueue,tempFlag,tempImage,img,myClass):
        temp = tempQueue.get()
        row = temp[0]
        col = temp[1]
        tempFlag[row, col] = 1

        tempImage[row, col] = myClass

        pixel1 = img[row - 1, col]
        if pixel1 == 0 and tempFlag[row - 1, col] == 0:
            tempQueue.put([row - 1, col])
            tempFlag[row - 1, col] = 1
        pixel2 = img[row + 1, col]
        if pixel2 == 0 and tempFlag[row + 1, col] == 0:
            tempQueue.put([row + 1, col])
            tempFlag[row + 1, col] = 1
        pixel3 = img[row, col - 1]
        if pixel3 == 0 and tempFlag[row, col - 1] == 0:
            tempQueue.put([row, col - 1])
            tempFlag[row, col - 1] = 1
        pixel4 = img[row, col + 1]
        if pixel4 == 0 and tempFlag[row, col + 1] == 0:
            tempQueue.put([row, col + 1])
            tempFlag[row, col + 1] = 1
        pixel5 = img[row - 1, col - 1]
        if pixel5 == 0 and tempFlag[row - 1, col - 1] == 0:
            tempQueue.put([row - 1, col - 1])
            tempFlag[row - 1, col - 1] = 1
        pixel6 = img[row - 1, col + 1]
        if pixel6 == 0 and tempFlag[row - 1, col + 1] == 0:
            tempQueue.put([row - 1, col + 1])
            tempFlag[row - 1, col + 1] = 1
        pixel7 = img[row + 1, col - 1]
        if pixel7 == 0 and tempFlag[row + 1, col - 1] == 0:
            tempQueue.put([row + 1, col - 1])
            tempFlag[row + 1, col - 1] = 1
        pixel8 = img[row + 1, col + 1]
        if pixel8 == 0 and tempFlag[row + 1, col + 1] == 0:
            tempQueue.put([row + 1, col + 1])
            tempFlag[row + 1, col + 1] = 1

    def handle(self,myQueue,flag,newImage,img,myClass):
        temp = myQueue.get()
        row = temp[0]
        col = temp[1]
        flag[row, col] = 1

        newImage[row, col] = myClass

        pixel1 = img[row - 1, col]
        if pixel1 == 0 and flag[row - 1, col] == 0:
            myQueue.put([row - 1, col])
            flag[row - 1, col] = 1
        pixel2 = img[row + 1, col]
        if pixel2 == 0 and flag[row + 1, col] == 0:
            myQueue.put([row + 1, col])
            flag[row + 1, col] = 1
        pixel3 = img[row, col - 1]
        if pixel3 == 0 and flag[row, col - 1] == 0:
            myQueue.put([row, col - 1])
            flag[row, col - 1] = 1
        pixel4 = img[row, col + 1]
        if pixel4 == 0 and flag[row, col + 1] == 0:
            myQueue.put([row, col + 1])
            flag[row, col + 1] = 1
        pixel5 = img[row - 1, col - 1]
        if pixel5 == 0 and flag[row - 1, col - 1] == 0:
            myQueue.put([row - 1, col - 1])
            flag[row - 1, col - 1] = 1
        pixel6 = img[row - 1, col + 1]
        if pixel6 == 0 and flag[row - 1, col + 1] == 0:
            myQueue.put([row - 1, col + 1])
            flag[row - 1, col + 1] = 1
        pixel7 = img[row + 1, col - 1]
        if pixel7 == 0 and flag[row + 1, col - 1] == 0:
            myQueue.put([row + 1, col - 1])
            flag[row + 1, col - 1] = 1
        pixel8 = img[row + 1, col + 1]
        if pixel8 == 0 and flag[row + 1, col + 1] == 0:
            myQueue.put([row + 1, col + 1])
            flag[row + 1, col + 1] = 1