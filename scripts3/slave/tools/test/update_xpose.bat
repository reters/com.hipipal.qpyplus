adb shell pm uninstall -k com.meiriq.xposehook
adb push C:\Users\Administrator\Desktop\xpose.apk  /sdcard/xpose.apk
adb shell pm install -f /sdcard/xpose.apk
adb shell rm /sdcard/xpose.apk 

pause