# Classify-rubbish-by-voice
![](https://img.shields.io/badge/platform-Raspbian-red.svg)
![](https://img.shields.io/badge/language-Python-orange.svg)
[![GitHub license](https://img.shields.io/github/license/Microactive/Classify-rubbish-by-voice.svg)](https://github.com/Microactive/Classify-rubbish-by-voice/blob/master/LICENSE)
# 项目简介
&emsp;&emsp;本项目基于树莓派和LD3320语音模块,实现了通过报出垃圾的名称即可识别垃圾种类，并让相应的LED灯闪烁。垃圾分类遵照[《广州市生活垃圾分类管理条例》](http://www.gd.gov.cn/zwgk/wjk/zcfgk/content/post_2724023.html)，目前已有的分类如下表，可根据自身需求在[代码](https://github.com/Microactive/Classify-rubbish-by-voice/blob/556d3a688e7a46ef4f37dc7feffef73a0b68f7e5/Speech_Rubbish_Recognition.py#L108)中自行增删。

| 垃圾种类  | 垃圾名称 |
|  :----:   | :----: | 
| 餐厨垃圾  | 米饭、饭菜、剩饭剩菜、食物、水果皮、水果 | 
| 可回收物  | 塑料、废纸、玻璃、金属、牛奶盒、背包、圆珠笔、矿泉水瓶、书本、塑料瓶、易拉罐、衣服、运动鞋、纸巾      | 
| 有害垃圾  |    电池、灯泡、药品、农药    |
| 其他垃圾  |  塑料袋、口罩      |

# 效果展示
&emsp;实物图片：
<p align="center"><img width="60%" src="https://github.com/Microactive/Classify-rubbish-by-voice/blob/master/readme_pictures/general.jpg" /></p>

&emsp;演示视频：[B站](https://www.bilibili.com/video/BV1Jh411Z7XW/)

# 实验材料
- 树莓派4B
- [LD3320语音模块](https://item.taobao.com/item.htm?spm=a230r.1.14.18.2ee2451cmzJ2NR&id=608144309220&ns=1&abbucket=18#detail)
- 音箱
- LED灯、杜邦线若干

# 实验流程
1. 连接实物，将LD3320语音模块与V5.0、GND、SDA、SCL引脚相连，LED与树莓派的GPIO口相连
2. 开启树莓派，在系统桌面上打开 LX 终端。
   <p align="center"><img width="60%" src="https://github.com/Microactive/Classify-rubbish-by-voice/blob/master/readme_pictures/terminal.png" /></p>

3. 输入下方图示指令，打开树莓派系统配置。
   ```
   sudo raspi-config
   ```
4. 使用键盘“↑↓”键选择图示箭头位置，按回车前往该选项。
   <p align="center"><img width="60%" src="https://github.com/Microactive/Classify-rubbish-by-voice/blob/master/readme_pictures/settings.png" /></p>
   
5. 选择“P5 I2C”功能会将该树莓派的 IIC 服务开启。
   <p align="center"><img width="60%" src="https://github.com/Microactive/Classify-rubbish-by-voice/blob/master/readme_pictures/I2C.png" /></p>
6. 使用“←→”按键选择“Yes”。
   <p align="center"><img width="60%" src="https://github.com/Microactive/Classify-rubbish-by-voice/blob/master/readme_pictures/I2C-yes.png" /></p>
7. 开启完成会再次回到一开始设置的蓝色主界面，按“Esc”键便可退出。
8. 输入``sudo reboot``指令，将树莓派重启（必须要做）。
   ```
   sudo reboot
   ```
9. 重启完毕后，再次打开 LX 终端。依次输入下方所示指令安装 I2C 的库文件、smbus
库及mpg123库（该过程需树莓派全程保持网络畅通）。
   ```
   sudo apt-get install i2c-tools -y
   ```
   ```
   sudo apt-get install python-smbus
   ```
   ```
   sudo apt-get install mpg123
   ```
10. 通过下方指令可以查看连接至树莓派拓展板上的语音识别模块。
    ```
    sudo i2cdetect -y -a 1
    ```
    <p align="center"><img width="60%" src="https://github.com/Microactive/Classify-rubbish-by-voice/blob/master/readme_pictures/check.png" /></p>
11. 下载[本项目的工程文件](https://github.com/Microactive/Classify-rubbish-by-voice)，运行里面的``Speech_Rubbish_Recognition.py``文件即可

# LD3320语音模块：[docs](https://github.com/Microactive/Classify-rubbish-by-voice/tree/master/documentations)