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


class TotalMachine(WorkMachine):
    def load_task_info(self):
        return []


    def setup_machine(self):
        dr = self.driver
        self.machine008 = Machine008(dr)
        self.machine008.task_schedule = ["record_file", "clear_data", "modify_data"]  # 007 task list


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
                MachineVPN(dr).run()
                m008.run()
                dr.press_keycode(3)
                time.sleep(1)
                dr.press_keycode(3)
                time.sleep(1)
                WebDriverWait(dr, 30).until(lambda d: d.find_element_by_name("testsdk")).click()
                time.sleep(5)
                if m008.remain_day == '1':
                    #效率控制
                    st = [600, 1200, 1500, 1500, 800, 100, 60, 40, 40, 40, 40, 20,
                          20, 40, 40, 40, 20, 20, 20, 20, 20, 20, 20, 80]
                    print("现在时间是%s:%s,脚本将在%s秒后继续执行" % (time.localtime().tm_hour, time.localtime().tm_min, st[time.localtime().tm_hour-1]))
                    time.sleep(st[time.localtime().tm_hour-1])
                else:
                    time.sleep(20)
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