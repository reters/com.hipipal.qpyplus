#! -*- coding=utf-8 -*-
import time
from appium4droid import webdriver
from appium4droid.common.exceptions import *
from appium4droid.support.ui import WebDriverWait
# from StateMachine import  Machine
from machines.StateMachine import Machine

try:
    from util import reset_wifi, alert
except ImportError:
    reset_wifi = lambda: 1
    alert = lambda: 1


class Machine008(Machine):
    def __init__(self, driver, tasks=None, **kwargs):
        super(Machine008, self).__init__(self.enter_008)
        self.driver = driver
        self.second_day = False
        self.enter_excetption_count = 0
        # self.task_schedule = ["uninstall_apk", "delete_dir", "delete_apk", "clear_apk_data", "listen_files", "listen_system_values", "do_all_one_key"]
        self.task_schedule = ["uninstall_apk", "do_all_one_key"] if tasks is None else tasks
        self.tasks = iter([])
        self.imei = None

    def enter_008(self):
        print("enter 008")
        dr = self.driver
        dr.press_keycode(3)  # back to Home
        time.sleep(1)
        dr.press_keycode(3)  # back to Home
        time.sleep(1)
        dr.find_element_by_name("008神器0301").click()
        try:
            WebDriverWait(dr, 10).until(lambda d: d.find_element_by_name("请检查当前网络是否可用"))
            time.sleep(1)
            WebDriverWait(dr, 10).until(lambda d: d.find_element_by_name("确定")).click()
            time.sleep(1)
            return self.onEnterException
        except TimeoutException:
            pass
        try:
            WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("确定")).click()
            return self.onEnterException
        except TimeoutException:
            pass
        try:
            toolbox = WebDriverWait(dr, 30).until(lambda d: d.find_element_by_name("工具箱"))
            # toolbox.click()
        except TimeoutException:
            return self.onEnterException

        return self.enter_toolbox

    def enter_toolbox(self):
        dr = self.driver
        dr.find_element_by_name("工具箱").click()
        time.sleep(2)
        try:
            dr.find_element_by_name("一键静默卸载")
        except NoSuchElementException:
            print("try toolbox again")
            dr.find_element_by_name("工具箱").click()
            time.sleep(3)
        # return self.uninstall_apk
        tasks = []
        for task in self.task_schedule:
            try:
                method = getattr(self, task)
                tasks.append(method)
            except AttributeError:
                print("no such method: %s" % task)
            self.tasks = iter(tasks)

        return self.do_toolbox_task

    def set_toolbox_task(self, task_list):
        self.task_schedule = task_list

    def do_toolbox_task(self):
        try:
            method = next(self.tasks)
            return method
        except StopIteration:
            return self.exit_008

    def uninstall_apk(self):
        dr = self.driver
        dr.find_element_by_name("一键静默卸载").click()
        time.sleep(1)
        dr.find_element_by_name("重置").click()
        time.sleep(1)
        dr.find_element_by_name("选择反选").click()
        time.sleep(1)
        dr.find_element_by_name("一键卸载").click()
        ## maybe should try and except here
        WebDriverWait(dr, 35).until_not(lambda d: d.find_elements_by_class_name("android.widget.CheckBox") != [])
        dr.press_keycode(4)  # keypress back
        time.sleep(0.5)
        # if self.del_dir:
        #     return self.delete_dir
        # else:
        #     return self.delete_apk
        return self.do_toolbox_task

    def delete_dir(self):
        dr = self.driver
        dr.find_element_by_name("一键删除文件夹").click()
        time.sleep(1)
        dr.find_element_by_name("删除文件夹").click()
        time.sleep(2)
        dr.press_keycode(4)  # keypress back
        time.sleep(0.5)
        # return self.delete_apk
        return self.do_toolbox_task

    def delete_apk(self):
        dr = self.driver
        dr.find_element_by_name("一键删除apk").click()
        time.sleep(1)
        dr.find_element_by_name("开始查找").click()
        # time.sleep(4)
        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_name("删除")).click()
        # dr.find_element_by_name("删除").click()
        time.sleep(2)
        dr.press_keycode(4)  # keypress back
        time.sleep(0.5)

        # return self.do_all_one_key
        return self.do_toolbox_task

    def clear_apk_data(self):
        dr = self.driver
        dr.find_element_by_name("一键数据清除（同时关闭应用）").click()
        time.sleep(1)
        dr.find_element_by_name("一键清除数据").click()
        time.sleep(2.5)
        dr.press_keycode(4)
        time.sleep(1)
        # dr.press_keycode(4)
        # time.sleep(1)
        # return self.remain_control
        return self.do_toolbox_task

    def listen_files(self):
        dr = self.driver
        dr.find_element_by_name("监听应用文件操作").click()
        time.sleep(1)
        dr.find_element_by_name("删除记录中的文件").click()
        time.sleep(2)
        dr.press_keycode(4)
        time.sleep(1)
        return self.do_toolbox_task

    def listen_system_values(self):
        dr = self.driver
        dr.find_element_by_name("监听系统值设置").click()
        time.sleep(1)
        dr.find_element_by_name("清除所选").click()
        time.sleep(2)
        dr.press_keycode(4)
        time.sleep(1)
        return self.do_toolbox_task

    def do_all_one_key(self):
        dr = self.driver
        dr.find_element_by_name("快捷操作").click()
        time.sleep(1)
        dr.find_element_by_name("一键操作").click()
        time.sleep(5)

        dr.press_keycode(4)  # keypress back
        time.sleep(0.5)
        dr.press_keycode(4)  # keypress back
        time.sleep(0.5)
        # dr.press_keycode(4)  # keypress back
        # time.sleep(0.5)
        # dr.find_element_by_name("确定").click()
        # time.sleep(1)
        # print("008 OK")
        # return self.Exit
        return self.do_toolbox_task

    def modify_data(self):
        dr = self.driver
        btmodify = WebDriverWait(dr, 30).until(lambda d: d.find_elements_by_class_name("android.widget.ImageView"))
        btmodify[1].click()
        time.sleep(1)
        dr.find_element_by_name("从网络获取数据").click()
        save = WebDriverWait(dr, 30).until(lambda d: d.find_element_by_name("保存"))
        save.click()
        time.sleep(1)
        dr.press_keycode(4)
        time.sleep(1)
        return self.do_toolbox_task
    def onEnterException(self):
        self.enter_excetption_count = self.enter_excetption_count + 1
        if self.enter_excetption_count > 3:
            alert()
            reset_wifi()
            self.enter_excetption_count = 0
        return self.reenter_008

    def exit_0082(self):
        print("Enter 008 failed!! going to exit")
        dr = self.driver
        Home_id = "com.miui.home:id/cell_layout"
        xpath = "//android.view.View[@package='com.miui.home']"
        print(Home_id)
        Home = dr.find_elements_by_xpath(xpath)  # 寻找miui home界面
        count = 0
        while Home == []:
            dr.press_keycode(4)
            time.sleep(1)
            exit_panel = dr.find_elements_by_name("是否退出008神器0301")
            if exit_panel != []:
                dr.find_element_by_name("确定").click()
            Home = dr.find_elements_by_xpath(xpath)  # 寻找miui home界面
            count = count + 1
        time.sleep(1)

    def exit_008(self):
        dr = self.driver
        exit_panel = dr.find_elements_by_name("是否退出008神器0301")
        count = 0
        while exit_panel == []:
            dr.press_keycode(4)
            time.sleep(2)
            exit_panel = dr.find_elements_by_name("是否退出008神器0301")
            count = count + 1
        else:
            print("found Exit")
            time.sleep(1)
            dr.find_element_by_name("确定").click()
            time.sleep(1)
        return self.exit

    def reenter_008(self):
        print("Going to exit and reenter")
        dr = self.driver
        Home_id = "com.miui.home:id/cell_layout"
        home_xpath = "//android.view.View[@package='com.miui.home']"
        print(Home_id)
        Home = dr.find_elements_by_xpath(home_xpath)  # 寻找miui home界面
        count = 0
        while Home == []:
            dr.press_keycode(4)
            time.sleep(1)
            exit_panel = dr.find_elements_by_name("是否退出008神器0301")
            xpath = "//android.widget.TextView[contains(@text, '连接服务器失败')]"
            connect_error = dr.find_elements_by_xpath(xpath)
            if exit_panel + connect_error != []:
                dr.find_element_by_name("确定").click()
            Home = dr.find_elements_by_xpath(home_xpath)  # 寻找miui home界面
            count = count + 1
        time.sleep(1)
        return self.enter_008
