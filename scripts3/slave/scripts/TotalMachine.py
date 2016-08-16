import json
import os
import threading
import time
from datetime import datetime, date, timedelta
from multiprocessing import Process
from machines.StateMachine import Machine
from appium4droid import webdriver
from bootstrap import setup_boostrap

try:
    from util import droid, show_message, alert, check_crash
except Exception as e:
    showMessage = lambda m: m
    alert = lambda: None
    check_crash = lambda m: m
    deviceInfo = {}

from machines.machineVPN import MachineVPN
from machines.machine008 import Machine008
# from machines.machineTTZ import MachineTTZ
# from machines.machineQD import MachineQD


def check_date_change(start_date):
    delta = date.today() - start_date
    if delta.days != 0:
        return True
    else:
        return False


NEW_DATE_DIR_BUILT = False


class WorkMachine(Machine):
    def __init__(self):
        super(WorkMachine, self).__init__(self.setup)
        self.config = {}

    def setup(self):
        bootstrap = threading.Thread(target=setup_boostrap)
        bootstrap.setDaemon(True)
        bootstrap.start()
        time.sleep(3)

        self.driver = webdriver.Remote()

        self.setup_config()
        self.setup_machine()

        return self.main_loop

    def setup_config(self):
        self.account, self.pwd = self.load_account_info()
        self.app_time_map = self.load_task_info()

    def load_account_info(self):
        try:
            f = open("/sdcard/device.txt", 'r')
            deviceInfo = json.loads(f.read())
            print(deviceInfo)
            f.close()
            account = deviceInfo['account']
        except IOError as e:
            print(e)
            account = "11011011011"
        print("Account --> %s" % account)
        # self.account = account
        # self.pwd = "123456"
        return account, "123456"

    def load_task_info(self):
        return self._load_task_set("zytasks")

    def _load_task_set(self, task_set_key):
        dir_path = os.path.dirname(os.path.abspath(__file__))
        f = open(os.path.join(dir_path, "app_tasks.json"), 'r')
        app_tasks = json.loads(f.read())
        app_time_map = app_tasks[task_set_key]
        print(app_time_map)
        f.close()
        # self.app_time_map = app_time_map
        return app_time_map

    def setup_machine(self):
        dr = self.driver
        self.machine008 = Machine008(dr)
        # self.machine = MachineTTZ(dr, self.account, self.pwd)
        # missionQD = MachineQD(self.machine, self.app_time_map)
        # self.machine.set_chanel_mission(missionQD)

    def main_loop(self):
        dr = self.driver
        m008 = self.machine008
        m = self.machine
        while True:
            try:
                MachineVPN(dr).run()
                m008.run()
                #############
                # m.set_chanel_mission(MachineQD(m, app_time_map))
                m.run()
            except Exception as e:
                print("somting wrong")
                print(e)
                alert()
                check_crash(dr)
            finally:
                pass
            print("Again\n")
            # show_message("Again\n")
        alert()
        return self.exit


class baseTotalMachine(object):
    def __init__(self):
        pass

    def run(self):
        pass


def change_dir():
    bootstrap = threading.Thread(target=setup_boostrap)
    bootstrap.start()
    time.sleep(3)
    dr = webdriver.Remote()

    m = Machine008(dr)
    m.task_schedule = ["change_date_dir"]
    m.run()
    # proc_bootstrap.terminate()

def get_wait_time(hour, min):
    now = datetime.now()
    delta = datetime(now.year, now.month, now.day, hour, min) - now
    if delta.total_seconds() < 0:
        delta = delta + timedelta(days=1)
    return delta.total_seconds()


def run_forever(workmachine):
    while True:
        TM = workmachine()
        proc = Process(target=TM.run)
        proc.start()

        wait_time = get_wait_time(0, 8)
        # wait_time = 120
        time.sleep(wait_time)
        proc.terminate()
        print("going to change date dir\n\n\n\n")
        proc = Process(target=change_dir)
        proc.start()
        proc.join()
        print("date dir\n\n\n\nDone!!!")


if __name__ == "__main__":
    # run_forever(WorkMachine)
    from scheduler import Scheduler
    from ttz.ttz_zy import TotalMachine as ZYMachine
    from ttz.ttz_qd import TotalMachine as QDMachine

    ztm = ZYMachine()
    qtm = QDMachine()

    s = Scheduler()
    s.set_routine(8, 10, ztm.run)
    s.set_routine(10, 30, change_dir)
    s.set_routine(10, 33, qtm.run)
    s.run_on_schedule()
