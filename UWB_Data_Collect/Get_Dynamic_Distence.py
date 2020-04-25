import requests
import time
import pandas
import threading
import queue
import json
from openpyxl import Workbook
from openpyxl import load_workbook

codeStart = time.time()
Detail_Data = queue.Queue()

AnchorName = ["An0011", "An0094", "An0095", "An0096", "An0099"]
Start_distance = {"An0011": 0, "An0094": 0, "An0095": 0, "An0096": 0, "An0099": 0}
Actual_distance = {"An0011": 0, "An0094": 0, "An0095": 0, "An0096": 0, "An0099": 0}

undone = True
class catchData(threading.Thread):
    def __init__(self, num):
        threading.Thread.__init__(self)
        self.num = num

    def run(self):
        before = {}
        max = 50
        while True:
            try:
                Ranging = {}
                data = {}
                distance = requests.get("http://192.168.8.107/php/diagnosis.php?getrangingdiagnosis=4210000000001198&project_id=1")
                distance = distance.json()

                for value, i in enumerate(AnchorName):
                    data[i] = eval((distance[i]))
                    Ranging[i] = data[i]["Ranging"]
                    Ranging["IMU" + str(value+1)] = data[i]["IMU"]
            except KeyError:
                continue
            except Exception:
                continue

            if before != Ranging:
                # print("Thread", self.num)
                before = Ranging
                Detail_Data.put(data)
                max -= 1
            if max <= 0:
                break



class writerData(threading.Thread):
    def __init__(self, num):
        threading.Thread.__init__(self)
        self.num = num

    def run(self):
        while Detail_Data.qsize() > 0 or undone:
            if Detail_Data.qsize() == 0:
                continue
            try:
                wb= load_workbook("G-print_3  .xlsx")
                wb.create_sheet('Name')
            except Exception:
                wb = Workbook()
            output = []
            ws = wb.active
            ws.append(["", "An0011", "", "", "An0094", "", "", "An0095", "", "", "An0096", "", "", "An0099", "", ""])
            for i in range(2,17,3):
                ws.merge_cells(start_row=1,start_column=i,end_row=1,end_column=i+2)

            ws.append(["Ranging", "IMU", "Actual"] * 5)
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

# class TagRealDistence(threading.Thread):
#     def __init__(self, num):
#         threading.Thread.__init__(self)
#         self.num = num
#
#     def run(self):
#         pass

# def TagRealDistence(Velocity):
#     pass

IMU = catchData("IMU")
Data = writerData(0)



IMU.start()
Data.start()

IMU.join()
undone = False  # 要求工作已做完
Data.join()

print("Done")

codeEnd = time.time()
print(codeEnd - codeStart)