'''
此程式用來將 socket 所接收到的資訊
開一條子程序將 "b'/x00......" 送進去 serial
'''

# 額外獨立
from socket import *
import serial

<<<<<<< HEAD
serport = serial.Serial('COM3', 115200)


HOST = '192.168.8.105'
PORT = 55688  #'Foword.py'是你的server

# HOST = '127.0.0.1'
# PORT = 55688  #'ControllCar.py'是你的client

=======
serport = serial.Serial('COM5', 115200)
HOST = '127.0.0.1'
PORT = 55688  #'ControllCar.py'是你的client
>>>>>>> 6409191193d2941ba24ea308b9a3839bce8f8a4a
ADDR = (HOST, PORT)
BUFFSIZE = 1024

server = socket(AF_INET, SOCK_STREAM)
server.bind(ADDR)
server.listen(1)

print("Wait the client connect...")
connectRoad, addr = server.accept()
while True:
    try:
        clientMessage = connectRoad.recv(BUFFSIZE)
        if clientMessage == b'\xFA\x01\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFB\x0D\x0A':
            serport.write(clientMessage)
            print("Client Message is: ", clientMessage)
        if clientMessage == b'\xFA\x08\x00\x00\x00\x00\x00\x00\x00\xFB\x0D\x0A':
            serport.write(clientMessage)
            returnMessage = "Already Stop"
            connectRoad.sendall(returnMessage.encode())
            break
        returnMessage = clientMessage
        connectRoad.sendall(returnMessage)  # send 不確定會不會都發送完成 https://blog.csdn.net/jing16337305/article/details/79856116
    except Exception:
        print("未找到 client")
        break

connectRoad.close()  # 不關在接受的話會一直收到 b'' 但在裡面關client端無法重複傳送

