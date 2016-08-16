import re
import time
import requests

SHENHUA_URL = "http://api.shjmpt.com:9002"

class Shenhua(object):
    def __init__(self, account, pwd, item_id, developer="Unv7wwazHxssYRVT98zVrQ%3d%3d"):
        self.token = None
        self.user = account
        self.pwd = pwd
        self.item_id = str(item_id)
        self.developer = developer
        # self.dev_param = dev_param
        self.session = requests.session()
        # self.login()

    def login(self):
        print("login shenhua...")
        params = {"uName": self.user, "pWord": self.pwd}
        res = self.session.get(SHENHUA_URL + '/pubApi/uLogin', params=params, timeout=10)
        if res.content.startswith('False'.encode()):
            self.raise_api_exception(res)
        self.token = res.text.split('&')[0]
        print("login succeed!")

    def getPhone(self, count=1, phone=None):
        print("获取号码")
        params = {"ItemId": self.item_id, "token": self.token, "Count": count}
        if phone:
            params["Phone"] = phone
        res = self.session.get(SHENHUA_URL + '/pubApi/GetPhone', params=params, timeout=10)
        if res.content.startswith('False'.encode()):
            self.raise_api_exception(res)
        # result = res.text
        print(res.text)
        return [p for p in res.text.split(';') if p][0]

    def getMessage(self, phone):
        params = {"token": self.token, "ItemId": self.item_id, "Phone": phone}
        res = self.session.get(SHENHUA_URL + '/pubApi/GMessage', params=params, timeout=10)
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
        params = {"token": self.token}
        if phone:
            params["phoneList"] = str(phone) + "-" + self.item_id
            res = self.session.get(SHENHUA_URL + '/pubApi/ReleasePhone', params=params, timeout=10)
        else:
            res = self.session.get(SHENHUA_URL + "/pubApi/ReleaseAllPhone", params=params, timeout=10)
        if res.content.startswith('False'.encode()):
            self.raise_api_exception(res)
        # result = res.text
        print(res.text)

    def addblackPhone(self, phone):
        print("加黑号码")
        params = {"token": self.token, "phoneList": self.item_id + "-" + str(phone)}
        res = self.session.get(SHENHUA_URL + '/pubApi/AddBlack', params=params, timeout=10)
        if res.content.startswith('False'.encode()):
            self.raise_api_exception(res)
        print(res.text)

    def exit(self):
        res = self.session.get(SHENHUA_URL + '/pubApi/uExit', params={"token": self.token}, timeout=10)
        print("shenhua exit")
        if res.content.startswith('False'.encode()):
            self.raise_api_exception(res)

    def raise_api_exception(self, response):
        raise Exception(response.content.decode('utf-8'))







if __name__ == '__main__':
    import time
    fm = Shenhua("xiaoxiaozhuan", "meiriq2014")
    fm.login()

# re.search(r'您的验证码为：(\d+)\[End\]', mm).group(1)