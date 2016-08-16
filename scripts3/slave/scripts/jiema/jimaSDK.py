import re
import time
import requests

JIMA_URL = "http://api.yzm8.net/api.aspx"

class Jima(object):
    def __init__(self, account, pwd, item_id):
        self.token = None
        self.user = account
        self.pwd = pwd
        self.item_id = str(item_id)
        self.session = requests.session()
        self.author_uid = ""
        # self.login()

    def login(self):
        print("login jima")
        params = {"action": "loginIn", "uid": self.user, "pwd": self.pwd}
        res = self.session.get(JIMA_URL, params=params, timeout=10)
        if res.content.startswith('False'.encode()):
            self.raise_api_exception(res)
        # print(res.text)
        self.token = res.text.split('|')[1]
        print("login succeed!")
        # print(self.token)

    def getPhone(self, phone=None, cr=None, pr=None, cy=None):
        print("获取号码")
        params = {"action": "getMobilenum", "pid": self.item_id,  "uid": self.user, "token": self.token}
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
        # http://www.yzm8.net/list.aspx?cid=2#mj2
        # 7. cr=指定运营商（1:电信 2:移动 3:联通） (可以不填写该参数)
        # 8. pr=指定省份ID，省份ID看下表（可以不填写）
        # 9. cy=指定城市ID，城市ID看下表（可以不填写）
        # 10. way=地区选择方式，0：选定指定的地区  1：排除指定的地区
        res = self.session.get(JIMA_URL, params=params, timeout=10)
        if res.content.startswith('False'.encode()):
            self.raise_api_exception(res)
        # result = res.text
        print(res.text)
        return res.text.split('|')[0]

    def getMessage(self, phone):
        params = {"action": "getVcodeAndReleaseMobile", "mobile": phone, "token": self.token, "uid": self.user, "pid": self.item_id}
        res = self.session.get(JIMA_URL, params=params, timeout=10)
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
        params = {"action": "ReleaseMobile", "uid": self.user, "token": self.token}
        res = self.session.get(JIMA_URL, params=params, timeout=10)
        if phone:
            params["mobile"] = phone
        if res.content.startswith('False'.encode()):
            self.raise_api_exception(res)
        print(res.text)

    def addblackPhone(self, phone):
        print("加黑号码")
        params = {"action": "addIgnoreList", "uid": self.user, "token": self.token, "mobiles": phone, "pid": self.item_id}
        res = self.session.get(JIMA_URL, params=params, timeout=10)
        if res.content.startswith('False'.encode()):
            self.raise_api_exception(res)
        print(res.text)

    # def exit(self):
    #     params = {"action": "logout", "token": self.token}
    #     res = self.session.get(JIMA_URL, params=params, timeout=10)
    #     print("yima exit")
    #     if res.content.startswith('False'.encode()):
    #         self.raise_api_exception(res)

    def raise_api_exception(self, response):
        raise Exception(response.content.decode('utf-8'))



if __name__ == '__main__':
    import time
    fm = Jima("xiaoxiaozhuan", "meiriq2014")
    fm.login()

# re.search(r'您的验证码为：(\d+)\[End\]', mm).group(1)