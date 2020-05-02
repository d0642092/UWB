'''
此程式用來將 socket 所接收到的資訊
開一條子程序將 "b'/x00......" 送進去 serial
'''

# 額外獨立
from socket import *
import serial

serport = serial.Serial('COM5', 115200)

HOST = '127.0.0.1'
PORT = 55688  #'Foword.py'是你的server
ADDR = (HOST, PORT)
BUFFSIZE = 1024

server = socket(AF_INET, SOCK_STREAM)
server.bind(ADDR)
server.listen(1)

# while True:
connectRoad, addr = server.accept()
while True:
    try:
        clientMessage = connectRoad.recv(BUFFSIZE)
        if clientMessage != b'':
            serport.write(clientMessage)
            print("Client Message is: ", clientMessage)
        if clientMessage == b'\xFA\x08\x00\x00\x00\x00\x00\x00\x00\xFB\x0D\x0A':
            returnMessage = "Already Stop"
            connectRoad.sendall(returnMessage.encode())
            break
        returnMessage = clientMessage
        connectRoad.sendall(returnMessage)  # send 不確定會不會都發送完成 https://blog.csdn.net/jing16337305/article/details/79856116
    except Exception:
        print("未找到 client")
        break

    # try:
    #     clientMessage = connectRoad.recv(BUFFSIZE)
    #     flag = True
    # except Exception:
    #     flag = False
connectRoad.close()  # 不關在接受的話會一直收到 b'' 但在裡面關client端無法重複傳送

