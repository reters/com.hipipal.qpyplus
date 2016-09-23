#! -*- coding=utf-8 -*-
import androidhelper
import time
import json
import os
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

#震动
def alert():
    now = datetime.now().hour
    if now > 7:
        # droid.vibrate(8000)  # 手机震动8000毫秒
        # droid.mediaPlay("/sdcard/com.hipipal.qpyplus/scripts3/res/killbill.mp3")  # 播放音乐
        time.sleep(30)
        # droid.mediaPlayClose()

#震动
def shock(times):
    droid.vibrate(times*1000)  # 手机震动8000毫秒
    # droid.mediaPlay("/sdcard/com.hipipal.qpyplus/scripts3/res/killbill.mp3")  # 播放音乐
    # time.sleep(30)
    # droid.mediaPlayClose()

#后台运行python2文件
def run_qpy2_script(script, args=None):
    su = subprocess.Popen(["su"], stdin=subprocess.PIPE)
    # cmd = "sh /data/data/com.hipipal.qpyplus/files/bin/qpython.sh  /sdcard/com.hipipal.qpyplus/scripts/guagua_captcha.py"
    cmd = "sh /data/data/com.hipipal.qpyplus/files/bin/qpython.sh  /sdcard/com.hipipal.qpyplus/scripts/%s" % script
    if args:
        cmd = cmd + " " + args
    ret = su.communicate(cmd.encode())
    return ret


#后台运行python3文件
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

#重启wifi
def reset_wifi():
    print("reset WiFi")
    droid.toggleWifiState()
    sleep_countdown(10)
    droid.toggleWifiState()
    sleep_countdown(10)

#关闭/打开wifi
def replace_wifi():
    print("replace WiFi")
    droid.toggleWifiState()
    sleep_countdown(1)


#截屏
def screenshot(path):
    su = subprocess.Popen("su", stdin=subprocess.PIPE)
    cmd = "/system/bin/screencap -p %s" % path
    print("***************************\n" + cmd)
    su.communicate(cmd.encode())

#关闭后台
def killapp(path):
    su = subprocess.Popen("su", stdin=subprocess.PIPE)
    # cmd = "/system/bin/kill %s" % path
    cmd = "/system/bin/am force-stop %s" % path
    print("***************************\n" + cmd)
    su.communicate(cmd.encode())

#安装
def install(path):
    su = subprocess.Popen("su", stdin=subprocess.PIPE)
    cmd = "/system/bin/pm install /sdcard/%s" % path
    print("***************************\n" + cmd)
    su.communicate(cmd.encode())
    # PATH 指 APK文件绝对路径和文件名。
    # 例如：
    # pm install /data/3dijoy_fane.apk

#卸载
def uninstall(path):
    su = subprocess.Popen("su", stdin=subprocess.PIPE)
    cmd = "/system/bin/pm uninstall %s" % path
    print("***************************\n" + cmd)
    su.communicate(cmd.encode())
    # pm uninstall 包名。
    # 例如：
    # pm uninstall com.TDiJoy.fane

#复制文件
def copyfile(file1, file2):
    su = subprocess.Popen("su", stdin=subprocess.PIPE)
    cmd = "/system/bin/cp -r %s %s" % (file1, file2)
    print("***************************\n" + cmd)
    su.communicate(cmd.encode())

#移动文件
def movefile(file1, file2):
    su = subprocess.Popen("su", stdin=subprocess.PIPE)
    cmd = "/system/bin/mv %s %s" % (file1, file2)
    print("***************************\n" + cmd)
    su.communicate(cmd.encode())

#删除文件
def removefile(file):
    su = subprocess.Popen("su", stdin=subprocess.PIPE)
    cmd = "/system/bin/rm -r %s" % file
    print("***************************\n" + cmd)
    su.communicate(cmd.encode())

#输入文字到剪贴板
def settext_clipboard(text):
    su = subprocess.Popen("su", stdin=subprocess.PIPE)
    cmd = "/system/bin/am broadcast -a clipper.set -e text %s" % text
    print("***************************\n" + cmd)
    su.communicate(cmd.encode())

def find_file_num(path):
    count = 0
    # path = r'/sdcard/1/1touxiang/'
    for root, dirs, files in os.walk(path):
        fileLength = len(files)
        if fileLength != 0:
            count = count + fileLength
    print("File number is: %d" % count)
    return count


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
