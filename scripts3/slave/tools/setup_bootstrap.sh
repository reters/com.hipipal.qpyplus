adb push ../scripts/AppiumBootstrap.jar /data/local/tmp/AppiumBootstrap.jar

adb forward tcp:4724 tcp:4724

adb shell uiautomator runtest AppiumBootstrap.jar -c io.appium.android.bootstrap.Bootstrap

read

