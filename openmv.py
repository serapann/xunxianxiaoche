import sensor, image, time
from pyb import UART
import json
blue_threshold   =  (80, 30, 90, 13, -75, 105)#(98, 35, 61, -13, 16, 91)蓝色的阈值
sensor.reset() # Initialize the camera sensor.
sensor.set_hmirror(True)
sensor.set_vflip(True)
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(10)
sensor.set_auto_whitebal(False)
#ain1 =  Pin('P1', Pin.OUT_PP)  #灯GPIO
#ain1.high()   #灯初始化
#ain2 =  Pin('P3', Pin.OUT_PP)  #灯GPIO
#ain2.high()   #灯初始化
clock = time.clock()

uart = UART(3, 9600)#串口波特率需要和arduino一致 这里设为9600
def find_max(blobs):
    max_size=1
    for blob in blobs:
        if blob.pixels() > max_size:
            max_blob=blob
            max_size = blob.pixels()
    return max_blob #寻找最大色块并返回最大色块的坐标

while(True):
    img = sensor.snapshot()#采集图像

    blobs = img.find_blobs([blue_threshold])
    if blobs:
        max_blob=find_max(blobs)
        img.draw_rectangle(max_blob.rect())#框选最大色块
        img.draw_cross(max_blob.cx(), max_blob.cy())#在最大色块中心画十字
        pcx = max_blob.cx()#定义pcx为最大色块中心的横坐标

        data = {"x":max_blob.cx()}
        output_str=json.dumps(data) #把pcx用json字符串的形式发送给arduino
        uart.write(output_str + '\r\n')
        print('you send:',output_str)
        print(clock.fps())
    else:
        print('not found!')
