import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("going to connect")
s.connect(("203.195.229.246", 3000))
# s.connect(("192.168.1.94", 3000))

print("connected")
while True:
    print(s._closed)
    l = s.recv(1024)
    print(l.decode())
    if l.decode() == '':
        print("connection closed")
        break

print("The End")

