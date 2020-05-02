import requests
import time
import threading
import queue

#資料輸出
from openpyxl import Workbook, load_workbook

# 拿取自己寫的檔案
from CalActualDis import *
from Foword import forward #從Forward檔案內import forward
from serialWrite import *

# 透過API拿取需要的資料
class catchData(threading.Thread):
    def __init__(self, name, flag):
        threading.Thread.__init__(self)
        self.name = name    # 沒甚麼意義
        self.flag = flag  # 為了能打斷thread

    def run(self):
        before = {}
        while self.flag:
            try:
                Ranging = {}
                data = {}
                distance = requests.get("http://192.168.8.107/php/diagnosis.php?getrangingdiagnosis=4210000000001198&project_id=1")
                distance = distance.json()  # 解json格式

                for value, anchor in enumerate(AnchorName):
                    data[anchor] = eval((distance[anchor]))    # 將字串轉字典
                    Ranging[anchor] = data[anchor]["Ranging"]  # 取判斷重複的值
                    Ranging["IMU" + str(value+1)] = data[anchor]["IMU"]

                if before != Ranging:      # 判斷重複
                    Catch_time.put(time.time())  # 拿取資料的時間
                    Detail_Data.put(data)  # 放入資料
                    before = Ranging
            except (KeyError, Exception):
                continue

class writerData(threading.Thread):
    def __init__(self, num):
        threading.Thread.__init__(self)
        self.num = num  # 第幾筆資料

    def run(self):
        beforeTime = time.time()  # 開始時間
        try:
            wb= load_workbook("G-print_3.xlsx")  # 嘗試開啟 excel
        except FileNotFoundError:
            wb = Workbook()    # 建立新的 excel
        ws = wb.create_sheet('Name')  # 建立 sheet

        # excel 排版
        # =========================================================================================================
        ws.append(["", "An0011", "", "", "An0094", "", "", "An0095", "", "", "An0096", "", "", "An0099", "", ""])
        for i in range(2,17,3):
            ws.merge_cells(start_row=1, start_column=i, end_row=1, end_column=i+2)
        ws.append(["Index"] + ["Ranging", "IMU", "Actual"] * 5)
        # =========================================================================================================

        output = []  # 暫存輸出資料
        while Detail_Data.qsize() > 0 or undone:  # 當佇列為空且 catchData 已做完則離開
            if Detail_Data.qsize() != 0:
                disData = Detail_Data.get()   # 拿取資料和時間
                arrive_time = Catch_time.get()
                self.num += 1  # 當前index
                for i in AnchorName:   # 資料排版
                    output.append(self.num)
                    output.append(disData[i]["Ranging"])
                    output.append(disData[i]["IMU"])
                    # 算實際距離 (時間差, 平均速度, CalActual的變數(  , anchor 座標,  ) )
                    output.append(calDis(arrive_time - beforeTime, avg_V, car_direction, anchorPositions[i], dire))
                ws.append(output)  # 輸出資料
                print(output)
            wb.save('Test.xlsx')  # 存檔


if __name__ == '__main__':
    # 佇列
    Detail_Data = queue.Queue()
    Catch_time = queue.Queue()


    car_runTime = 20  # How much time let the car run
    total_distance = 0  # How long if the car run car_runTime second
    # avg_V = total_distance / car_runTime  # The average velocity
    AnchorName = ["An0011", "An0094", "An0095", "An0096", "An0099"]

    # IMU = catchData("IMU", True)
    # Data = writerData(0)
    car = forward(True)
    commandIn = sendToSerial("sendIn")

    # 開始 catchData
    car.start()
    # IMU.start()

    commandIn.start()

    carStart = time.time()
    carEnd = time.time()

    undone = True  # flag for whether catchData has down
    # Data.start()

    try:
        while carEnd - carStart < car_runTime:
            carEnd = time.time()

        # 停止 thread
        car.flag = False
        # IMU.flag = False
    except KeyboardInterrupt:
        # 意外發生可打斷
        car.flag = False

        # IMU.flag = False
    undone = False  # 要求工作已做完
    commandIn.join()
    # Data.join()

    print("Done")


