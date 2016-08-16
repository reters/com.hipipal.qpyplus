#! -*- coding=utf-8 -*-
import os
import subprocess
import threading
import queue

# QPYTHON = "/data/data/com.hipipal.qpyplus/files/bin/python"
QPYTHON = "python"

project_dir = os.path.dirname(os.path.abspath(__file__))
scripts_dir = os.path.join(project_dir, "scripts")

class ScriptManager():
    def __init__(self, scripts_dir):
        self.scripts_dir = scripts_dir
        self.running_script = None
        self.output_handler = None

    def run(self, script):
        scrip_path = os.path.join(self.scripts_dir, script)
        if not os.path.isfile(scrip_path):
            raise Exception("script file not exisit")
        print(scrip_path)
        process = subprocess.Popen([QPYTHON, scrip_path], stdout=subprocess.PIPE)
        self.running_script = process
        self.output_handler = OutputHandler(process.stdout)

    def stop(self):
        if self.running_script:
            self.running_script.kill()
        self.output_handler = None

class OutputHandler():
    def __init__(self, stream):
        print(stream)
        self.stream = stream
        self.share = False
        self.queue = queue.Queue(maxsize=1)
        self.handle_thead = threading.Thread(target=self._print_stream)
        self.handle_thead.start()

    def _print_stream(self):
        print("start _print_stream")
        # for line in self.stream:
        for line in iter(self.stream.readline,''):

            line = line.decode()
            print(line.rstrip())
            try:
                self.queue.put_nowait(line)
            except queue.Full:
                pass
        try:
            self.queue.put_nowait(StopIteration())
        except queue.Full:
                pass
        print("stop!!")

    def stream_iterator(self):
        while True:
            c = self.queue.get()
            if isinstance(c, StopIteration):
                raise c
            yield c

if __name__ == "__main__":
    import time
    print("heiheihei")
    QPYTHON = "/data/data/com.hipipal.qpy3/files/bin/python"
    scripts_dir = os.path.join(project_dir, "scripts")
    # pp = subprocess.Popen(["python", "loop.py"], stdout=subprocess.PIPE)
    # pp = subprocess.Popen(["python", "loop.py"])
    pp = subprocess.Popen([QPYTHON, "-u", os.path.join(scripts_dir, "loop.py")], stdout=subprocess.PIPE)
    # pp = subprocess.Popen(["ls"], stdout=subprocess.PIPE)

    # for line in iter(proc.stdout.readline,''):
    #     print(line.rstrip())
    for line in pp.stdout:
        print(line)
    # while True:
    #     print(pp.stdout.read(1))
    #     time.sleep(1)

    print("The End")

