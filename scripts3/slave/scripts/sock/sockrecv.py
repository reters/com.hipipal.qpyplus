from socket import *
import struct
import time
import re


def recv_file(addr):
    ADDR = (addr, 1234)
    BUFSIZE = 10240
    FILEINFO_SIZE = struct.calcsize('128sI')
    recvSock = socket(AF_INET, SOCK_STREAM)
    recvSock.bind(ADDR)
    recvSock.listen(True)
    print("等待连接...")
    conn, addr = recvSock.accept()
    print("客户端已连接—> ", addr)
    fhead = conn.recv(FILEINFO_SIZE)
    filename, filesize = struct.unpack('128sI', fhead)
    # print(filename, len(filename), type(filename))
    # print(filesize)
    #截取传送文件名
    filename = filename.decode().strip('\00')
    #分类存放文档
    regrex = r'%s([0-9a-zA-Z]+).log' % filename[2:6]
    match = re.search(regrex, filename)
    try:
        fp = open("/sdcard/loginfo/"+filename, 'wb')
    except:
        fp = open("D:/%s/%s/%s" % (filename[2:6], match.group(1), filename), 'wb')
    restsize = filesize
    print("正在接收文件... ")
    while 1:
        if restsize > BUFSIZE:
            filedata = conn.recv(BUFSIZE)
        else:
            filedata = conn.recv(restsize)
        if not filedata:
            break
        fp.write(filedata)
        restsize = restsize - len(filedata)
        if restsize == 0:
            break
    print("接收文件%s完毕，正在断开连接..." % filename)
    fp.close()
    conn.close()
    recvSock.close()
    print("连接已关闭...")







if __name__ == '__main__':
    num = 0
    while 1:
        try:
            recv_file('10.0.0.22')
            num += 1
            print("接收文件数量:" + str(num))
            # if num == 30:
            #     break
            time.sleep(0.5)
        except Exception as e:
            print(e)