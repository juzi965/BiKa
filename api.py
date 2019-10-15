import time
import requests
from utils import PropertyUtil

prop = PropertyUtil()


def getCategories():
    tm = str(time.time())
    headers = prop.createHeaders(prop.CATEGORIES_URL, tm, "GET")
    response = requests.get(prop.CATEGORIES_URL, headers=headers)
    return response


def login():
    body = {'email': prop.USER_NAME, 'password': prop.PASSWORD}
    response = requests.post(prop.SING_URL, data=body)
    return response


if __name__ == "__main__":
    print(getCategories().json())
