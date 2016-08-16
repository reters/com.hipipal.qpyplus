import re
import time
import requests

YIMA_URL = "http://api.51ym.me/UserInterface.aspx"

class Yima(object):
    def __init__(self, account, pwd, item_id):
        self.token = None
        self.user = account
        self.pwd = pwd
        self.item_id = str(item_id)
        self.session = requests.session()
        # self.login()

    def login(self):
        print("login yima")
        params = {"action": "login", "username": self.user, "password": self.pwd}
        res = self.session.get(YIMA_URL, params=params, timeout=10)
        if res.content.startswith('False'.encode()):
            self.raise_api_exception(res)
        # print(res.text)
        self.token = res.text.split('|')[1]
        print("login succeed!")
        # print(self.token)

    def getPhone(self, phone=None):
        print("获取号码")
        params = {"action": "getmobile", "itemid": self.item_id, "token": self.token}
        if phone:
            params["mobile"] = phone
        res = self.session.get(YIMA_URL, params=params, timeout=10)
        if res.content.startswith('False'.encode()):
            self.raise_api_exception(res)
        # result = res.text
        print(res.text)
        return res.text.split('|')[1]

    def getMessage(self, phone):
        params = {"action": "getsms", "token": self.token, "itemid": self.item_id, "mobile": phone, "release": 1}
        res = self.session.get(YIMA_URL, params=params, timeout=10)
        # print(res.text)
        if res.content.startswith('False'.encode()):
            # self.raise_api_exception(res)
            return 'NULL'
        return res.content.decode('utf-8')

    def waitForMessage(self, regrex, phone, max_count=20, interval=3):
        count = 0
        while count <= max_count:
            msg = self.getMessage(phone)
            print(msg)
            match = re.search(regrex, msg)
            if match:
                # print("waitfor:%s" % match.group(1))
                return match.group(1)
            else:
                count += 1
                time.sleep(interval)
        else:
            print("poll timeout")
            return None

    def releasePhone(self, phone=None):
        print("释放号码")
        if phone:
            params = {"action": "release", "itemid": self.item_id, "mobile": phone, "token": self.token}
        else:
            params = {"action": "releaseall", "token": self.token}
        res = self.session.get(YIMA_URL, params=params, timeout=10)
        if res.content.startswith('False'.encode()):
            self.raise_api_exception(res)
        # result = res.text
        print(res.text)

    def addblackPhone(self, phone):
        print("加黑号码")
        params = {"action": "addignore", "token": self.token, "mobile": phone, "itemid": self.item_id}
        res = self.session.get(YIMA_URL, params=params, timeout=10)
        if res.content.startswith('False'.encode()):
            self.raise_api_exception(res)
        print(res.text)

    def exit(self):
        params = {"action": "logout", "token": self.token}
        res = self.session.get(YIMA_URL, params=params, timeout=10)
        print("yima exit")
        if res.content.startswith('False'.encode()):
            self.raise_api_exception(res)

    def raise_api_exception(self, response):
        raise Exception(response.content.decode('utf-8'))




if __name__ == '__main__':
    pass
    # import time
    # fm = Yima("xiaoxiaozhuan", "meiriq2014")
    # fm.login()

# re.search(r'您的验证码为：(\d+)\[End\]', mm).group(1)