# -*- coding:utf-8 -*-
# Date:2017-09-13

from PIL import Image,ImageOps
from cleanImage2 import main


def reSplit(start,end,image):
    middel = (end+start)/2 - start
    countList = []
    for x in range(start,end,1):
        count = 0
        for y in range(image.size[1]):
            pix = image.getpixel((x, y))
            if pix != 255:
                count += 1
        countList.append(count)
    newEnd = countList[middel-5:middel+5].index(min(countList[middel-5:middel+5])) + middel-5
    newStart = newEnd + 1
    return newStart,newEnd


def splitImage(image):
    # image = Image.open('../data/final_image9.png')
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
            foundletter = False
            end = x
            if end - start > 48:
                newStart, newEnd = reSplit(start,end,image)
                letters.append((start, newEnd+start))
                letters.append((newStart+start, end))
            else:
                letters.append((start, end))
        inletter = False

    count = 0
    for letter in letters:
        newImage = image.crop((letter[0], 0, letter[1], image.size[1]))

        for y in range(newImage.size[1]):
            for x in range(newImage.size[0]):
                pix = newImage.getpixel((x, y))
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
            im3 = newImage.crop((0,l[0],newImage.size[0],l[1]))
            # im3.save("../data/GG%d.png" %count)
            rotateImage(im3,count)
            count += 1
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
    for angle in range(10,40,1):
        newImage = inverted_image.rotate(angle, expand=True)
        myList = projection(newImage)
        index = myList.count(1)
        myDict[angle] = index
    maxIndex = sorted(myDict, key=lambda x: myDict[x])[0]
    finalImage = inverted_image.rotate(maxIndex, expand=True)
    finalImage = ImageOps.invert(finalImage)
    finalImage.save("../data/demo%d.png" %count)




def resizeImage():
    with Image.open("../data/0.png") as img:
        resized = img.resize((30, 50), resample=Image.NEAREST)
        resized.save("../data/0_0.png", format="png")

if __name__ == '__main__':
    import cv2
    img = cv2.imread('../data/10.png')
    image = main(img)
    cv2.imwrite("../data/demo.png",image)
    fianlImage = Image.fromarray(image)
    # fianlImage = Image.open("../data/bb.png")
    splitImage(fianlImage)
    # rotateImage()
    # rotateImage()


