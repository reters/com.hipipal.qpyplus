adb shell rm -r /sdcard/com.hipipal.qpyplus/scripts3/slave/

adb push ../res /sdcard/com.hipipal.qpyplus/scripts3/slave/res

adb push ../scripts /sdcard/com.hipipal.qpyplus/scripts3/slave/scripts

adb push ../main.py /sdcard/com.hipipal.qpyplus/scripts3/slave/main.py
adb push ../main0.py /sdcard/com.hipipal.qpyplus/scripts3/slave/main0.py
adb push ../config.json /sdcard/com.hipipal.qpyplus/scripts3/slave/config.json

adb push ../libs /sdcard/com.hipipal.qpyplus/lib/python3.2/site-packages

read

# sh /data/data/com.hipipal.qpy3/files/bin/qpython.sh  /sdcard/com.hipipal.qpyplus/scripts3/slave/scripts/ttz/ttz_xhook_reg_zy.py