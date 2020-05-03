'''
此程式用來將 socket 所接收到的資訊
開一條子程序將 "b'/x00......" 送進去 serial
'''
from socket import *
import serial
import threading
import sys
import traceback

# serport = serial.Serial('COM3', 115200)

HOST = '127.0.0.1'
PORT = 55688  #'Foword.py'是你的server
ADDR = (HOST, PORT)
BUFFSIZE = 1024

# clientOne = socket(AF_INET, SOCK_STREAM)
# clientOne.connect(ADDR)

# socket.AF_INET: IPv4 (Default)
# socket.SOCK_STREAM: TCP (Default)

class sendToSerial(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
    def run(self):
        # create an AF_INET, STREAM socket (TCP)
        try:
            clientOne = socket(AF_INET, SOCK_STREAM)
            clientOne.connect(ADDR)
        except Exception:
            print("Fail to Build")
            sys.exit(-1)
        print('Socket Created')

        #-----------------------------------------------
        lastcommand = b''
        while True:
            command = clientOne.recv(BUFFSIZE)
            if command != lastcommand:
                print(command)
            lastcommand = command
            # serport.write(command)
        clientOne.close()

if __name__ == "__main__":
    commandIn = sendToSerial("sendIn")
    commandIn.start()
    # commandIn.join()
