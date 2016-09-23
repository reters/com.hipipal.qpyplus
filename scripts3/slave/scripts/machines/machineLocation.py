#! -*- coding=utf-8 -*-
import time
from machines.StateMachine import Machine
from appium4droid import webdriver
from appium4droid.common.exceptions import *
from appium4droid.support.ui import WebDriverWait
import random

class MachineLocation(Machine):
    def __init__(self, driver, appname):
        super(MachineLocation, self).__init__(self.enter_location)
        self.driver = driver
        self.appname = appname
        self.reenter_num = 0

    def enter_location(self):
        dr = self.driver
        dr.press_keycode(3)  # back to Home
        time.sleep(1)
        dr.press_keycode(3)  # back to Home
        time.sleep(1)
        dr.find_element_by_name("模拟位置").click()
        time.sleep(1)
        return self.enter_app

    def enter_app(self):
        dr = self.driver
        try:
            dr.find_element_by_name(self.appname).click()
            time.sleep(1)
            print("thats ok")
        except NoSuchElementException as e:
            print("in else")
            return self.reenter
        return self.modify_data

    def modify_data(self):
        dr = self.driver
        #使用GPS模拟
        gps = dr.find_element_by_id("com.rong.xposed.fakelocation:id/gps_switch")
        if gps.text == "关闭":
            gps.click()
            time.sleep(0.5)

        #输入经度
        lat = WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.rong.xposed.fakelocation:id/edit_lat"))
        for x in range(10):
            lat.click()
            time.sleep(0.5)
            dr.press_keycode(123)
            time.sleep(0.5)
            for i in range(40):
                dr.press_keycode(67)
            if lat.text == "":
                break
        lat.send_keys(random.randint(27, 38)+random.randint(0, 1000000)/1000000)
        time.sleep(0.5)

        #输入纬度
        lot = WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.rong.xposed.fakelocation:id/edit_lot"))
        for x in range(10):
            lot.click()
            time.sleep(0.5)
            dr.press_keycode(123)
            time.sleep(0.5)
            for i in range(40):
                dr.press_keycode(67)
            if lot.text == "":
                break
        lot.send_keys(random.randint(107, 117)+random.randint(0, 1000000)/1000000)
        time.sleep(1)
        #即时更新
        dr.find_element_by_id("com.rong.xposed.fakelocation:id/chk_instant_update").click()
        time.sleep(1)
        print("修改定位完成")
        #退出
        dr.press_keycode(4)
        time.sleep(1)
        dr.press_keycode(4)
        time.sleep(1)
        return self.exit

    def reenter(self):
        dr = self.driver
        self.reenter_num += 1
        if self.reenter_num <= 3:
            dr.press_keycode(4)
            time.sleep(1)
            dr.press_keycode(4)
            time.sleep(1)
            print("reenter_location")
            return self.enter_location
        self.reconnect_times = 0
        dr.press_keycode(3)
        return self.exit


if __name__ == "__main__":
    dr = webdriver.Remote()
    time.sleep(2)
    dr.press_keycode(3)
    MachineLocation(dr, "").run()
    # pass
