# https://dotblogs.com.tw/yc421206/2011/01/04/20575
import time, os, threading
from catchData import CatchData
from writerData import WriterData
def checkFolder(path):
  if not os.path.exists(path):
    print('-----create '+ path +'-----')
    os.makedirs(path)
    print('-----create Image folder-----')
    os.makedirs(path+"Image/")
    print('-----create train_data folder-----')
    os.makedirs(path+"train_data/")
    print('-----create train_result folder-----')
    os.makedirs(path+"train_result/")
    print('-----Successful-----')

def envSetting(isStatic):
  ip = "enter ip address"
  url = "http://%s/php/diagnosis.php?getrangingdiagnosis=4210000000001198&project_id=1" % ip

  # Anchor Area
  x, y, z = 500, 500, 60
  # The average velocity
  avgV = 1240/14
  # Max data number
  maxsNumber = 50

  position = {
      "Anchor":{"An0011": [250, 250, 120],
          "An0094": [0, y, z],
          "An0095": [x, 0, z],
          "An0096": [x, y, z],
          "An0099": [0, 0, z]},
      # move along with positive y
      "Direction": [0, 1, 0]
  }
  # Tag position, Static or Dynamic
  position["Tag"] = [600, 250] if isStatic else [(x + 400), -y-248, 0]
  # result path
  resultInfo = {
      "ResultPath": "../../data/2020-09-10_parking/",
      "Filename": "outdoor_static_4_99.xlsx",
      "Sheetname": "Point"
  }
  checkFolder(resultInfo["ResultPath"])
  return url, avgV, maxsNumber, position, resultInfo


if __name__ == "__main__":
  try:
    isStatic = True
    url, avgV, maxsNumber, position, resultInfo = envSetting(isStatic)

    # initialize
    dataCatch = CatchData(API = url)
    dataWrite = WriterData(avgV, isStatic, position, resultInfo)

    # thread start
    print("READY...")
    dataCatch.start()
    dataWrite.start()

    # init time
    startTime = time.time()
    while dataCatch.nowNumber < maxsNumber:
      endTime = time.time()
  except KeyboardInterrupt:
    endTime = time.time()
  dataCatch.start = False
  dataWrite.catchDone = True

  if dataWrite.catchDone and dataWrite.writerDone:
    dataCatch.join()
    dataWrite.join()
  print(endTime - startTime)

