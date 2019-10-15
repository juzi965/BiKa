import time
import requests
from utils import Property


def getCategories():
    tm = str(time.time())
    headers = Property.createHeaders(Property.CATEGORIES_URL, tm, "GET")
    response = requests.get(Property.CATEGORIES_URL, headers=headers)
    return response


def login():
    tm = str(time.time())
    headers = Property.createHeaders(Property.SING_URL, tm, "POST")
    response = requests.post(Property.SING_URL, data=Property.USER_INFO, headers=headers)
    return response


if __name__ == "__main__":
    print(login().text)





