import time
import json
import requests
from flask import Flask, request, render_template
from flask_cors import CORS
from utils import Property


server = Flask(__name__)
# 解决跨域问题
# CORS(server, supports_credentials=True)


def get(url):
    headers = Property.createHeaders(url, "GET")
    return requests.get(url, headers=headers)


def post(url, data):
    headers = Property.createHeaders(url, "POST")
    return requests.post(url, data=data, headers=headers)


@server.route('/', methods=['get', 'post'])
def index():
    return render_template('index.html')
# 获取类别列表
@server.route('/categories', methods=['get', 'post'])
def getCategories():
    return get(Property.CATEGORIES_URL).json()


# 获取随机漫画
@server.route('/random', methods=['get', 'post'])
def getRandom():
    return get(Property.RANDOM_URL).json()


# 获取漫画描述信息
@server.route('/comicInfo/<comicId>', methods=['get', 'post'])
def getComicInfo(comicId):
    url = str(Property.COMIC_INFO_URL).replace("{comicId}", comicId)
    headers = Property.createHeaders(url, "GET")
    return requests.get(url, headers=headers).json()

# 获取漫画内容
@server.route('/comicContent/<comicId>/<espNum>/<pageNum>', methods=['get', 'post'])
def getComicContent(comicId, espNum, pageNum):
    url = str(Property.COMIC_CONTENT_URL).replace("{comicId}", comicId).replace(
        "{espNum}", espNum).replace("{pageNum}", pageNum)

    return get(url).json()


# 获取漫画图片并保存
def getComicPic(comicContent):
    # picUrl = str(comicContent['media']['fileServer'] +
    #              comicContent['media']['path']).replace('tobeimg', '')
    # headers = {'Host': 'img.picacomic.com',
    #            'accept-encoding': 'gzip', 'user-agent': 'okhttp/3.8.1'}
    picUrl = 'https://img.picacomic.com' + \
        comicContent['media']['path'].replace('tobeimg', '')
    originalName = comicContent['media']['originalName']
    with open('E:/img/'+originalName, 'wb') as img:
        img.write(get(picUrl).content)


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
        # 指定端口,host,0.0.0.0代表不管几个网卡，任何ip都可访问
    server.run(debug=True, port=8888, host='0.0.0.0')
