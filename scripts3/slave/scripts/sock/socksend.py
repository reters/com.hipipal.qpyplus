from socket import *
import os
import struct
import re
import time

def send_file(device, filename, addr):
    ADDR = (addr, 1234)
    BUFSIZE = 10240
    FILEINFO_SIZE = struct.calcsize('128sI')
    sendSock = socket(AF_INET, SOCK_STREAM)
    sendSock.connect(ADDR)
    try:
        fhead = struct.pack('128sI', (device+filename).encode('utf-8'), os.stat("/sdcard/1/"+filename).st_size)
    except:
        fhead = struct.pack('128sI', (device+filename).encode('utf-8'), os.stat(filename).st_size)
    sendSock.send(fhead)
    try:
        fp = open("/sdcard/1/"+filename, 'rb')
    except:
        fp = open(filename, 'rb')
    while 1:
        filedata = fp.read(BUFSIZE)
        if not filedata:
            break
        sendSock.send(filedata)
    print("文件传送完毕，正在断开连接...")
    fp.close()
    sendSock.close()
    print("连接已关闭...")


if __name__ == '__main__':
    file = ["userhuajiao.log", "usershanghai.log", "timehuajiao.log", "timeshanghai2.log"]
    addr = '192.168.1.76'
    try:
        with open('/sdcard/device.txt', 'r') as f:
            selectuser = f.read()
    except:
        with open('device.txt', 'r') as f:
            selectuser = f.read()
    device = re.search(r'device:([0-9a-zA-Z\.]+)', selectuser).group(1)
    # for num in range(20): #最多可发送文件数量
        # filename = re.search(r'filename%s:([0-9a-zA-Z\.]+)' % num, selectuser)
    for filename in file: #最多可发送文件数量
        if filename:
            if os.path.exists(filename) or os.path.exists('/sdcard/1/' + filename): #检测文件是否存在,不存在不发送
                try:
                    send_file(device, filename, addr)
                except Exception as e:
                    print(e)
            else:
                print("not find the file:%s" % filename)
        else:
            break
        time.sleep(2)