import time
import json
import requests
from urllib.request import quote, unquote
from flask import Flask, request, render_template
from flask_cors import CORS
from utils import Property


server = Flask(__name__)
# 解决跨域问题
# CORS(server, supports_credentials=True)


def get(url):
    headers = Property.createHeaders(url, "GET")
    print(url)
    return requests.get(url, headers=headers)


def post(url, data):
    headers = Property.createHeaders(url, "POST")
    return requests.post(url, data=data, headers=headers)

# 获取图片（非原图）
@server.route('/getImg/<path:picPath>', methods=['get', 'post'])
def getImg(picPath):
    picUrl = 'https://img.picacomic.com' + picPath.replace('tobeimg', '')
    return requests.get(picUrl).content

# 获取图片（原图）
@server.route('/getOriginalImg/<path:fileServer>/<path:picPath>', methods=['get', 'post'])
def getOriginalImg(fileServer, picPath):
    if 'static' in fileServer:
        picUrl = 'https://' + fileServer + picPath
    else:
        picUrl = 'https://' + fileServer + '/static/' + picPath
    return requests.get(picUrl).content


# 获取类别列表
@server.route('/api/categories', methods=['get', 'post'])
def getCategories():
    # categoryList = Property.readCategoryJson()
    return get(Property.CATEGORIES_URL).json()

# 获取漫画列表
@server.route('/api/comicList/<key>/<pageNum>/<orderType>', methods=['get', 'post'])
def getComicList(key, pageNum, orderType):
    key = quote(key)
    url = Property.COMIC_URL.replace("{KEY}", key).replace(
        "{pageNum}", pageNum).replace("{orderType}", orderType)
    return get(url).json()

# 获取漫画介绍信息
@server.route('/api/comicInfo/<comicId>', methods=['get', 'post'])
def getComicInfo(comicId):
    url = str(Property.COMIC_INFO_URL).replace("{comicId}", comicId)
    return get(url).json()

# 获取随机漫画
@server.route('/random', methods=['get', 'post'])
def getRandom():
    return get(Property.RANDOM_URL).json()

# 获取漫画内容
@server.route('/api/comicContent/<comicId>/<espNum>/<pageNum>', methods=['get', 'post'])
def getComicContent(comicId, espNum, pageNum):
    url = str(Property.COMIC_CONTENT_URL).replace("{comicId}", comicId).replace(
        "{espNum}", espNum).replace("{pageNum}", pageNum)
    return get(url).json()


@server.route('/api/login', methods=['get', 'post'])
def login():
    return post(Property.SING_URL, Property.USER_INFO).json()


if __name__ == "__main__":
        # print(login().text)
        # print(getRandom().text)
        # print(getComicInfo("59b36dfd61e69702aa4268a6").text)
        # print(getComicContent("59b36dfd61e69702aa4268a6", "1", "1")['data']['pages']['docs'][0])
        # getComicPic(getComicContent("59b36dfd61e69702aa4268a6", "1", "1")['data']['pages']['docs'][0])

        # response = getComicContent("59b36dfd61e69702aa4268a6", "1", "1")[
        #     'data']['pages']['docs']
        # for ob in response:
        #     getComicPic(ob)
        # 指定端口,host,0.0.0.0代表不管几个网卡，任何ip都可访问
    server.run(debug=True, port=9999, host='0.0.0.0')
