import socket
import threading
import _thread
from Program.Car.arduino_car import CarDirection
import time
from pynput import keyboard

HOSTip = '192.168.8.105'
PORTnum = 55688
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # socket使用IPV4連線
commandMessage = []
UserAutoSwitch = [False]  # True:追蹤模式, False:鍵盤模式

#=======KeyBoard_Direction======
def keyboardDirection(keyPressed):

    direction = {'w':'180+0', 's':'0+180', 'q':'30+30', 'e':'150+150', 'a':'120+0', 'd':'180+60', 'x':'90+90','c':'-1+-1'}

    if not UserAutoSwitch[0] or keyPressed == 'c':
        try:
            commandMessage.append(direction[keyPressed])
        except KeyError:
            pass



#============鍵盤監聽============
def on_press(key):
    try:
        print('alphanumeric key {0} pressed'.format(
            key.char))
        keyboardDirection(key.char)
    except AttributeError:
        print('special key {0} pressed'.format(
            key))

def on_release(key):
    print('{0} released'.format(
        key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False

#==伺服器端與車子的溝通thread==
def client_handler_car(connection):
    connection.send(str.encode('Welcome to the Server\n'))

    # 鍵盤輸入
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

    while True:
        # clientMessage = str(connection.recv(1024), encoding='utf-8')
        # print('Client:', clientMessage)
        if commandMessage:
            # 得到最新的指令
            command: str = commandMessage.pop()
            commandMessage.clear()

            # 若非切換模式時, 才進行輸出
            if command.split('+', 1)[0] != '-1':
                # connection.sendall(str("Send To WeMos Test\n").encode('utf-8'))
                # print("Send to Car Command is: {}".format(command))
                connection.sendall((command + '\n').encode('utf-8'))
            else:
                print("切換模式為:", end='')
                UserAutoSwitch[0] = not UserAutoSwitch[0]
                if UserAutoSwitch:
                    print("追蹤模式")
                else:
                    print("鍵盤模式")
        time.sleep(0.25)
    connection.close()

#==伺服器端與座標的溝通thread==
def client_handler_coordinate(connection):
    print("Sent welcome message")
    connection.send(str.encode('This is Car Server\n'))
    judge = CarDirection.coreJudge()

    while True:
        clientMessage = str(connection.recv(1024), encoding='utf-8')
        # 產生指令
        if UserAutoSwitch[0]:
            judge.direction(clientMessage)
            commandMessage.append(judge.command)

#=============通訊=============
class car_server(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.clientThreadCount = 0
        self.UserAuto_Switch = 0  # '0' 是使用者模式, '1' 是追蹤模式
    def run(self):
        HOST = HOSTip
        PORT = PORTnum

        server.bind((HOST, PORT))  # 綁定ip, 裡面要放tuple
        server.listen(2)  # 監聽幾個client

        #newAdded
        print('Waiting for Connection...')
        while True:
            # 保持等待client連入
            Client, address = server.accept()
            print('Connected to: ' + address[0] + ':' + str(address[1]))

            # 有連到, 開啟一個新的溝通Thread
            identify = Client.recv(2048)
            print("座標\\車子辨別: " + identify.decode('utf-8'))
            if identify.decode('utf-8') == '車子端':
                _thread.start_new_thread(client_handler_car, (Client,))
            elif identify.decode('utf-8') == '座標端':
                _thread.start_new_thread(client_handler_coordinate, (Client,))

            self.clientThreadCount += 1
            print('Thread Number: ' + str(self.clientThreadCount))

if __name__ == '__main__':
    ServerTd = car_server()
    ServerTd.start()
