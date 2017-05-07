# -*- coding:utf-8 -*-

import requests

def downloadImage(i):
    url = "http://login.sina.com.cn/cgi/pin.php?r=82428313&s=0&p=gz-c3bc8e8febf7d908aa471d44fc377d676218"
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'}
    result = requests.get(url, headers=headers)
    with open("D:/testImage/%d.png" %i,'wb')as f:
        f.write(result.content)


for i in range(20):
    downloadImage(i)
