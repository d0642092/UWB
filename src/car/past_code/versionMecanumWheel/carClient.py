'''
direction 跟 controlSignalModule 去做指令輸出
    Input: w, 1
    Output: 功率為 1 的前進指令

尚未完成
    1.direction 輸出
    2.隨時計時 以及判斷 是否需要 halt 的模組
'''
import socket
import serial
import threading
import time
import queue
import controlSignalModule as signalModule
import _thread

# -------序列埠-------
# 開啟serial序列埠, 設定鮑率為115200
COM_PORT = 'COM3'  # 需先檢測再設定
BAUD_RATES = 115200
ser = serial.Serial(COM_PORT, BAUD_RATES)


def serialcheck(ser):
    while True:
        print(ser.read(24))
        time.sleep(1)

def sendcommandTest(cmdSignal):
    print('輸出指令為', end='')
    print(cmdSignal)
    currentpower = signalModule.commandConvert()
    print(currentpower.cmdgetCurrentPower(cmdSignal, 2))

def direction_withpower(inputSignal):
    direct = inputSignal.split(',', 1)[0]
    power = float(inputSignal.split(',', 1)[1])

    signal = signalModule.commandConvert()
    if direct == 'w':
        signal.cmdModify(signal.cmd, '01', 0, power)
    elif direct == 's':
        signal.cmdModify(signal.cmd, '02', 0, power)
    elif direct == 'a':
        signal.cmdModify(signal.cmd, '03', 0, power)
    elif direct == 'd':
        signal.cmdModify(signal.cmd, '04', 0, power)
    elif direct == 'q':
        signal.cmdModify(signal.cmd, '05', 0, power)
    elif direct == 'e':
        signal.cmdModify(signal.cmd, '06', 0, power)

    sendcommandTest(cmdSignal=signal.cmd)
    ser.write(signal.cmd)

class car_client(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        # 紀錄指令間隔時間
        self.lastSendCmdTime = time.time()
        self.sendCmdTime = time.time()
        # 暫停輸入旗標
        self.pauseFlag = False
        self.timerStart = False
        self.outputHalt = False

    def serialsendTimer(self):
        # 序列埠輸出..>太快切換指令輪子會卡住..>需要數幾秒
        while True:
            if self.timerStart:
                while self.timerStart:
                    self.pauseFlag = True
                    time.sleep(0.5)
                    self.pauseFlag = False
                    self.timerStart = False
            else:
                time.sleep(0.5)

    def direction(self):
        cmdList = queue.Queue()
        if not cmdList.empty():
            self.timerStart = True
            if not self.pauseFlag:
                direction_withpower(cmdList.get())
                self.outputHalt = True
        while self.outputHalt:
            self.timerStart = True
            if not self.pauseFlag:
                direction_withpower('x,0')
                self.outputHalt = False

    def run(self):

        #--------通訊--------
        HOST = '127.0.0.1'
        PORT = 55688

        # 儲存送過來的指令
        cmdList = queue.Queue()

        clientMessage = '車子端'  # Client表明身分

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST, PORT)) # 向server端通訊
        client.sendall(clientMessage.encode()) # 轉成 16進制編碼, encode()可加入參數:'UTF-8', 'GBK'etc

        # 連線成功的 歡迎訊息
        serverMessage = str(client.recv(1024), encoding='utf-8')
        print(serverMessage)

        while True:
            try:
                # 接收檔案
                serverMessage = str(client.recv(1024), encoding='utf-8')
                if serverMessage != '':
                    print('Server response:{}'.format(serverMessage))
                    # 輸入太快會是一組字串, 把按太快(限制在3個字元以下)的砍掉
                    if serverMessage.count('\\') <= 3:
                        for mes in serverMessage.split('\\', serverMessage.count('\\')):
                            if mes != '':
                                cmdList.put(mes)

                while not cmdList.empty():
                    mess = cmdList.get()
                    direction_withpower(mess)
                    time.sleep(0.5)
                    direction_withpower('x,0')
                    time.sleep(0.5)
                print('下一組')


            except Exception as e:
                print('客戶端錯誤:', end='')
                print(repr(e))
                break



if __name__ == '__main__':
    ClientTd = car_client()
    ClientTd.start()
