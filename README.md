## 简介

手机端QPython的存放存档，

## 项目目录

    root
    |__doc  # 项目文档
    |__master  # 设备管理服务器(未完成)
    |  |__node # nodejs版本
    |  |__py   # python版本
    |
    |__slave  # qpython脚本
       |__scripts  # 执行任务的脚本
       |  |__appium4droid  # appium驱动
       |  |__machines  # Machine组件
       |  |__sock  # 上传记录文件服务器客户端相关文件
       |  |__jiema  # 接码平台SDK
       |  |__get_captchaimg  # 图片验证码切图
       |  |____AppiumBootstrap.jar  # appium框架的bootstrap包
       |  |____bootstrap.py  #
       |  |____util.py  # android手机端部分命令
       |  |____device.txt  # 设备标志文件, 保存设备号等信息, 需存放在手机sd卡根目录
       |  |____ ....
       |
       |
       |
       |__libs # 依赖库, 请将里面的文件全部放在手机 /sdcard/com.hipipal.qpyplus/lib/python3.2/site-packages/里
       |__res  # 资源文件
       |__test
       |__tools
       |____device.txt  # 设备标志文件, 保存设备号等信息, 需存放在手机sd卡根目录
       |____main.py  # 对应python服务器的客户端
       |____main2.py  # 对应nodejs服务器的客户端
       |____config.json  # main.py的配置
       |____config2.json  # main2.py的配置
       |_____ ..... # 其他文件