# 连接服务器失败
    def remain_control(self):
        dr = self.driver
        dr.press_keycode(4)
        time.sleep(1)
        WebDriverWait(dr, 5).until(
            lambda d: d.find_element_by_id("com.soft.apk008v:id/main_centerImg")).click()  ##008修改数据的图标
        # dr.find_element_by_id("com.soft.apk008v:id/main_centerImg").click()  ##008修改数据的图标o
        time.sleep(1)
        dr.find_element_by_id("com.soft.apk008v:id/menu_remainControl").click()  ## 留存控制按键
        time.sleep(1)
        dr.find_element_by_name("下一条数据").click()
        time.sleep(1)
        try:
            dr.find_element_by_name("保存").click()  # 若到达100%则无法返回上一个页面
        except Exception as e:
            self.second_day = False
            # dr.find_element_by_name("保存").click()
            dr.press_keycode(4)  # keypress back
            time.sleep(1)
            dr.press_keycode(4)  # keypress back
            time.sleep(0.5)
            dr.press_keycode(4)  # keypress back
            time.sleep(0.5)
            dr.find_element_by_name("确定").click()
            print("Mode Switch!@")
            return self.enter_008
            # raise NoHistoryRecordException

        return self.exit_008

    def ExceptinOccur(self):
        self.running = False
        print("ExceptinOccur!!!")
        self.driver.press_keycode(3)
        return None

    def change_date_dir(self):
        dr = self.driver
        dr.press_keycode(4)  # back to Home
        time.sleep(1)
        dr.find_element_by_id("com.soft.apk008v:id/main_centerImg").click()  ##008修改数据的图标
        WebDriverWait(dr, 30).until(lambda d: d.find_element_by_name("随机生成")).click()
        # dr.find_element_by_name("随机生成").click()
        time.sleep(1)
        dr.find_element_by_name("保存").click()
        time.sleep(3)
        try:
            dr.find_element_by_name("确定").click()
        except Exception as e:
            pass
        time.sleep(1)

        dr.press_keycode(4)  # keypress back
        time.sleep(0.5)
        dr.press_keycode(4)  # keypress back
        time.sleep(0.5)
        dr.find_element_by_name("确定").click()
        time.sleep(1)

        print("Something has changed")
        return self.exit


