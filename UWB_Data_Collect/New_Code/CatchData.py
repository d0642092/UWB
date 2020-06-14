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
        print("=================READY=================")
        while self.flag:
            try:
                # if maxs == 50:
                #     break
                Ranging = {}
                data = {}
                # distance = requests.get("http://192.168.8.107/php/diagnosis.php?getrangingdiagnosis=4210000000001198&project_id=1")
                # distance = distance.json()  # 解json格式
                distance = {"An0011":{"Ranging": "25",
                                        "PCnt":"1",
                                        "AnCnt":"1",
                                        "TagRecv":"2",
                                        "TagFP":"2",
                                        "AnRecv":"1",
                                        "AnFP":"1",
                                        "LostRate":"1",
                                        "DataRate":"2",
                                        "DataCount":"1",
                                        "SlotTime":"2",
                                        "ResetTime":"2",
                                        "TagVelocity":"a",
                                        "SD":"a",
                                        "IMU":"a"},
                            "An0094":{"Ranging": "94",
                                        "PCnt":"1",
                                        "AnCnt":"1",
                                        "TagRecv":"2",
                                        "TagFP":"2",
                                        "AnRecv":"1",
                                        "AnFP":"1",
                                        "LostRate":"1",
                                        "DataRate":"2",
                                        "DataCount":"1",
                                        "SlotTime":"2",
                                        "ResetTime":"2",
                                        "TagVelocity":"a",
                                        "SD":"a",
                                        "IMU":"a"},
                            "An0095": {"Ranging": "95",
                                       "PCnt": "1",
                                       "AnCnt": "1",
                                       "TagRecv": "2",
                                       "TagFP": "2",
                                       "AnRecv": "1",
                                       "AnFP": "1",
                                       "LostRate": "1",
                                       "DataRate": "2",
                                       "DataCount": "1",
                                       "SlotTime": "2",
                                       "ResetTime": "2",
                                       "TagVelocity": "a",
                                       "SD": "a",
                                       "IMU": "a"},
                            "An0096": {"Ranging": "96",
                                       "PCnt": "1",
                                       "AnCnt": "1",
                                       "TagRecv": "2",
                                       "TagFP": "2",
                                       "AnRecv": "1",
                                       "AnFP": "1",
                                       "LostRate": "1",
                                       "DataRate": "2",
                                       "DataCount": "1",
                                       "SlotTime": "2",
                                       "ResetTime": "2",
                                       "TagVelocity": "a",
                                       "SD": "a",
                                       "IMU": "a"},
                            "An0099": {"Ranging": "99",
                                       "PCnt": "1",
                                       "AnCnt": "1",
                                       "TagRecv": "2",
                                       "TagFP": "2",
                                       "AnRecv": "1",
                                       "AnFP": "1",
                                       "LostRate": "1",
                                       "DataRate": "2",
                                       "DataCount": "1",
                                       "SlotTime": "2",
                                       "ResetTime": "2",
                                       "TagVelocity": "a",
                                       "SD": "a",
                                       "IMU": "a"}}
                for value, anchor in enumerate(AnchorName):
                    # data[anchor] = eval((distance[anchor]))    # 將字串轉字典
                    data[anchor] = distance[anchor]
                    Ranging[anchor] = data[anchor]["Ranging"]  # 取判斷重複的值
                    Ranging["IMU" + anchor] = data[anchor]["IMU"]
                Catch_time.put(time.time())  # 拿取資料的時間
                Detail_Data.put(data)  # 放入資料
                time.sleep(1)
                if maxs > 30:
                    break
                else:
                    maxs+=1
                # if before != Ranging:      # 判斷重複
                #     Catch_time.put(time.time())  # 拿取資料的時間
                #     Detail_Data.put(data)  # 放入資料
                #     before = Ranging
                #     # maxs += 1
                #     print(before)
            except (KeyError, Exception):
                print("err")
                continue
