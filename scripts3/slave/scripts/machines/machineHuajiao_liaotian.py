#! -*- coding=utf-8 -*-
import os
import time
# import logging
import random
import re
from machines.StateMachine import Machine
from appium4droid import webdriver
from appium4droid.common.exceptions import *
from appium4droid.support.ui import WebDriverWait
from random import choice
from jiema.jiumaSDK import Jiuma
from jiema.feimaSDK import Feima
from jiema.yamaSDK import Yama
from jiema.ailezanSDK import Ailezan
from jiema.jimaSDK import Jima
from jiema.shenhuaSDK import Shenhua
from jiema.yimaSDK import Yima
try:
    from util import settext_clipboard
except ImportError:
    inputtext = lambda x: 1

class Machinex(Machine):
    def __init__(self, driver, code_platform, fm_uname, fm_pwd):
        super(Machinex, self).__init__(self.initdata)
        self.driver = driver
        self.code_platform = code_platform      #接码平台
        self.code_user = fm_uname       #接码平台帐号
        self.code_pwd = fm_pwd      #接码平台密码
        self.appname = "花椒直播"       #app名字
        self.appname_en = "huajiao"     #记录文件用缩写英文名
        self.imei = None
        self.runnum = None        #记录运行次数

    def initdata(self):
        self.phone = None
        self.pwd = None
        self.begintime = None
        self.endstime = None
        self.try_count = 0      #初始化出错尝试次数
        self.readnum = random.randint(2, 2)     #初始化阅读次数
        #初始化阅读菜单
        self.ismenu1 = True
        self.ismenu2 = True
        self.ismenu3 = True
        self.ismenu4 = True
        self.ismenu5 = True
        #选择初始化接码平台
        if self.code_platform == "feima":
            self.code = Feima(self.code_user, self.code_pwd, 20222)
        elif self.code_platform == "yama":
            self.code = Yama(self.code_user, self.code_pwd, 3441)
        elif self.code_platform == "yima":
            self.code = Yima(self.code_user, self.code_pwd, None)
        elif self.code_platform == "ailezan":
            self.code = Ailezan(self.code_user, self.code_pwd, 7435)
        elif self.code_platform == "jima":
            self.code = Jima(self.code_user, self.code_pwd, 1618)
        elif self.code_platform == "jiuma":
            self.code = Jiuma(self.code_user, self.code_pwd, 7798)
        else:
            self.code = Shenhua(self.code_user, self.code_pwd, 16853)

        return self.begin

    def begin(self):
        dr = self.driver
        dr.press_keycode(3)
        time.sleep(1)
        WebDriverWait(dr, 30).until(lambda d: d.find_element_by_name(self.appname)).click()
        time.sleep(10)
        #检测已进入app
        WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("com.huajiao:id/enter_tv"))
        self.begintime = "开始:%s:%s:%s" % (time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec)
        time.sleep(1)
        #注册率
        sign_rate = random.randint(1, 10000)
        if sign_rate <= 2000:
            WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("com.huajiao:id/enter_tv")).click()
            time.sleep(1)
            return self.login_code_platform
        time.sleep(random.randint(20, 30))
        return self.ends

    def login_code_platform(self):
        #登录接码平台
        print("login %s getcode ......" % self.code_platform)
        try:
            self.code.login()
        except Exception as e:
            print("error in login getcodeplatform,try_count:%s" % self.try_count)
            self.try_count += 1
            if self.try_count > 5:
                print("on try_count,exit")
                return self.exit
            return self.login_code_platform
        return self.begin_signup

    def begin_signup(self):
        dr = self.driver
        try:
            #进入注册页面
            WebDriverWait(dr, 10).until(lambda d: d.find_element_by_id("com.huajiao:id/top_bar_right_btn")).click()
            time.sleep(1)
            #输入昵称
            edts = WebDriverWait(dr, 15).until(lambda d: d.find_element_by_class_name("android.widget.EditText"))
            edts.send_keys(self.get_filemessage("name.txt"))
            time.sleep(1)
            if random.randint(1, 10000) < 1000:
                #选择头像
                WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.huajiao:id/auchor_iv")).click()
                time.sleep(1)
                WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("本地相册")).click()
                time.sleep(1)
                WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("文件管理")).click()
                time.sleep(1)
                WebDriverWait(dr, 15).until(lambda d: d.find_element_by_name("1")).click()
                time.sleep(1)
                WebDriverWait(dr, 15).until(lambda d: d.find_element_by_name("1touxiang")).click()
                time.sleep(1)
                self.swipes(300, random.randint(800, 1000), 300, random.randint(300, 500), random.randint(0, 80))
                time.sleep(5)
                self.select_one_by_id("com.android.fileexplorer:id/file_image")
                time.sleep(1)
                WebDriverWait(dr, 15).until(lambda d: d.find_element_by_name("应用")).click()
                time.sleep(5)
            #保存信息按钮
            WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.huajiao:id/next_btn")).click()
            time.sleep(5)
            #检测进入下一步
            WebDriverWait(dr, 60).until(lambda d: d.find_element_by_name("输入手机号"))
            return self.signup
        except:
            self.try_count += 1
            if self.try_count > 5:
                return self.exit
            dr.press_keycode(4)
            time.sleep(2)
            return self.begin_signup

    def signup(self):
        dr = self.driver
        pwd_li = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
                  "1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
                  "a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
                  "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
                  "u", "v", "w", "x", "y", "z"]
        self.pwd = choice(pwd_li)+choice(pwd_li)+choice(pwd_li)+choice(pwd_li)+choice(pwd_li)+choice(pwd_li)
        try:
            #选择接码平台获取手机号码
            self.phone = self.code.getPhone()
            edts = WebDriverWait(dr, 15).until(lambda d: d.find_elements_by_class_name("android.widget.EditText"))
            #输入手机号码
            edts[0].send_keys(self.phone)
            time.sleep(1)
            #输入密码
            edts[1].send_keys(self.pwd)
            time.sleep(1)
            #点击获取验证码按钮
            WebDriverWait(dr, 10).until(lambda d: d.find_element_by_id("com.huajiao:id/next_btn")).click()
            time.sleep(5)
            WebDriverWait(dr, 30).until(lambda d: d.find_element_by_name("填写验证码"))
            #选择接码平台获取验证码
            #956380（验证码），此验证码仅用于注册花椒；请在20分钟内完成验证。【花椒直播】
            regrex = r'(\d+)（验证码）'
            captcha = self.code.waitForMessage(regrex, self.phone)
            if captcha is None:
                print("getMessage failed,try_count:%s" % self.try_count)
                #释放号码
                self.code.releasePhone(self.phone)
                self.try_count += 1
                if self.try_count > 5:
                    return self.exit
                dr.press_keycode(4)
                time.sleep(5)
                return self.signup
            #输入验证码
            edts = WebDriverWait(dr, 15).until(lambda d: d.find_element_by_class_name("android.widget.EditText"))
            edts.send_keys(captcha)
            time.sleep(1)
            #点击完成按钮按钮
            WebDriverWait(dr, 10).until(lambda d: d.find_element_by_id("com.huajiao:id/goto_huajiao_btn")).click()
            time.sleep(1)
            #进入
            try:
                WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.huajiao:id/onesharedialog_imagebutton_close")).click()
                time.sleep(1)
            except TimeoutException:
                pass
            #更新检测
            try:
                WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.huajiao:id/btn_close")).click()
                time.sleep(1)
            except TimeoutException:
                pass
            dr.press_keycode(4)
            time.sleep(5)
            dr.press_keycode(4)
            time.sleep(1)
            #检测注册成功进入下一步
            WebDriverWait(dr, 120).until(lambda d: d.find_element_by_id("com.huajiao:id/onesharedialog_imagebutton_close")).click()
            time.sleep(1)
            #记录帐号密码
            try:
                with open('/sdcard/1/user%s.log' % self.appname_en, 'a') as f:
                    f.write('\nimei:%s,%s,%s (time %s.%s  %s:%s:%s)' % (self.imei, self.phone, self.pwd, time.localtime().tm_mon, time.localtime().tm_mday, time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec))
            except:
                with open('D:/brush/slave/scripts/doc/user%s.log' % self.appname_en, 'a') as f:
                    f.write('\nimei:%s,%s,%s (time %s.%s  %s:%s:%s)' % (self.imei, self.phone, self.pwd, time.localtime().tm_mon, time.localtime().tm_mday, time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec))
            time.sleep(1)
            return self.do
        except Exception as e:
            print("error in getPhone,try_count:%s" % self.try_count)
            self.try_count += 1
            if self.try_count > 5:
                return self.exit
            dr.press_keycode(4)
            time.sleep(2)
            dr.press_keycode(4)
            time.sleep(2)
            dr.press_keycode(4)
            time.sleep(2)
            dr.press_keycode(4)
            time.sleep(2)
            try:
                WebDriverWait(dr, 2).until(lambda d: d.find_element_by_name(self.appname)).click()
            except TimeoutException:
                pass
            time.sleep(5)
            WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("com.huajiao:id/enter_tv")).click()
            time.sleep(1)
            return self.begin_signup

    def do(self):
        dr = self.driver
        try:
            while self.readnum:
                print("剩下阅读次数:%s" % self.readnum)
                random_read = random.randint(0, 4)
                if random_read == 0:
                    if self.ismenu1:
                        print("goto menu1")
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.huajiao:id/tab_find_tv")).click()
                        time.sleep(5)
                        return self.menu1
                    return self.do
                elif random_read == 1:
                    if self.ismenu2:
                        print("goto menu2")
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.huajiao:id/tab_home_tv")).click()
                        time.sleep(5)
                        return self.menu2
                    return self.do
                elif random_read == 2:
                    if self.ismenu3:
                        print("goto menu3")
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.huajiao:id/bottom_tab_play")).click()
                        time.sleep(5)
                        return self.menu3
                    return self.do
                elif random_read == 3:
                    if self.ismenu4:
                        print("goto menu4")
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.huajiao:id/tab_hot_tv")).click()
                        time.sleep(5)
                        return self.menu4
                    return self.do
                else:
                    if self.ismenu5:
                        print("goto menu5")
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.huajiao:id/tab_user_tv")).click()
                        time.sleep(5)
                        return self.menu5
                    return self.do
        except TimeoutException:
            print("查找菜单出错")
            return self.exception_returnapp()
        print("阅览完毕")
        return self.ends

    def menu1(self):
        dr = self.driver
        try:
            #选择分类
            self.select_one_by_id("com.huajiao:id/tab_text")
            time.sleep(5)
            #选择视频观看
            self.swipes(300, random.randint(800, 1000), 300, random.randint(400, 600), random.randint(0, 1), 5)
            try:
                self.select_one_by_id("com.huajiao:id/cover_image")
            except:
                self.select_one_by_id("com.huajiao:id/feed_live_cover_view")
            time.sleep(10)
            time.sleep(random.randint(60, 90))
            try:
                WebDriverWait(dr, 5).until(lambda d: d.find_element_by_id("com.huajiao:id/btn_comment")).click()
                time.sleep(5)
            except TimeoutException:
                pass
            try:
                WebDriverWait(dr, 5).until(lambda d: d.find_element_by_class_name("android.widget.EditText"))
                settext_clipboard(self.get_filemessage("context.txt"))
                time.sleep(1)
                dr.swipe(350, 1250, 360, 1250, 50)
                time.sleep(0.5)
                dr.tap(146, 1169)
                time.sleep(1)
                WebDriverWait(dr, 10).until(lambda d: d.find_element_by_id("com.huajiao:id/btn_send")).click()
                time.sleep(5)
                time.sleep(random.randint(60, 90))
            except TimeoutException:
                pass
            #转换到其他房间
            for i in range(random.randint(1, 2)):
                dr.swipe(300, 500, random.randint(50, 600), 500)
                time.sleep(10)
                time.sleep(random.randint(60, 90))
                try:
                    WebDriverWait(dr, 5).until(lambda d: d.find_element_by_id("com.huajiao:id/btn_comment")).click()
                    time.sleep(5)
                except TimeoutException:
                    pass
                try:
                    WebDriverWait(dr, 5).until(lambda d: d.find_element_by_class_name("android.widget.EditText"))
                    settext_clipboard(self.get_filemessage("context.txt"))
                    time.sleep(1)
                    dr.swipe(350, 1250, 360, 1250, 50)
                    time.sleep(0.5)
                    dr.tap(146, 1169)
                    time.sleep(1)
                    WebDriverWait(dr, 10).until(lambda d: d.find_element_by_id("com.huajiao:id/btn_send")).click()
                    time.sleep(5)
                    time.sleep(random.randint(60, 90))
                except TimeoutException:
                    pass
            dr.press_keycode(4)
            time.sleep(1)
            dr.press_keycode(4)
            time.sleep(5)
            self.readnum -= 1
            self.ismenu1 = False
        except Exception as e:
            print("error in menu1")
            return self.exception_returnapp()
        return self.do

    def menu2(self):
        dr = self.driver
        try:
            try:
                WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.huajiao:id/jump_follow_btn")).click()
                time.sleep(5)
                self.swipes(300, random.randint(800, 1000), 300, random.randint(400, 600), random.randint(1, 4), 5)
                #关注
                for x in range(random.randint(1, 2)):
                    self.select_one_by_id("com.huajiao:id/focus_iv")
                    time.sleep(1)
                self.select_one_by_id("com.huajiao:id/img_header")
                time.sleep(5)
                self.swipes(300, random.randint(800, 1000), 300, random.randint(400, 600), random.randint(1, 3), 5)
                try:
                    self.select_one_by_id(choice(["com.huajiao:id/left_img", "com.huajiao:id/center_img", "com.huajiao:id/right_img"]))
                    time.sleep(random.randint(20, 30))
                    dr.press_keycode(4)
                    time.sleep(1)
                except TimeoutException:
                    pass
                dr.press_keycode(4)
                time.sleep(5)
                dr.press_keycode(4)
                time.sleep(5)
            except TimeoutException:
                pass
            self.swipes(300, random.randint(800, 1000), 300, random.randint(400, 600), random.randint(1, 2), 5)
            self.readnum -= 1
            self.ismenu2 = False
        except Exception as e:
            print("error in menu2")
            return self.exception_returnapp()
        return self.do

    def menu3(self):
        dr = self.driver
        try:
            WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.huajiao:id/img_close")).click()
            time.sleep(5)
            self.ismenu3 = False
        except Exception as e:
            print("error in menu3")
            return self.exception_returnapp()
        return self.do

    def menu4(self):
        dr = self.driver
        try:
            self.ismenu4 = False
        except Exception as e:
            print("error in menu4")
            return self.exception_returnapp()
        return self.do

    def menu5(self):
        dr = self.driver
        try:
            # liread = ["com.huajiao:id/my_videos_layout", "com.huajiao:id/level_layout", "com.huajiao:id/recharge_layout",
            #           "com.huajiao:id/recharge_layout", "com.huajiao:id/withdraw_layout", "com.huajiao:id/top_bar_left_btn",
            #           "com.huajiao:id/top_bar_right_btn", "com.huajiao:id/me_setting_layout", "com.huajiao:id/fans_go_btn",
            #           "com.huajiao:id/follow_go_btn"]
            # WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id(choice(liread))).click()
            # time.sleep(5)
            # dr.press_keycode(4)
            # time.sleep(2)
            self.ismenu5 = False
        except Exception as e:
            print("error in menu5")
            return self.exception_returnapp()
        return self.do

    def ends(self):
        #记录时间
        self.endstime = "结束:%s:%s:%s" % (time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec)
        print(self.begintime)
        print(self.endstime)
        time.sleep(2)
        try:
            with open('/sdcard/1/time%s.log' % self.appname_en, 'a') as f:
                f.write('\n激活 %s.%s, %s, %s, count:%s' % (time.localtime().tm_mon, time.localtime().tm_mday, self.begintime, self.endstime, self.runnum))
        except:
            pass
        time.sleep(3)
        #效率控制
        # st = [1200, 1200, 1200, 1200, 1200, 1200, 180, 120, 40, 20, 10, 10,
        #       10, 20, 20, 20, 10, 10, 5, 0, 0, 0, 0, 0]
        #
        # print("现在时间是%s:%s,脚本将在%s秒后继续执行" % (time.localtime().tm_hour, time.localtime().tm_min, st[time.localtime().tm_hour-1]))
        # time.sleep(st[time.localtime().tm_hour-1])

        return self.exit

    def get_filemessage(self, filename):
        if os.path.exists("D:/brush/slave/scripts/doc/%s" % filename):
            with open("D:/brush/slave/scripts/doc/%s" % filename, 'r', encoding='utf-8') as f:
                 strname = f.readlines()
        elif os.path.exists("/sdcard/1/%s" % filename):
            with open("/sdcard/1/%s" % filename, 'r', encoding='utf-8') as f:
                 strname = f.readlines()
        else:
            strname = ""
        time.sleep(1)
        return strname[random.randint(0, strname.__len__()-1)].strip()

    def swipes(self, x1, y1, x2, y2, swipe_num=1, swipe_time=1):
        dr = self.driver
        print("swipenum:%s" % swipe_num)
        for x in range(swipe_num):
            dr.swipe(x1, y1, x2, y2)
            time.sleep(swipe_time)

    def select_one_by_id(self, find_id, find_time=30, find_min=0, find_max=0):
        selectone = WebDriverWait(self.driver, find_time).until(lambda d: d.find_elements_by_id(find_id))
        if find_max == 0:
            selectone[random.randint(find_min, selectone.__len__()-1)].click()
        else:
            selectone[random.randint(find_min, find_max)].click()

    def exception_returnapp(self):
        dr = self.driver
        print("try_count:%s" % self.try_count)
        self.try_count += 1
        if self.try_count > 5:
            return self.exit
        dr.press_keycode(4)
        time.sleep(1)
        dr.press_keycode(4)
        time.sleep(1)
        dr.press_keycode(82)
        time.sleep(2)
        try:
            WebDriverWait(dr, 2).until(lambda d: d.find_element_by_name(self.appname)).click()
        except TimeoutException:
            dr.press_keycode(4)
        time.sleep(5)
        return self.do


