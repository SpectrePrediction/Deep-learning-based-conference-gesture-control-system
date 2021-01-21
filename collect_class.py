'''
本脚本将完成一个数据收集系统
通过调用电脑的摄像头
每5秒收集一个动作，收集完成后发出滴的一声开始下一次收集
并将收集的动作放入指定文件夹下

'''
import os
import numpy as np
import cv2
import winsound  #导入声音文件
import threading    #python 多线程操作库
duration = 100  # millisecond
freq = 1940  # Hz

def Contrast_and_Brightness(alpha, beta, img):
    '''调节图像亮度、暂不启用'''
    blank = np.zeros(img.shape, img.dtype)
    # dst = alpha * img + beta * blank
    dst = cv2.addWeighted(img, alpha, blank, 1-alpha, beta)
    return dst
class RecordingThread(threading.Thread):
    def __init__(self, name, camera,class_name:str,filename:str):
        threading.Thread.__init__(self)
        self.name = name
        self.isRunning = True
        self.class_name = class_name
        self.filename = filename
        self.cap = camera
        fourcc = cv2.VideoWriter_fourcc(*'MJPG') #设置视频编码方式
        self.out = cv2.VideoWriter('./'+class_name+'/'+filename+'.avi', fourcc, 20.0, (640, 480))
        print(self.out)
        # out 是VideoWriter的实列对象，就是写入视频的方式，第一个参数是存放写入视频的位置，
        # 第二个是编码方式，20是帧率，最后是视频的高宽，如果录入视频为灰度，则还需加一个false

    def run(self):
        while self.isRunning:
            ret, frame = self.cap.read()  #read()函数表示按帧读取视频，success，frame是read()的两个返回值，
            # ret是布尔值——如果读取帧是正确的则返回True，如果文件读取到结尾则返回False，Frame表示的是每一帧的图像，是一个三维矩阵
            # frame = Contrast_and_Brightness(0.1,0.2,frame)
            if ret:
                self.out.write(frame)

        self.out.release()

    def stop(self):
        self.isRunning = False


    def __del__(self):
        self.out.release()


class VideoCamera(object):
    def __init__(self,class_name:str,filename:str):
        # 打开摄像头， 0代表笔记本内置摄像头
        self.cap = cv2.VideoCapture(0)
        self.class_name = class_name
        self.filename = filename
        # 初始化视频录制环境
        self.is_record = False
        self.out = None

        # 视频录制线程
        self.recordingThread = None

    # 退出程序释放摄像头
    def __del__(self):
        self.cap.release()

    def close(self):
        if self.cap.isOpened():
            self.cap.release()

    def start_record(self):
        self.is_record = True
        self.recordingThread = RecordingThread("Video Recording Thread", self.cap,self.class_name,self.filename)
        self.recordingThread.start()

    def stop_record(self):
        self.is_record = False

        if self.recordingThread != None:
            self.recordingThread.stop()

    def beep(self):
        '''利用蜂鸣器播放提示音，提示下一次录制开始'''
        winsound.Beep(freq,duration)

import time
def main():
    '''主程序'''
    class_name = input("请输入你要录制的种类名字：")
    os.mkdir(class_name)
    print("---录制种类接受完成，请注意每一次录制为五秒---")
    num = int(input("请输入你要录制的次数：如100次 则到程序结束为止会产生一百个视频:"))
    time_sleep = int(input("请输入你要录制视频的时长，一旦开始时长不能改变:"))
    num_in = 0
    while num_in<num:
        filename = str(num_in)
        camera = VideoCamera(class_name,filename)
        camera.start_record()
        camera.beep()
        time.sleep(time_sleep)
        camera.stop_record()
        print("第",num_in,end='')
        print('次录制完成')
        num_in+=1
    camera.beep()
    camera.beep()
    camera.beep()
    print("录制结束")

if __name__ == '__main__':
    main()
