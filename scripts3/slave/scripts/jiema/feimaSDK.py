import re
import time
import requests

FEIMA_URL = "http://xapi.yika66.com"

class Feima(object):
    def __init__(self, account, pwd, item_id, developer="yqrH5C9L5cd07K5iPuNZlg%3d%3d"):
        self.token = None
        self.user = account
        self.pwd = pwd
        self.item_id = str(item_id)
        self.developer = developer
        # self.dev_param = dev_param
        self.session = requests.session()
        # self.login()

    def login(self):
        print("login feima...")
        params = {"uName": self.user, "pWord": self.pwd, "Developer": self.developer}
        res = self.session.get(FEIMA_URL + '/User/login', params=params, timeout=10)
        if res.content.startswith('False'.encode()):
            self.raise_api_exception(res)
        self.token = res.text.split('&')[0]
        print("login succeed!")
        print(self.token)

    def getPhone(self, phone_type=0, phone=None, count=1, area=None):
        print("获取号码")
        params = {"ItemId": self.item_id, "token": self.token, "phoneType": phone_type, "Count": count, "Area": area}
        if phone:
            params["Phone"] = phone
        if area:
            params["Area"] = area
        res = self.session.get(FEIMA_URL + '/User/getPhone', params=params, timeout=10)
        if res.content.startswith('False'.encode()):
            self.raise_api_exception(res)
        # result = res.text
        # return result
        return [p for p in res.text.split(';') if p][0]

    def getMessage(self, phone):
        params = {"token": self.token, "Phone": phone}
        res = self.session.get(FEIMA_URL + '/User/getMessage', params=params, timeout=10)
        # print(res.text)
        if res.content.startswith('False'.encode()):
            self.raise_api_exception(res)
        return res.content.decode('gbk')

    def waitForMessage(self, regrex, phone, max_count=20, interval=3):
        count = 0
        while count <= max_count:
            msg = self.getMessage(phone)
            print(msg)
            match = re.search(regrex, msg)
            if match:
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
            res = self.session.get(FEIMA_URL + "/User/releasePhone", params=params, timeout=10)
        else:
            res = self.session.get(FEIMA_URL + "/User/ReleaseAllPhone", params=params, timeout=10)
        if res.content.startswith('False'.encode()):
            self.raise_api_exception(res)
        print(res.text)

    def addblackPhone(self, phone):
        print("加黑号码")
        params = {"token": self.token, "phoneList": self.item_id + "-" + str(phone)}
        res = self.session.get(FEIMA_URL + "/User/addBlack", params=params, timeout=10)
        if res.content.startswith('False'.encode()):
            self.raise_api_exception(res)
        print(res.text)

    def exit(self):
        res = self.session.get(FEIMA_URL + '/User/exit', params={"token": self.token}, timeout=10)
        print("feima exit")
        if res.content.startswith('False'.encode()):
            self.raise_api_exception(res)

    def raise_api_exception(self, response):
        raise Exception(response.content.decode('gbk'))





if __name__ == '__main__':
    pass
    # import time
    # fm = Feima("xiaoxiaozhuan", "meiriq2014")
    # fm.login()
    # "yqrH5C9L5cd07K5iPuNZlg%3d%3d"
# re.search(r'您的验证码为：(\d+)\[End\]', mm).group(1)