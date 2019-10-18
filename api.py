import time
import json
import requests
from utils import Property


proxies = {"http": "http://104.20.180.50:1087", "https": "http://104.20.181.50:1087"}

def getCategories():  # 获取类别列表
    tm = str(time.time())
    headers = Property.createHeaders(Property.CATEGORIES_URL, tm, "GET")
    return requests.get(Property.CATEGORIES_URL, headers=headers).json()


def getRandom():  # 获取随机漫画
    tm = str(time.time())
    headers = Property.createHeaders(Property.RANDOM_URL, tm, "GET")
    return requests.get(Property.RANDOM_URL, headers=headers).json()


def getComicInfo(comicId):  # 获取漫画描述信息
    tm = str(time.time())
    url = str(Property.COMIC_INFO_URL).replace("{comicId}", comicId)
    headers = Property.createHeaders(url, tm, "GET")
    return requests.get(url, headers=headers).json()


def getComicContent(comicId, espNum, pageNum):  # 获取漫画内容
    tm = str(time.time())
    url = str(Property.COMIC_CONTENT_URL).replace("{comicId}", comicId).replace("{espNum}", espNum).replace("{pageNum}",
                                                                                                            pageNum)
    headers = Property.createHeaders(url, tm, "GET")
    return requests.get(url, headers=headers).json()


def getComicPic(comicContent):  # 获取漫画图片并保存
    picUrl = str(comicContent['media']['fileServer'] + comicContent['media']['path']).replace('tobeimg', '')
    headers = {'Host': 'img.picacomic.com', 'accept-encoding': 'gzip', 'user-agent': 'okhttp/3.8.1'}
    response = requests.get(picUrl, headers=header, proxies=proxies, verify=False)
    with open('E:/img/'+comicContent['media']['originalName'], 'wb') as img:
        img.write(response.content)


def login():
    tm = str(time.time())
    headers = Property.createHeaders(Property.SING_URL, tm, "POST")
    response = requests.post(Property.SING_URL, data=Property.USER_INFO, headers=headers)
    return response


if __name__ == "__main__":
    # print(getRandom().text)
    # print(getComicInfo("59b36dfd61e69702aa4268a6").text)
    # print(getComicContent("59b36dfd61e69702aa4268a6", "1", "1")['data']['pages']['docs'][0])
    # getComicPic(getComicContent("59b36dfd61e69702aa4268a6", "1", "1")['data']['pages']['docs'][0])

    response = getComicContent("59b36dfd61e69702aa4268a6", "1", "1")['data']['pages']['docs']
    for ob in response:
        getComicPic(ob)
