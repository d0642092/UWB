import socket
import time

'''模擬座標傳送'''

# data_x = [0.0, 34.2, 98.5, 98.5, 34.2, 0.0, -34.2, -98.5, -98.5, -34.2]
# data_y = [100.0, 93.9, 17.3, -17.3, -93.9, -100.0, -93.9, -17.3, 17.3, 93.9]

data_x = [0.0,0.0,20,10,0.0]
data_y = [100.0,80,60.0,40,20.0]


ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = 55688

try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))

ClientSocket.sendall('座標端'.encode('utf-8'))  # Client 表明身分

# Server 的歡迎訊息
Response = ClientSocket.recv(1024)
print('Server response:{}'.format(Response.decode('utf-8')))
while True:
    for y in range(360, 0, -20):
        time.sleep(1)
        message = '0' + ',' + str(y)
        ClientSocket.sendall(message.encode('utf-8'))
    # for x, y in zip(data_x, data_y):
    #     time.sleep(3)
    #     message = str(x) + ',' + str(y)
    #     ClientSocket.sendall(message.encode('utf-8'))
    print('重新傳座標')

ClientSocket.close()