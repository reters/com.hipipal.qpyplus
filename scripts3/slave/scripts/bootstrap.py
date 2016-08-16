import subprocess
import time
import os


# su = subprocess.Popen(["su"], stdin=subprocess.PIPE)
# su.communicate("uiautomator runtest /sdcard/com.hipipal.qpyplus/scripts/mmzpy/AppiumBootstrap.jar -c io.appium.android.bootstrap.Bootstrap")

def setup_boostrap():
    su = subprocess.Popen(["su"], stdin=subprocess.PIPE)
    cmd = "uiautomator runtest /sdcard/com.hipipal.qpyplus/scripts3/slave/scripts/AppiumBootstrap.jar -c io.appium.android.bootstrap.Bootstrap"
    # cmd = "uiautomator runtest /sdcard/com.hipipal.qpyplus/lib/python3.2/site-packages/AppiumBootstrap.jar -c io.appium.android.bootstrap.Bootstrap"
    su.stdin.write(bytearray(cmd + "\n", "ascii"))
    su.stdin.flush()


# su.communicate(cmd)

if __name__ == "__main__":
    setup_boostrap()
