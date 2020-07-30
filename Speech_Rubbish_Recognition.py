'''
 * 只能识别汉字，将要识别的汉字转换成拼音字母，每个汉字之间空格隔开，比如：塑料袋 --> su liao dai 
 * 最多添加50个词条，每个词条最长为79个字符，每个词条最多10个汉字
 * 每个词条都对应一个识别号（1~255随意设置）不同的语音词条可以对应同一个识别号，
 模块上的STA状态灯：亮起表示正在识别语音，灭掉表示不会识别语音，当识别到语音时状态灯会变暗，或闪烁，等待读取后会恢复当前的状态指示
'''

import smbus
import time
import numpy
import os

class ASR:

    # Global Variables
    address = None
    bus = None
    
    ASR_RESULT_ADDR = 100   #识别结果存放处，通过不断读取此地址的值判断是否识别到语音，不同的值对应不同的语音
    

    ASR_WORDS_ERASE_ADDR = 101   #擦除所有词条
    

    ASR_MODE_ADDR = 102
    

    ASR_ADD_WORDS_ADDR = 160
    #词条添加的地址，支持掉电保存

    def __init__(self, address, bus=1):
        self.address = address
        self.bus = smbus.SMBus(bus)
        
    def readByte(self):
        return self.bus.read_byte(self.address)

    def writeByte(self, val):               
        value = self.bus.write_byte(self.address, val)
        if value != 0:
            return False
        return True
    
    def writeData(self, reg, val):
        self.bus.write_byte(self.address,  reg)
        self.bus.write_byte(self.address,  val)

    def getResult(self):
        if ASR.writeByte(self, self.ASR_RESULT_ADDR):
            return -1        
        value = self.bus.read_byte(self.address)
        return value
    
    
    
    '''
    * 添加词条函数，
    * idNum：词条对应的识别号，1~255随意设置。识别到该号码对应的词条语音时，
    *        会将识别号存放到ASR_RESULT_ADDR处，等待主机读取，读取后清0
    * words：要识别汉字词条的拼音，汉字之间用空格隔开
    * 
    * 执行该函数，词条是自动往后排队添加的。   
    '''
    def addWords(self, idNum, words):
        buf = [idNum]       
        for i in range(0, len(words)):
            buf.append(eval(hex(ord(words[i]))))
        self.bus.write_i2c_block_data(self.address, self.ASR_ADD_WORDS_ADDR, buf)
        time.sleep(0.05)
        
    def eraseWords(self):
        result = self.bus.write_byte_data(self.address, self.ASR_WORDS_ERASE_ADDR, 0)
        time.sleep(0.06)
        if result != 0:
           return False
        return True
    
    def setMode(self, mode): 
        result = self.bus.write_byte_data(self.address, self.ASR_MODE_ADDR, mode)
        if result != 0:
           return False
        return True
        
if __name__ == "__main__":
    addr = 0x79 #传感器iic地址
    asr = ASR(addr)

    #添加的词条和识别模式是可以掉电保存的，第一次设置完成后，可以将1改为0
    if 1:
        asr.eraseWords()
        
        
        #setMode：识别模式设置，值范围1~3
        #1：循环识别模式。状态灯常亮（默认模式）    
        #2：口令模式，以第一个词条为口令。状态灯常灭，当识别到口令词时常亮，等待识别到新的语音,并且读取识别结果后即灭掉
        #3：按键模式，按下开始识别，不按不识别。支持掉电保存。状态灯随按键按下而亮起，不按不亮
        asr.setMode(1)           # 选择模式1，即循环识别模式。状态灯常亮（默认模式）
       
        # 广州垃圾分类标准
        # 种类1：餐厨垃圾 
        # 米饭、饭菜、剩饭剩菜、食物、水果皮、水果           
        asr.addWords(1, 'mi fan')
        asr.addWords(1, 'fan cai')
        asr.addWords(1, 'sheng fan sheng cai')
        asr.addWords(1, 'shi wu')
        asr.addWords(1, 'shui guo pi')
        asr.addWords(1, 'shui guo')
        
        # 种类2：可回收物
        # 塑料、废纸、玻璃、金属、牛奶盒、背包、圆珠笔、矿泉水瓶、书本、塑料瓶、易拉罐、衣服、运动鞋、纸巾
        asr.addWords(2, 'su liao')
        asr.addWords(2, 'fei zhi')
        asr.addWords(2, 'bo li')
        asr.addWords(2, 'jin shu')
        asr.addWords(2, 'niu nai he')
        asr.addWords(2, 'bei bao')
        asr.addWords(2, 'yuan zhu bi')
        asr.addWords(2, 'kuang quan shui ping')
        asr.addWords(2, 'shu ben')
        asr.addWords(2, 'su liao ping')
        asr.addWords(2, 'yi la guan')
        asr.addWords(2, 'yi fu')
        asr.addWords(2, 'yun dong xie')
        asr.addWords(2, 'zhi jin')
        
        # 种类3：有害垃圾
        # 电池、灯泡、药品、农药
        asr.addWords(3, 'dian chi')
        asr.addWords(3, 'deng pao')
        asr.addWords(3, 'yao pin')
        asr.addWords(3, 'nong yao')
        
        # 种类4：其他垃圾
        # 塑料袋、口罩
        asr.addWords(4, 'su liao dai')
        asr.addWords(4, 'kou zhao')
        
        # 排除受播报语音的影响
        asr.addWords(5, 'zhe shi can chu la ji')       # 这是餐厨垃圾
        asr.addWords(5, 'zhe shi ke hui shou wu')      # 这是可回收物
        asr.addWords(5, 'zhe shi you hai la ji')       # 这是有害垃圾
        asr.addWords(5, 'zhe shi qi ta la ji')         # 这是其他垃圾
        asr.addWords(5, 'zhe shi')                     # 这是
        asr.addWords(5, 'la ji')                       # 垃圾
        asr.addWords(5, 'can chu la ji')               # 餐厨垃圾
        asr.addWords(5, 'ke hui shou wu')              # 可回收物  
        asr.addWords(5, 'you hai la ji')               # 有害垃圾 
        asr.addWords(5, 'qi ta la ji')                 # 其他垃圾 
        
        
    while 1:
        data = asr.getResult()
        print("result:", data)
        
        if data == 1:   # 种类1：餐厨垃圾
            os.system("sudo mpg123 Kitchen_Waste.mp3")    # 播报Kitchen_Waste.mp3
            #可在此处写代码控制外设，如舵机等
            
        elif data == 2:    # 种类2：可回收物
            os.system("sudo mpg123 Recyclable_Waste.mp3")    # 播报Recyclable_waste.mp3
            #可在此处写代码控制外设，如舵机等
            
        elif data == 3:    # 种类3：有害垃圾
            os.system("sudo mpg123 Harmful_Waste.mp3")    # 播报Harmful_Waste.mp3
            #可在此处写代码控制外设，如舵机等
            
        elif data == 4:    # 种类4：其他垃圾
            os.system("sudo mpg123 Other_Waste.mp3")    # 播报Other_Waste.mp3
            #可在此处写代码控制外设，如舵机等
        else:
            print("无法识别该垃圾种类")
        
        
        
        
        
        
        