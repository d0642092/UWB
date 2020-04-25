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
Actual_distanceA = {"An0011": 0, "An0094": 0, "An0095": 0, "An0096": 0, "An0099": 0}

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
                distance = requests.get("http://192.168.8.107/php/diagnosis.php?getrangingdiagnosis=4210000000001198&project_id=1")

                distance = distance.json()
                # distance["An0011"]["Ranging"] is string
                for i in AnchorName:
                    dis = json.loads(distance[i])

                Ranging = [dis["Ranging"], dis["IMU"]]
                # data = {"An0011": eval(distance["An0011"]),
                #         "An0094": eval(distance["An0094"]),
                #         "An0095": eval(distance["An0095"]),
                #         "An0096": eval(distance["An0096"]),
                #         "An0099": eval(distance["An0099"])}
                # Ranging = {"An0011": data["An0011"]["Ranging"], "IMU11": data["An0011"]["IMU"],
                #            "An0094": data["An0094"]["Ranging"], "IMU94": data["An0094"]["IMU"],
                #            "An0095": data["An0095"]["Ranging"], "IMU95": data["An0095"]["IMU"],
                #            "An0096": data["An0096"]["Ranging"], "IMU96": data["An0096"]["IMU"],
                #            "An0099": data["An0099"]["Ranging"], "IMU99": data["An0099"]["IMU"]
                #            }
            except KeyError:
                continue
            except Exception:
                continue

            if before != Ranging:
                # print("Thread", self.num)
                before = Ranging
                Detail_Data.put(Ranging)
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
                wb= load_workbook("G-print_3.xlsx")
                wb.create_sheet('Name', index=1)
            except Exception:
                wb = Workbook()
            finally:
                ws = wb.active
                ws.append(["An0011", "", "", "An0094", "", "", "An0095", "", "", "An0096", "", "", "An0099", "", ""])
                ws.append(["Ranging", "IMU", "Actual"] * 5)
                disData = Detail_Data.get()
                ws.append(disData["Ranging"],disData["IMU"], Actual_distanceA["An0011"])
                wb.save('Test.xlsx')

            print("An0011", disData["An0011"]["Ranging"], "IMU", disData["An0011"]["IMU"], "TagV", disData["An0011"]["TagVelocity"], "Actual distance" ,  Actual_distance11)
            print("An0094", disData["An0094"]["Ranging"], "IMU", disData["An0094"]["IMU"], "TagV", disData["An0094"]["TagVelocity"], "Actual distance",  Actual_distance94)
            print("An0095", disData["An0095"]["Ranging"], "IMU", disData["An0095"]["IMU"], "TagV", disData["An0095"]["TagVelocity"], "Actual distance",  Actual_distance95)
            print("An0096", disData["An0096"]["Ranging"], "IMU", disData["An0096"]["IMU"], "TagV", disData["An0096"]["TagVelocity"], "Actual distance",  Actual_distance96)
            print("An0099", disData["An0099"]["Ranging"], "IMU", disData["An0099"]["IMU"], "TagV", disData["An0099"]["TagVelocity"], "Actual distance",  Actual_distance99)
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
Data = writerData("writer")



IMU.start()
Data.start()

IMU.join()
undone = False  # 要求工作已做完
Data.join()

print("Done")

codeEnd = time.time()
print(codeEnd - codeStart)