class Second008(Machine008):
    def __init__(self, dr):
        super(Second008, self).__init__(dr)
        self.second_day = True
        self.second_tasks = ["uninstall_apk", "clear_apk_data", "remain_control"]
        self.first_tasks = ["uninstall_apk", "do_all_one_key"]
        self.task_schedule = self.second_tasks

    # def enter_toolbox(self):
    #     return super(Second008, self).enter_toolbox()

    def remain_control(self):
        dr = self.driver
        dr.press_keycode(4)
        time.sleep(1)
        WebDriverWait(dr, 5).until(
            lambda d: d.find_element_by_id("com.soft.apk008v:id/main_centerImg")).click()  ##008修改数据的图标
        # dr.find_element_by_id("com.soft.apk008v:id/main_centerImg").click()  ##008修改数据的图标o
        time.sleep(1)
        dr.find_element_by_id("com.soft.apk008v:id/menu_remainControl").click()  ## 留存控制按键
        time.sleep(1)

        dr.find_element_by_name("下一条数据").click()
        time.sleep(1)
        try:
            dr.find_element_by_name("保存").click()  # 若到达100%则无法返回上一个页面
        except Exception as e:
            self.second_day = False
            self.task_schedule = self.first_tasks
            dr.press_keycode(4)  # keypress back
            time.sleep(1)
            dr.press_keycode(4)  # keypress back
            time.sleep(0.5)
            # dr.press_keycode(4)  # keypress back
            # time.sleep(0.5)
            # dr.find_element_by_name("确定").click()
            print("Mode Switch!@")
            return self.enter_toolbox
            # raise NoHistoryRecordException

        # dr.press_keycode(4)  # keypress back
        # time.sleep(0.5)
        # dr.press_keycode(4)  # keypress back
        # time.sleep(0.5)
        # dr.find_element_by_name("确定").click()
        # time.sleep(1)
        # return self.Exit
        return self.exit_008


def change_date_dir(driver):
    dr = driver
    dr.press_keycode(3)  # back to Home
    time.sleep(1)
    dr.press_keycode(3)  # back to Home
    time.sleep(1)
    dr.find_element_by_name("008神器0301").click()
    WebDriverWait(dr, 30).until(
        lambda d: d.find_element_by_id("com.soft.apk008v:id/main_centerImg")).click()  ##008修改数据的图标
    WebDriverWait(dr, 30).until(lambda d: d.find_element_by_name("随机生成")).click()
    time.sleep(1)
    dr.find_element_by_name("保存").click()
    time.sleep(2)
    try:
        dr.find_element_by_name("确定").click()
    except Exception as e:
        pass
    time.sleep(1)

    dr.press_keycode(4)  # keypress back
    time.sleep(0.5)
    dr.press_keycode(4)  # keypress back
    time.sleep(0.5)
    dr.find_element_by_name("确定").click()
    time.sleep(1)
    print("Something has changed")


if __name__ == "__main__":
    dr = webdriver.Remote()
    time.sleep(2)
    dr.press_keycode(3)
    #
    # # m = Machine008(dr)
    # m = Second008(dr)
    # while True:
    #     m.run()
    #     print("m.second= %s" % m.second_day)
    #     print("Again")

    m = Machine008(dr)
    m.task_schedule = ["change_date_dir"]
    m.run()
