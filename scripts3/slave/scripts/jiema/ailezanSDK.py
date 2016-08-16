import re
import time
import requests

AILEZAN_URL = "http://api.hellotrue.com/api/do.php"

class Ailezan(object):
    def __init__(self, account, pwd, item_id):
        self.token = None
        self.user = account
        self.pwd = pwd
        self.item_id = str(item_id)
        self.session = requests.session()
        # self.login()

    def login(self):
        print("login ailezan")
        params = {"action": "loginIn", "name": self.user, "password": self.pwd}
        res = self.session.get(AILEZAN_URL, params=params, timeout=10)
        if res.content.startswith('False'.encode()):
            self.raise_api_exception(res)
        print(res.text)
        self.token = res.text.split('|')[1]
        print("login succeed!")
        # print(self.token)

    def getPhone(self, phone=None, phoneType=None, locationMatching=None, locationLevel=None, location=None):
        print("获取号码")
        params = {"action": "getPhone", "sid": self.item_id, "token": self.token}
        if phone:
            params["phone"] = phone
        if phoneType:
            params["locationLevel"] = phoneType
        if locationMatching:
            params["locationMatching"] = locationMatching
        if locationLevel:
            params["locationLevel"] = locationLevel
        if location:
            params["location"] = location
        #CMCC是指移动，UNICOM是指联通，TELECOM是指电信
        res = self.session.get(AILEZAN_URL, params=params, timeout=10)
        if res.content.startswith('False'.encode()):
            self.raise_api_exception(res)
        # result = res.text
        print(res.text)
        return res.text.split('|')[1]

    # 同时取两个以上的码，项目id之间用逗号(,)隔开，如sid=1000,1001。如果要获取指定号码，再在后面加一个phone=要指定获取的号码
    # locationMatching、locationLevel、location三个为可选参数。用来取某些区域的手机号或者不要某些区域的手机号
    # locationMatching的参数值只能是include或者exclude中的一个。include指的是包含区域，exclude指的是不包含区域
    # locationLevel参数只能是p或者c中的一个。p指的是省（province），c指的是市（city）
    # location指的是区域，中文值。可以在取验证码中查询到具体中文内容。需要utf8编码一下
    # 现在，我来举个例子：
    # locationMatching=include&locationLevel=c&location=开封
    # 匹配 城市 开封（意思是只选城市开封的号）
    # locationMatching=exclude&locationLevel=c&location=开封
    # 排除 城市 开封（意思是不选城市开封的号）
    # locationMatching=include&locationLevel=p&location=上海
    # 匹配 省份 河南（意思是只选省份河南的号）
    # locationMatching=exclude&locationLevel=p&location=上海
    # 排除 省份 开封（意思是不选省份河南的号）
    #
    # 注：location 参数为中文，编要编码 例上海 编码后为 %E4%B8%8A%E6%B5%B7
    # 编码工具：http://tool.oschina.net/encode?type=4

    def getMessage(self, phone):
        params = {"action": "getMessage", "sid": self.item_id, "phone": phone, "token": self.token}
        res = self.session.get(AILEZAN_URL, params=params, timeout=10)
        # print(res.text)
        # if res.content.startswith('False'.encode()):
            # self.raise_api_exception(res)
        # if res.text[0] == '0':
        #     return None
        return res.content.decode('utf-8')

    def waitForMessage(self, regrex, phone, max_count=20, interval=5):
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
            params = {"action": "cancelRecv", "sid": self.item_id, "phone": phone, "token": self.token}
        else:
            params = {"action": "cancelAllRecv", "token": self.token}
        res = self.session.get(AILEZAN_URL, params=params, timeout=10)
        if res.content.startswith('False'.encode()):
            self.raise_api_exception(res)
        # result = res.text
        print(res.text)

    def addblackPhone(self, phone):
        print("加黑号码")
        params = {"action": "addBlacklist", "sid": self.item_id, "phone": phone,  "token": self.token}
        res = self.session.get(AILEZAN_URL, params=params, timeout=10)
        if res.content.startswith('False'.encode()):
            self.raise_api_exception(res)
        print(res.text)

    # def exit(self):
    #     params = {"action": "logout", "token": self.token}
    #     res = self.session.get(AILEZAN_URL, params=params, timeout=10)
    #     print("yima exit")
    #     if res.content.startswith('False'.encode()):
    #         self.raise_api_exception(res)

    def raise_api_exception(self, response):
        raise Exception(response.content.decode('utf-8'))



if __name__ == '__main__':
    pass
    # import time
    # fm = Ailezan("xiaoxiaozhuan", "meiriq2014")
    # fm.login()

# re.search(r'您的验证码为：(\d+)\[End\]', mm).group(1)