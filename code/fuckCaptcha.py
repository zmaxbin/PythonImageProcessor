# -*- coding:utf-8 -*-
# Date:2017/9/27

# from sklearn.externals import joblib
# model = joblib.load("train_model.m")

import requests
import cv2
from splitImage import preHandle,cutImage
from CFS import myCFS
from PIL import Image
import numpy as np
import os
from lxml import etree
import re
import MySQLdb
import pandas as pd
import json
from pyMysql import MysqlPipline,CreateDatabase
import uuid
import time
import random
from myRetry import retry
from myLogger import logger

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# 删除文件
def removeFileInFirstDir(targetDir):
    for file in os.listdir(targetDir):
        targetFile = os.path.join(targetDir,  file)
        if os.path.isfile(targetFile):
            os.remove(targetFile)

url = "http://shixin.court.gov.cn/findDisNew"

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': '__utma=221842138.778438802.1506319571.1506319571.1506319571.1; __utmz=221842138.1506319571.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _gscs_2025930969=t06498236pr5y4p12|pv:3; _gscbrs_2025930969=1; JSESSIONID=D0E3A06F90BB464F2191A23284F74DD3; _gscu_2025930969=039873972iigyc60',
    'Host': 'shixin.court.gov.cn',
    'Origin': 'http://www.cqupb.gov.cn',
    'Referer': 'http://www.cqupb.gov.cn/wsfw/wsfw_1S3Z_listDetails.aspx?classname=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
}

conn = MysqlPipline()

def getCaptcha():
    url = "http://shixin.court.gov.cn/captchaNew.do?captchaId=21cf3616122e4ee4b2c0aa8ed3f45136&random=0.881534265713533"
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'}
    result = requests.get(url, headers=headers)
    with open("../data/testFile/test.png", 'wb')as f:
        f.write(result.content)


    captcha = raw_input("输入验证码:")
    return captcha

    # try:
    #     img = cv2.imread("../data/test/test.png")
    #     img = preHandle(img)
    #     height = img.shape[0]
    #     width = img.shape[1]
    #
    #     mycfs = myCFS(img, 30, 55)
    #     newImage, number_of_character = mycfs.cfs()
    #     cutImage(height,width,newImage,img)
    #
    #     captcha = ''
    #     for i in range(1,5,1):
    #         testImage = Image.open("../data/testFile/%d.png" %i)
    #         testImage_array = np.array(testImage)
    #         testImage_array[testImage_array == 0] = 1
    #         testImage_array[testImage_array == 255] = 0
    #         test_imgList = testImage_array.flatten().reshape(1,-1)
    #
    #         y_pred = model.predict(test_imgList)
    #         captcha = captcha + y_pred
    #
    #         return captcha
    # except :
    #     print "出错！！！"
    #
    # removeFileInFirstDir("../data/testFile/")

def readSQL():
    database_host = 'localhost'
    database_username = 'root'
    database_password = '123.'
    database_dbname = 'antifraud'
    database_charset = 'utf8'

    conn = MySQLdb.connect(database_host, database_username, database_password, database_dbname, charset=database_charset)
    sqlcmd = 'select name from top_managers'
    name_list = pd.read_sql(sqlcmd, conn).values.tolist()
    sqlcmd = 'select sex from top_managers'
    sex_list = pd.read_sql(sqlcmd, conn).values.tolist()
    sqlcmd = 'select age from top_managers'
    age_list = pd.read_sql(sqlcmd, conn).values.tolist()
    return name_list,sex_list,age_list


captcha = getCaptcha()

def getContent():
    # name_list, sex_list, age_list = readSQL()
    # for i in range(len(name_list)):
    #     name = str(name_list[i][0])
    #     sex = str(sex_list[i][0])
    #     age = age_list[i][0]
    #     getDetail(name,sex,age)
    name = '陈志文'
    sex = '男'
    age = 30
    getDetail(name,sex,age)

@retry(logger,3,3)
def getDetail(name,sex,age):
    data = {'currentPage':1,'pName':name,'pProvince':'0','pCode':captcha,'captchaId':'21cf3616122e4ee4b2c0aa8ed3f45136'}
    content = requests.post(url,data,headers=headers).content
    dom_tree = etree.HTML(content)
    temp = dom_tree.xpath("//div[@align='right']/text()")
    pageNum = re.findall(r'/(.*?) ',temp[-1].strip())[0]
    for i in range(1,int(pageNum)+1,1):
        data = {'currentPage': i, 'pName': name, 'pProvince': '0', 'pCode': captcha,
                'captchaId': '21cf3616122e4ee4b2c0aa8ed3f45136'}
        content = requests.post(url, data, headers=headers).content
        dom_tree = etree.HTML(content)
        idList = dom_tree.xpath("//a[@class='View']/@id")
        for id in idList:
            getMessage(id,name,sex,age)

@retry(logger,3,3)
def getMessage(id,name,sex,age):
    values = []
    cursor = conn.cursor()
    SQLid = str(uuid.uuid1())
    url = "http://shixin.court.gov.cn/disDetailNew?id={0}&pCode={1}&captchaId=21cf3616122e4ee4b2c0aa8ed3f45136".format(id,captcha)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
    myJson = requests.get(url=url,headers=headers).content
    final_json = json.loads(myJson)
    iname = final_json['iname']
    print iname
    iage = final_json['age']
    print iage
    sexy = final_json['sexy']
    print sexy
    cardNum = final_json['cardNum']
    courtName = final_json['courtName']
    areaName = final_json['areaName']
    gistId = final_json['gistId']
    regDate = final_json['regDate']
    caseCode= final_json['caseCode']
    gistUnit = final_json['gistUnit']
    duty = final_json['duty']
    performance = final_json['performance']
    disruptTypeName = final_json['disruptTypeName']
    publishDate = final_json['publishDate']
    update_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    if str(iname) == name and str(iage) == str(age) and int(sexy) == int(sex):
        values.append((SQLid,str(iname),str(sexy),str(iage),str(cardNum),str(iname),str(courtName),str(areaName),str(gistId),str(regDate),
                       str(caseCode),str(gistUnit),str(duty),str(performance),str(disruptTypeName),str(publishDate),update_time))
        cursor.executemany('INSERT INTO loss_trust_execution values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', values)
        conn.commit()
        print ""
    else:
        time.sleep(random.uniform(1, 3))

# CreateDatabase()
getContent()