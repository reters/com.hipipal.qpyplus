#! -*- coding=utf-8 -*-
import json
import logging
import random
import threading
import time
import requests
from machines.machine008 import Machine008
from appium4droid import webdriver
from appium4droid.common.exceptions import *
from appium4droid.support.ui import WebDriverWait
from bootstrap import setup_boostrap

# logging.basicConfig(filename='/sdcard/qpy.log')

try:
    from util import reset_wifi, alert
except ImportError:
    reset_wifi = lambda: 1
    alert = lambda: 1

api_url = "http://m008.meiriq.com/phone"

key_map = {
    "getSimSerialNumber": "sim_card_id",
    "getSimState": "status",
    "getPhoneType": "type",
    "getMacAddress": "mac",
    "getString": "android_id",
    "getLine1Number": "phone_number",
    "getDeviceId": "imei",
    "getSimOperator": "operator",
    "getRadioVersion": "hardware_version",
    "getNetworkOperatorName": "networks_type_name",
    "getNetworkType": "networks_type_id",
    "getSubscriberId": "imsi",
    "getSSID": "wireless_router_name",
    "getBSSID": "wireless_router_address",
    "RELEASE": "android_version",
    "SDK": "system_value",
    "ARCH": "system_architecture",
    "getMetrics": "resolution",
    "BRAND": "brand",
    "MODEL": "model_number",
    "PRODUCT": "product_name",
    "MANUFACTURER": "manufacturer",
    "DEVICE": "device_number",
    "setCpuName": "cpu",
    "HARDWARE": "hardware",
    "FINGERPRINT": "fingerprint_key",
    "SERIAL": "serial_interface_number",
    "getAddress": "bluetooth_address",
    "getIpAddress": "local_area_networks_ip",
}
xpath0 = "//android.widget.ScrollView/android.widget.LinearLayout/*"
xpath = "//android.widget.ScrollView/android.widget.LinearLayout/android.widget.EditText"
xpath2 = "//android.widget.ScrollView/android.widget.LinearLayout/android.widget.TextView"
xpath3 = "//android.widget.ScrollView/android.widget.LinearLayout/android.widget.TextView/following-sibling::*"
xpath4 = "//following-sibling::*"
xpath5 = "//android.widget.TextView[@text='android_id']/following::*"


class Primary008(Machine008):
    def __init__(self, driver):
        super(Primary008, self).__init__(driver)
        self.task_schedule = ["setup_dir"]
        self.tmpfile = "tmp"


    def setup_dir(self):
        dr = self.driver
        dr.press_keycode(4)
        time.sleep(1)
        ##008修改数据的图标
        WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("com.soft.apk008v:id/main_centerImg")).click()
        time.sleep(1)
        WebDriverWait(dr, 30).until(lambda d: d.find_element_by_name("随机生成"))
        # WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("历史记录")).click()
        # time.sleep(0.5)
        # WebDriverWait(dr, 5).until(lambda d: d.find_element_by_class_name("android.widget.ImageButton")).click()
        # time.sleep(0.5)
        # WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("新建分类")).click()
        # time.sleep(0.5)
        # edt = WebDriverWait(dr, 15).until(lambda d: d.find_element_by_class_name("android.widget.EditText"))
        # edt.send_keys(self.tmpfile)
        # time.sleep(0.5)
        # WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("确定")).click()
        # time.sleep(0.5)
        # WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("切换分类")).click()
        # time.sleep(0.5)
        # WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name(self.tmpfile)).click()
        # time.sleep(1)
        # dr.press_keycode(4)
        # time.sleep(1)
        return self.get_data_from_server()

    def get_data_from_server(self):
        # find_value = lambda x: dr.find_element_by_xpath("//android.widget.TextView[contains(@text, '%s')]/following::*" % x).text
        dr = self.driver
        try:
            for x in range(50):
                WebDriverWait(dr, 30).until(lambda d: d.find_element_by_name("从网络获取数据")).click()
                try:
                    WebDriverWait(dr, 60).until(lambda d: d.find_element_by_name("保存")).click()
                except TimeoutException:
                    try:
                        WebDriverWait(dr, 60).until(lambda d: d.find_element_by_name("确定")).click()
                    except TimeoutException:
                        pass
                    logging.info("fetch data from server timeout")
                    continue
                # time.sleep(1)
            return self.upload_data
        except Exception as e:
            print(e)
            return self.upload_data

    def upload_data(self):
        def translate(origin_data):
            key_map = {
                "getSimSerialNumber": "sim_card_id",
                "getSimState": "status",
                "getPhoneType": "type",
                "getMacAddress": "mac",
                "getString": "android_id",
                "getLine1Number": "phone_number",
                "getDeviceId": "imei",
                "getSimOperator": "operator",
                "getRadioVersion": "hardware_version",
                "getNetworkOperatorName": "networks_type_name",
                "getNetworkType": "networks_type_id",
                "getSubscriberId": "imsi",
                "getSSID": "wireless_router_name",
                "getBSSID": "wireless_router_address",
                "RELEASE": "android_version",
                "SDK": "system_value",
                "ARCH": "system_architecture",
                "getMetrics": "resolution",
                "BRAND": "brand",
                "MODEL": "model_number",
                "PRODUCT": "product_name",
                "MANUFACTURER": "manufacturer",
                "DEVICE": "device_number",
                "setCpuName": "cpu",
                "HARDWARE": "hardware",
                "FINGERPRINT": "fingerprint_key",
                "SERIAL": "serial_interface_number",
                "getAddress": "bluetooth_address",
                "getIpAddress": "local_area_networks_ip",
            }
            print("on upload procedure")
            data = {}
            for k in origin_data:
                api_key = key_map.get(k)
                if api_key:
                    data[api_key] = origin_data[k]
            return data

        with open("/sdcard/kind/%s" % self.tmpfile) as f:
            logging.info("in upload process")
            dataset = json.loads(f.read())
            dd = []
            for origin_data in dataset:
                data = translate(origin_data)
                print(data)
                logging.info(data)
                dd.append(data)
                try:
                    requests.post(api_url, data=data)
                    print("data has send")
                    logging.info("data has send")
                except Exception as e:
                    print(e)
                    logging.exception(e)
                    # try:
                    #     os.remove("/sdcard/kind/%s" % self.tmpfile)
                    # except:
                    #     logging.exception("no such file")
        # return self.reenter_008
        return self.del_current_data_dir

    def del_current_data_dir(self):
        dr = self.driver
        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_name("历史记录")).click()
        time.sleep(0.5)
        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_class_name("android.widget.ImageButton")).click()
        time.sleep(0.5)
        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_name("清空当前分类")).click()
        time.sleep(0.5)
        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_name("确定")).click()
        return self.reenter_008

    def on_exception(self):
        pass
        # TODO


if __name__ == "__main__":
    bootstrap = threading.Thread(target=setup_boostrap)
    bootstrap.start()
    time.sleep(3)
    dr = webdriver.Remote()

    m = Primary008(dr)
    while True:
        try:
            m.run()
        except Exception as e:
            logging.exception(e)
