import re
import time
import requests

JIUMA_URL = "http://api.9mli.com/http.aspx"

class Jiuma(object):
    def __init__(self, account, pwd, item_id):
        self.token = None
        self.user = account
        self.pwd = pwd
        self.item_id = str(item_id)
        self.session = requests.session()
        # self.login()

    def login(self):
        print("login jiuma")
        params = {"action": "loginIn", "uid": self.user, "pwd": self.pwd}
        res = self.session.get(JIUMA_URL, params=params, timeout=10)
        if res.content.startswith('False'.encode()):
            self.raise_api_exception(res)
        # print(res.text)
        self.token = res.text.split('|')[1]
        print("login succeed!")

    def getPhone(self, phone=None, cr=None, pr=None, cy=None):
        print("获取号码")
        params = {"action": "getMobilenum", "pid": self.item_id, "uid": self.user, "token": self.token}
        if phone:
            params["mobile"] = phone
        if cr:
            params["cr"] = cr
        if pr:
            params["pr"] = pr
        if cy:
            params["cy"] = cy
        if pr or cy:
            params["way"] = 0
        res = self.session.get(JIUMA_URL, params=params, timeout=10)
        if res.content.startswith('False'.encode()):
            self.raise_api_exception(res)
        # result = res.text
        print(res.text)
        return res.text.split('|')[0]

    def getMessage(self, phone):
        params = {"action": "getVcodeAndReleaseMobile", "uid": self.user, "token": self.token, "pid": self.item_id, "mobile": phone}
        res = self.session.get(JIUMA_URL, params=params, timeout=10)
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
        print("释放号码号码")
        params = {"action": "ReleaseMobile", "uid": self.user, "token": self.token}
        if phone:
            params["mobile"] = phone
        res = self.session.get(JIUMA_URL, params=params, timeout=10)

        if res.content.startswith('False'.encode()):
            self.raise_api_exception(res)
        # result = res.text
        print(res.text)

    def addblackPhone(self, phone):
        print("加黑号码")
        params = {"action": "addIgnoreList", "pid": self.item_id, "phone": phone, "uid": self.user, "token": self.token}
        if phone:
            params["mobile"] = phone
        res = self.session.get(JIUMA_URL, params=params, timeout=10)
        if res.content.startswith('False'.encode()):
            self.raise_api_exception(res)
        # result = res.text
        print(res.text)

    # def exit(self):
    #     params = {"action": "logout", "token": self.token}
    #     res = self.session.get(JIUMA_URL, params=params, timeout=10)
    #     print("yima exit")
    #     if res.content.startswith('False'.encode()):
    #         self.raise_api_exception(res)

    def raise_api_exception(self, response):
        raise Exception(response.content.decode('utf-8'))



if __name__ == '__main__':
    import time
    fm = Jiuma("xiaoxiaozhuan", "meiriq2014")
    fm.login()

# re.search(r'您的验证码为：(\d+)\[End\]', mm).group(1)