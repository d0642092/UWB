import requests
import time
import threading
import queue

from Forword import forward  #從Forward檔案內import forward
from CalActulDis import *
from openpyxl import Workbook
from openpyxl import load_workbook




class catchData(threading.Thread):
    def __init__(self, num):
        threading.Thread.__init__(self)
        self.num = num

    def run(self):
        try:
            before = {}
            # max = 50
            while True:
                try:
                    Ranging = {}
                    data = {}
                    distance = requests.get("http://192.168.8.107/php/diagnosis.php?getrangingdiagnosis=4210000000001198&project_id=1")
                    distance = distance.json()

                    for value, anchor in enumerate(AnchorName):
                        data[anchor] = eval((distance[anchor]))
                        Ranging[anchor] = data[anchor]["Ranging"]
                        Ranging["IMU" + str(value+1)] = data[anchor]["IMU"]
                    if before != Ranging:
                        # print("Thread", self.num)
                        before = Ranging
                        Detail_Data.put(data)
                        Catch_time.put(time.time())
                        max -= 1
                    if max <= 0:
                        break
                except KeyError:
                    continue
                except Exception:
                    continue
        except KeyboardInterrupt:
            pass





class writerData(threading.Thread):
    def __init__(self, num):
        threading.Thread.__init__(self)
        self.num = num

    def run(self):
        beforeTime = time.time()
        try:
            wb= load_workbook("G-print_3  .xlsx")
        except FileNotFoundError:
            wb = Workbook()
        ws = wb.create_sheet('Name')
        output = []
        ws.append(["", "An0011", "", "", "An0094", "", "", "An0095", "", "", "An0096", "", "", "An0099", "", ""])
        for i in range(2,17,3):
            ws.merge_cells(start_row=1, start_column=i, end_row=1, end_column=i+2)

        ws.append(["Index"] + ["Ranging", "IMU", "Actual"] * 5)
        while Detail_Data.qsize() > 0 or undone:
            if Detail_Data.qsize() != 0:
                disData = Detail_Data.get()
                self.num += 1
                for i in AnchorName:
                    output.append(self.num)
                    output.append(disData[i]["Ranging"])
                    output.append(disData[i]["IMU"])
                    output.append(Actual_distance[i])
                ws.append(output)
            wb.save('Test.xlsx')

            for i in AnchorName:
                print(i, disData[i]["Ranging"], "IMU", disData[i]["IMU"], "TagV", disData[i]["TagVelocity"], "Actual distance", Actual_distance[i])
            print("\n")





if __name__ == '__main__':
    codeStart = time.time()
    Detail_Data = queue.Queue()
    Catch_time = queue.Queue()
    car_runTime = 0  # How much time let the car run
    total_distance = 0  # How long if the car run car_runTime second
    avg_V = total_distance / car_runTime  # The average velocity
    AnchorName = ["An0011", "An0094", "An0095", "An0096", "An0099"]
    # Start_distance = {"An0011": 0, "An0094": 0, "An0095": 0, "An0096": 0, "An0099": 0}
    Actual_distance = {"An0011": 0, "An0094": 0, "An0095": 0, "An0096": 0, "An0099": 0}


    IMU = catchData("IMU")
    Data = writerData(0)
    car = forward()

    car.start(car_runTime)
    IMU.start()
    undone = True
    Data.start()

    car.join()
    IMU.join()
    undone = False  # 要求工作已做完
    Data.join()

    print("Done")

    codeEnd = time.time()
    print(codeEnd - codeStart)
