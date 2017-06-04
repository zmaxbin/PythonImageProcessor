# -*- coding:utf-8 -*-
# Date:2017/9/27

import os
import cv2
import numpy as np
import pandas as pd
from PIL import Image
from CFS import myCFS
from sklearn.svm import SVC
from splitImage import preHandle,cutImage


def removeFileInFirstDir(targetDir):
    for file in os.listdir(targetDir):
        targetFile = os.path.join(targetDir,  file)
        if os.path.isfile(targetFile):
            os.remove(targetFile)


def myModel():
    path = "../data/result/"
    f = os.listdir(path)

    fileList = []
    for i in f:
        fileList.append(i)

    tempList = []
    for j in fileList:
        img = Image.open(path+j)
        im_array = np.array(img)
        im_array[im_array == 0] = 1
        im_array[im_array == 255] = 0
        imgList = im_array.flatten().tolist()
        y = j[0]
        temp_imgList = list(imgList)
        temp_imgList.append(y)
        tempList.append(temp_imgList)

    df = pd.DataFrame(tempList)
    X_train = df[list(range(375))].values
    y_trian = df[375].values
    # model = LinearSVC().fit(X_train,y_trian)
    model = SVC(kernel='linear').fit(X_train,y_trian)
    # from sklearn.externals import joblib
    # joblib.dump(model, "train_model.m")


    path = "../data/test/"
    fileList = os.listdir(path)
    cnt1 = 0
    cnt2 = 0
    for f in fileList:
        try:
            realCaptcha = f.split('.')[0]
            img = cv2.imread(path+f)
            # img = cv2.imread("../data/test/test.png")
            img = preHandle(img)
            height = img.shape[0]
            width = img.shape[1]

            mycfs = myCFS(img, 30, 55)
            newImage, number_of_character = mycfs.cfs()
            cutImage(height,width,newImage,img)

            captcha = ''
            for i in range(1,5,1):
                testImage = Image.open("../data/testFile/%d.png" %i)
                testImage_array = np.array(testImage)
                testImage_array[testImage_array == 0] = 1
                testImage_array[testImage_array == 255] = 0
                test_imgList = testImage_array.flatten().reshape(1,-1)

                y_pred = model.predict(test_imgList)
                captcha = captcha + y_pred

            print captcha
            if captcha == realCaptcha:
                cnt1 += 1
        except :
            print "出错！！！"

        cnt2 += 1

        removeFileInFirstDir("../data/testFile/")
    print cnt1
    print float(cnt1)/cnt2
    print "************************"

if __name__ == '__main__':
    myModel()











