import re
import time
import requests

YAMA_URL = "http://www.yayayama.com:19876"

class Yama(object):
    def __init__(self, account, pwd, item_id):
        self.token = None
        self.user = account
        self.pwd = pwd
        self.item_id = str(item_id)
        self.session = requests.session()
        # self.login()

    def login(self):
        print("login yama...")
        params = {"uName": self.user, "pWord": self.pwd}
        res = self.session.get(YAMA_URL + '/Url/userLogin', params=params, timeout=10)
        if res.content.startswith('False'.encode()):
            self.raise_api_exception(res)
        self.token = res.text.split('&')[0]
        # print(self.token)
        print("login succeed!")

    def getPhone(self, phonetype=0):
        print("获取号码")
        params = {"ItemId": self.item_id, "token":  self.token, "PhoneType":  phonetype}
        res = self.session.get(YAMA_URL + '/Url/userGetPhone', params=params, timeout=10)
        if res.content.startswith('False'.encode()):
            self.raise_api_exception(res)
        # print(res.text)
        return [p for p in res.text.split(';') if p][0]

    def getMessage(self, phone):
        params = {"token": self.token, "Phone": phone}
        res = self.session.get(YAMA_URL + '/Url/getMsgQueue', params=params, timeout=20)
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
        params = {"token": self.token, "phoneList": str(phone) + "-" + self.item_id}
        res = self.session.get(YAMA_URL + '/Url/userResPhoneList', params=params, timeout=10)
        if res.content.startswith('False'.encode()):
            self.raise_api_exception(res)
        print(res.text)

    def addblackPhone(self, phone):
        print("加黑号码")
        params = {"token": self.token, "phoneList": self.item_id + "-" + str(phone)}
        res = self.session.get(YAMA_URL + "/Url/userAddBlack", params=params, timeout=10)
        if res.content.startswith('False'.encode()):
            self.raise_api_exception(res)
        print(res.text)

    def exit(self):
        res = self.session.get(YAMA_URL + '/Url/userExit', params={"token": self.token}, timeout=10)
        print("yama exit")
        if res.content.startswith('False'.encode()):
            self.raise_api_exception(res)

    def raise_api_exception(self, response):
        raise Exception(response.content.decode('gbk'))


if __name__ == '__main__':
    pass
    # import time
    # fm = Yama("xiaoxiaozhuan", "meiriq2014")
    # fm.login()

# re.search(r'您的验证码为：(\d+)\[End\]', mm).group(1)