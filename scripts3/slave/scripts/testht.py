#! -*- coding=utf-8 -*-
import os
import sys


filepath = os.path.abspath(__file__)
sys.path.append(os.path.dirname(os.path.dirname(filepath)))

import threading
import time

from datetime import datetime
from multiprocessing import Process
from machines.machineVPN import MachineVPN
from machines.machineXposeHook import MachineXHook as Machine008
from appium4droid import webdriver
from bootstrap import setup_boostrap
from TotalMachine import WorkMachine
from appium4droid.support.ui import WebDriverWait
from machines.StateMachine import Machine
import random

class TotalMachine(WorkMachine):
    def load_task_info(self):
        return []


    def setup_machine(self):
        dr = self.driver
        self.machine008 = Machine008(dr)
        self.machine008.task_schedule = ["record_file", "clear_data", "modify_data"]  # 007 task list
        self.appname = "UMengTest"

    def main_loop(self):
        dr = self.driver
        m008 = self.machine008
        while True:
            try:
                dr.press_keycode(3)
                time.sleep(1)
                dr.press_keycode(3)
                time.sleep(1)
                #清后台
                dr.press_keycode(82)
                time.sleep(1)
                WebDriverWait(dr, 10).until(lambda d: d.find_element_by_id("com.android.systemui:id/clearButton")).click()
                time.sleep(1)
                # MachineVPN(dr).run()
                WebDriverWait(dr, 30).until(lambda d: d.find_element_by_name("无极VPN")).click()
                time.sleep(1)
                WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("org.wuji:id/exit_vpn")).click()
                time.sleep(5)
                m008.run()
                dr.press_keycode(3)
                time.sleep(1)
                dr.press_keycode(3)
                time.sleep(1)
                WebDriverWait(dr, 30).until(lambda d: d.find_element_by_name(self.appname)).click()
                time.sleep(5)
                #开启加速
                dr.press_keycode(3)
                time.sleep(1)
                WebDriverWait(dr, 30).until(lambda d: d.find_element_by_name("GMD Speed Time")).click()
                time.sleep(1)
                WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("com.gmd.speedtime:id/buttonStart")).click()
                time.sleep(2)
                dr.press_keycode(3)
                time.sleep(1)
                WebDriverWait(dr, 30).until(lambda d: d.find_element_by_name(self.appname)).click()
                time.sleep(1)
                if m008.remain_day == '1':
                    #效率控制
                    # st = [600, 1200, 1500, 1500, 800, 100, 60, 40, 40, 40, 40, 20,
                    #       20, 40, 40, 40, 20, 20, 20, 20, 20, 20, 20, 80]
                    # print("现在时间是%s:%s,脚本将在%s秒后继续执行" % (time.localtime().tm_hour, time.localtime().tm_min, st[time.localtime().tm_hour-1]))
                    # time.sleep(st[time.localtime().tm_hour-1])
                    time.sleep(random.randint(15, 30))
                else:
                    time.sleep(20)
                #关闭加速
                dr.press_keycode(3)
                time.sleep(1)
                WebDriverWait(dr, 30).until(lambda d: d.find_element_by_name("GMD Speed Time")).click()
                time.sleep(1)
                WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("com.gmd.speedtime:id/buttonStop")).click()
                time.sleep(1)
                dr.press_keycode(3)
                time.sleep(1)
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