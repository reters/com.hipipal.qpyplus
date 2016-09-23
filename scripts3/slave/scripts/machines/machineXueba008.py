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


class Machinex(Machine):
    def __init__(self, driver, code_platform, fm_uname, fm_pwd):
        super(Machinex, self).__init__(self.initdata)
        self.driver = driver
        self.code_platform = code_platform      #接码平台
        self.code_user = fm_uname       #接码平台帐号
        self.code_pwd = fm_pwd      #接码平台密码
        self.appname = "学霸君"       #app名字
        self.appname_en = "xueba"     #记录文件用缩写英文名
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
            self.code = Feima(self.code_user, self.code_pwd, None)
        elif self.code_platform == "yama":
            self.code = Yama(self.code_user, self.code_pwd, None)
        elif self.code_platform == "yima":
            self.code = Yima(self.code_user, self.code_pwd, None)
        elif self.code_platform == "ailezan":
            self.code = Ailezan(self.code_user, self.code_pwd, 3547)
        elif self.code_platform == "jima":
            self.code = Jima(self.code_user, self.code_pwd, None)
        elif self.code_platform == "jiuma":
            self.code = Jiuma(self.code_user, self.code_pwd, None)
        elif self.code_platform == "shenhua":
            self.code = Shenhua(self.code_user, self.code_pwd, None)

        return self.begin

    def begin(self):
        dr = self.driver
        dr.press_keycode(3)
        time.sleep(1)
        WebDriverWait(dr, 30).until(lambda d: d.find_element_by_name(self.appname)).click()
        time.sleep(10)
        #检测已进入app
        WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("com.wenba.bangbang:id/login_guide_submit_btn"))
        self.begintime = "开始:%s:%s:%s" % (time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec)
        time.sleep(1)
        #注册率
        sign_rate = random.randint(1, 10000)
        if sign_rate <= 5000:
            #进入注册页面
            WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("com.wenba.bangbang:id/login_guide_submit_btn")).click()
            time.sleep(1)
            return self.login_code_platform
        time.sleep(random.randint(5, 10))
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
            #选择接码平台获取手机号码
            self.phone = self.code.getPhone()
            edts = WebDriverWait(dr, 15).until(lambda d: d.find_element_by_class_name("android.widget.EditText"))
            edts.click()
            dr.press_keycode(123)
            time.sleep(0.5)
            for i in range(15):
                dr.press_keycode(67)
                if edts.text == " 请输入手机号":
                    break
            #输入手机号码
            edts.send_keys(self.phone)
            time.sleep(1)
            #点击获取验证码按钮
            WebDriverWait(dr, 10).until(lambda d: d.find_element_by_id("com.wenba.bangbang:id/login_enter_submit_tv")).click()
            time.sleep(5)
            #选择接码平台获取验证码
            #【学霸君】您的验证码: 8877，若非本人操作请，谢谢！(来自106906555908)
            regrex = r'验证码: (\d+)'
            captcha = self.code.waitForMessage(regrex, self.phone)
            if captcha is None:
                print("getMessage failed,try_count:%s" % self.try_count)
                #释放号码
                self.code.releasePhone(self.phone)
                self.try_count += 1
                if self.try_count > 5:
                    return self.exit
                dr.press_keycode(4)
                time.sleep(1)
                return self.signup
            #输入验证码
            edts = WebDriverWait(dr, 15).until(lambda d: d.find_element_by_class_name("android.widget.EditText"))
            edts.send_keys(captcha)
            time.sleep(1)
            #检测注册成功进入下一步
            WebDriverWait(dr, 60).until(lambda d: d.find_element_by_id("com.wenba.bangbang:id/home_fragment_btn_camera"))
            return self.after_signup
        except Exception as e:
            print("error in getPhone,try_count:%s" % self.try_count)
            self.try_count += 1
            if self.try_count > 5:
                return self.exit
            dr.press_keycode(4)
            time.sleep(1)
            return self.signup

    def after_signup(self):
        dr = self.driver
        #修改个人信息
        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.wenba.bangbang:id/home_main_fragment_bar_setting")).click()
        time.sleep(1)
        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.wenba.bangbang:id/setting_avatar")).click()
        time.sleep(1)
        #修改性别
        if random.randint(0, 1):
            WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.wenba.bangbang:id/user_info_item_sex_layout")).click()
            time.sleep(1)
            WebDriverWait(dr, 20).until(lambda d: d.find_element_by_name(choice(["男生", "女生"]))).click()
            time.sleep(1)
        #修改昵称
        if random.randint(0, 1):
            WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.wenba.bangbang:id/user_info_item_nickname_layout")).click()
            time.sleep(1)
            edts = WebDriverWait(dr, 15).until(lambda d: d.find_element_by_class_name("android.widget.EditText"))
            edts.send_keys(self.get_filemessage("name.txt"))
            time.sleep(1)
            WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.wenba.bangbang:id/user_save")).click()
            time.sleep(1)
        #修改生日
        if random.randint(0, 1):
            WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.wenba.bangbang:id/user_info_item_brithday_layout")).click()
            time.sleep(1)
            btyear_up = WebDriverWait(dr, 10).until(lambda d: d.find_element_by_xpath("//android.widget.ImageButton[@content-desc='增大年份值']"))
            btyear_down = WebDriverWait(dr, 10).until(lambda d: d.find_element_by_xpath("//android.widget.ImageButton[@content-desc='减小年份值']"))
            btmon_up = WebDriverWait(dr, 10).until(lambda d: d.find_element_by_xpath("//android.widget.ImageButton[@content-desc='增大月份值']"))
            btday_up = WebDriverWait(dr, 10).until(lambda d: d.find_element_by_xpath("//android.widget.ImageButton[@content-desc='增大日期值']"))
            if random.randint(0, 1):
                #增加年份
                for x in range(random.randint(0, 4)):
                    btyear_up.click()
            else:
                #降低年份
                for x in range(random.randint(1, 4)):
                    btyear_down.click()
            #增加月份
            for x in range(random.randint(0, 10)):
                btmon_up.click()
            #增加日期
            for x in range(random.randint(0, 30)):
                btday_up.click()
            time.sleep(1)
            WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("android:id/button1")).click()
            time.sleep(1)
        #选择头像
        if random.randint(0, 4) == 0:
            WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.wenba.bangbang:id/user_info_item_header_img")).click()
            time.sleep(1)
            WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("从相册")).click()
            time.sleep(1)
            self.swipes(300, random.randint(800, 1000), 300, random.randint(300, 500), random.randint(3, 80))
            time.sleep(5)
            self.select_one_by_id("com.wenba.bangbang:id/photoselector_photo_thumbnail")
            time.sleep(1)
            WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.wenba.bangbang:id/comm_titlebar_menu_layout")).click()
            time.sleep(5)
        #绑定QQ号
        if random.randint(0, 1):
            WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.wenba.bangbang:id/user_info_item_bindqq_layout")).click()
            time.sleep(1)
            edts = WebDriverWait(dr, 15).until(lambda d: d.find_element_by_class_name("android.widget.EditText"))
            edts.send_keys(random.randint(10000000, 9999999999))
            time.sleep(1)
            WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.wenba.bangbang:id/user_bindqq_btn")).click()
            time.sleep(1)
            WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.wenba.bangbang:id/comm_dialog_right_btn")).click()
            time.sleep(1)
        #修改密码
        time.sleep(1)
        dr.swipe(300, 800, 300, 400)
        time.sleep(1)
        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.wenba.bangbang:id/user_info_item_changepassword_layout")).click()
        time.sleep(1)
        edts = WebDriverWait(dr, 15).until(lambda d: d.find_element_by_class_name("android.widget.EditText"))
        edts.send_keys(self.pwd)
        time.sleep(1)
        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.wenba.bangbang:id/user_password_edit_submit_btn")).click()
        time.sleep(1)
        #检测信息保存完毕跳转页面
        WebDriverWait(dr, 60).until(lambda d: d.find_element_by_id("com.wenba.bangbang:id/comm_titlebar_back")).click()
        #记录帐号密码
        try:
            with open('/sdcard/1/user%s.log' % self.appname_en, 'a') as f:
                f.write('\nimei:%s,%s,%s (time %s.%s  %s:%s:%s)' % (self.imei, self.phone, self.pwd, time.localtime().tm_mon, time.localtime().tm_mday, time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec))
        except:
            with open('D:/brush/slave/scripts/doc/user%s.log' % self.appname_en, 'a') as f:
                f.write('\nimei:%s,%s,%s (time %s.%s  %s:%s:%s)' % (self.imei, self.phone, self.pwd, time.localtime().tm_mon, time.localtime().tm_mday, time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec))
        time.sleep(1)
        return self.do

    def do(self):
        dr = self.driver
        try:
            while self.readnum:
                print("剩下阅读次数:%s" % self.readnum)
                random_read = random.randint(0, 4)
                if random_read == 0:
                    if self.ismenu1:
                        print("goto menu1")
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.wenba.bangbang:id/home_main_fragment_bar_search")).click()
                        time.sleep(5)
                        return self.menu1
                    return self.do
                elif random_read == 1:
                    if self.ismenu2:
                        print("goto menu2")
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.wenba.bangbang:id/home_main_fragment_bar_exercise")).click()
                        time.sleep(5)
                        return self.menu2
                    return self.do
                elif random_read == 2:
                    if self.ismenu3:
                        print("goto menu3")
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.wenba.bangbang:id/home_main_fragment_bar_more")).click()
                        time.sleep(5)
                        return self.menu3
                    return self.do
                else:
                    if self.ismenu4:
                        print("goto menu4")
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.wenba.bangbang:id/home_main_fragment_bar_setting")).click()
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
            WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.wenba.bangbang:id/home_fragment_sign")).click()
            time.sleep(5)
            dr.press_keycode(4)
            time.sleep(1)
            if random.randint(0, 4) == 0:
                for x in range(random.randint(1, 2)):
                    #选题
                    WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.wenba.bangbang:id/home_fragment_btn_camera")).click()
                    time.sleep(1)
                    WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.wenba.bangbang:id/camera_control_panel_album")).click()
                    time.sleep(1)
                    WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.wenba.bangbang:id/comm_titlebar_back")).click()
                    time.sleep(1)
                    WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.wenba.bangbang:id/photoselector_album_name")).click()
                    time.sleep(1)
                    self.swipes(300, random.randint(800, 1000), 300, random.randint(300, 500), random.randint(0, 5))
                    time.sleep(1)
                    self.select_one_by_id("com.wenba.bangbang:id/photoselector_photo_thumbnail")
                    time.sleep(5)
                    dr.swipe(300, 530, 300, random.randint(200, 900))
                    time.sleep(1)
                    WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.wenba.bangbang:id/camera_image_publish_edit_opt_submit")).click()
                    time.sleep(random.randint(10, 15))
                    self.swipes(300, random.randint(800, 1000), 300, random.randint(400, 600), random.randint(0, 2), 10, 15)
                    self.swipes(600, 800, 100, 800, random.randint(0, 3), 5, 10)
                    if random.randint(0, 1):
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.wenba.bangbang:id/comm_titlebar_menu2")).click()
                        time.sleep(1)
                    WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.wenba.bangbang:id/comm_titlebar_back")).click()
                    time.sleep(1)
            self.readnum -= 1
            self.ismenu1 = False
        except Exception as e:
            print("error in menu1")
            return self.exception_returnapp()
        return self.do

    def menu2(self):
        dr = self.driver
        try:
            self.ismenu2 = False
        except Exception as e:
            print("error in menu2")
            return self.exception_returnapp()
        return self.do

    def menu3(self):
        dr = self.driver
        try:
            #作文助手
            if random.randint(0, 1) == 0:
                WebDriverWait(dr, 15).until(lambda d: d.find_element_by_name("作文助手")).click()
                time.sleep(1)
                self.swipes(300, random.randint(800, 1000), 300, random.randint(400, 600), random.randint(1, 3), 2, 5)
                self.select_one_by_id("com.wenba.bangbang:id/comp_tv_cotent")
                self.swipes(300, random.randint(800, 1000), 300, random.randint(400, 600), random.randint(3, 5), 5, 10)
                dr.press_keycode(4)
                time.sleep(1)
                dr.press_keycode(4)
                time.sleep(1)
            #轻松学古文
            if random.randint(0, 1) == 0:
                WebDriverWait(dr, 15).until(lambda d: d.find_element_by_name("轻松学古文")).click()
                time.sleep(1)
                self.swipes(300, random.randint(800, 1000), 300, random.randint(400, 600), random.randint(0, 5), 2, 5)
                WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.wenba.bangbang:id/guwen_arc_switch_layout")).click()
                time.sleep(1)
                self.select_one_by_id("com.wenba.bangbang:id/guwen_arc_bg")
                time.sleep(1)
                self.swipes(300, random.randint(800, 1000), 300, random.randint(400, 600), random.randint(3, 5), 5, 10)
                dr.press_keycode(4)
                time.sleep(1)
                dr.press_keycode(4)
                time.sleep(1)
            #单词翻译
            if random.randint(0, 1) == 0:
                WebDriverWait(dr, 15).until(lambda d: d.find_element_by_name("单词翻译")).click()
                time.sleep(5)
                dr.press_keycode(4)
                time.sleep(1)
            #老师答疑
            if random.randint(0, 1) == 0:
                WebDriverWait(dr, 15).until(lambda d: d.find_element_by_name("老师答疑")).click()
                time.sleep(8)
                dr.press_keycode(4)
                time.sleep(1)
            #课间10分
            if random.randint(0, 1) == 0:
                WebDriverWait(dr, 15).until(lambda d: d.find_element_by_name("课间10分")).click()
                time.sleep(5)
                dr.tap(random.randint(100, 600), random.randint(300, 1000))
                time.sleep(5)
                self.swipes(300, random.randint(800, 1000), 300, random.randint(400, 600), random.randint(1, 3), 5, 10)
                dr.press_keycode(4)
                time.sleep(1)
                dr.press_keycode(4)
                time.sleep(1)
            self.readnum -= 1
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

    def swipes(self, x1, y1, x2, y2, swipe_num=1, swipe_time_a=1, swipe_time_b=1):
        dr = self.driver
        print("swipenum:%s" % swipe_num)
        for x in range(swipe_num):
            dr.swipe(x1, y1, x2, y2)
            time.sleep(random.randint(swipe_time_a, swipe_time_b))

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
        try:
            WebDriverWait(dr, 2).until(lambda d: d.find_element_by_id("com.wenba.bangbang:id/comm_dialog_left_btn")).click()
        except TimeoutException:
            pass
        time.sleep(5)
        return self.do


