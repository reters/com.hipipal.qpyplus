#! -*- coding=utf-8 -*-
import os
import sys


filepath = os.path.abspath(__file__)
sys.path.append(os.path.dirname(os.path.dirname(filepath)))

import threading
import time
import re
import random
from datetime import datetime
from multiprocessing import Process
from machines.machineVPN import MachineVPN
# from machines.machine008 import Machine008
from machines.machineXposeHook import MachineXHook as Machine008
from appium4droid import webdriver
from bootstrap import setup_boostrap
from TotalMachine import WorkMachine
from appium4droid.support.ui import WebDriverWait
from machines.machineHuajiao_suoshui import Machinex, Machinex2
from machines.StateMachine import Machine
from sock.socksend import send_file
from random import choice
try:
    from util import replace_wifi
except ImportError:
    replace_wifi = lambda: 1


class TotalMachine(WorkMachine):
    def load_task_info(self):
        return []

    def setup_machine(self):
        dr = self.driver
        self.runnum = 0
        self.machine008 = Machine008(dr)
        self.machine008.task_schedule = ["record_file", "clear_data", "modify_data"]    # 007 task list
        self.machine1 = Machinex(dr, "shenhua", "xiaoxiaozhuan", "meiriq2014")       # feima/yama/shenhua
        self.machine2 = Machinex2(dr)


    def main_loop(self):
        dr = self.driver
        m008 = self.machine008
        m1 = self.machine1
        m2 = self.machine2
        #切换脚本输入法
        dr.press_keycode(63)
        time.sleep(1)
        dr.find_element_by_name("Appium Android Input Manager for Unicode").click()
        time.sleep(1)
        while True:
            try:
                dr.press_keycode(3)
                time.sleep(1)
                dr.press_keycode(3)
                time.sleep(1)
                dr.press_keycode(66)
                time.sleep(1)
                dr.press_keycode(66)
                time.sleep(1)
                #清后台
                dr.press_keycode(82)
                time.sleep(1)
                WebDriverWait(dr, 10).until(lambda d: d.find_element_by_id("com.android.systemui:id/clearButton")).click()
                time.sleep(1)
                # 上传记录文件
                # if time.localtime().tm_hour == 8 and time.localtime().tm_min >= 30:
                try:
                    self.upload_file(choice(['192.168.2.108', '10.0.0.22']), ["userhuajiao.log", "timehuajiao.log", "timehuajiao2.log"])
                except:
                    pass
                #计数器清0
                if time.localtime().tm_hour == 0 and self.runnum > 12:
                    self.runnum = 0
                MachineVPN(dr).run()
                m008.run()
                #周末控制效率
                # if m008.remain_day == '1' and (time.localtime().tm_wday == 5 or time.localtime().tm_wday == 6):
                #     print("周末激活暂停1800s....")
                #     time.sleep(1800)
                #     continue
                if m008.remain_day == '1':
                    print("激活")
                    m1.imei = m008.imei
                    m1.runnum = self.runnum
                    m1.run()
                    self.runnum += 1
                    #控制激活量
                    # self.ctrl_new("timehuajiao.log", 100, 1800)      #filename, num, sleep_time
                else:
                    print("留存")
                    m2.imei = m008.imei
                    m2.remainday = m008.remain_day
                    m2.run()
            except Exception as e:
                print("somting wrong")
                print(e)
            finally:
                pass
            print("Again\n")
        return self.exit

    # 上传记录文件
    def upload_file(self, addr, file):
        replace_wifi()
        time.sleep(1)
        replace_wifi()
        time.sleep(5)
        try:
            with open('/sdcard/device.txt', 'r') as f:
                selectuser = f.read()
        except:
            with open('device.txt', 'r') as f:
                selectuser = f.read()
        device = re.search(r'device:([0-9a-zA-Z\.]+)', selectuser).group(1)
        for filename in file: #最多可发送文件数量
            # filename = re.search(r'filename%s:([0-9a-zA-Z\.]+)' % num, selectuser)
            if filename:
                if os.path.exists(filename) or os.path.exists('/sdcard/1/' + filename): #检测文件是否存在,不存在不发送
                    send_file(device, filename, addr)
                else:
                    print("not find the file:%s" % filename)
            else:
                break
            time.sleep(2)
        time.sleep(5)

    #控制激活量
    def ctrl_new(self, filename, num=100, sleep_time=1800):
        with open("/sdcard/1/%s.log" % filename, 'r', encoding='utf-8') as f:
            a = f.read()
        match = re.findall(r'激活 %s.%s' % (time.localtime().tm_mon, time.localtime().tm_mday), a)
        if match.__len__() >= num:
            print("激活数已达%s,暂停30分钟" % match.__len__())
            time.sleep(sleep_time)
            return True
        else:
            return False


if __name__ == "__main__":
    TM = TotalMachine()
    TM.run()
