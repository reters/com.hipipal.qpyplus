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
from machines.machineXueba008 import Machinex, Machinex2
from machines.StateMachine import Machine
from sock.socksend import send_file
try:
    from util import replace_wifi
except ImportError:
    replace_wifi = lambda: 1


class TotalMachine(WorkMachine):
    def load_task_info(self):
        return []

    def setup_machine(self):
        dr = self.driver
       #  [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,
       #   13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 0]
        self.st = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.runnum = 0         #计数器
        self.machine008 = Machine008(dr)
        self.machine008.task_schedule = ["do_all_one_key", "modify_data"]
        self.machine1 = Machinex(dr, "ailezan", "api-4tuoz9od", "meiriq2014")       # feima/yama/yima/ailezan/shenhua            api-a3t06fpx/api-4tuoz9od
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
                MachineVPN(dr).run()
                #留存率设置
                m008.remain_rate = [50, 45, 40, 35, 30, 25, 20, 15, 10, 5]
                m008.frist_day = self.st[time.localtime().tm_hour-1]
                #留存做完是否跳转做激活   True/Fasle
                m008.change = True
                m008.run()
                if m008.frist_day == 1:
                    print("激活")
                    m1.imei = m008.imei
                    m1.runnum = self.runnum
                    m1.run()
                    self.runnum += 1
                    m008.task_schedule = ["backup_ap"]
                    m008.run()
                    m008.task_schedule = ["do_all_one_key", "modify_data"]
                    #控制激活量
                    # self.ctrl_new("", 100, 1800)      #filename, num, sleep_time
                elif m008.frist_day == 2:
                    print("留存已完成暂停30分钟")
                    time.sleep(1800)
                else:
                    print("留存")
                    m2.imei = m008.imei
                    m008.task_schedule = ["backup_ap"]
                    m008.run()
                    m008.task_schedule = ["do_all_one_key", "modify_data"]
                    m2.run()
            except Exception as e:
                print("somting wrong")
                print(e)
            finally:
                pass
            print("Again\n")
        return self.exit

    #上传记录文件
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
