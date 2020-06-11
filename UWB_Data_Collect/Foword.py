'''
將東西送進去 socket
'''
from socket import *
import threading
import time
from pynput import keyboard

HOST = '127.0.0.1'  #socket 的ip
PORT = 55688 # 'serialWrite.py'是你的client
ADDR = (HOST, PORT)
BUFFSIZE = 1024

serverOne = socket(AF_INET, SOCK_STREAM)  #socket.socket(socket.AF_INET "or" socket.AF_UNIX, socket.SOCK_STREAM "or socket.SOCK_DGRAM")
serverOne.bind(ADDR)
serverOne.listen(1)# 此port上面有一個服務對象
# ZMQ版本:一個服務對象(server <--> client)(zmq.REP <> zmq.REQ)..>可以廣播[對多個](server <--> client)(zmq.PUB <> zmq.SUB)..>pipeline(有queue buffer ..> worker做快取)(server <--> worker <--> client)(zmq.PUSH <> zmq.PULL, zmq.PUSH <> zmq.PULL)

class forward(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
        # self.time = time
    def run(self):
        print('Wait for connect...')
        start = time.time()
        end = time.time()
        try:
            # end = time.time()
            while True:#  不打開會瞬間關閉clientConnection
                clientConnection, addr = serverOne.accept()
                with clientConnection:
                    print('...connected from:', addr)
                    clientConnection.send(b'\xFA\x01\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFB\x0D\x0A')
                    while True:#  不打開會只傳送一次
                        end = time.time()
                        if (end - start) >= 10:
                            clientConnection.send(b'\xFA\x08\x00\x00\x00\x00\x00\x00\x00\xFB\x0D\x0A')
                            clientConnection.close()
                            break
                    clientConnection.close()
                    # while True:
                    #     data = clientConnection.recv(BUFFSIZE) #byte格式資料..>此資料來自'serialWrite.py'..>也許是確認用
                    #     print(data.decode('utf-8')) #轉成string
                    #     #...

        except KeyboardInterrupt:
            clientConnection, addr = serverOne.accept()
            clientConnection.send(b'\xFA\x08\x00\x00\x00\x00\x00\x00\x00\xFB\x0D\x0A')
            clientConnection.close()
        serverOne.close()


def keyboard_on_press(key):
    if key:
        print(key)
        clientConnection, addr = serverOne.accept()
        clientConnection.send(b'\xFA\x08\x00\x00\x00\x00\x00\x00\x00\xFB\x0D\x0A')
        clientConnection.close()
        serverOne.close()

def keyboard_on_release(key):
    print('{0} release'.format(key))
    if key == key.esc:
        # Stop listener
        return False

def keytest():
    with keyboard.Listener(on_press=keyboard_on_press,
                      on_release=keyboard_on_release) as listener: #  press的時候, 執行method
        listener.join()

# class timeCounter(threading.Thread):
#     def __init__(self, endtime):
#         threading.Thread.__init__(self)
#     def run(self):
#         time.sleep(0.5)
#         serverOne.send(b'\xFA\x08\x00\x00\x00\x00\x00\x00\x00\xFB\x0D\x0A')  #停止用

# keyboardThread = threading.Thread(target=keytest)

if __name__ == '__main__':
    keyboardThread = threading.Thread(target=keytest)
    keyboardThread.start()
    carControlServer = forward("carServer")
    carControlServer.start()
    carControlServer.join()