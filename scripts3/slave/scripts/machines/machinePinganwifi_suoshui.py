#! -*- coding=utf-8 -*-
import os
import time
import random
import re
# import logging

from machines.StateMachine import Machine
from appium4droid import webdriver
from appium4droid.common.exceptions import *
from appium4droid.support.ui import WebDriverWait
from jiema.jiumaSDK import Jiuma
from jiema.feimaSDK import Feima
from jiema.yamaSDK import Yama
from jiema.ailezanSDK import Ailezan
from jiema.jimaSDK import Jima
from jiema.shenhuaSDK import Shenhua
from jiema.yimaSDK import Yima
from random import choice


class Machinex(Machine):
    def __init__(self, driver, code_platform, fm_uname, fm_pwd):
        super(Machinex, self).__init__(self.initdata)
        self.driver = driver
        self.code_platform = code_platform      #接码平台
        self.code_user = fm_uname       #接码平台帐号
        self.code_pwd = fm_pwd      #接码平台密码
        self.appname = "平安WiFi"       #app名字
        self.appname_en = "wifi"     #记录文件用缩写英文名
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
        #选择初始化接码平台
        if self.code_platform == "feima":
            self.code = Feima(self.code_user, self.code_pwd, 2055)
        elif self.code_platform == "yama":
            self.code = Yama(self.code_user, self.code_pwd, 599)
        elif self.code_platform == "yima":
            self.code = Yima(self.code_user, self.code_pwd, 26)
        elif self.code_platform == "ailezan":
            self.code = Ailezan(self.code_user, self.code_pwd, 2395)
        elif self.code_platform == "jima":
            self.code = Jima(self.code_user, self.code_pwd, 4568)
        elif self.code_platform == "jiuma":
            self.code = Jiuma(self.code_user, self.code_pwd, 17564)
        else:
            self.code = Shenhua(self.code_user, self.code_pwd, 581)

        return self.begin

    def begin(self):
        dr = self.driver
        dr.press_keycode(3)
        time.sleep(1)
        WebDriverWait(dr, 30).until(lambda d: d.find_element_by_name(self.appname)).click()
        time.sleep(10)
        #检测已进入app
        WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("com.pingan.pinganwifi:id/guide_now_experience_btn"))
        self.begintime = "开始:%s:%s:%s" % (time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec)
        #新开软件随机翻页
        self.swipes(600, 300, 300, 300, random.randint(0, 2), 2)
        WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("com.pingan.pinganwifi:id/guide_now_experience_btn")).click()
        time.sleep(1)
        #关闭广告
        try:
            WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("com.pingan.pinganwifi:id/img_general_advert_close")).click()
            time.sleep(1)
        except TimeoutException:
            pass
        WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("com.pingan.pinganwifi:id/tv_self"))
        #注册率
        sign_rate = random.randint(1, 10000)
        if sign_rate <= 10000:
            WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("com.pingan.pinganwifi:id/tv_self")).click()
            time.sleep(1)
            return self.login_code_platform

        return self.do

    def login_code_platform(self):
        #登录接码平台
        print("login %s getcode ......" % self.code_platform)
        try:
            self.code.login()
        except Exception as e:
            print("error in login getcodeplatform,try_count:%s" % self.try_count)
            self.try_count += 1
            if self.try_count > 10:
                print("on try_count,exit")
                self.try_count = 0
                return self.exit
            return self.login_code_platform
        return self.signup

    def signup(self):
        dr = self.driver
        pwd_li = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
                  "1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
                  "a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
                  "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
                  "u", "v", "w", "x", "y", "z"]
        self.pwd = choice(pwd_li)+choice(pwd_li)+choice(pwd_li)+choice(pwd_li)+choice(pwd_li)+choice(pwd_li)
        try:
            #进入注册页面
            WebDriverWait(dr, 10).until(lambda d: d.find_element_by_id("com.pingan.pinganwifi:id/center_login_btn")).click()
            time.sleep(1)
            #选择接码平台获取手机号码
            self.phone = self.code.getPhone()
            edts = WebDriverWait(dr, 15).until(lambda d: d.find_elements_by_class_name("android.widget.EditText"))
            for x in range(5):
                #输入手机号码
                edts[0].send_keys(self.phone)
                time.sleep(1)
                if edts[0].text.__len__() == 13:
                    break
                else:
                    WebDriverWait(dr, 5).until(lambda d: d.find_element_by_id("com.pingan.pinganwifi:id/delete")).click()
                    time.sleep(1)
            #点击获取验证码按钮
            WebDriverWait(dr, 10).until(lambda d: d.find_element_by_id("com.pingan.pinganwifi:id/reg_getcode_btn")).click()
            time.sleep(1)
            #检测是否已注册
            try:
                WebDriverWait(dr, 5).until(lambda d: d.find_element_by_id("com.pingan.pinganwifi:id/cancel")).click()
                #释放号码
                self.code.releasePhone(self.phone)
                self.code.addblackPhone(self.phone)
                self.try_count += 1
                if self.try_count > 10:
                    self.try_count = 0
                    return self.exit
                dr.press_keycode(4)
                time.sleep(1)
                return self.signup
            except TimeoutException:
                pass
            #获取验证码
            #平安WiFi验证码0577，祝您使用愉快！【中国平安】
            regrex = r'验证码(\d+)'
            captcha = self.code.waitForMessage(regrex, self.phone)
            if captcha is None:
                print("getMessage failed,try_count:%s" % self.try_count)
                #释放号码
                self.code.releasePhone(self.phone)
                self.try_count += 1
                if self.try_count > 10:
                    self.try_count = 0
                    return self.exit
                dr.press_keycode(4)
                time.sleep(1)
                return self.signup
            #输入验证码
            edts[1].send_keys(captcha)
            time.sleep(1)
            #点击完成按钮按钮
            WebDriverWait(dr, 10).until(lambda d: d.find_element_by_id("com.pingan.pinganwifi:id/reg_submit_btn")).click()
            time.sleep(1)
            edts = WebDriverWait(dr, 15).until(lambda d: d.find_elements_by_class_name("android.widget.EditText"))
            #输入密码
            edts[1].send_keys(self.pwd)
            time.sleep(1)
            #检测注册成功进入下一步
            WebDriverWait(dr, 60).until(lambda d: d.find_element_by_id("com.pingan.pinganwifi:id/pwd_setting_submit_btn")).click()
            time.sleep(1)
            #检测信息保存完毕跳转页面
            WebDriverWait(dr, 60).until(lambda d: d.find_element_by_id("com.pingan.pinganwifi:id/tv_self"))
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
            if self.try_count > 10:
                self.try_count = 0
                return self.exit
            dr.press_keycode(4)
            time.sleep(2)
            return self.signup

    def do(self):
        dr = self.driver
        try:
            while self.readnum:
                print("剩下阅读次数:%s" % self.readnum)
                random_read = random.randint(0, 3)
                if random_read == 0:
                    if self.ismenu1:
                        print("goto menu1")
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_name("连网")).click()
                        time.sleep(5)
                        return self.menu1
                    return self.do
                elif random_read == 1:
                    if self.ismenu2:
                        print("goto menu2")
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.pingan.pinganwifi:id/tv_action")).click()
                        time.sleep(5)
                        return self.menu2
                    return self.do
                elif random_read == 2:
                    if self.ismenu3:
                        print("goto menu3")
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.pingan.pinganwifi:id/tv_service")).click()
                        time.sleep(5)
                        return self.menu3
                    return self.do
                else:
                    if self.ismenu4:
                        print("goto menu5")
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.pingan.pinganwifi:id/tv_self")).click()
                        time.sleep(5)
                        return self.menu4
                    return self.do
        except TimeoutException:
            print("查找菜单出错")
            return self.exception_returnapp()
        print("阅览完毕")
        return self.ends

    def menu1(self):
        dr = self.driver
        try:
            #关闭广告
            try:
                WebDriverWait(dr, 5).until(lambda d: d.find_element_by_id("com.pingan.pinganwifi:id/img_general_advert_close")).click()
                time.sleep(1)
            except TimeoutException:
                pass
            self.swipes(300, random.randint(800, 900), 300, random.randint(600, 700), random.randint(0, 2), random.randint(10, 15))
            self.readnum -= 1
            self.ismenu1 = False
        except Exception as e:
            print("error in menu1")
            return self.exception_returnapp()
        return self.do

    def menu2(self):
        dr = self.driver
        try:
            self.select_one_by_id("com.pingan.pinganwifi:id/channel_grid_item_iv")
            time.sleep(random.randint(5, 10))
            dr.press_keycode(4)
            time.sleep(1)
            for x in range(random.randint(1, 2)):
                self.swipes(300, random.randint(800, 900), 300, random.randint(600, 700), random.randint(1, 3), random.randint(2, 5))
                self.select_one_by_id("com.pingan.pinganwifi:id/tv_title")
                time.sleep(random.randint(5, 10))
                self.swipes(300, random.randint(800, 1000), 300, random.randint(400, 600), random.randint(2, 3), random.randint(5, 10))
                dr.press_keycode(4)
                time.sleep(1)
            self.readnum -= 1
            self.ismenu2 = False
        except Exception as e:
            print("error in menu2")
            return self.exception_returnapp()
        return self.do

    def menu3(self):
        dr = self.driver
        try:
            # try:
            #     WebDriverWait(dr, 5).until(lambda d: d.find_element_by_id("")).click()
            #     time.sleep(0.5)
            #     WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.pingan.pinganwifi:id/tv_self")).click()
            #     time.sleep(1)
            # except TimeoutException:
            self.swipes(300, random.randint(800, 1000), 300, random.randint(400, 600), random.randint(0, 2), random.randint(2, 5))
            self.ismenu3 = False
        except Exception as e:
            print("error in menu3")
            return self.exception_returnapp()
        return self.do

    def menu4(self):
        dr = self.driver
        try:
            #每日签到
            WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.pingan.pinganwifi:id/self_day_singn_group")).click()
            time.sleep(5)
            dr.press_keycode(4)
            time.sleep(1)
            # liread = ["com.pingan.pinganwifi:id/my_points",  "com.pingan.pinganwifi:id/task_earm_points",
            #           "com.pingan.pinganwifi:id/exchange_center", "com.pingan.pinganwifi:id/user_found",
            #           "com.pingan.pinganwifi:id/international_wifi", "com.pingan.pinganwifi:id/unlogin_center_face_image"]
            # WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id(choice(liread))).click()
            # time.sleep(5)
            # dr.press_keycode(4)
            # time.sleep(5)
            self.ismenu4 = False
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
        if self.try_count > 10:
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
        self.appname = "平安WiFi"       #app名字
        self.appname_en = "wifi"     #记录文件用缩写英文名
        self.imei = None
        self.remainday = None

    def initdata(self):
        self.begintime = None
        self.endstime = None
        self.try_count = 0      #初始化出错尝试次数

        return self.begin

    def begin(self):
        dr = self.driver
        dr.press_keycode(3)
        time.sleep(1)
        WebDriverWait(dr, 30).until(lambda d: d.find_element_by_name(self.appname)).click()
        time.sleep(10)
        #检测已进入app
        WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("com.pingan.pinganwifi:id/guide_now_experience_btn"))
        self.begintime = "开始:%s:%s:%s" % (time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec)
        #新开软件翻页
        self.swipes(600, 300, 300, 300, random.randint(0, 2), 2)
        WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("com.pingan.pinganwifi:id/guide_now_experience_btn")).click()
        time.sleep(1)
        try:
            WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("com.pingan.pinganwifi:id/img_general_advert_close")).click()
            time.sleep(1)
        except TimeoutException:
            pass
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
            WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("com.pingan.pinganwifi:id/tv_self")).click()
            time.sleep(1)
            WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.pingan.pinganwifi:id/center_login_btn")).click()
            time.sleep(1)
            WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.pingan.pinganwifi:id/common_topview_img_right")).click()
            time.sleep(1)
            edit = WebDriverWait(dr, 15).until(lambda d: d.find_elements_by_class_name("android.widget.EditText"))
            edit[0].send_keys(str(user.group(1)))
            time.sleep(1)
            edit[1].send_keys(str(pwd.group(1)))
            time.sleep(1)
            WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.pingan.pinganwifi:id/btn_login")).click()
            time.sleep(5)
            WebDriverWait(dr, 60).until(lambda d: d.find_element_by_id("com.pingan.pinganwifi:id/tv_self"))
        time.sleep(30)
        return self.ends


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
        if self.try_count > 10:
            # self.try_count = 0
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