class Machinex2(Machine):
    def __init__(self, driver):
        super(Machinex2, self).__init__(self.initdata)
        self.driver = driver
        self.appname = "花椒直播"       #app名字
        self.appname_en = "huajiao"     #记录文件用缩写英文名
        self.imei = None
        self.remainday = None

    def initdata(self):
        self.begintime = None
        self.endstime = None
        self.try_count = 0      #初始化出错尝试次数
        self.readnum = random.randint(1, 1)     #初始化阅读次数
        #初始化阅读菜单
        self.ismenu1 = True
        self.ismenu2 = True
        self.ismenu3 = True
        self.ismenu4 = True
        self.ismenu5 = True

        return self.begin

    def begin(self):
        dr = self.driver
        dr.press_keycode(3)
        time.sleep(1)
        WebDriverWait(dr, 30).until(lambda d: d.find_element_by_name(self.appname)).click()
        time.sleep(10)
        #检测已进入app
        WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("com.huajiao:id/enter_tv"))
        self.begintime = "开始:%s:%s:%s" % (time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec)
        time.sleep(1)
        return self.login

    def login(self):
        dr = self.driver
        try:
            with open('/sdcard/1/user%s.log' % self.appname_en, 'r') as f:
                selectuser = f.read()
        except:
            with open('D:/brush/slave/scripts/doc/user%s.log' % self.appname_en, 'r') as f:
                selectuser = f.read()
        user = re.search(r'imei:%s,(\d+)' % self.imei, selectuser)
        pwd = re.search(r'imei:%s,\d+,([0-9a-z]+)' % self.imei, selectuser)
        if user and pwd:
            WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.huajiao:id/enter_tv")).click()
            time.sleep(1)
            edit = WebDriverWait(dr, 15).until(lambda d: d.find_elements_by_class_name("android.widget.EditText"))
            edit[0].send_keys(str(user.group(1)))
            time.sleep(1)
            edit[1].send_keys(str(pwd.group(1)))
            time.sleep(1)
            WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.huajiao:id/login_btn")).click()
            time.sleep(5)
            #进入
            try:
                WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.huajiao:id/onesharedialog_imagebutton_close")).click()
                time.sleep(1)
            except TimeoutException:
                pass
            #更新检测
            try:
                WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.huajiao:id/btn_close")).click()
                time.sleep(1)
            except TimeoutException:
                pass
            dr.press_keycode(4)
            time.sleep(5)
            dr.press_keycode(4)
            time.sleep(1)
            #检测注册成功进入下一步
            WebDriverWait(dr, 120).until(lambda d: d.find_element_by_id("com.huajiao:id/bottom_tab_play"))
            time.sleep(1)
            return self.do
        time.sleep(random.randint(10, 20))
        return self.ends

    def do(self):
        dr = self.driver
        try:
            while self.readnum:
                print("剩下阅读次数:%s" % self.readnum)
                random_read = random.randint(0, 4)
                if random_read == 0:
                    if self.ismenu1:
                        print("goto menu1")
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.huajiao:id/tab_find_tv")).click()
                        time.sleep(5)
                        return self.menu1
                    return self.do
                elif random_read == 1:
                    if self.ismenu2:
                        print("goto menu2")
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.huajiao:id/tab_home_tv")).click()
                        time.sleep(5)
                        return self.menu2
                    return self.do
                elif random_read == 2:
                    if self.ismenu3:
                        print("goto menu3")
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.huajiao:id/bottom_tab_play")).click()
                        time.sleep(5)
                        return self.menu3
                    return self.do
                elif random_read == 3:
                    if self.ismenu4:
                        print("goto menu4")
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.huajiao:id/tab_hot_tv")).click()
                        time.sleep(5)
                        return self.menu4
                    return self.do
                else:
                    if self.ismenu5:
                        print("goto menu5")
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.huajiao:id/tab_user_tv")).click()
                        time.sleep(5)
                        return self.menu5
                    return self.do
        except TimeoutException:
            print("查找菜单出错")
            return self.exception_returnapp()
        print("阅览完毕")
        return self.ends

    def menu1(self):
        dr = self.driver
        try:
            #选择分类
            self.select_one_by_id("com.huajiao:id/tab_text")
            time.sleep(5)
            #选择视频观看
            self.swipes(300, random.randint(800, 1000), 300, random.randint(400, 600), random.randint(1, 2), 5)
            try:
                self.select_one_by_id("com.huajiao:id/cover_image")
            except:
                self.select_one_by_id("com.huajiao:id/feed_live_cover_view")
            time.sleep(random.randint(60, 90))
            try:
                WebDriverWait(dr, 5).until(lambda d: d.find_element_by_id("com.huajiao:id/btn_comment")).click()
                time.sleep(5)
            except TimeoutException:
                pass
            try:
                WebDriverWait(dr, 5).until(lambda d: d.find_element_by_class_name("android.widget.EditText"))
                settext_clipboard(self.get_filemessage("context.txt"))
                time.sleep(1)
                dr.swipe(350, 1250, 360, 1250, 50)
                time.sleep(0.5)
                dr.tap(146, 1169)
                time.sleep(1)
                WebDriverWait(dr, 10).until(lambda d: d.find_element_by_id("com.huajiao:id/btn_send")).click()
                time.sleep(5)
                time.sleep(random.randint(60, 90))
            except TimeoutException:
                pass
            dr.press_keycode(4)
            time.sleep(1)
            dr.press_keycode(4)
            time.sleep(5)
            self.readnum -= 1
            self.ismenu1 = False
        except Exception as e:
            print("error in menu1")
            return self.exception_returnapp()
        return self.do

    def menu2(self):
        dr = self.driver
        try:
            self.swipes(300, random.randint(800, 1000), 300, random.randint(400, 600), random.randint(3, 5), 5)
            self.ismenu2 = False
        except Exception as e:
            print("error in menu2")
            return self.exception_returnapp()
        return self.do

    def menu3(self):
        dr = self.driver
        try:
            WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.huajiao:id/img_close")).click()
            time.sleep(5)
            self.ismenu3 = False
        except Exception as e:
            print("error in menu3")
            return self.exception_returnapp()
        return self.do

    def menu4(self):
        dr = self.driver
        try:
            self.ismenu4 = False
        except Exception as e:
            print("error in menu4")
            return self.exception_returnapp()
        return self.do

    def menu5(self):
        dr = self.driver
        try:
            # liread = ["com.huajiao:id/my_videos_layout", "com.huajiao:id/level_layout", "com.huajiao:id/recharge_layout",
            #           "com.huajiao:id/recharge_layout", "com.huajiao:id/withdraw_layout", "com.huajiao:id/top_bar_left_btn",
            #           "com.huajiao:id/top_bar_right_btn", "com.huajiao:id/me_setting_layout", "com.huajiao:id/fans_go_btn",
            #           "com.huajiao:id/follow_go_btn"]
            # WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id(choice(liread))).click()
            # time.sleep(5)
            # dr.press_keycode(4)
            # time.sleep(2)
            self.ismenu5 = False
        except Exception as e:
            print("error in menu5")
            return self.exception_returnapp()
        return self.do

    def ends(self):
        #记录时间
        self.endstime = "结束:%s:%s:%s" % (time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec)
        print(self.begintime)
        print(self.endstime)
        time.sleep(2)
        try:
            with open('/sdcard/1/time%s2.log' % self.appname_en, 'a') as f:
                f.write('\n留存%s %s.%s, %s, %s' % (self.remainday, time.localtime().tm_mon, time.localtime().tm_mday, self.begintime, self.endstime))
        except:
            pass
        time.sleep(3)
        return self.exit

    def get_filemessage(self, filename):
        if os.path.exists("D:/brush/slave/scripts/doc/%s" % filename):
            with open("D:/brush/slave/scripts/doc/%s" % filename, 'r', encoding='utf-8') as f:
                 strname = f.readlines()
        elif os.path.exists("/sdcard/1/%s" % filename):
            with open("/sdcard/1/%s" % filename, 'r', encoding='utf-8') as f:
                 strname = f.readlines()
        else:
            strname = ""
        time.sleep(1)
        return strname[random.randint(0, strname.__len__()-1)].strip()

    def swipes(self, x1, y1, x2, y2, swipe_num=1, swipe_time=1):
        dr = self.driver
        print("swipenum:%s" % swipe_num)
        for x in range(swipe_num):
            dr.swipe(x1, y1, x2, y2)
            time.sleep(swipe_time)

    def select_one_by_id(self, find_id, find_time=30, find_min=0, find_max=0):
        selectone = WebDriverWait(self.driver, find_time).until(lambda d: d.find_elements_by_id(find_id))
        if find_max == 0:
            selectone[random.randint(find_min, selectone.__len__()-1)].click()
        else:
            selectone[random.randint(find_min, find_max)].click()

    def exception_returnapp(self):
        dr = self.driver
        print("try_count:%s" % self.try_count)
        self.try_count += 1
        if self.try_count > 5:
            return self.exit
        dr.press_keycode(4)
        time.sleep(1)
        dr.press_keycode(4)
        time.sleep(1)
        dr.press_keycode(82)
        time.sleep(2)
        try:
            WebDriverWait(dr, 2).until(lambda d: d.find_element_by_name(self.appname)).click()
        except TimeoutException:
            dr.press_keycode(4)
        time.sleep(5)
        return self.do



if __name__ == "__main__":
    wd = webdriver.Remote()
    time.sleep(2)

