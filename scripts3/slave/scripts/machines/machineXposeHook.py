#! -*- coding=utf-8 -*-
import time
import random
import re
from appium4droid import webdriver
from appium4droid.common.exceptions import *
from appium4droid.support.ui import WebDriverWait
from machines.StateMachine import Machine


try:
    from util import reset_wifi, alert
except ImportError:
    reset_wifi = lambda: 1
    alert = lambda: 1


class MachineXHook(Machine):
    def __init__(self, driver, tasks=None, chanel='zy', remain_day=1):
        super(MachineXHook, self).__init__(self.setup_task)
        self.driver = driver
        self.second_day = False
        self.enter_excetption_count = 0
        # self.task_schedule = ["uninstall_apk", "clear_data", "find_apk", "record_file", "modify_data"]
        self.task_schedule = [] if tasks is None else tasks
        self.tasks = iter([])
        self.chanel = chanel
        self.remain_day = remain_day
        self.imei = None
        self.try_count = 0

    def setup_task(self):
        tasks = []
        for task in self.task_schedule:
            try:

                method = getattr(self, task)
                tasks.append(method)
            except AttributeError:
                print("no such method: %s" % task)
            self.tasks = iter(tasks)
        return self.enter_xposehook

    def enter_xposehook(self):
        print("enter xpose hook")
        dr = self.driver
        dr.press_keycode(3)  # back to Home
        time.sleep(1)
        dr.press_keycode(3)  # back to Home
        time.sleep(1)
        dr.find_element_by_name("XposeHook").click()
        time.sleep(1)
        try:
            xpath = "//android.support.v7.widget.LinearLayoutCompat/android.widget.ImageView"
            dr.find_element_by_xpath(xpath)
        except NoSuchElementException:
            print("wrong page")
            return self.reenter
        return self.do_task

    def reenter(self):
        self.exit_xposehook()
        return self.enter_xposehook

    def do_task(self):
        try:
            method = next(self.tasks)
            return method
        except StopIteration:
            return self.exit_xposehook

    #一键卸载
    def uninstall_apk(self):
        dr = self.driver
        dr.find_element_by_name("一键卸载").click()
        time.sleep(1)
        dr.find_element_by_name("全选").click()
        time.sleep(1)
        dr.find_element_by_class_name("android.widget.ImageView").click()
        time.sleep(5)
        dr.press_keycode(4)
        time.sleep(1)
        return self.do_task

    #清除数据
    def clear_data(self):
        dr = self.driver
        dr.find_element_by_name("清除数据").click()
        time.sleep(1)
        dr.find_element_by_class_name("android.widget.ImageView").click()
        time.sleep(3)
        dr.press_keycode(4)
        time.sleep(1)
        return self.do_task

    #查找apk
    def find_apk(self):
        dr = self.driver
        dr.find_element_by_name("查找apk").click()
        time.sleep(1)
        dr.find_element_by_class_name("android.widget.ImageView").click()
        time.sleep(5)
        dr.find_element_by_name("删除").click()
        time.sleep(5)
        dr.press_keycode(4)
        time.sleep(1)
        return self.do_task

    #清除记录文件
    def record_file(self):
        dr = self.driver
        dr.find_element_by_name("记录文件").click()
        time.sleep(1)
        dr.find_element_by_name("删除").click()
        time.sleep(3)
        dr.press_keycode(4)
        time.sleep(1)
        return self.do_task

    #更换数据
    def replace_data(self):
        dr = self.driver
        dr.find_element_by_name("修改数据").click()
        time.sleep(1)
        try:
            WebDriverWait(dr, 10).until(lambda d: d.find_element_by_name("本地数据")).click()
            time.sleep(1)
            WebDriverWait(dr, 10).until(lambda d: d.find_elements_by_class_name("android.widget.TextView"))[1].click()
            time.sleep(1)
            randomdate = WebDriverWait(dr, 10).until(lambda d: d.find_elements_by_class_name("android.widget.TextView"))
            randomdate[random.randint(1, randomdate.__len__()-1)].click()
            time.sleep(1)
            WebDriverWait(dr, 30).until(lambda d: d.find_element_by_name("保存")).click()
            time.sleep(1)
        except TimeoutException:
            dr.press_keycode(4)
            time.sleep(1)
            dr.press_keycode(4)
            time.sleep(1)
            dr.find_element_by_name("网络获取失败,退出重新调VPN")
        #获取imei
        edts = dr.find_elements_by_class_name("android.widget.EditText")
        if edts.__len__() > 6:
            self.imei = edts[9].text
        else:
            self.imei = edts[0].text
        print('imei:' + self.imei)
        dr.press_keycode(4)
        time.sleep(1)
        return self.do_task

    #修改数据
    def modify_data(self):
        # chanel_map = {
        #     'zy': 0,
        #     'gm': 1,
        #     'qd': 2,
        # }
        dr = self.driver
        dr.find_element_by_name("修改数据").click()
        time.sleep(1)
        xpath = "//android.widget.Spinner/android.widget.TextView"
        spinners = dr.find_elements_by_xpath(xpath)
        self.chanel = spinners[0].text
        self.remain_day = spinners[1].text.split(":")[1]
        #获取imei
        edts = dr.find_elements_by_class_name("android.widget.EditText")
        if edts.__len__() > 6:
            oldimei = edts[9].text
        else:
            oldimei = edts[0].text

        if self.remain_day == '1':
            dr.find_element_by_name("网络获取").click()
            # dr.find_element_by_name("随机数据").click()
        elif self.remain_day == '0':
            dr.press_keycode(4)
            time.sleep(60)
            return self.modify_data
        else:
            dr.find_element_by_name("本地获取").click()
        try:
            save = WebDriverWait(dr, 15).until(lambda d: d.find_element_by_name("保存"))
            save.click()
        except TimeoutException:
            self.try_count += 1
            if self.try_count <= 3:
                dr.press_keycode(4)
                time.sleep(1)
                dr.press_keycode(4)
                time.sleep(1)
                return self.modify_data
            self.try_count = 0
            dr.press_keycode(4)
            time.sleep(1)
            dr.press_keycode(4)
            time.sleep(1)
            dr.find_element_by_name("网络获取失败,退出重新调VPN")
        time.sleep(1)
        #获取imei
        edts = dr.find_elements_by_class_name("android.widget.EditText")
        if edts.__len__() > 6:
            self.imei = edts[9].text
        else:
            self.imei = edts[0].text
        print('imei:' + self.imei)
        # if oldimei == self.imei:
        #     dr.press_keycode(4)
        #     print("留存已跑完挂机300s")
        #     time.sleep(300)
        #     return self.modify_data
        dr.press_keycode(4)
        time.sleep(1)
        return self.do_task

    #修改数据_随机
    def modify_data_suiji(self):
        dr = self.driver
        dr.find_element_by_name("修改数据").click()
        time.sleep(1)
        xpath = "//android.widget.Spinner/android.widget.TextView"
        spinners = dr.find_elements_by_xpath(xpath)
        self.chanel = spinners[0].text
        self.remain_day = spinners[1].text.split(":")[1]
        #获取imei
        edts = dr.find_elements_by_class_name("android.widget.EditText")
        if edts.__len__() > 6:
            oldimei = edts[9].text
        else:
            oldimei = edts[0].text

        if self.remain_day == '1':
            # dr.find_element_by_name("网络获取").click()
            dr.find_element_by_name("随机数据").click()
        elif self.remain_day == '0':
            dr.press_keycode(4)
            time.sleep(60)
            return self.modify_data
        else:
            dr.find_element_by_name("本地获取").click()
        try:
            save = WebDriverWait(dr, 15).until(lambda d: d.find_element_by_name("保存"))
            save.click()
        except TimeoutException:
            self.try_count += 1
            if self.try_count <= 3:
                dr.press_keycode(4)
                time.sleep(1)
                dr.press_keycode(4)
                time.sleep(1)
                return self.modify_data
            self.try_count = 0
            dr.press_keycode(4)
            time.sleep(1)
            dr.press_keycode(4)
            time.sleep(1)
            dr.find_element_by_name("网络获取失败,退出重新调VPN")
        time.sleep(1)
        #获取imei
        edts = dr.find_elements_by_class_name("android.widget.EditText")
        if edts.__len__() > 6:
            self.imei = edts[9].text
        else:
            self.imei = edts[0].text
        print('imei:' + self.imei)
        # if oldimei == self.imei:
        #     dr.press_keycode(4)
        #     print("留存已跑完挂机300s")
        #     time.sleep(300)
        #     return self.modify_data
        dr.press_keycode(4)
        time.sleep(1)
        return self.do_task

    #再激活
    def is0(self):
        dr = self.driver
        dr.find_element_by_name("修改数据").click()
        time.sleep(1)
        xpath = "//android.widget.Spinner/android.widget.TextView"
        spinners = dr.find_elements_by_xpath(xpath)
        self.remain_day = spinners[1].text.split(":")[1]

        if self.remain_day == '0':
            WebDriverWait(dr, 10).until(lambda d: d.find_element_by_name("本地数据")).click()
            time.sleep(1)
            lastdata = WebDriverWait(dr, 10).until(lambda d: d.find_elements_by_class_name("android.widget.TextView"))
            lastdata[lastdata.__len__()-1].click()
            # lastdata[1].click()
            time.sleep(1)
            for i in range(20):
                dr.swipe(300, 800, 300, 200)
                time.sleep(1)
                datetext = WebDriverWait(dr, 10).until(lambda d: d.find_elements_by_class_name("android.widget.TextView"))
                match = None
                for x in range(datetext.__len__()):
                    print("现在钟数:%s点，查找%s点前数据" % (time.localtime().tm_hour, time.localtime().tm_hour-3))
                    if time.localtime().tm_mday > 9:
                        match = re.search(r'2016-03-%s %s(.+)' % (time.localtime().tm_mday, time.localtime().tm_hour-3), datetext[x].text)
                    else:
                        match = re.search(r'2016-03-0%s %s(.+)' % (time.localtime().tm_mday, time.localtime().tm_hour-3), datetext[x].text)
                    if match:
                        print("查询成功,数据是:%s" % match.group(0))
                        break
                    if time.localtime().tm_mday > 9:
                        match = re.search(r'2016-03-%s %s(.+)' % (time.localtime().tm_mday, time.localtime().tm_hour-2), datetext[x].text)
                    else:
                        match = re.search(r'2016-03-0%s %s(.+)' % (time.localtime().tm_mday, time.localtime().tm_hour-2), datetext[x].text)
                    if match:
                        print("查询成功,数据是:%s" % match.group(0))
                        break
                    if time.localtime().tm_mday > 9:
                        match = re.search(r'2016-03-%s %s(.+)' % (time.localtime().tm_mday, time.localtime().tm_hour-1), datetext[x].text)
                    else:
                        match = re.search(r'2016-03-0%s %s(.+)' % (time.localtime().tm_mday, time.localtime().tm_hour-1), datetext[x].text)
                    if match:
                        print("查询成功,数据是:%s" % match.group(0))
                        break
                if match:
                    print("开始寻找3小时前数据")
                    break
            for x in range(random.randint(1, 5)):
                dr.swipe(300, random.randint(200, 400), 300, random.randint(500, 700))
                time.sleep(1)
            time.sleep(1)
            randomdate = WebDriverWait(dr, 10).until(lambda d: d.find_elements_by_class_name("android.widget.TextView"))
            randomdate[random.randint(1, randomdate.__len__()-1)].click()
            time.sleep(1)
            WebDriverWait(dr, 30).until(lambda d: d.find_element_by_name("保存")).click()
            time.sleep(1)
            #获取imei
            edts = dr.find_elements_by_class_name("android.widget.EditText")
            if edts.__len__() > 6:
                self.imei = edts[9].text
            else:
                self.imei = edts[0].text

            print('imei:' + self.imei)
            dr.press_keycode(4)
            time.sleep(1)
            return self.exit
        dr.press_keycode(4)
        time.sleep(1)
        return self.do_task

    #更换运营商
    def replace_operator(self):
        dr = self.driver
        dr.find_element_by_name("修改数据").click()
        time.sleep(2)
        dr.swipe(200, 1000, 200, 850)
        time.sleep(1)
        edts = WebDriverWait(dr, 10).until(lambda d: d.find_elements_by_class_name("android.widget.EditText"))
        #修改isim
        oldisim = edts[3].text
        newisim = '46003'+oldisim[5: 15]
        for x in range(5):
            edts[3].click()
            for i in range(5):
                dr.press_keycode(67)
            if not edts[3].text:
                edts[3].send_keys(newisim)
                break
        #修改运营商
        for x in range(5):
            edts[4].click()
            for i in range(5):
                dr.press_keycode(67)
            if not edts[4].text:
                edts[4].send_keys(46003)
                break
        #修改网络类型名
        for x in range(5):
            edts[5].click()
            for i in range(10):
                dr.press_keycode(67)
            if not edts[5].text:
                edts[5].send_keys("中国电信")
                break
        time.sleep(1)
        dr.press_keycode(4)
        time.sleep(1)
        return self.do_task

    #退出007
    def exit_xposehook(self):
        dr = self.driver
        # for _ in range(5):
        #     dr.press_keycode(4)
        #     time.sleep(1)
        xpath = "//android.view.View[@package='com.miui.home']"
        Home = dr.find_elements_by_xpath(xpath)  # 寻找miui home界面
        while Home == []:
            dr.press_keycode(4)
            time.sleep(1)
            Home = dr.find_elements_by_xpath(xpath)  # 寻找miui home界面
        return self.exit


if __name__ == "__main__":
    wd = webdriver.Remote()
    mxh = MachineXHook(wd)
    mxh.task_schedule = ["uninstall_apk", "clear_data", "find_apk", "record_file", "modify_data"]

    mxh.run()
