#! -*- coding=utf-8 -*-
import time
import logging
import random
import re
from machines.StateMachine import Machine
from appium4droid import webdriver
from appium4droid.common.exceptions import *
from appium4droid.support.ui import WebDriverWait
from feimaSDK import Feima
from yamaSDK import Yama
from shenhuaSDK import Shenhua
from random import choice


class Machineyouxun(Machine):
    def __init__(self, driver, getcaptch, fm_uname, fm_pwd, imei=None, runnum=0):
        super(Machineyouxun, self).__init__(self.begin)
        self.driver = driver
        self.jiema = getcaptch
        self.feima = Feima(fm_uname, fm_pwd)
        self.yama = Yama(fm_uname, fm_pwd)
        self.shenhua = Shenhua(fm_uname, fm_pwd)
        self.try_count = 0
        self.readnum = random.randint(2, 2)
        self.phone = None
        self.pwd = None
        self.imei = imei
        self.begintime = None
        self.endstime = None
        self.islike = True
        self.ismenu1 = True
        self.ismenu2 = True
        self.ismenu3 = True
        self.ismenu4 = True
        self.ismenu5 = True
        self.runnum = runnum


    def begin(self):
        dr = self.driver
        self.try_count = 0
        self.readnum = random.randint(2, 2)
        self.ismenu1 = True
        self.ismenu2 = True
        self.ismenu3 = True
        self.ismenu4 = True
        self.ismenu5 = True
        dr.press_keycode(3)
        time.sleep(1)
        WebDriverWait(dr, 30).until(lambda d: d.find_element_by_name("友寻交友")).click()
        time.sleep(10)
        return self.newenter

    def newenter(self):
        dr = self.driver
        WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("com.iyouxun:id/dotBox"))
        self.begintime = "开始:%s:%s:%s" % (time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec)
        time.sleep(1)
        #新开软件翻页
        for x in range(4):
            dr.swipe(600, 300, 200, 300)
            time.sleep(2)
        # time.sleep(5)
        if self.jiema == 'feima':
            return self.login_feima
        elif self.jiema == 'yama':
            return self.login_yama
        else:
            return self.login_shenhua

    def login_feima(self):
        print("login......")
        try:
            self.feima.login()
        except Exception as e:
            self.try_count += 1
            if self.try_count > 5:
                self.try_count = 0
                return self.exit
            return self.login_feima
        return self.signup

    def login_yama(self):
        print("login......")
        try:
            self.yama.login()
        except Exception as e:
            self.try_count += 1
            if self.try_count > 5:
                self.try_count = 0
                return self.exit
            return self.login_yama
        return self.signup

    def login_shenhua(self):
        print("login......")
        try:
            self.shenhua.login()
        except Exception as e:
            self.try_count += 1
            if self.try_count > 5:
                self.try_count = 0
                return self.exit
            return self.login_shenhua
        return self.signup

    def signup(self):
        dr = self.driver
        signpwdli = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
                     "1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
                     "a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
                     "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
                     "u", "v", "w", "x", "y", "z"]
        self.pwd = choice(signpwdli)+choice(signpwdli)+choice(signpwdli)+choice(signpwdli)+choice(signpwdli)+choice(signpwdli)
        time.sleep(1)
        try:
            WebDriverWait(dr, 10).until(lambda d: d.find_element_by_xpath("//android.widget.ImageButton[@resource-id='com.iyouxun:id/guide_btn_register']")).click()
            time.sleep(1)
            edts = WebDriverWait(dr, 15).until(lambda d: d.find_elements_by_class_name("android.widget.EditText"))
            if self.jiema == 'feima':
                self.phone = self.feima.getPhone(6863)[0]
            elif self.jiema == 'yama':
                self.phone = self.yama.getPhone(3625)[0]
            else:
                self.phone = self.shenhua.getPhone(7823)[0]
            edts[0].send_keys(self.phone)
            time.sleep(1)
            WebDriverWait(dr, 10).until(lambda d: d.find_element_by_xpath("//android.widget.Button[@resource-id='com.iyouxun:id/register_btn_get_security_code']")).click()
            time.sleep(5)
            edts[2].send_keys(self.pwd)
            time.sleep(1)
            #【友寻】您的临时验证码为：302855，有效时间为30分钟。
            if self.jiema == 'feima':
                captcha = self.feima.waitForMessage(r'验证码为：(\d+)', self.phone)
            elif self.jiema == 'yama':
                captcha = self.yama.waitForMessage(r'验证码为：(\d+)', self.phone)
            else:
                captcha = self.shenhua.waitForMessage(r'验证码为：(\d+)', 7823, self.phone)
            if captcha is None:
                print("getMessage failed")
                self.try_count += 1
                if self.try_count > 5:
                    self.try_count = 0
                    return self.exit
                time.sleep(1)
                dr.press_keycode(4)
                time.sleep(1)
                return self.signup
            edts[1].send_keys(captcha)
            time.sleep(1)
            WebDriverWait(dr, 10).until(lambda d: d.find_element_by_xpath("//android.widget.Button[@resource-id='com.iyouxun:id/register_btn_complete']")).click()
            time.sleep(1)
            WebDriverWait(dr, 60).until(lambda d: d.find_element_by_xpath("//android.widget.Button[@resource-id='com.iyouxun:id/register_user_info_btn_save']"))
            return self.after_signup
        except Exception as e:
            print("error in getPhone")
            self.try_count += 1
            if self.try_count > 5:
                self.try_count = 0
                return self.exit
            dr.press_keycode(4)
            time.sleep(2)
            return self.signup

    def after_signup(self):
        dr = self.driver
        #选择性别
        WebDriverWait(dr, 20).until(lambda d: d.find_element_by_xpath("//android.widget.Button[@resource-id='com.iyouxun:id/supplement_btn_%s']" % choice(["woman", "man"]))).click()
        time.sleep(1)
        #输入昵称
        try:
            with open("/sdcard/1/name.txt", 'r', encoding='utf-8') as f:
                 strname = f.readlines()
        except:
            with open("D:/brush/slave/scripts/doc/name.txt", 'r', encoding='utf-8') as f:
                 strname = f.readlines()
        time.sleep(2)
        edts = WebDriverWait(dr, 15).until(lambda d: d.find_element_by_class_name("android.widget.EditText"))
        edts.send_keys(strname[random.randint(0, strname.__len__()-1)].strip())
        time.sleep(1)
        #选择情感状态
        WebDriverWait(dr, 20).until(lambda d: d.find_element_by_xpath("//android.widget.Button[@resource-id='com.iyouxun:id/supplement_btn_emotional']")).click()
        time.sleep(1)
        emotional = WebDriverWait(dr, 20).until(lambda d: d.find_elements_by_xpath("//android.widget.TextView[@resource-id='com.iyouxun:id/emotional_item_text']"))
        emotional[random.randint(0, emotional.__len__()-1)].click()
        time.sleep(1)
        WebDriverWait(dr, 20).until(lambda d: d.find_element_by_xpath("//android.widget.Button[@resource-id='com.iyouxun:id/titleLeftButton']")).click()
        time.sleep(5)
        for x in range(3):
            WebDriverWait(dr, 20).until(lambda d: d.find_element_by_xpath("//android.widget.Button[@resource-id='com.iyouxun:id/register_user_info_btn_save']")).click()
            time.sleep(10)
            try:
                WebDriverWait(dr, 50).until(lambda d: d.find_element_by_xpath("//android.widget.ImageView[@resource-id='com.iyouxun:id/dialog_guide_layer']"))
                break
            except TimeoutException:
                dr.press_keycode(4)
                time.sleep(1)
            if x == 2:
                return self.exit
        for x in range(3):
            WebDriverWait(dr, 20).until(lambda d: d.find_element_by_xpath("//android.widget.ImageView[@resource-id='com.iyouxun:id/dialog_guide_layer']")).click()
            time.sleep(2)
        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_xpath("//android.widget.Button[@resource-id='com.iyouxun:id/titleLeftButton']")).click()
        time.sleep(1)
        try:
            WebDriverWait(dr, 10).until(lambda d: d.find_element_by_name("你可能错过了好友的动态"))
            dr.press_keycode(4)
            time.sleep(1)
        except TimeoutException:
            pass
        #记录帐号密码
        try:
            with open('/sdcard/1/useryx.log', 'a') as f:
                f.write('\nimei:%s,%s,%s (time %s:%s:%s)' % (self.imei, self.phone, self.pwd, time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec))
        except:
            with open('D:/brush/slave/scripts/doc/useryx.log', 'a') as f:
                f.write('\nimei:%s,%s,%s (time %s:%s:%s)' % (self.imei, self.phone, self.pwd, time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec))
        #选择头像
        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.iyouxun:id/global_menu_button_center")).click()
        time.sleep(1)
        WebDriverWait(dr, 20).until(lambda d: d.find_element_by_id("com.iyouxun:id/profile_avatar_change")).click()
        time.sleep(1)
        WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("从相册选择")).click()
        time.sleep(1)
        WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("文件管理")).click()
        time.sleep(1)
        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_name("1")).click()
        time.sleep(1)
        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_name("1touxiang")).click()
        time.sleep(1)
        for x in range(random.randint(0, 80)):
            dr.swipe(300, random.randint(800, 1000), 300, random.randint(300, 500))
            time.sleep(1)
        time.sleep(5)
        imghead = WebDriverWait(dr, 15).until(lambda d: d.find_elements_by_id("com.android.fileexplorer:id/file_image"))
        imghead[random.randint(0, imghead.__len__()-1)].click()
        time.sleep(1)
        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_name("应用")).click()
        time.sleep(5)
        WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("com.iyouxun:id/profile_avatar_change"))
        return self.do

    def do(self):
        dr = self.driver
        try:
            while self.readnum:
                print("剩下阅读次数:%s" % self.readnum)
                rdread = random.randint(0, 4)
                if rdread == 0:
                    if self.ismenu1:
                        print("熟人圈")
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_xpath("//android.widget.ImageView[@resource-id='com.iyouxun:id/global_menu_button_news']")).click()
                        time.sleep(5)
                        return self.menu1
                    return self.do
                elif rdread == 1:
                    if self.ismenu2:
                        print("消息")
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_xpath("//android.widget.ImageView[@resource-id='com.iyouxun:id/global_menu_button_msg']")).click()
                        time.sleep(5)
                        return self.menu2
                    return self.do
                elif rdread == 2:
                    if self.ismenu3:
                        print("发动态爆料")
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_xpath("//android.widget.ImageView[@resource-id='com.iyouxun:id/global_menu_button_add']")).click()
                        time.sleep(5)
                        return self.menu3
                    return self.do
                elif rdread == 3:
                    if self.ismenu4:
                        print("发现")
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_xpath("//android.widget.ImageView[@resource-id='com.iyouxun:id/global_menu_button_find']")).click()
                        time.sleep(5)
                        return self.menu4
                    return self.do
                else:
                    if self.ismenu5:
                        print("我")
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_xpath("//android.widget.ImageView[@resource-id='com.iyouxun:id/global_menu_button_center']")).click()
                        time.sleep(5)
                        return self.menu5
                    return self.do
        except TimeoutException:
            print("查找菜单出错")
            self.try_count += 1
            if self.try_count > 5:
                self.try_count = 0
                return self.exit
            dr.press_keycode(4)
            time.sleep(1)
            dr.press_keycode(4)
            time.sleep(1)
            dr.press_keycode(82)
            time.sleep(2)
            try:
                WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("友寻交友")).click()
            except TimeoutException:
                dr.press_keycode(4)
            time.sleep(5)
            return self.do
        print("阅览完毕")
        return self.ends

    #熟人圈
    def menu1(self):
        dr = self.driver
        try:
            if random.randint(0, 2):
                #爆料
                WebDriverWait(dr, 15).until(lambda d: d.find_element_by_xpath("//android.widget.TextView[@resource-id='com.iyouxun:id/news_main_tab3']")).click()
                time.sleep(5)
                #随机滑动
                for x in range(random.randint(2, 3)):
                    dr.swipe(random.randint(200, 400), random.randint(800, 1000), random.randint(200, 400), random.randint(400, 600))
                    time.sleep(5)
                #点赞
                if random.randint(0, 1):
                    like = WebDriverWait(dr, 15).until(lambda d: d.find_elements_by_xpath("//android.widget.Button[@resource-id='com.iyouxun:id/item_disclose_main_praisecount']"))
                    like[random.randint(0, like.__len__()-1)].click()
                    time.sleep(1)
                #评论
                if random.randint(0, 2):
                    for x in range(random.randint(2, 3)):
                        dr.swipe(random.randint(200, 400), random.randint(800, 1000), random.randint(200, 400), random.randint(400, 600))
                        time.sleep(5)
                else:
                    comment = WebDriverWait(dr, 15).until(lambda d: d.find_elements_by_xpath("//android.widget.Button[@resource-id='com.iyouxun:id/item_disclose_main_commentcount']"))
                    comment[random.randint(0, comment.__len__()-1)].click()
                    time.sleep(5)
                    for x in range(random.randint(2, 3)):
                        dr.swipe(300, random.randint(700, 1000), 300, random.randint(200, 500))
                        time.sleep(5)
                    pltext = None
                    try:
                        pltext = WebDriverWait(dr, 15).until(lambda d: d.find_elements_by_xpath("//android.widget.TextView[@resource-id='com.iyouxun:id/item_broke_news_detail_comment_comment']"))
                    except TimeoutException:
                        pass
                    # WebDriverWait(dr, 15).until(lambda d: d.find_element_by_xpath("//android.widget.LinearLayout[@resource-id='com.yc.ai:id/bottom_comment_img']")).click()
                    # time.sleep(3)
                    edts = WebDriverWait(dr, 5).until(lambda d: d.find_element_by_class_name('android.widget.EditText'))
                    if pltext:
                        if random.randint(0, 1):
                            edts.send_keys(pltext[random.randint(0, pltext.__len__()-1)].text)
                        else:
                            edts.send_keys(choice(["路过", "不错啊", "可以的", "赞", "赞一个", "必须赞啊", "大赞", "好", "赞!", "支持", "厉害", "好看", "漂亮", "交个朋友吧", "nice"]))
                    else:
                        edts.send_keys(choice(["路过", "不错啊", "可以的", "赞", "赞一个", "必须赞啊", "大赞", "好", "赞!", "支持", "厉害", "好看", "漂亮", "交个朋友吧", "nice"]))
                    time.sleep(1)
                    WebDriverWait(dr, 15).until(lambda d: d.find_element_by_xpath("//android.widget.Button[@resource-id='com.iyouxun:id/btn_setting_msg']")).click()
                    time.sleep(5)
                    dr.press_keycode(4)
                    time.sleep(1)
            else:
                #动态
                WebDriverWait(dr, 15).until(lambda d: d.find_element_by_xpath("//android.widget.TextView[@resource-id='com.iyouxun:id/news_main_tab2']")).click()
                time.sleep(1)
                WebDriverWait(dr, 15).until(lambda d: d.find_element_by_xpath("//android.widget.Button[@resource-id='com.iyouxun:id/titleRightButton']")).click()
                time.sleep(1)
                try:
                    with open("/sdcard/1/duanzi.txt", 'r', encoding='utf-8') as f:
                        strduanzi = f.readlines()
                except:
                    with open("D:/brush/slave/scripts/doc/duanzi.txt", 'r', encoding='utf-8') as f:
                        strduanzi = f.readlines()
                edts = WebDriverWait(dr, 5).until(lambda d: d.find_element_by_class_name("android.widget.EditText"))
                edts.send_keys(strduanzi[random.randint(0, strduanzi.__len__()-1)].strip())
                time.sleep(5)
                #随机选择是否添加图片
                if random.randint(0, 1):
                    WebDriverWait(dr, 15).until(lambda d: d.find_element_by_xpath("//android.widget.ImageButton[@resource-id='com.iyouxun:id/photoLayerButton']")).click()
                    time.sleep(1)
                    for x in range(random.randint(1, 1)):
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_xpath("//android.widget.ImageButton[@resource-id='com.iyouxun:id/addNewsSelectAlbum']")).click()
                        time.sleep(1)
                        WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("文件管理")).click()
                        time.sleep(1)
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_name("1")).click()
                        time.sleep(1)
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_name("1xiangce")).click()
                        time.sleep(1)
                        for i in range(random.randint(0, 50)):
                            dr.swipe(300, random.randint(800, 1000), 300, random.randint(300, 500))
                            time.sleep(1)
                        time.sleep(5)
                        imghead = WebDriverWait(dr, 15).until(lambda d: d.find_elements_by_id("com.android.fileexplorer:id/file_image"))
                        imghead[random.randint(0, imghead.__len__()-1)].click()
                        time.sleep(5)
                    if random.randint(0, 1):
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_class_name("android.widget.CheckBox")).click()
                        time.sleep(1)
                WebDriverWait(dr, 15).until(lambda d: d.find_element_by_xpath("//android.widget.Button[@resource-id='com.iyouxun:id/titleRightButton']")).click()
                time.sleep(5)
                for x in range(random.randint(1, 2)):
                    dr.swipe(random.randint(200, 400), random.randint(400, 1000), random.randint(200, 400), random.randint(400, 1000))
                    time.sleep(5)
            self.readnum -= 1
            self.ismenu1 = False
        except Exception as e:
            print("查看熟人圈出错")
            dr.press_keycode(4)
            time.sleep(1)
            dr.press_keycode(4)
            time.sleep(1)
            dr.press_keycode(82)
            time.sleep(2)
            try:
                WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("友寻交友")).click()
            except TimeoutException:
                dr.press_keycode(4)
            time.sleep(5)
        return self.do

    #消息
    def menu2(self):
        dr = self.driver
        try:
            WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name(choice(["我的群组", "系统消息", "建立群组", "友寻小秘书"]))).click()
            time.sleep(1)
            try:
                WebDriverWait(dr, 5).until(lambda d: d.find_element_by_xpath("//android.widget.TextView[@resource-id='com.iyouxun:id/system_message_btn_%s']" % choice(["agree", "refuse"]))).click()
                time.sleep(2)
            except:
                pass
            self.ismenu2 = False
            dr.press_keycode(4)
            time.sleep(5)
        except Exception as e:
            print("查看消息出错")
            dr.press_keycode(4)
            time.sleep(1)
            dr.press_keycode(4)
            time.sleep(1)
            dr.press_keycode(82)
            time.sleep(2)
            try:
                WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("友寻交友")).click()
            except TimeoutException:
                dr.press_keycode(4)
                time.sleep(1)
        return self.do

    #发动态爆料
    def menu3(self):
        dr = self.driver
        try:
            if random.randint(0, 1):
                #爆料
                WebDriverWait(dr, 15).until(lambda d: d.find_element_by_xpath("//android.widget.TextView[@resource-id='com.iyouxun:id/main_add_create_broke_news']")).click()
                time.sleep(1)
                #添加图片
                for x in range(random.randint(1, 1)):
                    try:
                        WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("可以上传9张照片")).click()
                    except TimeoutException:
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_xpath("//android.widget.ImageView[@resource-id='com.iyouxun:id/add_photo_btn_add']")).click()
                    time.sleep(1)
                    WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("从相册选择")).click()
                    time.sleep(1)
                    WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("文件管理")).click()
                    time.sleep(1)
                    WebDriverWait(dr, 15).until(lambda d: d.find_element_by_name("1")).click()
                    time.sleep(1)
                    WebDriverWait(dr, 15).until(lambda d: d.find_element_by_name("1xiangce")).click()
                    time.sleep(1)
                    for i in range(random.randint(0, 50)):
                        dr.swipe(300, random.randint(800, 1000), 300, random.randint(300, 500))
                        time.sleep(1)
                    time.sleep(5)
                    imghead = WebDriverWait(dr, 15).until(lambda d: d.find_elements_by_id("com.android.fileexplorer:id/file_image"))
                    imghead[random.randint(0, imghead.__len__()-1)].click()
                    time.sleep(5)
                #添加标签
                WebDriverWait(dr, 15).until(lambda d: d.find_element_by_xpath("//android.widget.TextView[@resource-id='com.iyouxun:id/create_broke_the_news_add_tag']")).click()
                time.sleep(1)
                for x in range(random.randint(1, 3)):
                    biaoqian = WebDriverWait(dr, 15).until(lambda d: d.find_elements_by_xpath("//android.widget.ImageView[@resource-id='com.iyouxun:id/item_tag_add']"))
                    biaoqian[random.randint(0, biaoqian.__len__()-1)].click()
                    time.sleep(1)
                    if random.randint(0, 1):
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_name("换一批")).click()
                        time.sleep(1)
                dr.press_keycode(4)
                time.sleep(1)
                #介绍
                try:
                    with open("/sdcard/1/duanzi2.txt", 'r', encoding='utf-8') as f:
                        strduanzi = f.readlines()
                except:
                    with open("D:/brush/slave/scripts/doc/duanzi2.txt", 'r', encoding='utf-8') as f:
                        strduanzi = f.readlines()
                edts = WebDriverWait(dr, 5).until(lambda d: d.find_element_by_class_name("android.widget.EditText"))
                edts.send_keys(strduanzi[random.randint(0, strduanzi.__len__()-1)].strip())
                time.sleep(1)
                #发布
                WebDriverWait(dr, 15).until(lambda d: d.find_element_by_xpath("//android.widget.Button[@resource-id='com.iyouxun:id/titleRightButton']")).click()
                time.sleep(5)
            else:
                #动态
                WebDriverWait(dr, 15).until(lambda d: d.find_element_by_xpath("//android.widget.TextView[@resource-id='com.iyouxun:id/main_add_create_news']")).click()
                time.sleep(1)
                # WebDriverWait(dr, 15).until(lambda d: d.find_element_by_xpath("//android.widget.Button[@resource-id='com.iyouxun:id/titleRightButton']")).click()
                # time.sleep(1)
                try:
                    with open("/sdcard/1/duanzi.txt", 'r', encoding='utf-8') as f:
                        strduanzi = f.readlines()
                except:
                    with open("D:/brush/slave/scripts/doc/duanzi.txt", 'r', encoding='utf-8') as f:
                        strduanzi = f.readlines()
                edts = WebDriverWait(dr, 5).until(lambda d: d.find_element_by_class_name("android.widget.EditText"))
                edts.send_keys(strduanzi[random.randint(0, strduanzi.__len__()-1)].strip())
                time.sleep(5)
                #随机选择是否添加图片
                if random.randint(0, 1):
                    WebDriverWait(dr, 15).until(lambda d: d.find_element_by_xpath("//android.widget.ImageButton[@resource-id='com.iyouxun:id/photoLayerButton']")).click()
                    time.sleep(1)
                    for x in range(random.randint(1, 1)):
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_xpath("//android.widget.ImageButton[@resource-id='com.iyouxun:id/addNewsSelectAlbum']")).click()
                        time.sleep(1)
                        WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("文件管理")).click()
                        time.sleep(1)
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_name("1")).click()
                        time.sleep(1)
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_name("1xiangce")).click()
                        time.sleep(1)
                        for i in range(random.randint(0, 50)):
                            dr.swipe(300, random.randint(800, 1000), 300, random.randint(300, 500))
                            time.sleep(1)
                        time.sleep(5)
                        imghead = WebDriverWait(dr, 15).until(lambda d: d.find_elements_by_id("com.android.fileexplorer:id/file_image"))
                        imghead[random.randint(0, imghead.__len__()-1)].click()
                        time.sleep(5)
                    if random.randint(0, 1):
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_class_name("android.widget.CheckBox")).click()
                        time.sleep(1)
                WebDriverWait(dr, 15).until(lambda d: d.find_element_by_xpath("//android.widget.Button[@resource-id='com.iyouxun:id/titleRightButton']")).click()
                time.sleep(5)
                for x in range(random.randint(1, 2)):
                    dr.swipe(random.randint(200, 400), random.randint(400, 1000), random.randint(200, 400), random.randint(400, 1000))
                    time.sleep(5)
            self.readnum -= 1
            self.ismenu3 = False
        except Exception as e:
            print("发动态爆料出错")
            dr.press_keycode(4)
            time.sleep(1)
            dr.press_keycode(4)
            time.sleep(1)
            dr.press_keycode(82)
            time.sleep(2)
            try:
                WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("友寻交友")).click()
            except TimeoutException:
                dr.press_keycode(4)
            time.sleep(5)
        return self.do

    #发现
    def menu4(self):
        dr = self.driver
        try:
            if self.islike:
                try:
                    WebDriverWait(dr, 10).until(lambda d: d.find_element_by_name("猜你喜欢")).click()
                    time.sleep(5)
                    for x in range(15):
                        try:
                            WebDriverWait(dr, 5).until(lambda d: d.find_element_by_xpath("//android.widget.Button[@resource-id='com.iyouxun:id/%s']" % choice(["find_u_like_button", "find_u_not_like_button"]))).click()
                            time.sleep(random.randint(3, 5))
                        except TimeoutException:
                            break
                    WebDriverWait(dr, 15).until(lambda d: d.find_element_by_xpath("//android.widget.Button[@resource-id='com.iyouxun:id/titleRightButton']")).click()
                    time.sleep(1)
                    for i in range(random.randint(1, 3)):
                        try:
                            mylike = WebDriverWait(dr, 5).until(lambda d: d.find_elements_by_name("加好友"))
                            mylike[random.randint(0, mylike.__len__()-1)].click()
                            time.sleep(2)
                        except TimeoutException:
                            pass
                    dr.press_keycode(4)
                    time.sleep(2)
                    dr.press_keycode(4)
                    time.sleep(2)
                    self.islike = False
                except TimeoutException:
                    pass
            read = WebDriverWait(dr, 15).until(lambda d: d.find_elements_by_xpath("//android.widget.RelativeLayout[@resource-id='com.iyouxun:id/find_friend_show_view']"))
            read[random.randint(0, read.__len__()-1)].click()
            time.sleep(5)
            dr.press_keycode(4)
            time.sleep(1)
            self.ismenu4 = False
        except Exception as e:
            print("查看发现出错")
            dr.press_keycode(4)
            time.sleep(1)
            dr.press_keycode(4)
            time.sleep(1)
            dr.press_keycode(82)
            time.sleep(2)
            try:
                WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("友寻交友")).click()
            except TimeoutException:
                dr.press_keycode(4)
                time.sleep(1)
        return self.do

    #我
    def menu5(self):
        dr = self.driver
        try:
            for x in range(2):
                num = random.randint(0, 3)
                if num == 0:
                    #我的爆料
                    dr.swipe(200, 200, 200, 800)
                    time.sleep(2)
                    WebDriverWait(dr, 15).until(lambda d: d.find_element_by_xpath("//android.widget.Button[@resource-id='com.iyouxun:id/profile_main_disclose']")).click()
                    time.sleep(5)
                    for i in range(random.randint(3, 4)):
                        dr.swipe(random.randint(50, 200), random.randint(300, 500),  random.randint(250, 600), random.randint(700, 1000))
                        time.sleep(5)
                    dr.press_keycode(4)
                    time.sleep(5)
                elif num == 1:
                    #上传图片
                    dr.swipe(200, 200, 200, 800)
                    time.sleep(2)
                    WebDriverWait(dr, 15).until(lambda d: d.find_element_by_xpath("//android.widget.ImageButton[@resource-id='com.iyouxun:id/profile_photo_add_button']")).click()
                    time.sleep(2)
                    WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("从相册选择")).click()
                    time.sleep(1)
                    WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("文件管理")).click()
                    time.sleep(1)
                    WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("1")).click()
                    time.sleep(1)
                    WebDriverWait(dr, 15).until(lambda d: d.find_element_by_name("1xiangce")).click()
                    time.sleep(1)
                    for i in range(random.randint(0, 80)):
                        dr.swipe(300, random.randint(800, 1000), 300, random.randint(300, 500))
                        time.sleep(1)
                    time.sleep(5)
                    imghead = WebDriverWait(dr, 15).until(lambda d: d.find_elements_by_id("com.android.fileexplorer:id/file_image"))
                    imghead[random.randint(0, imghead.__len__()-1)].click()
                    time.sleep(10)
                    break
                elif num == 2:
                    dr.swipe(200, 800, 200, 200)
                    time.sleep(2)
                    WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("编辑标签")).click()
                    time.sleep(5)
                    if random.randint(0, 1):
                        #编辑标签
                        for i in range(random.randint(3, 4)):
                            if random.randint(0, 1):
                                WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("换一批")).click()
                                time.sleep(1)
                            if random.randint(0, 2):
                                #添加标签
                                biaoqian = WebDriverWait(dr, 15).until(lambda d: d.find_elements_by_xpath("//android.widget.ImageView[@resource-id='com.iyouxun:id/item_tag_add']"))
                            else:
                                #删除标签
                                try:
                                    biaoqian = WebDriverWait(dr, 5).until(lambda d: d.find_elements_by_xpath("//android.widget.ImageView[@resource-id='com.iyouxun:id/item_tag_close']"))
                                except TimeoutException:
                                    biaoqian = WebDriverWait(dr, 15).until(lambda d: d.find_elements_by_xpath("//android.widget.ImageView[@resource-id='com.iyouxun:id/item_tag_add']"))
                            biaoqian[random.randint(0, biaoqian.__len__()-1)].click()
                            time.sleep(random.randint(4, 6))

                        if random.randint(0, 1):
                            WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("标签历史")).click()
                            #随机滑动
                            dr.swipe(300, random.randint(400, 1000), 300, random.randint(400, 800))
                            time.sleep(random.randint(4, 6))
                    WebDriverWait(dr, 15).until(lambda d: d.find_element_by_xpath("//android.widget.Button[@resource-id='com.iyouxun:id/titleLeftButton']")).click()
                    time.sleep(1)
                    try:
                        WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("确定")).click()
                    except TimeoutException:
                        pass
                    time.sleep(5)
                else:
                    dr.swipe(200, 200, 200, 800)
                    time.sleep(2)
                    edts = WebDriverWait(dr, 15).until(lambda d: d.find_element_by_class_name("android.widget.EditText"))
                    if edts.text == "暂无签名":
                        for i in range(5):
                            edts.click()
                            if edts.text:
                                for j in range(10):
                                    dr.pres_keycode(67)
                                continue
                            break
                        try:
                            with open("/sdcard/1/qianming.txt", 'r', encoding='utf-8') as f:
                                qianming = f.readlines()
                        except:
                            with open("D:/brush/slave/scripts/doc/qianming.txt", 'r', encoding='utf-8') as f:
                                qianming = f.readlines()
                        edts.send_keys(qianming[random.randint(0, qianming.__len__()-1)].strip())
                        time.sleep(1)
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_xpath("//android.widget.Button[@resource-id='com.iyouxun:id/titleRightButton']")).click()
                        time.sleep(5)
                    else:
                        for i in range(random.randint(2, 3)):
                            dr.swipe(300, random.randint(400, 1000), 300, random.randint(400, 800))
                            time.sleep(5)
            self.readnum -= 1
            self.ismenu5 = False
        except Exception as e:
            print("查看我出错")
            dr.press_keycode(4)
            time.sleep(1)
            dr.press_keycode(4)
            time.sleep(1)
            dr.press_keycode(82)
            time.sleep(2)
            try:
                WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("友寻交友")).click()
            except TimeoutException:
                dr.press_keycode(4)
                time.sleep(1)
        return self.do

    def ends(self):
        #记录时间
        time.sleep(5)
        self.endstime = "结束:%s:%s:%s" % (time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec)
        print(self.begintime)
        print(self.endstime)
        try:
            with open('/sdcard/1/timeyouxun.log', 'a') as f:
                f.write('\n激活 %s.%s, %s, %s, count:%s' % (time.localtime().tm_mon, time.localtime().tm_mday, self.begintime, self.endstime, self.runnum))
        except:
            pass
        time.sleep(5)
        #效率控制
        # st = [1200, 1200, 1200, 1200, 1200, 1200, 180, 120, 40, 20, 10, 10,
        #       10, 20, 20, 20, 10, 10, 5, 0, 0, 0, 0, 0]
        #
        # print("现在时间是%s:%s,脚本将在%s秒后继续执行" % (time.localtime().tm_hour, time.localtime().tm_min, st[time.localtime().tm_hour-1]))
        # time.sleep(st[time.localtime().tm_hour-1])

        return self.exit