class Machinex2(Machine):
    def __init__(self, driver):
        super(Machinex2, self).__init__(self.initdata)
        self.driver = driver
        self.appname = "学霸君"       #app名字
        self.appname_en = "xueba"     #记录文件用缩写英文名
        self.imei = None        #imei
        self.remain_day = None      #留存天数

    def initdata(self):
        self.begintime = None
        self.endstime = None
        self.try_count = 0      #初始化出错尝试次数
        self.readnum = random.randint(2, 2)     #初始化阅读次数
        #初始化阅读菜单
        self.ismenu1 = True
        self.ismenu2 = True
        self.ismenu3 = True
        self.ismenu4 = True

        return self.begin

    def begin(self):
        dr = self.driver
        dr.press_keycode(3)
        time.sleep(1)
        WebDriverWait(dr, 30).until(lambda d: d.find_element_by_name(self.appname)).click()
        time.sleep(10)
        #检测已进入app
        # WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("com.wenba.bangbang:id/login_guide_submit_btn"))
        # self.begintime = "开始:%s:%s:%s" % (time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec)
        # time.sleep(1)
        try:
            with open('/sdcard/1/user%s.log' % self.appname_en, 'r') as f:
                selectuser = f.read()
        except:
            with open('D:/brush/slave/scripts/doc/user%s.log' % self.appname_en, 'r') as f:
                selectuser = f.read()
        user = re.search(r'imei:%s,(\d+)' % self.imei, selectuser)
        pwd = re.search(r'imei:%s,\d+,([0-9a-z]+)' % self.imei, selectuser)
        if user and pwd:
            return self.login
        time.sleep(random.randint(5, 10))
        return self.ends

    def login(self):
        # dr = self.driver
        # try:
        #     with open('/sdcard/1/user%s.log' % self.appname_en, 'r') as f:
        #         selectuser = f.read()
        # except:
        #     with open('D:/brush/slave/scripts/doc/user%s.log' % self.appname_en, 'r') as f:
        #         selectuser = f.read()
        # user = re.search(r'imei:%s,(\d+)' % self.imei, selectuser)
        # pwd = re.search(r'imei:%s,\d+,([0-9a-z]+)' % self.imei, selectuser)
        # if user and pwd:
        #     WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.wenba.bangbang:id/login_guide_submit_btn")).click()
        #     time.sleep(1)
        #     edit = WebDriverWait(dr, 15).until(lambda d: d.find_element_by_class_name("android.widget.EditText"))
        #     edit.send_keys(str(user.group(1)))
        #     time.sleep(1)
        #     WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.wenba.bangbang:id/login_enter_submit_tv")).click()
        #     time.sleep(1)
        #     edit = WebDriverWait(dr, 15).until(lambda d: d.find_element_by_class_name("android.widget.EditText"))
        #     edit.send_keys(str(pwd.group(1)))
        #     time.sleep(1)
        #     WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.wenba.bangbang:id/login_submit_btn")).click()
        #     time.sleep(5)
        #     WebDriverWait(dr, 60).until(lambda d: d.find_element_by_id("com.wenba.bangbang:id/home_fragment_btn_camera"))
        # time.sleep(5)
        return self.do

    def do(self):
        dr = self.driver
        try:
            while self.readnum:
                print("剩下阅读次数:%s" % self.readnum)
                random_read = random.randint(0, 4)
                if random_read == 0:
                    if self.ismenu1:
                        print("goto menu1")
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.wenba.bangbang:id/home_main_fragment_bar_search")).click()
                        time.sleep(5)
                        return self.menu1
                    return self.do
                elif random_read == 1:
                    if self.ismenu2:
                        print("goto menu2")
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.wenba.bangbang:id/home_main_fragment_bar_exercise")).click()
                        time.sleep(5)
                        return self.menu2
                    return self.do
                elif random_read == 2:
                    if self.ismenu3:
                        print("goto menu3")
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.wenba.bangbang:id/home_main_fragment_bar_more")).click()
                        time.sleep(5)
                        return self.menu3
                    return self.do
                else:
                    if self.ismenu4:
                        print("goto menu4")
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.wenba.bangbang:id/home_main_fragment_bar_setting")).click()
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
            WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.wenba.bangbang:id/home_fragment_sign")).click()
            time.sleep(5)
            dr.press_keycode(4)
            time.sleep(1)
            if random.randint(0, 4) == 0:
                for x in range(random.randint(1, 2)):
                    #选题
                    WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.wenba.bangbang:id/home_fragment_btn_camera")).click()
                    time.sleep(1)
                    WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.wenba.bangbang:id/camera_control_panel_album")).click()
                    time.sleep(1)
                    WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.wenba.bangbang:id/comm_titlebar_back")).click()
                    time.sleep(1)
                    WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.wenba.bangbang:id/photoselector_album_name")).click()
                    time.sleep(1)
                    self.swipes(300, random.randint(800, 1000), 300, random.randint(300, 500), random.randint(0, 5))
                    time.sleep(1)
                    self.select_one_by_id("com.wenba.bangbang:id/photoselector_photo_thumbnail")
                    time.sleep(5)
                    dr.swipe(300, 530, 300, random.randint(200, 900))
                    time.sleep(1)
                    WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.wenba.bangbang:id/camera_image_publish_edit_opt_submit")).click()
                    time.sleep(random.randint(10, 15))
                    self.swipes(300, random.randint(800, 1000), 300, random.randint(400, 600), random.randint(0, 2), 10, 15)
                    self.swipes(600, 800, 100, 800, random.randint(0, 3), 5, 10)
                    if random.randint(0, 1):
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.wenba.bangbang:id/comm_titlebar_menu2")).click()
                        time.sleep(1)
                    WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.wenba.bangbang:id/comm_titlebar_back")).click()
                    time.sleep(1)
            self.readnum -= 1
            self.ismenu1 = False
        except Exception as e:
            print("error in menu1")
            return self.exception_returnapp()
        return self.do

    def menu2(self):
        dr = self.driver
        try:
            self.ismenu2 = False
        except Exception as e:
            print("error in menu2")
            return self.exception_returnapp()
        return self.do

    def menu3(self):
        dr = self.driver
        try:
            #作文助手
            if random.randint(0, 2) == 0:
                WebDriverWait(dr, 15).until(lambda d: d.find_element_by_name("作文助手")).click()
                time.sleep(1)
                self.swipes(300, random.randint(800, 1000), 300, random.randint(400, 600), random.randint(1, 3), 2, 5)
                self.select_one_by_id("com.wenba.bangbang:id/comp_tv_cotent")
                self.swipes(300, random.randint(800, 1000), 300, random.randint(400, 600), random.randint(3, 5), 5, 10)
                dr.press_keycode(4)
                time.sleep(1)
                dr.press_keycode(4)
                time.sleep(1)
            #轻松学古文
            if random.randint(0, 2) == 0:
                WebDriverWait(dr, 15).until(lambda d: d.find_element_by_name("轻松学古文")).click()
                time.sleep(1)
                self.swipes(300, random.randint(800, 1000), 300, random.randint(400, 600), random.randint(0, 5), 2, 5)
                WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.wenba.bangbang:id/guwen_arc_switch_layout")).click()
                time.sleep(1)
                self.select_one_by_id("com.wenba.bangbang:id/guwen_arc_bg")
                time.sleep(1)
                self.swipes(300, random.randint(800, 1000), 300, random.randint(400, 600), random.randint(3, 5), 5, 10)
                dr.press_keycode(4)
                time.sleep(1)
                dr.press_keycode(4)
                time.sleep(1)
            #单词翻译
            if random.randint(0, 2) == 0:
                WebDriverWait(dr, 15).until(lambda d: d.find_element_by_name("单词翻译")).click()
                time.sleep(5)
                dr.press_keycode(4)
                time.sleep(1)
            #老师答疑
            if random.randint(0, 2) == 0:
                WebDriverWait(dr, 15).until(lambda d: d.find_element_by_name("老师答疑")).click()
                time.sleep(8)
                dr.press_keycode(4)
                time.sleep(1)
            #课间10分
            if random.randint(0, 2) == 0:
                WebDriverWait(dr, 15).until(lambda d: d.find_element_by_name("课间10分")).click()
                time.sleep(5)
                dr.tap(random.randint(100, 600), random.randint(300, 1000))
                time.sleep(5)
                self.swipes(300, random.randint(800, 1000), 300, random.randint(400, 600), random.randint(1, 3), 5, 10)
                dr.press_keycode(4)
                time.sleep(1)
                dr.press_keycode(4)
                time.sleep(1)
            self.readnum -= 1
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

    def ends(self):
        #记录时间
        self.endstime = "结束:%s:%s:%s" % (time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec)
        print(self.begintime)
        print(self.endstime)
        time.sleep(2)
        try:
            with open('/sdcard/1/time%s2.log' % self.appname_en, 'a') as f:
                f.write('\n留存%s  %s.%s, %s, %s' % (self.remain_day, time.localtime().tm_mon, time.localtime().tm_mday, self.begintime, self.endstime))
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

    def swipes(self, x1, y1, x2, y2, swipe_num=1, swipe_time_a=1, swipe_time_b=1):
        dr = self.driver
        print("swipenum:%s" % swipe_num)
        for x in range(swipe_num):
            dr.swipe(x1, y1, x2, y2)
            time.sleep(random.randint(swipe_time_a, swipe_time_b))

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
        try:
            WebDriverWait(dr, 2).until(lambda d: d.find_element_by_id("com.wenba.bangbang:id/comm_dialog_left_btn")).click()
        except TimeoutException:
            pass
        time.sleep(5)
        return self.do



if __name__ == "__main__":
    wd = webdriver.Remote()
    time.sleep(2)

