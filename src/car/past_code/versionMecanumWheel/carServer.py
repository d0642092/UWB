'''
Server 將嵌入 judge 的物件 紀錄 歷史移動 以及方位
    Input: 座標, 前次功率_平移, 前次功率_旋轉, 前次/本次 距離, 前次/本次 車頭方位
    Output: w, 1

等待思考:
    追蹤/手動模式 判斷 以及 halt

Bug:
    1. 輸入太快會把一整串都吃掉
        ex: Input asdasd in 0.1sec
            Output asdasd 會被傳送到 "車車客戶端" 整串吃掉
'''
import socket
import threading
import _thread
import time
import queue
from pynput import keyboard
# import Car_ver2
import carClient_coordinate_easyjudge as carjudge
import carClient_coordinate_judge as carjudge_formal

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
commandMessage = queue.Queue()
positionQueue = queue.Queue()
UserAutoSwitch = [0]  # '0' 是使用者模式, '1' 是追蹤模式..>切換模式參數

#=============Pressed===========
def sendcommand(keyPressed):
    print('Message Created: ', end='')
    if UserAutoSwitch[0] == 0 or keyPressed == 'c':  # 用來擋追蹤模式的鍵盤輸入
        commandMessage.put(keyPressed + ',1.2' + '\\')

#============鍵盤監聽============
def on_press(key):
    try:
        print('alphanumeric key {0} pressed'.format(
            key.char))
        sendcommand(key.char)
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
    UserAutoSwitch[0] = 0  # '0' 是使用者模式, '1' 是追蹤模式
    cmdMessage = ''
    # 鍵盤輸入
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

    while True:
        # 傳送給Client的資料
        if not commandMessage.empty(): #  得到指令
            cmdMessage = commandMessage.get()
            cmdMes = cmdMessage.split(',', 1)[0]

            if cmdMes == 'c':  # 按下空白鍵切換模式
                print('切換模式')
                UserAutoSwitch[0] = (UserAutoSwitch[0] + 1) % 2
                continue  # 切換模式時, 不傳送指令...>好像擋不到, 改用往下 3行的code來擋

        if cmdMessage.encode() != b'':
            if cmdMessage.split(',', 1)[0] != 'c':  # 切換模式不輸出
                connection.sendall(cmdMessage.encode())
                print(cmdMessage.encode())

        cmdMessage = ''

    connection.close()

#==伺服器端與座標的溝通thread==
def client_handler_coordinate(connection):
    connection.send(str.encode('Welcome to the Server\n'))

    # 追蹤判斷 物件
    judge = carjudge_formal.coreJudge()
    # 座標是否可傳入
    goalTime = time.time()
    while True:
        data = str(connection.recv(2048), encoding='utf-8')
        print('座標端資料' + data)
        currentTime = time.time()
        if goalTime <= currentTime:
            if UserAutoSwitch[0] == 1:  # 追蹤模式時, 座標才能輸入
                positionQueue.put(data)

            if not positionQueue.empty():
                position = positionQueue.get()
                x = float(position.split(',', 1)[0])
                y = float(position.split(',', 1)[1])

                # # 簡易追蹤
                # if carjudge.easyjudge(x, y) == 0 and UserAutoSwitch[0] == 1:  # 追蹤模式時
                #     commandMessage.put('w,1\\')
                # elif carjudge.easyjudge(x, y) == 1 and UserAutoSwitch[0] == 1:
                #     commandMessage.put('s,1\\')

                # 正式追蹤
                # Step 1. 判斷方向 以及 距離資料
                judge.direction(x, y)
                # Step 2. 調控功率
                # 車頭平移調整功率
                if judge.disFlag - judge.lastdisFlag == 2:
                    judge.shiftPower *= 0.5
                elif judge.disFlag - judge.lastdisFlag == 1:
                    judge.shiftPower *= 0.8
                # 車頭旋轉調整功率
                if judge.disFlag == 0 or judge.disFlag == 2:
                    if judge.turnflagOverJudge() == 1:
                        judge.turnPower *= 0.8
                    elif judge.turnflagOverJudge() == 0:
                        judge.turnPower *= 1.25
                # Step 3. 輸出 以及 紀錄更新
                if judge.disFlag == 2:
                    if judge.turnFlag == 0:
                        commandMessage.put('w,' + str(judge.shiftPower) + '\\')
                    elif 3 >= judge.turnFlag >= 1:
                        commandMessage.put('e,' + str(judge.turnPower) + '\\')
                    elif 6 >= judge.turnFlag >= 4:
                        commandMessage.put('q,' + str(judge.turnPower) + '\\')
                    elif judge.turnFlag == 7:
                        commandMessage.put('e,' + str(judge.turnPower * 1.25) + '\\')
                elif judge.disFlag == 1:
                    if judge.turnFlag == 0:
                        commandMessage.put('w,' + str(judge.shiftPower * 1.0) + '\\')
                    elif judge.turnFlag == 1:
                        commandMessage.put('d,' + str(judge.shiftPower * 1.8) + '\\')
                    elif judge.turnFlag == 2:
                        commandMessage.put('d,' + str(judge.shiftPower * 1.8) + '\\')
                    elif judge.turnFlag == 3:
                        commandMessage.put('d,' + str(judge.shiftPower * 1.8) + '\\')
                    elif judge.turnFlag == 4:
                        commandMessage.put('a,' + str(judge.shiftPower * 1.8) + '\\')
                    elif judge.turnFlag == 5:
                        commandMessage.put('a,' + str(judge.shiftPower * 1.8) + '\\')
                    elif judge.turnFlag == 6:
                        commandMessage.put('a,' + str(judge.shiftPower * 1.8) + '\\')
                    elif judge.turnFlag == 7:
                        commandMessage.put('s,' + str(judge.shiftPower * 1.0) + '\\')
                elif judge.disFlag == 0:
                    if 3 >= judge.turnFlag >= 1:
                        commandMessage.put('e,' + str(judge.turnPower) + '\\')
                    elif 6 >= judge.turnFlag >= 4:
                        commandMessage.put('q,' + str(judge.turnPower) + '\\')
                    elif judge.turnFlag == 7:
                        commandMessage.put('e,' + str(judge.turnPower * 1.25) + '\\')
                judge.update()

                # 給予下次可傳入座標的時間點
                if judge.disFlag == 0:
                    goalTime = currentTime + 1
                elif judge.disFlag == 1:
                    goalTime = currentTime + 2
                elif judge.disFlag == 2:
                    goalTime = currentTime + 3
                else:
                    goalTime = currentTime + 3
        if not data:
            break
    connection.close()

#=============通訊=============
class car_server(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.clientThreadCount = 0
        self.UserAuto_Switch = 0  # '0' 是使用者模式, '1' 是追蹤模式
    def run(self):
        HOST = '127.0.0.1'
        PORT = 55688

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
            if identify.decode('utf-8') == '車子端':
                _thread.start_new_thread(client_handler_car, (Client,))
            elif identify.decode('utf-8') == '座標端':
                _thread.start_new_thread(client_handler_coordinate, (Client,))

            self.clientThreadCount += 1
            print('Thread Number: ' + str(self.clientThreadCount))

if __name__ == '__main__':
    ServerTd = car_server()
    ServerTd.start()
