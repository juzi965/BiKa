import uuid
import hmac
import json
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
        # 用户登录信息
        self.USER_INFO = json.dumps({"email": self.USER_NAME, "password": self.PASSWORD})
        # 域名
        self.DOMAIN = config['param']['domain']
        # 应用KEY
        self.API_KEY = config['param']['apiKey']
        # 密钥
        self.SECRET_KEY = config['param']['secretKey']
        # TOKEN
        self.AUTHORIZATION = config['param']['authorization']
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
            'authorization': self.AUTHORIZATION,
            'app-build-version': self.APP_BUILD_VERSION,
            'time': tm,
            'signature': signature,
            'Host': 'picaapi.picacomic.com',
            'accept': 'application/vnd.picacomic.com.v1+json',
            'app-uuid': 'defaultUuid',
            'image-quality': 'low',
            'app-platform': 'android',
            "content-type": "application/json; charset=UTF-8",
            'accept-encoding': 'gzip',
        }
        return headers


Property = PropertyUtil()
