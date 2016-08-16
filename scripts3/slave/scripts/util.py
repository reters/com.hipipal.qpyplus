#! -*- coding=utf-8 -*-
import androidhelper
import time
import json
import logging
import subprocess
from datetime import datetime

# logging.basicConfig(filename='example.log')

droid = androidhelper.Android()

deviceInfo = {}
try:
    f = open("/sdcard/device.txt", 'r')
    deviceInfo = json.loads(f.read())
    print(deviceInfo)
except Exception as e:
    print(e)
    deviceInfo = {}


def alert():
    now = datetime.now().hour
    if now > 7:
        # droid.vibrate(8000)  # 手机震动8000毫秒
        # droid.mediaPlay("/sdcard/com.hipipal.qpyplus/scripts3/res/killbill.mp3")  # 播放音乐
        time.sleep(30)
        # droid.mediaPlayClose()

def shock(times):
    droid.vibrate(times*1000)  # 手机震动8000毫秒
    # droid.mediaPlay("/sdcard/com.hipipal.qpyplus/scripts3/res/killbill.mp3")  # 播放音乐
    # time.sleep(30)
    # droid.mediaPlayClose()

def run_qpy2_script(script, args=None):
    su = subprocess.Popen(["su"], stdin=subprocess.PIPE)
    # cmd = "sh /data/data/com.hipipal.qpyplus/files/bin/qpython.sh  /sdcard/com.hipipal.qpyplus/scripts/guagua_captcha.py"
    cmd = "sh /data/data/com.hipipal.qpyplus/files/bin/qpython.sh  /sdcard/com.hipipal.qpyplus/scripts/%s" % script
    if args:
        cmd = cmd + " " + args
    ret = su.communicate(cmd.encode())
    return ret

def run_qpy3_script(script, args=None):
    su = subprocess.Popen(["su"], stdin=subprocess.PIPE)
    cmd = "sh /data/data/com.hipipal.qpy3/files/bin/qpython.sh  /sdcard/com.hipipal.qpyplus/scripts3/slave/scripts/%s" % script
    if args:
        cmd = cmd + " " + args
    ret = su.communicate(cmd.encode())
    return ret

def show_message(msg):
    # print(msg)
    droid.makeToast(msg)


def check_crash(driver):
    try:
        comfirm = driver.find_element_by_name("确定")
    except Exception as e:
        print(e)
    else:
        comfirm.click()
        time.sleep(1)


def sleep_countdown(t):
    while t > 0:
        t = t - 5
        time.sleep(5)
        droid.makeToast("remain %s s" % t)


def reset_wifi():
    print("reset WiFi")
    droid.toggleWifiState()
    sleep_countdown(20)
    droid.toggleWifiState()
    sleep_countdown(20)

def replace_wifi():
    print("replace WiFi")
    droid.toggleWifiState()
    sleep_countdown(20)

def screenshot(path):
    su = subprocess.Popen("su", stdin=subprocess.PIPE)
    cmd = "/system/bin/screencap -p %s" % path
    print("***************************\n" + cmd)
    su.communicate(cmd.encode())

def killapp(path):
    su = subprocess.Popen("su", stdin=subprocess.PIPE)
    # cmd = "/system/bin/kill %s" % path
    cmd = "/system/bin/am force-stop %s" % path
    print("***************************\n" + cmd)
    su.communicate(cmd.encode())

def install(path):
    su = subprocess.Popen("su", stdin=subprocess.PIPE)
    cmd = "/system/bin/pm install /sdcard/%s" % path
    print("***************************\n" + cmd)
    su.communicate(cmd.encode())
    # PATH 指 APK文件绝对路径和文件名。
    # 例如：
    # pm install /data/3dijoy_fane.apk

def uninstall(path):
    su = subprocess.Popen("su", stdin=subprocess.PIPE)
    cmd = "/system/bin/pm uninstall %s" % path
    print("***************************\n" + cmd)
    su.communicate(cmd.encode())
    # pm uninstall 包名。
    # 例如：
    # pm uninstall com.TDiJoy.fane


if __name__ == "__main__":
    pass
    # account = None
    # try:
    #     f = open("/sdcard/device.txt", 'r')
    #     device_info = json.loads(f.read())
    #     print(device_info)
    #     account = device_info['Account']
    # except Exception as e:
    #     print(e)
    #     print("device.txt not found")
    #     account = "11011011011"
    #
    # print("Account --> %s" % account)
    #
    # droid.toggleWifiState()
    # sleep_countdown(16)
    # droid.toggleWifiState()

    # while True:
    #     time.sleep(2)
    #     droid.makeToast("gagagagaga")

    # screenshot("/sdcard/ff.png")
    import requests
    # screenshot("/sdcard/screen.png")
    # run_qpy2_script("guagua_captcha.py")
    # r = requests.get("http://127.0.0.1:8080/captcha?target=captcha.png")
    # res = r.json()
    # if not res['ret']:
    #     pass
    # print(res.content)
