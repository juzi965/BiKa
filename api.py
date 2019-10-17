import time
import json
import requests
from utils import Property


def getCategories():
    tm = str(time.time())
    headers = Property.createHeaders(Property.CATEGORIES_URL, tm, "GET")
    response = requests.get(Property.CATEGORIES_URL, headers=headers)
    return response


def getRandom():
    tm = str(time.time())
    headers = Property.createHeaders(Property.RANDOM_URL, tm, "GET")
    response = requests.get(Property.RANDOM_URL, headers=headers)
    return response


def getComicInfo(comicId):
    tm = str(time.time())
    url = str(Property.COMIC_INFO_URL).replace("{comicId}", comicId)
    headers = Property.createHeaders(url, tm, "GET")
    response = requests.get(url, headers=headers)
    return response


def getComicContent(comicId, espNum, pageNum):
    tm = str(time.time())
    url = str(Property.COMIC_CONTENT_URL).replace("{comicId}", comicId).replace("{espNum}", espNum).replace("{pageNum}",
                                                                                                            pageNum)
    headers = Property.createHeaders(url, tm, "GET")
    response = requests.get(url, headers=headers)
    return response.json()


def getComicPic(comicContent):
    picUrl = str(comicContent['media']['fileServer'] + comicContent['media']['path']).replace('tobeimg', '')
    print(picUrl)
    headers = {
        'Host': 'img.picacomic.com',
        'accept-encoding': 'gzip',
        'user-agent': 'okhttp/3.8.1',
    }

    response = requests.post(picUrl, headers=headers)
    print(response.content)

def login():
    tm = str(time.time())
    headers = Property.createHeaders(Property.SING_URL, tm, "POST")
    response = requests.post(Property.SING_URL, data=Property.USER_INFO, headers=headers)
    return response


if __name__ == "__main__":
    # print(getRandom().text)
    # print(getComicInfo("59b36dfd61e69702aa4268a6").text)
    # print(getComicContent("59b36dfd61e69702aa4268a6", "1", "1")['data']['pages']['docs'][0])
     print(getComicPic(getComicContent("59b36dfd61e69702aa4268a6", "1", "1")['data']['pages']['docs'][0]))

