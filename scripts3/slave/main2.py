import os
import json
import base64
import socket
import sched
import time
import threading
import subprocess

from socketIO_client import SocketIO, BaseNamespace

project_dir = os.path.dirname(os.path.abspath(__file__))
scripts_dir = os.path.join(project_dir, "scripts")

QPYTHON = "/data/data/com.hipipal.qpy3/files/bin/python"

class Slave():
    def __init__(self):
        self.config = self.load_config()
        print(self.config)
        self.process = None
        self.terminal_connecting = False
        self.script_output = None

    def load_config(self):
        device_info = open("/sdcard/device.txt", 'r')
        config = json.loads(device_info.read())
        f = open(os.path.join(project_dir, "config2.json"), 'r')
        hub_info = json.loads(f.read())
        config.update(hub_info)
        device_info.close()
        f.close()
        print(config)
        return config

    def initialize(self):
        print("running...")
        yield self.connect()

    def connect(self):
        host = self.config["hub_address"]
        port = self.config['port']
        print("going to connect %s:%s" % (host, port))
        return SocketIO(host, port)
        # try:
        #     return SocketIO(host, port)
        # except Exception as e:
        #     print("fail to connect %s:%s" % (host, port))
        #     print("failed to connect %s" % url)
        #     print("going to retry 30s later")
        #     ioloop.call_later(60, self.connect)


    def reconnect(self):
        pass

    def on_connect_failed(self):
        print("going to retry 30s later")
        s = sched.scheduler(time.time, time.sleep)
        s.enter(30, 1, self.connect, ())
        s.run()

    def main_loop(self):
        print("main loop")
        try:
            while True:
                msg = yield self.ws.read_message()
                print(msg)
                result = self.dispatch(json.loads(msg))
                yield self.ws.write_message(result)
        except Exception as e:
            print(e)
            print("going to reconnect 30s later")
            self.ioloop.call_later(30, self.connect)


    def dispatch(self, msg):
        cmd = msg.get("cmd")
        params = msg.get("params")
        result = {"cmd": cmd + 1}
        if cmd == 101:
            result["ret"], result["params"] = 1, {"id": self.config.get("ID", "undefined")}
        elif cmd == 103:
            print("103")
            result["ret"], result["params"] = self.handler_file_upload(params)
        elif cmd == 105:
            print("105")
            result["ret"], result["params"] = self.handler_run_script(params)
        elif cmd == 107:
            print("107")
            result["ret"], result["params"] = self.handler_stop_script(params)
        elif cmd == 109:
            print(109)
            result["ret"], result["params"] = self.start_terminal(params)
        elif cmd == 111:
            print(111)
            result["ret"], result["params"] = self.end_termainal(params)
        else:
            return "no such command"

        return json.dumps(result)

    def run(self):
        socketio = self.connect()
        self.socketio = socketio
        socketio.on("connect", self.on_connect)
        socketio.on("reconnect", self.on_connect)
        socketio.on("run_script", self.handler_run_script)
        socketio.on("stop_script", self.handler_stop_script)
        socketio.on("upload", self.handler_file_upload)

        while True:
            socketio.wait(5)

    def on_connect(self):
        print("connect to server")
        self.socketio.emit("reg", self.config.get("ID", "undefined"))

    def handler_run_script(self, params):
        script = params.get("script", "")
        if not script:
            return -1, "wrong parameter"
        scrip_path = os.path.join(scripts_dir, script)
        if not os.path.isfile(scrip_path):
            return -1, "wrong parameter"
        process = self.process
        if process:
            process.kill()
        process = subprocess.Popen([QPYTHON, "-u", scrip_path], stdout=subprocess.PIPE)
        # process = subprocess.Popen([QPYTHON, scrip_path], )
        self.process = process
        self.stream_handler = threading.Thread(target=self._print_stream, args=(process.stdout,))
        self.stream_handler.start()
        # self.script_output = OutputHandler(process.stdout).stream_iterator()
        print("runing")

    def _print_stream(self, stream):
        print("start _print_stream")
        for line in stream:
            line = line.decode().rstrip()
            if self.terminal_connecting:
                try:
                    self.ws.write_message(json.dumps({"cmd": 200, "params": {"content": line}}))
                except:
                    pass
            print(line)
        print("stream handler: mission completed!!")

    def handler_stop_script(self, params):
        process = self.process
        if process:
            process.kill()
            self.process = None
            self.script_output = None
        print("stop")

    def handler_file_upload(self, params):
        file_metas = params
        if file_metas:
            filename = file_metas['filename']
            print("get file %s" % filename)
            # raw = file_metas['payload']
            raw = base64.b64decode(file_metas['payload'].encode())
            file = open(os.path.join(scripts_dir, filename), 'wb')
            file.write(raw)
            file.close()
            return 1, "ok"
        else:
            return -1, "no file upload"

    def start_terminal(self, params):
        if not self.process:
            # self.ws.send("****** NO SCRIPT RUNNING *******")
            return -1, "****** NO SCRIPT RUNNING *******"
        self.output = self.script_output
        self.terminal_connecting= True
        return 1, "========= Running ==========="

    def end_termainal(self, params):
        self.terminal_connecting = False
        return 1, "========== End ============="


def test():
    class Namespace(BaseNamespace):

        def on_connect(self):
            print('[Connected]')

    def on_connect_response(*args):
        print('on_connect_response', args)

    def on_news_response(*args):
        print('on_news_response', args)

    def on_disconnect_response(*args):
        print('disconnect', args)


    socketio = SocketIO("localhost", 4000)
    # socketio = SocketIO("203.195.229.246", 4000, Namespace)
    # socketio = SocketIO("203.195.229.246", 4000)
    socketio.on("connect", on_connect_response)
    socketio.on("news", on_news_response)
    socketio.on("disconnect", on_disconnect_response)
    print("Done!!")
    while True:
        socketio.wait(5)
        socketio.emit("event", "qqlove")

if __name__ == "__main__":
    s = Slave()
    s.run()
