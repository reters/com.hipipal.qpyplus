#! -*- coding=utf-8 -*-
import os
import sys


filepath = os.path.abspath(__file__)
sys.path.append(os.path.dirname(os.path.dirname(filepath)))

import threading
import time
import re
from datetime import datetime
from multiprocessing import Process
from machines.machineVPN import MachineVPN
from machines.machinenew008 import Machine008
from appium4droid import webdriver
from bootstrap import setup_boostrap
from TotalMachine import WorkMachine
from appium4droid.support.ui import WebDriverWait
from machines.machinePinganwifi import Machinex, Machinex2
from machines.StateMachine import Machine
from socksend import send_file
try:
    from util import replace_wifi, reset_wifi
except ImportError:
    replace_wifi = lambda: 1
    reset_wifi = lambda: 1


class TotalMachine(WorkMachine):
    def load_task_info(self):
        return []

    def upload_file(self):
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
        for num in range(10): #最多可发送文件数量
            filename = re.search(r'filename%s:([0-9a-zA-Z\.]+)' % num, selectuser)
            if filename:
                if os.path.exists(filename.group(1)) or os.path.exists('/sdcard/1/' + filename.group(1)): #检测文件是否存在,不存在不发送
                    send_file(device, filename.group(1))
                else:
                    print("not find the file:%s" % filename.group(1))
            else:
                break
            time.sleep(2)
        time.sleep(5)

    def setup_machine(self):
        dr = self.driver
        self.st = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.runnum = 0
        self.machine008 = Machine008(dr)
        self.machine008backup = Machine008(dr)
        self.machine008recovery = Machine008(dr)
        self.machine008.task_schedule = ["do_all_one_key", "modify_data"]
        self.machine008backup.task_schedule = ["backup_app"]
        self.machine008recovery.task_schedule = ["recovery_app"]
        self.machine1 = Machinex(dr, "shenhua", "xiaoxiaozhuan", "meiriq2014")       # feima/yama/shenhua
        self.machine2 = Machinex2(dr)


    def main_loop(self):
        dr = self.driver
        m008 = self.machine008
        m008backup = self.machine008backup
        m008recovery = self.machine008recovery
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
                reset_wifi()
                #上传记录文件
                # if time.localtime().tm_hour == 8 and time.localtime().tm_min >= 30:
                #     self.upload_file()
                #周末控制效率
                # if m008.frist_day and (time.localtime().tm_wday == 5 or time.localtime().tm_wday == 6):
                #     print("周末激活暂停1800s....")
                #     time.sleep(1800)
                #计数器清0
                if time.localtime().tm_hour == 0 and self.runnum > 12:
                    self.runnum = 0
                #留存率设置
                m008.remain_rate = [50, 45, 40, 35, 30, 25, 20, 15, 10, 5]
                m008.frist_day = self.st[time.localtime().tm_hour-1]
                m008.run()
                MachineVPN(dr).run()
                if m008.frist_day:
                    print("激活")
                    m1.imei = m008.imei
                    m1.runnum = self.runnum
                    m1.run()
                    self.runnum += 1
                    dr.press_keycode(3)
                    time.sleep(1)
                    dr.press_keycode(3)
                    time.sleep(1)
                    #清后台
                    dr.press_keycode(82)
                    time.sleep(1)
                    WebDriverWait(dr, 10).until(lambda d: d.find_element_by_id("com.android.systemui:id/clearButton")).click()
                    time.sleep(1)
                    m008backup.run()
                    #控制激活量
                    # try:
                    #     with open("/sdcard/1/time.log", 'r', encoding='utf-8') as f:
                    #         a = f.read()
                    #     match = re.findall(r'激活 %s.%s' % (time.localtime().tm_mon, time.localtime().tm_mday), a)
                    #     if match.__len__() >= 100:
                    #         print("控制激活数量,暂停30分钟")
                    #         time.sleep(1800)
                    #         continue
                    # except:
                    #     pass
                else:
                    print("留存")
                    m008recovery.imei = m008.imei
                    m008recovery.run()
                    m2.imei = m008.imei
                    m2.run()
            except Exception as e:
                print("somting wrong")
                print(e)
            finally:
                pass
            print("Again\n")
        return self.exit


if __name__ == "__main__":
    TM = TotalMachine()
    TM.run()
