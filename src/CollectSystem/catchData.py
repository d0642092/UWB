import requests, threading, time, queue
# create empty queue list
detailData = queue.Queue()
catchTime = queue.Queue()
ANCHOR = ["An0011", "An0094", "An0096", "An0099"]
class CatchData(threading.Thread):
  def __init__(self, API):
    threading.Thread.__init__(self)
    ## get data from API
    self.name = "Get Data Thread"
    self.nowNumber = 0
    self.start = True
    self.API = API

  def run(self):
    previousData = {}
    while self.start:
      try:
        cmpData = {}
        data = {}
        distance = requests.get(self.API)
        distance = distance.json()
        getTime = time.time()
        for name in ANCHOR:
          # conver str into dict
          data[name] = eval(distance[name])
          # get the attr to compare repeat
          cmpData[name] = data[name]["Ranging"]
          cmpData["IMU"+name] = data[name]["IMU"]
        if previousData != cmpData:
          catchTime.put(getTime)
          detailData.put(data)
          previousData = cmpData
          self.nowNumber += 1
          print(previousData)
          print(self.nowNumber)
      except (KeyError, Exception):
        # It is possible get the empty data from API
        # possible reason network is offline, or anchors offline
        continue