class Machineyouxun2(Machine):
    def __init__(self, driver, imei=None, runnum=0):
        super(Machineyouxun2, self).__init__(self.begin)
        self.driver = driver
        self.try_count = 0
        self.readnum = random.randint(2, 2)
        self.imei = imei
        self.begintime = None
        self.endstime = None
        self.islike = True
        self.ismenu1 = True
        self.ismenu2 = True
        self.ismenu3 = True
        self.ismenu4 = True
        self.ismenu5 = True
        self.runnum = runnum

    def begin(self):
        dr = self.driver
        self.try_count = 0
        self.readnum = random.randint(2, 2)
        self.ismenu1 = True
        self.ismenu2 = True
        self.ismenu3 = True
        self.ismenu4 = True
        self.ismenu5 = True
        dr.press_keycode(3)
        time.sleep(1)
        WebDriverWait(dr, 30).until(lambda d: d.find_element_by_name("友寻交友")).click()
        time.sleep(10)
        return self.newenter

    def newenter(self):
        dr = self.driver
        self.begintime = "开始:%s:%s:%s" % (time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec)
        WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("com.iyouxun:id/dotBox"))
        time.sleep(1)
        #新开软件翻页
        for x in range(4):
            dr.swipe(600, 300, 200, 300)
            time.sleep(2)
        # time.sleep(5)
        return self.login

    def login(self):
        dr = self.driver
        try:
            with open('/sdcard/1/useryx.log', 'r') as f:
                selectuser = f.read()
        except:
            with open('D:/brush/slave/scripts/doc/useryx.log', 'r') as f:
                selectuser = f.read()
        try:
            user = re.search(r'imei:%s,(\d+)' % self.imei, selectuser).group(1)
            pwd = re.search(r'imei:%s,\d+,([0-9a-zA-Z]+)' % self.imei, selectuser).group(1)
            WebDriverWait(dr, 15).until(lambda d: d.find_element_by_xpath("//android.widget.ImageButton[@resource-id='com.iyouxun:id/guide_btn_login']")).click()
            edit = WebDriverWait(dr, 15).until(lambda d: d.find_elements_by_class_name("android.widget.EditText"))
            edit[0].send_keys(str(user))
            time.sleep(1)
            edit[1].send_keys(str(pwd))
            time.sleep(1)
            WebDriverWait(dr, 15).until(lambda d: d.find_element_by_xpath("//android.widget.Button[@resource-id='com.iyouxun:id/login_btn_login']")).click()
            time.sleep(5)
            for x in range(3):
                WebDriverWait(dr, 15).until(lambda d: d.find_element_by_xpath("//android.widget.ImageView[@resource-id='com.iyouxun:id/dialog_guide_layer']")).click()
                time.sleep(2)
            WebDriverWait(dr, 15).until(lambda d: d.find_element_by_xpath("//android.widget.Button[@resource-id='com.iyouxun:id/titleLeftButton']")).click()
            time.sleep(1)
            try:
                WebDriverWait(dr, 10).until(lambda d: d.find_element_by_name("你可能错过了好友的动态"))
                dr.press_keycode(4)
            except TimeoutException:
                pass
        except:
            time.sleep(random.randint(30, 60))
            try:
                with open('/sdcard/1/timeyouxun2.log', 'a') as f:
                    f.write('\n登录失败')
            except:
                pass
            return self.ends
        time.sleep(5)
        return self.do

    def do(self):
        dr = self.driver
        try:
            while self.readnum:
                print("剩下阅读次数:%s" % self.readnum)
                rdread = random.randint(0, 4)
                if rdread == 0:
                    if self.ismenu1:
                        print("熟人圈")
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_xpath("//android.widget.ImageView[@resource-id='com.iyouxun:id/global_menu_button_news']")).click()
                        time.sleep(5)
                        return self.menu1
                    return self.do
                elif rdread == 1:
                    if self.ismenu2:
                        print("消息")
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_xpath("//android.widget.ImageView[@resource-id='com.iyouxun:id/global_menu_button_msg']")).click()
                        time.sleep(5)
                        return self.menu2
                    return self.do
                elif rdread == 2:
                    if self.ismenu3:
                        print("发动态爆料")
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_xpath("//android.widget.ImageView[@resource-id='com.iyouxun:id/global_menu_button_add']")).click()
                        time.sleep(5)
                        return self.menu3
                    return self.do
                elif rdread == 3:
                    if self.ismenu4:
                        print("发现")
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_xpath("//android.widget.ImageView[@resource-id='com.iyouxun:id/global_menu_button_find']")).click()
                        time.sleep(5)
                        return self.menu4
                    return self.do
                else:
                    if self.ismenu5:
                        print("我")
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_xpath("//android.widget.ImageView[@resource-id='com.iyouxun:id/global_menu_button_center']")).click()
                        time.sleep(5)
                        return self.menu5
                    return self.do
        except TimeoutException:
            print("查找菜单出错")
            self.try_count += 1
            if self.try_count > 5:
                self.try_count = 0
                return self.exit
            dr.press_keycode(4)
            time.sleep(1)
            dr.press_keycode(4)
            time.sleep(1)
            dr.press_keycode(82)
            time.sleep(2)
            try:
                WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("友寻交友")).click()
            except TimeoutException:
                dr.press_keycode(4)
            time.sleep(5)
            return self.do
        print("阅览完毕")
        return self.ends

    #熟人圈
    def menu1(self):
        dr = self.driver
        try:
            if random.randint(0, 2):
                #爆料
                WebDriverWait(dr, 15).until(lambda d: d.find_element_by_xpath("//android.widget.TextView[@resource-id='com.iyouxun:id/news_main_tab3']")).click()
                time.sleep(5)
                #随机滑动
                for x in range(random.randint(2, 3)):
                    dr.swipe(random.randint(200, 400), random.randint(800, 1000), random.randint(200, 400), random.randint(400, 600))
                    time.sleep(5)
                #点赞
                if random.randint(0, 1):
                    like = WebDriverWait(dr, 15).until(lambda d: d.find_elements_by_xpath("//android.widget.Button[@resource-id='com.iyouxun:id/item_disclose_main_praisecount']"))
                    like[random.randint(0, like.__len__()-1)].click()
                    time.sleep(1)
                #评论
                if random.randint(0, 2):
                    for x in range(random.randint(2, 3)):
                        dr.swipe(random.randint(200, 400), random.randint(800, 1000), random.randint(200, 400), random.randint(400, 600))
                        time.sleep(5)
                else:
                    comment = WebDriverWait(dr, 15).until(lambda d: d.find_elements_by_xpath("//android.widget.Button[@resource-id='com.iyouxun:id/item_disclose_main_commentcount']"))
                    comment[random.randint(0, comment.__len__()-1)].click()
                    time.sleep(5)
                    for x in range(random.randint(2, 3)):
                        dr.swipe(300, random.randint(700, 1000), 300, random.randint(200, 500))
                        time.sleep(5)
                    pltext = None
                    try:
                        pltext = WebDriverWait(dr, 15).until(lambda d: d.find_elements_by_xpath("//android.widget.TextView[@resource-id='com.iyouxun:id/item_broke_news_detail_comment_comment']"))
                    except TimeoutException:
                        pass
                    # WebDriverWait(dr, 15).until(lambda d: d.find_element_by_xpath("//android.widget.LinearLayout[@resource-id='com.yc.ai:id/bottom_comment_img']")).click()
                    # time.sleep(3)
                    edts = WebDriverWait(dr, 5).until(lambda d: d.find_element_by_class_name('android.widget.EditText'))
                    if pltext:
                        if random.randint(0, 1):
                            edts.send_keys(pltext[random.randint(0, pltext.__len__()-1)].text)
                        else:
                            edts.send_keys(choice(["路过", "不错啊", "可以的", "赞", "赞一个", "必须赞啊", "大赞", "好", "赞!", "支持", "厉害", "好看", "漂亮", "交个朋友吧", "nice"]))
                    else:
                        edts.send_keys(choice(["路过", "不错啊", "可以的", "赞", "赞一个", "必须赞啊", "大赞", "好", "赞!", "支持", "厉害", "好看", "漂亮", "交个朋友吧", "nice"]))
                    time.sleep(1)
                    WebDriverWait(dr, 15).until(lambda d: d.find_element_by_xpath("//android.widget.Button[@resource-id='com.iyouxun:id/btn_setting_msg']")).click()
                    time.sleep(5)
                    dr.press_keycode(4)
                    time.sleep(1)
            else:
                #动态
                WebDriverWait(dr, 15).until(lambda d: d.find_element_by_xpath("//android.widget.TextView[@resource-id='com.iyouxun:id/news_main_tab2']")).click()
                time.sleep(1)
                WebDriverWait(dr, 15).until(lambda d: d.find_element_by_xpath("//android.widget.Button[@resource-id='com.iyouxun:id/titleRightButton']")).click()
                time.sleep(1)
                try:
                    with open("/sdcard/1/duanzi.txt", 'r', encoding='utf-8') as f:
                        strduanzi = f.readlines()
                except:
                    with open("D:/brush/slave/scripts/doc/duanzi.txt", 'r', encoding='utf-8') as f:
                        strduanzi = f.readlines()
                edts = WebDriverWait(dr, 5).until(lambda d: d.find_element_by_class_name("android.widget.EditText"))
                edts.send_keys(strduanzi[random.randint(0, strduanzi.__len__()-1)].strip())
                time.sleep(5)
                #随机选择是否添加图片
                if random.randint(0, 1):
                    WebDriverWait(dr, 15).until(lambda d: d.find_element_by_xpath("//android.widget.ImageButton[@resource-id='com.iyouxun:id/photoLayerButton']")).click()
                    time.sleep(1)
                    for x in range(random.randint(1, 1)):
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_xpath("//android.widget.ImageButton[@resource-id='com.iyouxun:id/addNewsSelectAlbum']")).click()
                        time.sleep(1)
                        WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("文件管理")).click()
                        time.sleep(1)
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_name("1")).click()
                        time.sleep(1)
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_name("1xiangce")).click()
                        time.sleep(1)
                        for i in range(random.randint(0, 50)):
                            dr.swipe(300, random.randint(800, 1000), 300, random.randint(300, 500))
                            time.sleep(1)
                        time.sleep(5)
                        imghead = WebDriverWait(dr, 15).until(lambda d: d.find_elements_by_id("com.android.fileexplorer:id/file_image"))
                        imghead[random.randint(0, imghead.__len__()-1)].click()
                        time.sleep(5)
                    if random.randint(0, 1):
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_class_name("android.widget.CheckBox")).click()
                        time.sleep(1)
                WebDriverWait(dr, 15).until(lambda d: d.find_element_by_xpath("//android.widget.Button[@resource-id='com.iyouxun:id/titleRightButton']")).click()
                time.sleep(5)
                for x in range(random.randint(1, 2)):
                    dr.swipe(random.randint(200, 400), random.randint(400, 1000), random.randint(200, 400), random.randint(400, 1000))
                    time.sleep(5)
            self.readnum -= 1
            self.ismenu1 = False
        except Exception as e:
            print("查看熟人圈出错")
            dr.press_keycode(4)
            time.sleep(1)
            dr.press_keycode(4)
            time.sleep(1)
            dr.press_keycode(82)
            time.sleep(2)
            try:
                WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("友寻交友")).click()
            except TimeoutException:
                dr.press_keycode(4)
            time.sleep(5)
        return self.do

    #消息
    def menu2(self):
        dr = self.driver
        try:
            WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name(choice(["我的群组", "系统消息", "建立群组", "友寻小秘书"]))).click()
            time.sleep(1)
            try:
                WebDriverWait(dr, 5).until(lambda d: d.find_element_by_xpath("//android.widget.TextView[@resource-id='com.iyouxun:id/system_message_btn_%s']" % choice(["agree", "refuse"]))).click()
                time.sleep(2)
            except:
                pass
            self.ismenu2 = False
            dr.press_keycode(4)
            time.sleep(5)
        except Exception as e:
            print("查看消息出错")
            dr.press_keycode(4)
            time.sleep(1)
            dr.press_keycode(4)
            time.sleep(1)
            dr.press_keycode(82)
            time.sleep(2)
            try:
                WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("友寻交友")).click()
            except TimeoutException:
                dr.press_keycode(4)
                time.sleep(1)
        return self.do

    #发动态爆料
    def menu3(self):
        dr = self.driver
        try:
            if random.randint(0, 1):
                #爆料
                WebDriverWait(dr, 15).until(lambda d: d.find_element_by_xpath("//android.widget.TextView[@resource-id='com.iyouxun:id/main_add_create_broke_news']")).click()
                time.sleep(1)
                #添加图片
                for x in range(random.randint(1, 1)):
                    try:
                        WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("可以上传9张照片")).click()
                    except TimeoutException:
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_xpath("//android.widget.ImageView[@resource-id='com.iyouxun:id/add_photo_btn_add']")).click()
                    time.sleep(1)
                    WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("从相册选择")).click()
                    time.sleep(1)
                    WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("文件管理")).click()
                    time.sleep(1)
                    WebDriverWait(dr, 15).until(lambda d: d.find_element_by_name("1")).click()
                    time.sleep(1)
                    WebDriverWait(dr, 15).until(lambda d: d.find_element_by_name("1xiangce")).click()
                    time.sleep(1)
                    for i in range(random.randint(0, 50)):
                        dr.swipe(300, random.randint(800, 1000), 300, random.randint(300, 500))
                        time.sleep(1)
                    time.sleep(5)
                    imghead = WebDriverWait(dr, 15).until(lambda d: d.find_elements_by_id("com.android.fileexplorer:id/file_image"))
                    imghead[random.randint(0, imghead.__len__()-1)].click()
                    time.sleep(5)
                #添加标签
                WebDriverWait(dr, 15).until(lambda d: d.find_element_by_xpath("//android.widget.TextView[@resource-id='com.iyouxun:id/create_broke_the_news_add_tag']")).click()
                time.sleep(1)
                for x in range(random.randint(1, 3)):
                    biaoqian = WebDriverWait(dr, 15).until(lambda d: d.find_elements_by_xpath("//android.widget.ImageView[@resource-id='com.iyouxun:id/item_tag_add']"))
                    biaoqian[random.randint(0, biaoqian.__len__()-1)].click()
                    time.sleep(1)
                    if random.randint(0, 1):
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_name("换一批")).click()
                        time.sleep(1)
                dr.press_keycode(4)
                time.sleep(1)
                #介绍
                try:
                    with open("/sdcard/1/duanzi2.txt", 'r', encoding='utf-8') as f:
                        strduanzi = f.readlines()
                except:
                    with open("D:/brush/slave/scripts/doc/duanzi2.txt", 'r', encoding='utf-8') as f:
                        strduanzi = f.readlines()
                edts = WebDriverWait(dr, 5).until(lambda d: d.find_element_by_class_name("android.widget.EditText"))
                edts.send_keys(strduanzi[random.randint(0, strduanzi.__len__()-1)].strip())
                time.sleep(1)
                #发布
                WebDriverWait(dr, 15).until(lambda d: d.find_element_by_xpath("//android.widget.Button[@resource-id='com.iyouxun:id/titleRightButton']")).click()
                time.sleep(5)
            else:
                #动态
                WebDriverWait(dr, 15).until(lambda d: d.find_element_by_xpath("//android.widget.TextView[@resource-id='com.iyouxun:id/main_add_create_news']")).click()
                time.sleep(1)
                # WebDriverWait(dr, 15).until(lambda d: d.find_element_by_xpath("//android.widget.Button[@resource-id='com.iyouxun:id/titleRightButton']")).click()
                # time.sleep(1)
                try:
                    with open("/sdcard/1/duanzi.txt", 'r', encoding='utf-8') as f:
                        strduanzi = f.readlines()
                except:
                    with open("D:/brush/slave/scripts/doc/duanzi.txt", 'r', encoding='utf-8') as f:
                        strduanzi = f.readlines()
                edts = WebDriverWait(dr, 5).until(lambda d: d.find_element_by_class_name("android.widget.EditText"))
                edts.send_keys(strduanzi[random.randint(0, strduanzi.__len__()-1)].strip())
                time.sleep(5)
                #随机选择是否添加图片
                if random.randint(0, 1):
                    WebDriverWait(dr, 15).until(lambda d: d.find_element_by_xpath("//android.widget.ImageButton[@resource-id='com.iyouxun:id/photoLayerButton']")).click()
                    time.sleep(1)
                    for x in range(random.randint(1, 1)):
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_xpath("//android.widget.ImageButton[@resource-id='com.iyouxun:id/addNewsSelectAlbum']")).click()
                        time.sleep(1)
                        WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("文件管理")).click()
                        time.sleep(1)
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_name("1")).click()
                        time.sleep(1)
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_name("1xiangce")).click()
                        time.sleep(1)
                        for i in range(random.randint(0, 50)):
                            dr.swipe(300, random.randint(800, 1000), 300, random.randint(300, 500))
                            time.sleep(1)
                        time.sleep(5)
                        imghead = WebDriverWait(dr, 15).until(lambda d: d.find_elements_by_id("com.android.fileexplorer:id/file_image"))
                        imghead[random.randint(0, imghead.__len__()-1)].click()
                        time.sleep(5)
                    if random.randint(0, 1):
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_class_name("android.widget.CheckBox")).click()
                        time.sleep(1)
                WebDriverWait(dr, 15).until(lambda d: d.find_element_by_xpath("//android.widget.Button[@resource-id='com.iyouxun:id/titleRightButton']")).click()
                time.sleep(5)
                for x in range(random.randint(1, 2)):
                    dr.swipe(random.randint(200, 400), random.randint(400, 1000), random.randint(200, 400), random.randint(400, 1000))
                    time.sleep(5)
            self.readnum -= 1
            self.ismenu3 = False
        except Exception as e:
            print("发动态爆料出错")
            dr.press_keycode(4)
            time.sleep(1)
            dr.press_keycode(4)
            time.sleep(1)
            dr.press_keycode(82)
            time.sleep(2)
            try:
                WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("友寻交友")).click()
            except TimeoutException:
                dr.press_keycode(4)
            time.sleep(5)
        return self.do

    #发现
    def menu4(self):
        dr = self.driver
        try:
            if self.islike:
                try:
                    WebDriverWait(dr, 10).until(lambda d: d.find_element_by_name("猜你喜欢")).click()
                    time.sleep(5)
                    for x in range(15):
                        try:
                            WebDriverWait(dr, 5).until(lambda d: d.find_element_by_xpath("//android.widget.Button[@resource-id='com.iyouxun:id/%s']" % choice(["find_u_like_button", "find_u_not_like_button"]))).click()
                            time.sleep(random.randint(3, 5))
                        except TimeoutException:
                            break
                    WebDriverWait(dr, 15).until(lambda d: d.find_element_by_xpath("//android.widget.Button[@resource-id='com.iyouxun:id/titleRightButton']")).click()
                    time.sleep(1)
                    for i in range(random.randint(1, 3)):
                        try:
                            mylike = WebDriverWait(dr, 5).until(lambda d: d.find_elements_by_name("加好友"))
                            mylike[random.randint(0, mylike.__len__()-1)].click()
                            time.sleep(2)
                        except TimeoutException:
                            pass
                    dr.press_keycode(4)
                    time.sleep(2)
                    dr.press_keycode(4)
                    time.sleep(2)
                    self.islike = False
                except TimeoutException:
                    pass
            read = WebDriverWait(dr, 15).until(lambda d: d.find_elements_by_xpath("//android.widget.RelativeLayout[@resource-id='com.iyouxun:id/find_friend_show_view']"))
            read[random.randint(0, read.__len__()-1)].click()
            time.sleep(5)
            dr.press_keycode(4)
            time.sleep(1)
            self.ismenu4 = False
        except Exception as e:
            print("查看发现出错")
            dr.press_keycode(4)
            time.sleep(1)
            dr.press_keycode(4)
            time.sleep(1)
            dr.press_keycode(82)
            time.sleep(2)
            try:
                WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("友寻交友")).click()
            except TimeoutException:
                dr.press_keycode(4)
                time.sleep(1)
        return self.do

    #我
    def menu5(self):
        dr = self.driver
        try:
            for x in range(2):
                num = random.randint(0, 3)
                if num == 0:
                    #我的爆料
                    dr.swipe(200, 200, 200, 800)
                    time.sleep(2)
                    WebDriverWait(dr, 15).until(lambda d: d.find_element_by_xpath("//android.widget.Button[@resource-id='com.iyouxun:id/profile_main_disclose']")).click()
                    time.sleep(5)
                    for i in range(random.randint(3, 4)):
                        dr.swipe(random.randint(50, 200), random.randint(300, 500),  random.randint(250, 600), random.randint(700, 1000))
                        time.sleep(5)
                    dr.press_keycode(4)
                    time.sleep(5)
                elif num == 1:
                    #上传图片
                    dr.swipe(200, 200, 200, 800)
                    time.sleep(2)
                    WebDriverWait(dr, 15).until(lambda d: d.find_element_by_xpath("//android.widget.ImageButton[@resource-id='com.iyouxun:id/profile_photo_add_button']")).click()
                    time.sleep(2)
                    WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("从相册选择")).click()
                    time.sleep(1)
                    WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("文件管理")).click()
                    time.sleep(1)
                    WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("1")).click()
                    time.sleep(1)
                    WebDriverWait(dr, 15).until(lambda d: d.find_element_by_name("1xiangce")).click()
                    time.sleep(1)
                    for i in range(random.randint(0, 80)):
                        dr.swipe(300, random.randint(800, 1000), 300, random.randint(300, 500))
                        time.sleep(1)
                    time.sleep(5)
                    imghead = WebDriverWait(dr, 15).until(lambda d: d.find_elements_by_id("com.android.fileexplorer:id/file_image"))
                    imghead[random.randint(0, imghead.__len__()-1)].click()
                    time.sleep(10)
                    break
                elif num == 2:
                    dr.swipe(200, 800, 200, 200)
                    time.sleep(2)
                    WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("编辑标签")).click()
                    time.sleep(5)
                    if random.randint(0, 1):
                        #编辑标签
                        for i in range(random.randint(3, 4)):
                            if random.randint(0, 1):
                                WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("换一批")).click()
                                time.sleep(1)
                            if random.randint(0, 2):
                                #添加标签
                                biaoqian = WebDriverWait(dr, 15).until(lambda d: d.find_elements_by_xpath("//android.widget.ImageView[@resource-id='com.iyouxun:id/item_tag_add']"))
                            else:
                                #删除标签
                                try:
                                    biaoqian = WebDriverWait(dr, 5).until(lambda d: d.find_elements_by_xpath("//android.widget.ImageView[@resource-id='com.iyouxun:id/item_tag_close']"))
                                except TimeoutException:
                                    biaoqian = WebDriverWait(dr, 15).until(lambda d: d.find_elements_by_xpath("//android.widget.ImageView[@resource-id='com.iyouxun:id/item_tag_add']"))
                            biaoqian[random.randint(0, biaoqian.__len__()-1)].click()
                            time.sleep(random.randint(4, 6))

                        if random.randint(0, 1):
                            WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("标签历史")).click()
                            #随机滑动
                            dr.swipe(300, random.randint(400, 1000), 300, random.randint(400, 800))
                            time.sleep(random.randint(4, 6))
                    WebDriverWait(dr, 15).until(lambda d: d.find_element_by_xpath("//android.widget.Button[@resource-id='com.iyouxun:id/titleLeftButton']")).click()
                    time.sleep(1)
                    try:
                        WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("确定")).click()
                    except TimeoutException:
                        pass
                    time.sleep(5)
                else:
                    dr.swipe(200, 200, 200, 800)
                    time.sleep(2)
                    edts = WebDriverWait(dr, 15).until(lambda d: d.find_element_by_class_name("android.widget.EditText"))
                    if edts.text == "暂无签名":
                        for i in range(5):
                            edts.click()
                            if edts.text:
                                for j in range(10):
                                    dr.pres_keycode(67)
                                continue
                            break
                        try:
                            with open("/sdcard/1/qianming.txt", 'r', encoding='utf-8') as f:
                                qianming = f.readlines()
                        except:
                            with open("D:/brush/slave/scripts/doc/qianming.txt", 'r', encoding='utf-8') as f:
                                qianming = f.readlines()
                        edts.send_keys(qianming[random.randint(0, qianming.__len__()-1)].strip())
                        time.sleep(1)
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_xpath("//android.widget.Button[@resource-id='com.iyouxun:id/titleRightButton']")).click()
                        time.sleep(5)
                    else:
                        for i in range(random.randint(2, 3)):
                            dr.swipe(300, random.randint(400, 1000), 300, random.randint(400, 800))
                            time.sleep(5)
            self.readnum -= 1
            self.ismenu5 = False
        except Exception as e:
            print("查看我出错")
            dr.press_keycode(4)
            time.sleep(1)
            dr.press_keycode(4)
            time.sleep(1)
            dr.press_keycode(82)
            time.sleep(2)
            try:
                WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("友寻交友")).click()
            except TimeoutException:
                dr.press_keycode(4)
                time.sleep(1)
        return self.do

    def ends(self):
        #记录时间
        time.sleep(5)
        self.endstime = "结束:%s:%s:%s" % (time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec)
        print(self.begintime)
        print(self.endstime)
        try:
            with open('/sdcard/1/timeyouxun2.log', 'a') as f:
                f.write('\n留存 %s.%s, %s, %s, count:%s' % (time.localtime().tm_mon, time.localtime().tm_mday, self.begintime, self.endstime, self.runnum))
        except:
            pass
        time.sleep(5)
        return self.exit


if __name__ == "__main__":
    wd = webdriver.Remote()
    time.sleep(2)

