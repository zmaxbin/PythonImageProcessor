# -*- coding:utf-8 -*-

import cv2
import numpy

def cleanImage():
    img = cv2.imread('../data/8.png')
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
                if row-1>0 and row+1<height and col-1>0 and col+1<width:
                    sum_list = []
                    w_cnt = 0
                    c_cnt = 0
                    s_point = int(R) + int(G) + int(B)
                    tempB1, tempG1, tempR1 = img[row - 1, col] #上面
                    sum1 = int(tempB1) + int(tempG1) + int(tempR1)
                    tempB2, tempG2, tempR2 = img[row + 1, col] #下面
                    sum2 = int(tempB2) + int(tempG2) + int(tempR2)
                    tempB3, tempG3, tempR3 = img[row, col - 1] #左边
                    sum3 = int(tempB3) + int(tempG3) + int(tempR3)
                    tempB4, tempG4, tempR4 = img[row, col + 1] #右边
                    sum4 = int(tempB4) + int(tempG4) + int(tempR4)
                    sum_list.append(sum1)
                    sum_list.append(sum2)
                    sum_list.append(sum3)
                    sum_list.append(sum4)
                    for data in sum_list:
                        if data == 765:
                            w_cnt = w_cnt + 1
                        if data == s_point:
                            c_cnt = c_cnt + 1
                    if w_cnt > 0 and c_cnt >1:
                        gray_img[row, col] = 255
                    else:
                        gray_img[row, col] = 0.2989 * R + 0.5870 * G + 0.1140 * B

                elif col + 1 >width:
                    sum_list = []
                    w_cnt = 0
                    c_cnt = 0
                    s_point = int(R) + int(G) + int(B)
                    tempB1, tempG1, tempR1 = img[row - 1, col]  # 上面
                    sum1 = int(tempB1) + int(tempG1) + int(tempR1)
                    tempB2, tempG2, tempR2 = img[row + 1, col]  # 下面
                    sum2 = int(tempB2) + int(tempG2) + int(tempR2)
                    tempB3, tempG3, tempR3 = img[row, col - 1]  # 左边
                    sum3 = int(tempB3) + int(tempG3) + int(tempR3)
                    sum_list.append(sum1)
                    sum_list.append(sum2)
                    sum_list.append(sum3)
                    for data in sum_list:
                        if data == 765:
                            w_cnt = w_cnt + 1
                        if data == s_point:
                            c_cnt = c_cnt + 1
                    if w_cnt > 0 and c_cnt > 1:
                        gray_img[row, col] = 255
                    else:
                        gray_img[row, col] = 0.2989 * R + 0.5870 * G + 0.1140 * B

                elif col - 1 < 0:
                    sum_list = []
                    w_cnt = 0
                    c_cnt = 0
                    s_point = int(R) + int(G) + int(B)
                    tempB1, tempG1, tempR1 = img[row - 1, col]  # 上面
                    sum1 = int(tempB1) + int(tempG1) + int(tempR1)
                    tempB2, tempG2, tempR2 = img[row + 1, col]  # 下面
                    sum2 = int(tempB2) + int(tempG2) + int(tempR2)
                    tempB3, tempG3, tempR3 = img[row, col + 1]  # 右边
                    sum3 = int(tempB3) + int(tempG3) + int(tempR3)
                    sum_list.append(sum1)
                    sum_list.append(sum2)
                    sum_list.append(sum3)
                    for data in sum_list:
                        if data == 765:
                            w_cnt = w_cnt + 1
                        if data == s_point:
                            c_cnt = c_cnt + 1
                    if w_cnt > 0 and c_cnt > 1:
                        gray_img[row, col] = 255
                    else:
                        gray_img[row, col] = 0.2989 * R + 0.5870 * G + 0.1140 * B

            else:
                gray_img[row, col] = 765

    cv2.imwrite('../data/result_8.png', gray_img)
    return gray_img

def im2bw():
    img = cv2.imread('../data/result_8.png',0)
    hist = cv2.calcHist([img], [0], None, [256], [0, 256])
    s = []
    for i in range(len(hist)):
        s.append(hist[i][0])
    s.remove(max(s))
    flag = s.index(max(s))
    ret, thresh1 = cv2.threshold(img, flag+30, 255, cv2.THRESH_BINARY)
    cv2.imwrite('../data/final_image8.png', thresh1)



if __name__ == '__main__':
    gray_img = cleanImage()
    im2bw()