## 简介

手机端QPython3的存放存档

## 项目目录

    com.hipipal.qpyplus
    |__scripts3
       |__test  # 测试脚本
       |__slave  # qpython脚本
          |__scripts  # 执行任务的脚本
          |  |__appium4droid  # appium驱动
          |  |__machines  # Machine组件
          |  |__danbao  # 单包运行文件
          |  |__sock  # 上传记录文件服务器客户端相关文件
          |  |__jiema  # 接码平台SDK
          |  |____AppiumBootstrap.jar  # appium框架的bootstrap包
          |  |____bootstrap.py  #
          |  |____util.py  # android手机端部分命令
          |  |____primary008.py  # 008上传数据脚本
          |  |____ ...  # 其他文件
          |
          |
          |
          |__libs # 依赖库, 请将里面的文件全部放在手机 /sdcard/com.hipipal.qpyplus/lib/python3.2/site-packages/里
          |__res  # 资源文件
          |__tools
          |____device.txt  # 设备标志文件, 保存设备号等信息, 需存放在手机sd卡根目录
          |____main.py  # 对应python服务器的客户端
          |____main2.py  # 对应nodejs服务器的客户端
          |____config.json  # main.py的配置
          |____config2.json  # main2.py的配置
          |_____ ...  # 其他文件

