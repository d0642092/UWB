import requests
import time
import threading
import queue


# 佇列
Detail_Data = queue.Queue()
Catch_time = queue.Queue()
AnchorName = ["An0011", "An0094", "An0095", "An0096", "An0099"]


class catchData(threading.Thread):
    def __init__(self, name, flag):
        threading.Thread.__init__(self)
        self.name = name    # 沒甚麼意義
        self.flag = flag  # 為了能打斷thread

    def run(self):
        before = {}
        maxs = 0
        while self.flag:
            try:
                if maxs == 50:
                    break
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
                    maxs += 1
                    print(before)
            except (KeyError, Exception):
                continue
