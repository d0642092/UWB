import requests
import time
import pandas
import threading
import queue

codeStart = time.time()
q = queue.Queue()

class dataAsk(threading.Thread):
    def __init__(self, num):
        threading.Thread.__init__(self)
        self.num = num

    def run(self):
        print("Thread", self.num)
        before = {}
        max = 500

        while True:
            distance = requests.get("http://192.168.8.107/php/vilsnodes.php?LOADFILE=RANGING")
            if before != distance.json():
                q.put(distance.json())
                before = distance.json()
                max -= 1
            if max <= 0:
                break

undone = True
# re11 = 266
# re94 = 222
# re95 = 442
# re96 = 394
# re99 = 100
# lost = 100


class dataWork(threading.Thread):
    def __init__(self, num):
        threading.Thread.__init__(self)
        self.num = num

    def run(self):
        print("Thread", self.num)

        # excel 無法一行一行輸入會一直增加sheet
        # while q.qsize() >= 0 or Ndone:
        #     if q.qsize() == 0:
        #         if not Ndone:
        #             break
        #         continue
        #
        #     disData = eval(q.get()["Tag1198"])
        #     print(disData)
        #     df = pandas.Series(
        #         {"An0011": disData.get("An0011", "N\A"), "Real11": 0,
        #          "An0094": disData.get("An0094", "N\A"), "Real94": 0,
        #          "An0095": disData.get("An0095", "N\A"), "Real95": 0,
        #          "An0096": disData.get("An0096", "N\A"), "Real96": 0,
        #          "An0099": disData.get("An0099", "N\A"), "Real99": 0})
        #     try:
        #         with pandas.ExcelWriter('excel_thread_distance.xlsx', mode='a') as writer:
        #             df.to_excel(writer, sheet_name='single100_An96_90', encoding="utf_8")
        #     except FileNotFoundError:
        #         df.to_excel('excel_thread_distance.xlsx', sheet_name='distance50', encoding="utf_8")

        while q.qsize() > 0 or undone:
            if q.qsize() == 0:
                continue
            try:
                disD = q.get()
                disData = eval(disD["Tag1198"])
            except Exception:
                print(disD)
                print(type(disD))
                continue
            print(disData)
            # dis11.append(disData.get("An0011", "N\A") if disData.get("An0011", "0") > str(re11-lost) and disData.get("An0011", "0") < str(re11+lost) else "0")
            # dis94.append(disData.get("An0094", "N\A") if disData.get("An0094", "0") > str(re94-lost) and disData.get("An0094", "0") < str(re94+lost) else "0")
            # dis95.append(disData.get("An0095", "N\A") if disData.get("An0095", "0") > str(re95-lost) and disData.get("An0095", "0") < str(re95+lost) else "0")
            # dis96.append(disData.get("An0096", "N\A") if disData.get("An0096", "0") > str(re96-lost) and disData.get("An0096", "0") < str(re96+lost) else "0")
            # dis99.append(disData.get("An0099", "N\A") if disData.get("An0099", "0") > str(re99-lost) and disData.get("An0099", "0") < str(re99+lost) else "0")
            dis11.append(disData.get("An0011", 0))
            dis94.append(disData.get("An0094", 0))
            dis95.append(disData.get("An0095", 0))
            dis96.append(disData.get("An0096", 0))
            dis99.append(disData.get("An0099", 0))

        df = pandas.DataFrame(
            {"An0011": dis11, "Real11": 162,
             "An0094": dis94, "Real94": 121,
             "An0095": dis95, "Real95": 216,
             "An0096": dis96, "Real96": 124,
             "An0099": dis99, "Real99": 217})
        try:
            with pandas.ExcelWriter('G-print_2.xlsx', mode='a') as writer:
                df.to_excel(writer, sheet_name='100x100_An96_124', encoding="utf_8")
        except FileNotFoundError:
            df.to_excel('G-print_2.xlsx', sheet_name='440x170_An96_274', encoding="utf_8")


ask = dataAsk(1)
work = dataWork(2)

dis11 = []
dis94 = []
dis95 = []
dis96 = []
dis99 = []

ask.start()
work.start()

ask.join()
undone = False  # 要求工作已做完
work.join()

print("Done")

codeEnd = time.time()
print(codeEnd - codeStart)