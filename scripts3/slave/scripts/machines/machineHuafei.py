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


class Machinex(Machine):
    def __init__(self, driver, code_platform, fm_uname, fm_pwd):
        super(Machinex, self).__init__(self.initdata)
        self.driver = driver
        self.code_platform = code_platform      #接码平台
        self.code_user = fm_uname       #接码平台帐号
        self.code_pwd = fm_pwd      #接码平台密码
        self.appname = "掌上充值"       #app名字
        self.appname_en = "huafei"     #记录文件用缩写英文名
        self.imei = None
        self.runnum = None        #记录运行次数

    def initdata(self):
        self.phone = None
        self.pwd = None
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
        WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("xmgwa.xzxjtwg.nuktvi:id/relative"))
        self.begintime = "开始:%s:%s:%s" % (time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec)
        time.sleep(1)
        return self.do

    def do(self):
        dr = self.driver
        try:
            liphone = ['130', '131', '132', '155', '156', '186', '185',
                       '134', '135', '136', '137', '138', '139', '150', '151', '152', '157', '158', '159', '182', '183', '188', '187',
                       '133', '153', '180', '181', '189']
            phone = choice(liphone) + str(random.randint(10000000, 99999999))
            if random.randint(0, 1):
                WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("xmgwa.xzxjtwg.nuktvi:id/mianze")).click()
                time.sleep(random.randint(5, 15))
                WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("xmgwa.xzxjtwg.nuktvi:id/button1")).click()
                time.sleep(1)
            if random.randint(0, 1):
                WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("xmgwa.xzxjtwg.nuktvi:id/imageView1")).click()
                time.sleep(random.randint(5, 15))
                WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("xmgwa.xzxjtwg.nuktvi:id/imageView1")).click()
                time.sleep(1)
            if random.randint(0, 1):
                edts = WebDriverWait(dr, 15).until(lambda d: d.find_element_by_class_name("android.widget.EditText"))
                #输入手机号码
                edts.send_keys(phone)
                time.sleep(random.randint(10, 20))
                limoney = ["xmgwa.xzxjtwg.nuktvi:id/num10", "xmgwa.xzxjtwg.nuktvi:id/num20", "xmgwa.xzxjtwg.nuktvi:id/num30",
                           "xmgwa.xzxjtwg.nuktvi:id/num50", "xmgwa.xzxjtwg.nuktvi:id/num100", "xmgwa.xzxjtwg.nuktvi:id/num200",
                           "xmgwa.xzxjtwg.nuktvi:id/num300", "xmgwa.xzxjtwg.nuktvi:id/num500"]
                WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id(choice(limoney)))
                time.sleep(random.randint(10, 30))
                dr.press_keycode(4)
                time.sleep(1)

        except TimeoutException:
            print("查找菜单出错")
            return self.exception_returnapp()
        print("阅览完毕")
        return self.ends

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
        self.appname = "掌上充值"       #app名字
        self.appname_en = "huafei"     #记录文件用缩写英文名
        self.imei = None        #imei
        self.remain_day = None      #留存天数

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
        WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("xmgwa.xzxjtwg.nuktvi:id/relative"))
        self.begintime = "开始:%s:%s:%s" % (time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec)
        time.sleep(1)
        return self.do

    def do(self):
        dr = self.driver
        try:
            liphone = ['130', '131', '132', '155', '156', '186', '185',
                       '134', '135', '136', '137', '138', '139', '150', '151', '152', '157', '158', '159', '182', '183', '188', '187',
                       '133', '153', '180', '181', '189']
            phone = choice(liphone) + str(random.randint(10000000, 90000000))
            if random.randint(0, 1):
                WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("xmgwa.xzxjtwg.nuktvi:id/mianze")).click()
                time.sleep(random.randint(5, 15))
                WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("xmgwa.xzxjtwg.nuktvi:id/button1")).click()
                time.sleep(1)
            if random.randint(0, 1):
                WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("xmgwa.xzxjtwg.nuktvi:id/imageView1")).click()
                time.sleep(random.randint(5, 15))
                WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("xmgwa.xzxjtwg.nuktvi:id/imageView1")).click()
                time.sleep(1)
            if random.randint(0, 1):
                edts = WebDriverWait(dr, 15).until(lambda d: d.find_element_by_class_name("android.widget.EditText"))
                #输入手机号码
                edts.send_keys(phone)
                time.sleep(random.randint(10, 20))
                limoney = ["xmgwa.xzxjtwg.nuktvi:id/num10", "xmgwa.xzxjtwg.nuktvi:id/num20", "xmgwa.xzxjtwg.nuktvi:id/num30",
                           "xmgwa.xzxjtwg.nuktvi:id/num50", "xmgwa.xzxjtwg.nuktvi:id/num100", "xmgwa.xzxjtwg.nuktvi:id/num200",
                           "xmgwa.xzxjtwg.nuktvi:id/num300", "xmgwa.xzxjtwg.nuktvi:id/num500"]
                WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id(choice(limoney)))
                time.sleep(random.randint(10, 30))
                dr.press_keycode(4)
                time.sleep(1)

        except TimeoutException:
            print("查找菜单出错")
            return self.exception_returnapp()
        print("阅览完毕")
        return self.ends

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

