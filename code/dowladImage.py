# -*- coding:utf-8 -*-

import requests
import time
import random

def downloadImage(i):
    url = "http://shixin.court.gov.cn/captchaNew.do?captchaId=21cf3616122e4ee4b2c0aa8ed3f45136&random=0.881534265713533"
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'}
    result = requests.get(url, headers=headers)
    with open("../data/new1/%d.png" %i,'wb')as f:
        f.write(result.content)
    time.sleep(random.uniform(0.5, 1.5))


# for i in range(50):
#     downloadImage(i)

import os

path = "../data/cut/"
f = os.listdir(path)

myList = []
for i in f:
   myList.append(i[0])

from collections import Counter
myDict = dict(Counter(myList))
print myDict

# n = 0
# for i in f:
#     # 设置旧文件名（就是路径+文件名）
#     oldname = path + f[n]
#
#     # 设置新文件名
#     newname = path + str(n + 200) + '.png'
#
#     # 用os模块中的rename方法对文件改名
#     os.rename(oldname, newname)
#
#     n += 1