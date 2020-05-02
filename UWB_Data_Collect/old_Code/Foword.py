'''
將東西送進去 socket
'''
from socket import *
import threading

import time
# from pynput import keyboard

HOST = '127.0.0.1'  #socket 的ip
PORT = 55688 # 'serialWrite.py'是你的client
ADDR = (HOST, PORT)
BUFFSIZE = 1024

serverOne = socket(AF_INET, SOCK_STREAM)  #socket.socket(socket.AF_INET "or" socket.AF_UNIX, socket.SOCK_STREAM "or socket.SOCK_DGRAM")
serverOne.bind(ADDR)
serverOne.listen(1)# 此port上面有一個服務對象
# ZMQ版本:一個服務對象(server <--> client)(zmq.REP <> zmq.REQ)..>可以廣播[對多個](server <--> client)(zmq.PUB <> zmq.SUB)..>pipeline(有queue buffer ..> worker做快取)(server <--> worker <--> client)(zmq.PUSH <> zmq.PULL, zmq.PUSH <> zmq.PULL)

class forward(threading.Thread):
    def __init__(self,flag):
        threading.Thread.__init__(self)
        self.flag = flag
        # self.time = time
    def run(self):
        print('Wait for connect...')
        # start = time.time()
        # end = time.time()
        # while self.flag:
        clientConnection, addr = serverOne.accept()

        while self.flag:
            # end = time.time()
            print('...connected from:', addr)
            print(self.flag)
            clientConnection.send(b'\xFA\x01\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFB\x0D\x0A')
            time.sleep(1)
            # while True:
            #     data = clientConnection.recv(BUFFSIZE) #byte格式資料..>此資料來自'serialWrite.py'..>也許是確認用
            #     print(data.decode('utf-8')) #轉成string
            #     #...
        clientConnection.send(b'\xFA\x08\x00\x00\x00\x00\x00\x00\x00\xFB\x0D\x0A')
        clientConnection.close()
        serverOne.close()



# def keyboard_on_press(key):
#     serverOne.send(b'\xFA\x08\x00\x00\x00\x00\x00\x00\x00\xFB\x0D\x0A')
#     serverOne.close()
#
# def keyboard_on_release(key):
#     print('{0} release'.format(key))
#     if key == key.esc:
#         # Stop listener
#         return False
#
# def keytest():
#     with keyboard.Listener(on_press=keyboard_on_press,
#                       on_release=keyboard_on_release) as listener: #  press的時候, 執行method
#         listener.join()
# keyboardThread = threading.Thread(target=keytest)
# class timeCounter(threading.Thread):
#     def __init__(self, endtime):
#         threading.Thread.__init__(self)
#     def run(self):
#         time.sleep(0.5)
#         serverOne.send(b'\xFA\x08\x00\x00\x00\x00\x00\x00\x00\xFB\x0D\x0A')  #停止用

