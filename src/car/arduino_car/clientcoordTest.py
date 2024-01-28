import socket
import time
from Program.Car.arduino_car import CarDirection
'''座標模擬器'''
HOST = '172.20.10.3'
PORT = 55688

data_x = [0.0, -1.0, 2.0, 10.0, -6.0, -8.0]
data_y = [0.0, 2.0, -1.0, 8.0, -6.0, 10.0]
short_x = [0.0, 75.0, -75.0, -75.0, 75.0, 0.0]
short_y = [150.0, 75.0, 75.0, -75.0, -75.0, -150.0]
long_x = [0.0, 200.0, -200.0, -200.0, 200.0, 0.0]
long_y = [250.0, 200.0, 200.0, -200.0, -200.0, -250.0]
test_x = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
test_y = [250.0, 250.0, 250.0, -250.0, -250.0, -250.0]

ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    ClientSocket.connect((HOST, PORT))
except socket.error as e:
    print(str(e))

ClientSocket.sendall('座標端'.encode('utf-8'))

Responce = str(ClientSocket.recv(1024), encoding='utf-8')
print('Server response:{}'.format(Responce))

while True:
    for(x, y) in zip(test_x, test_y):
        message: str = str(x) + ',' + str(y) + '\\'
        # ClientSocket.sendall(message.encode('utf-8'))
        if y >= 0:
            print('前進')
            ClientSocket.sendall(message.encode('utf-8'))
        elif y < 0:
            print('後退')

        # 緩衝時間, 不確定之後要不要移除
        time.sleep(0.5)
    print('重新迴圈')

ClientSocket.close()
