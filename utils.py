import uuid
import hmac
import hashlib
import configparser


class PropertyUtil:

    def __init__(self):
        # 读取配置文件
        config = configparser.ConfigParser()
        config.read('conf/resources.conf')
        # 用户名
        self.USER_NAME = config['userInfo']['userName']
        # 密码
        self.PASSWORD = config['userInfo']['password']
        # 域名
        self.DOMAIN = config['param']['domain']
        # 应用KEY
        self.API_KEY = config['param']['apiKey']
        # 密钥
        self.SECRET_KEY = config['param']['secretKey']
        # APP版本
        self.APP_VERSION = config['param']['appVersion']
        # UA
        self.USER_AGENT = config['param']['userAgent']
        # APP构建版本
        self.APP_BUILD_VERSION = config['param']['appBuildVersion']
        # 分流类型
        self.APP_CHANNEL = config['param']['appChannel']
        # UUID
        self.UUID = str(uuid.uuid4()).replace("-", "")
        # 登陆地址
        self.SING_URL = self.DOMAIN + "auth/sign-in"
        # 类别地址
        self.CATEGORIES_URL = self.DOMAIN + "categories"

    def createSignature(self, url, tm, method):
        raw = url.replace("https://picaapi.picacomic.com/", "") + tm + self.UUID + method + self.API_KEY
        raw = raw.lower()
        toSignature = hmac.new(self.SECRET_KEY.encode(), digestmod=hashlib.sha256)
        toSignature.update(raw.encode())
        return toSignature.hexdigest()

    def createHeaders(self, url, tm, method):
        signature = self.createSignature(url, tm, method)
        headers = {
            'nonce': self.UUID,
            'api-key': self.API_KEY,
            'user-agent': self.USER_AGENT,
            'app-version': self.APP_VERSION,
            'app-channel': self.APP_CHANNEL,
            'app-build-version': self.APP_BUILD_VERSION,
            'time': tm,
            'signature': signature,
            'authorization': "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI1Y2RlY2M5Y2RlMGFjMTRiYmRkZDA1NDciLCJlbWFpbCI6Imp1emk5NjUiLCJyb2xlIjoibWVtYmVyIiwibmFtZSI6IuahlOWtkFlZIiwidmVyc2lvbiI6IjIuMi4xLjAuMS4yIiwiYnVpbGRWZXJzaW9uIjoiNDMiLCJwbGF0Zm9ybSI6ImFuZHJvaWQiLCJpYXQiOjE1NzEwNjI5NjUsImV4cCI6MTU3MTY2Nzc2NX0.F4nQNYdzVyMLfRrN-nI5VGxYEbAr7sJs4K4TRSD--GA",
            'Host': 'picaapi.picacomic.com',
            'accept': 'application/vnd.picacomic.com.v1+json',
            'app-uuid': 'defaultUuid',
            'image-quality': 'low',
            'app-platform': 'android',
            'accept-encoding': 'gzip',
        }
        return headers
