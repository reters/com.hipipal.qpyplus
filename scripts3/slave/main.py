import os
import json
import base64
import sched
import time
import threading
import subprocess
import requests

from websocket import create_connection
from tornado.ioloop import IOLoop
from tornado import gen
from tornado.websocket import websocket_connect

project_dir = os.path.dirname(os.path.abspath(__file__))
scripts_dir = os.path.join(project_dir, "scripts")

QPYTHON = "/data/data/com.hipipal.qpy3/files/bin/python"

class Slave():
    def __init__(self, ioloop):
        self.config = self.load_config()
        self.ws = None
        self.ioloop = ioloop
        print(self.config)
        self.process = None
        self.terminal_connecting = False
        self.script_output = None
        self.ioloop.add_callback(self.initialize)

    def load_config(self):
        device_info = open("/sdcard/device.txt", 'r')
        config = json.loads(device_info.read())
        f = open(os.path.join(project_dir, "config.json"), 'r')
        hub_info = json.loads(f.read())
        config.update(hub_info)
        device_info.close()
        f.close()
        print(config)
        return config

    @gen.coroutine
    def initialize(self):
        print("running...")
        yield self.connect()

    @gen.coroutine
    def connect(self):
        url = self.config["hub_address"]
        ioloop = self.ioloop
        print("going to connect %s" % url)
        try:
            # self.ws = create_connection(url)
            self.ws = yield websocket_connect(url, connect_timeout=10)
            ioloop.add_callback(self.main_loop)
            ioloop.call_later(16, self.check_connect)
        except Exception as e:
            print(e)
            print("failed to connect %s" % url)
            print("going to retry 30s later")
            ioloop.call_later(60, self.connect)

    def check_connect(self):
        ioloop = self.ioloop
        print("check exisit")
        url = self.config["hub_address"]
        addr = url.split("/")[2]
        try:
            r = requests.get("http://%s/beats",  params={"id": self.config.get("ID", "undefined")})
            print(r)
        except Exception as e:
            print(e)
            ioloop.add_callback(self.reconnect)

        ioloop.call_later(16, self.check_connect)

    def reconnect(self):
        pass

    def on_connect_failed(self):
        print("going to retry 30s later")
        s = sched.scheduler(time.time, time.sleep)
        s.enter(30, 1, self.connect, ())
        s.run()

    @gen.coroutine
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
        self.ioloop.start()

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
        return 1, "runing"

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
        return 1, "stop"

    def handler_file_upload(self, params):
        file_metas = params
        if file_metas:
            filename = file_metas['filename']
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

if __name__ == "__main__":
    loop = IOLoop.current()
    s = Slave(loop)
    print(123344444)
    s.run()

