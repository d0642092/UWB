import requests
import time
import pandas

codeStart = time.time()

def dataAsk():
    i = 1
    timeStart = time.time()
    while i <= 20:
        # time.sleep(0.5)
        timeEnd = time.time()
        if timeEnd - timeStart >= 0.5:
            distance = requests.get("http://192.168.8.107/php/vilsnodes.php?LOADFILE=RANGING")
            timeStart = time.time()
            excel(distance.json())
            i += 1

def excel(dataStore):
    disData = eval(dataStore["Tag1198"])
    print(disData)

    dis11.append(disData.get("An0011", "N\A"))
    dis94.append(disData.get("An0094", "N\A"))
    dis95.append(disData.get("An0095", "N\A"))
    dis96.append(disData.get("An0096", "N\A"))
    dis99.append(disData.get("An0099", "N\A"))




re11 = 0
re94 = 0
re95 = 0
re96 = 0
re99 = 0


dis11 = []
dis94 = []
dis95 = []
dis96 = []
dis99 = []

dataAsk()



df = pandas.DataFrame(
    {"An0011": dis11, "Real11": re11, "An0094": dis94, "Real94": re94, "An0095": dis95, "Real95": re95, "An0096": dis96,
     "Real96": re96, "An0099": dis99, "Real99": re99})

try:
    with pandas.ExcelWriter('excel_UWB_distance.xlsx', mode='a') as writer:
        df.to_excel(writer, sheet_name='single100_An96_90斜', encoding="utf_8")
except FileNotFoundError:
    df.to_excel('excel_UWB_distance.xlsx', sheet_name='distance50', encoding="utf_8")

codeEnd = time.time()
print(codeEnd - codeStart)