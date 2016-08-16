#! -*- coding=utf-8 -*-
import socket
import json

# from exceptions import WebDriverException

BOOSTRAP_HOST, BOOSTRAP_PORT = "localhost", 4724


class Bootstrap(object):
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((BOOSTRAP_HOST, BOOSTRAP_PORT))

    def send_command(self, cmd_type, extra):
        cmd = {"cmd": cmd_type}
        cmd.update(extra)
        cmdjson = json.dumps(cmd)
        # print(cmdjson)
        self.sock.sendall((cmdjson + "\n").encode())
        received = self.sock.recv(1024).decode()
        # print("received from bootstrap:", received)
        return json.loads(received)

    def shutdown(self):
        self.send_command("shutdown", {})


if __name__ == "__main__":
    bq = Bootstrap()
    bq.send_command("action", {"action": "pressKeyCode", "params": {"keycode": 3, "metastate": None}})
