import time
import math
import json
import requests
from urllib.request import quote, unquote
from flask import Flask, request, render_template
from flask_cors import CORS
from utils import Property


server = Flask(__name__)
# 解决跨域问题
# CORS(server, supports_credentials=True)


# 封装的GET方法
def get(url):
    headers = Property.createHeaders(url, "GET")
    return requests.get(url, headers=headers)


# 封装的POST方法
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
        picUrl = fileServer + picPath
    else:
        picUrl = 'https://' + fileServer + '/static/' + picPath
    return requests.get(picUrl).content

# 默认页
@server.route('/', methods=['get', 'post'])
def index():
        # categoryList = get(Property.CATEGORIES_URL).json()
    categoryList = Property.readCategoryJson()
    randomList = get(Property.RANDOM_URL).json()
    return render_template('index.html', categoryList=categoryList, randomList=randomList)

# 获取随机漫画
@server.route('/random', methods=['get', 'post'])
def getRandom():
    data = get(Property.RANDOM_URL).json()
    return render_template('index.html', data=data)

# 获取漫画列表
@server.route('/comicList/<key>/<pageNum>/<orderType>', methods=['get', 'post'])
def getComicList(key, pageNum, orderType):
    key = quote(key)
    url = Property.COMIC_URL.replace("{KEY}", key).replace(
        "{pageNum}", pageNum).replace("{orderType}", orderType)
    comicList = get(url).json()
    return render_template('comicList.html', comicList=comicList, key=unquote(key), pageNum=pageNum, orderType=orderType)

# 获取漫画介绍信息
@server.route('/comicInfo/<comicId>', methods=['get', 'post'])
def getComicInfo(comicId):
    url = str(Property.COMIC_INFO_URL).replace("{comicId}", comicId)
    data = get(url).json()
    return render_template('comicInfo.html', data=data)

# 获取漫画内容
@server.route('/comicContent/<comicId>/<espNum>/<pageNum>', methods=['get', 'post'])
def getComicContent(comicId, espNum, pageNum):
    infoUrl = str(Property.COMIC_INFO_URL).replace("{comicId}", comicId)
    info = get(infoUrl).json()

    contentUrl = str(Property.COMIC_CONTENT_URL).replace("{comicId}", comicId).replace(
        "{espNum}", espNum).replace("{pageNum}", pageNum)
    data = get(contentUrl).json()

    return render_template('comicContent.html', data=data, comicId=comicId, espNum=espNum, pageNum=pageNum, info=info)


# 登录，获取token
@server.route('/login', methods=['get', 'post'])
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
    # 指定端口, host, 0.0.0.0代表不管几个网卡，任何ip都可访问
    server.run(debug=True, port=9999, host='0.0.0.0')
